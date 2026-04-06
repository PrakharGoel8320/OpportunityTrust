import re


def extract_upi_id(text):
    """Find first UPI id like name@upi from message text."""
    if not text:
        return None

    # Keep this strict so normal email-like text does not get treated as a UPI id.
    # Common UPI handles used in India are listed below.
    pattern = r"\b[a-zA-Z0-9._-]{2,}@(upi|ybl|ibl|axl|okhdfcbank|okicici|oksbi|okaxis|paytm)\b"
    match = re.search(pattern, text)
    if match:
        return match.group(0).lower()
    return None


def extract_company_name(text):
    """Very basic company extraction using simple keywords around company name."""
    if not text:
        return "Unknown"

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Beginner-friendly simple checks
    for line in lines:
        lower_line = line.lower()

        if "company:" in lower_line:
            return line.split(":", 1)[1].strip()

        if "from" in lower_line and len(line.split()) >= 2:
            words = line.split()
            if "from" in [w.lower() for w in words]:
                index = [w.lower() for w in words].index("from")
                if index + 1 < len(words):
                    return words[index + 1]

    # fallback: look for known company words
    company_words = ["technologies", "solutions", "private", "pvt", "ltd", "limited"]
    for line in lines:
        for word in company_words:
            if word in line.lower():
                return line

    return "Unknown"
