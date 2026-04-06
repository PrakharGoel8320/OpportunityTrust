import re


def get_risk_level(trust_score):
    if trust_score >= 70:
        return "Low"
    if trust_score >= 40:
        return "Medium"
    return "High"


def calculate_trust_score(
    complaint_count,
    company_linked,
    **signals,
):
    score = 100
    reasons = []

    def flag(name):
        return bool(signals.get(name, False))

    if complaint_count > 2:
        score -= 40
        reasons.append(f"UPI has high complaints ({complaint_count}).")

    if company_linked:
        score -= 30
        reasons.append("Company is linked with this UPI in graph data.")

    if flag("has_job_offer_words"):
        score -= 4
        reasons.append("Message looks like a job or internship offer.")

    if flag("has_secure_internship_words"):
        score -= 4
        reasons.append("Message uses a 'secure your internship' style pitch.")

    if flag("has_basic_details_words"):
        score -= 5
        reasons.append("Message asks for basic or personal details.")

    if flag("has_resume_and_details_phrase"):
        score -= 24
        reasons.append("Message asks for a resume and details together.")

    if flag("has_limited_time_offer_words"):
        score -= 16
        reasons.append("Message creates a limited-time offer pressure.")

    if flag("has_urgency_words"):
        score -= 6
        reasons.append("Message creates urgency pressure.")

    if flag("has_money_request_words") and not flag("has_no_payment_disclaimer"):
        score -= 12
        reasons.append("Message asks for money or a fee to move forward.")

    if flag("has_refundable_deposit_words") and not flag("has_no_payment_disclaimer"):
        score -= 24
        reasons.append("Message asks for a refundable deposit.")

    if flag("has_background_check_fee_words") and not flag("has_no_payment_disclaimer"):
        score -= 34
        reasons.append("Message asks for a background check fee.")

    if flag("has_official_handle_words"):
        score -= 8
        reasons.append("Message mentions an official payment identity or account.")

    if flag("has_handle_like_words") and (
        flag("has_money_request_words")
        or flag("has_refundable_deposit_words")
        or flag("has_background_check_fee_words")
        or flag("has_resume_and_details_phrase")
    ):
        score -= 8
        reasons.append("Message contains a handle-like payment address.")

    if (
        flag("has_job_offer_words")
        and flag("has_resume_and_details_phrase")
        and flag("has_urgency_words")
        and flag("has_handle_like_words")
    ):
        score -= 12
        reasons.append("Job offer, details request, handle, and urgency appear together.")

    if score < 0:
        score = 0

    risk = get_risk_level(score)

    if not reasons:
        reasons.append("No strong scam signals found.")

    explanation = " ".join(reasons)

    return {
        "trust_score": score,
        "risk_level": risk,
        "explanation": explanation,
    }


def check_text_signals(text):
    text_lower = text.lower()

    payment_words = [
        "pay",
        "payment",
        "transfer",
        "advance",
        "send it",
    ]

    money_request_words = [
        "send money",
        "required to begin",
        "pay now",
        "confirm your joining slot",
        "registration fee",
        "processing fee",
    ]

    refundable_deposit_words = [
        "refundable deposit",
    ]

    background_check_fee_words = [
        "background check fee",
    ]

    job_offer_words = [
        "congratulations",
        "congratulation",
        "selected",
        "selection",
        "shortlisted",
        "offer letter",
        "internship",
        "job",
        "hiring",
        "offering",
        "work from home",
        "joining slot",
        "training program",
        "remote developers",
        "remote developer",
        "remote internship",
    ]

    basic_details_words = [
        "basic details",
        "personal details",
        "contact details",
        "send your details",
    ]

    resume_words = [
        "resume",
        "cv",
        "portfolio",
    ]

    resume_and_details_phrase = [
        "send your resume and details",
        "share your cv quickly",
        "share your cv",
        "send your cv",
        "send your resume",
    ]

    secure_internship_words = [
        "secure your internship",
    ]

    limited_time_offer_words = [
        "limited time offer",
    ]

    official_handle_words = [
        "official id",
        "official upi",
        "official account",
        "verified account",
        "official handle",
        "hr team",
    ]

    no_payment_disclaimer_words = [
        "no payment is required",
        "no fee is required",
        "do not pay",
        "never pay",
    ]

    urgency_words = [
        "urgent",
        "immediately",
        "today",
        "now",
        "last chance",
        "asap",
        "soon",
    ]

    def has_word_or_phrase(text_value, words):
        for word in words:
            if " " in word:
                if word in text_value:
                    return True
            else:
                # Word boundary avoids accidental matches inside another word.
                if re.search(rf"\b{re.escape(word)}\b", text_value):
                    return True
        return False

    def has_handle_like_address(text_value):
        return re.search(r"\b[a-zA-Z0-9._-]{2,}@[a-zA-Z0-9.-]+\b", text_value) is not None

    return {
        "has_urgency_words": has_word_or_phrase(text_lower, urgency_words),
        "has_job_offer_words": has_word_or_phrase(text_lower, job_offer_words),
        "has_basic_details_words": has_word_or_phrase(text_lower, basic_details_words),
        "has_resume_words": has_word_or_phrase(text_lower, resume_words),
        "has_resume_and_details_phrase": has_word_or_phrase(text_lower, resume_and_details_phrase),
        "has_money_request_words": has_word_or_phrase(text_lower, money_request_words),
        "has_refundable_deposit_words": has_word_or_phrase(text_lower, refundable_deposit_words),
        "has_background_check_fee_words": has_word_or_phrase(text_lower, background_check_fee_words),
        "has_official_handle_words": has_word_or_phrase(text_lower, official_handle_words),
        "has_limited_time_offer_words": has_word_or_phrase(text_lower, limited_time_offer_words),
        "has_secure_internship_words": has_word_or_phrase(text_lower, secure_internship_words),
        "has_no_payment_disclaimer": has_word_or_phrase(text_lower, no_payment_disclaimer_words),
        "has_handle_like_words": has_handle_like_address(text_lower),
    }
