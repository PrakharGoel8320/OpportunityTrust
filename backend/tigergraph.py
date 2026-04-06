import os
import requests


def _extract_items_from_result(result):
    """Flatten TigerGraph query result into one list of dict items."""
    items = []

    if isinstance(result, list):
        for block in result:
            if isinstance(block, dict):
                for value in block.values():
                    if isinstance(value, list):
                        items.extend(value)
                    elif isinstance(value, dict):
                        items.append(value)
    elif isinstance(result, dict):
        for value in result.values():
            if isinstance(value, list):
                items.extend(value)
            elif isinstance(value, dict):
                items.append(value)

    return items


def query_complaints_by_upi(upi_id):
    """Call live TigerGraph installed query: find_complaints_by_upi."""
    host = os.getenv("TIGERGRAPH_HOST", "").strip().rstrip("/")
    graph_name = os.getenv("TIGERGRAPH_GRAPH_NAME", "").strip()
    token = os.getenv("TIGERGRAPH_TOKEN", "").strip()
    param_name = os.getenv("TG_UPI_PARAM_NAME", "input_upi").strip()

    if not host or not graph_name or not token:
        return {
            "error": "TigerGraph config missing. Check TIGERGRAPH_HOST, TIGERGRAPH_GRAPH_NAME, TIGERGRAPH_TOKEN",
            "complaint_count": 0,
            "linked_companies": [],
        }

    query_name = os.getenv("TIGERGRAPH_QUERY_NAME", "find_complaints_by_upi").strip()
    candidate_urls = [
        f"{host}/query/{graph_name}/{query_name}",
        f"{host}/restpp/query/{graph_name}/{query_name}",
    ]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    params = {param_name: upi_id}

    try:
        response = None

        for url in candidate_urls:
            test_response = requests.get(url, headers=headers, params=params, timeout=15)

            # Simple debug output for hackathon testing.
            print("TigerGraph URL:", test_response.url)
            print("TigerGraph Status:", test_response.status_code)

            if test_response.status_code != 200:
                print("TigerGraph Error Body:", test_response.text)

            # If first path fails with 404, try second path.
            if test_response.status_code == 404:
                response = test_response
                continue

            response = test_response
            break

        if response is None:
            return {
                "error": "TigerGraph request failed before getting a response",
                "complaint_count": 0,
                "linked_companies": [],
            }

        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            return {
                "error": f"TigerGraph response is not valid JSON. Body: {response.text[:300]}",
                "complaint_count": 0,
                "linked_companies": [],
            }

        result = data.get("results", [])
        flat_items = _extract_items_from_result(result)

        complaint_count = 0
        linked_companies = []

        # Try to read direct values if query returns aggregated data
        for item in flat_items:
            if not isinstance(item, dict):
                continue

            if "complaint_count" in item:
                try:
                    complaint_count = max(complaint_count, int(item["complaint_count"]))
                except (TypeError, ValueError):
                    pass

            if "company" in item and item["company"]:
                linked_companies.append(str(item["company"]))

            if "company_name" in item and item["company_name"]:
                linked_companies.append(str(item["company_name"]))

            if "complaints" in item and isinstance(item["complaints"], list):
                complaint_count = max(complaint_count, len(item["complaints"]))

            if "complaint" in item and item["complaint"]:
                complaint_count += 1

            # If complaint vertices are returned one-by-one, count them
            item_type = str(item.get("v_type", "")).lower()
            if "complaint" in item_type:
                complaint_count += 1

        # Remove duplicates
        linked_companies = list(set(linked_companies))

        return {
            "error": None,
            "complaint_count": complaint_count,
            "linked_companies": linked_companies,
            "raw_response": data,
        }

    except requests.exceptions.RequestException as e:
        suggestion = (
            " Check graph name, installed query name, and whether your endpoint uses /query or /restpp/query."
        )
        return {
            "error": f"TigerGraph API request failed: {str(e)}.{suggestion}",
            "complaint_count": 0,
            "linked_companies": [],
        }
