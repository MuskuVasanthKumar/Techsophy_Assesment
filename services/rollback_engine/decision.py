def should_rollback(risk_score, threshold=0.7):
    if risk_score >= threshold:
        return True, f"High risk score ({risk_score}) exceeds threshold."
    return False, "Risk score within acceptable limits."
    