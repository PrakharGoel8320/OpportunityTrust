from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from utils import extract_company_name, extract_upi_id
from logic import calculate_trust_score, check_text_signals
from tigergraph import query_complaints_by_upi

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/docs", methods=["GET"])
def docs():
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Opportunity Trust API Docs</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                background: #07111f;
                color: #eef2ff;
                line-height: 1.6;
            }
            .wrap {
                max-width: 1000px;
                margin: 0 auto;
                padding: 32px 20px 60px;
            }
            .card {
                background: rgba(10, 18, 33, 0.92);
                border: 1px solid rgba(148, 163, 184, 0.16);
                border-radius: 18px;
                padding: 22px;
                margin-bottom: 18px;
            }
            h1, h2, h3 { margin-top: 0; }
            code, pre {
                background: #0d1729;
                border-radius: 10px;
            }
            code {
                padding: 2px 6px;
            }
            pre {
                padding: 16px;
                overflow-x: auto;
            }
            .tag {
                display: inline-block;
                padding: 6px 10px;
                border-radius: 999px;
                background: rgba(20, 184, 255, 0.16);
                color: #7fe2ff;
                font-size: 14px;
                margin-bottom: 10px;
            }
            .muted { color: rgba(238, 242, 255, 0.72); }
            ul { padding-left: 20px; }
            a { color: #7fe2ff; }
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="card">
                <div class="tag">Backend Docs</div>
                <h1>Opportunity Trust Intelligence Network API</h1>
                <p class="muted">Simple Flask API for scam detection using text signals and live TigerGraph data.</p>
            </div>

            <div class="card">
                <h2>Available Endpoints</h2>
                <ul>
                    <li><code>GET /</code> - API health check</li>
                    <li><code>GET /docs</code> - This docs page</li>
                    <li><code>POST /analyze</code> - Analyze a job or internship message</li>
                </ul>
            </div>

            <div class="card">
                <h2>POST /analyze</h2>
                <p>Send a message in JSON format.</p>
                <pre>{
  "message": "Work from home internship. Pay 499 on fakejob@upi now."
}</pre>
            </div>

            <div class="card">
                <h2>Response Example</h2>
                <pre>{
  "input": {
    "message": "Work from home internship...",
    "company_name": "ABC Technologies",
    "upi_id": "fakejob@upi"
  },
  "graph_data": {
    "complaint_count": 4,
    "linked_companies": ["ABC Technologies"]
  },
  "trust_score": 0,
  "risk_level": "High",
  "explanation": "UPI has high complaints (4). Message contains payment-related words."
}</pre>
            </div>

            <div class="card">
                <h2>Scoring Rules</h2>
                <ul>
                    <li>Start score = 100</li>
                    <li>Complaints count &gt; 2 = minus 40</li>
                    <li>Company linked to same UPI = minus 30</li>
                    <li>Job offer words = minus 5</li>
                    <li>Secure internship pitch = minus 5</li>
                    <li>Basic details request = minus 5</li>
                    <li>Resume and details together = minus 25</li>
                    <li>Limited-time offer language = minus 15</li>
                    <li>Urgency words found = minus 5</li>
                    <li>Money request linked to a handle = minus 10</li>
                    <li>Refundable deposit = minus 20</li>
                    <li>Background check fee = minus 35</li>
                    <li>Payment words found = minus 0</li>
                    <li>Official payment identity or account words = minus 10</li>
                    <li>Handle-like payment address used in a scam combo = minus 5</li>
                </ul>
            </div>

            <div class="card">
                <h2>TigerGraph Integration</h2>
                <p>The backend calls the live installed query <code>find_complaints_by_upi</code> using:</p>
                <pre>https://&lt;host&gt;/query/&lt;graph_name&gt;/find_complaints_by_upi</pre>
                <p>Query parameter name:</p>
                <pre>input_upi</pre>
                <p>Header used:</p>
                <pre>Authorization: Bearer &lt;token&gt;</pre>
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Opportunity Trust Intelligence Network API running"})


@app.route("/analyze", methods=["POST"])
def analyze_message():
    body = request.get_json(silent=True) or {}
    message = body.get("message", "")

    if not message or not message.strip():
        return jsonify({"error": "Message is required"}), 400

    upi_id = extract_upi_id(message)
    company_name = extract_company_name(message)
    signals = check_text_signals(message)

    complaint_count = 0
    linked_companies = []
    tigergraph_error = None

    if upi_id:
        tg_data = query_complaints_by_upi(upi_id)
        complaint_count = tg_data.get("complaint_count", 0)
        linked_companies = tg_data.get("linked_companies", [])
        tigergraph_error = tg_data.get("error")

    company_linked = False
    if linked_companies:
        company_linked = True

    score_data = calculate_trust_score(
        complaint_count=complaint_count,
        company_linked=company_linked,
        **signals,
    )

    response = {
        "input": {
            "message": message,
            "company_name": company_name,
            "upi_id": upi_id,
        },
        "graph_data": {
            "complaint_count": complaint_count,
            "linked_companies": linked_companies,
        },
        "trust_score": score_data["trust_score"],
        "risk_level": score_data["risk_level"],
        "explanation": score_data["explanation"],
    }

    if tigergraph_error:
        response["tigergraph_warning"] = tigergraph_error

    return jsonify(response), 200


@app.route("/graph", methods=["GET"])
def get_graph_by_upi():
    upi_id = (request.args.get("upi") or "").strip()

    if not upi_id:
        return jsonify({"error": "Query parameter 'upi' is required"}), 400

    tg_data = query_complaints_by_upi(upi_id)

    if tg_data.get("error"):
        return jsonify({
            "error": tg_data.get("error"),
            "upi_id": upi_id,
            "complaint_count": 0,
            "linked_companies": [],
            "nodes": [],
            "connections": [],
        }), 502

    linked_companies = tg_data.get("linked_companies", [])
    complaint_count = tg_data.get("complaint_count", 0)

    nodes = [{"id": upi_id, "type": "UPI", "label": upi_id}]
    connections = []

    for company in linked_companies:
        nodes.append({"id": company, "type": "Company", "label": company})
        connections.append({"from": company, "to": upi_id, "label": "linked_to"})

    if complaint_count > 0:
        complaint_node_id = f"complaints_{upi_id}"
        nodes.append({"id": complaint_node_id, "type": "Complaint", "label": f"Complaints: {complaint_count}"})
        connections.append({"from": complaint_node_id, "to": upi_id, "label": "reported_on"})

    return jsonify({
        "upi_id": upi_id,
        "complaint_count": complaint_count,
        "linked_companies": linked_companies,
        "nodes": nodes,
        "connections": connections,
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
