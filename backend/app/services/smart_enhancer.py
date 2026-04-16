def generate_smart_summary(findings):
    if not findings:
        return "No major issues detected. Code appears clean for basic use."

    high = sum(1 for f in findings if f.get("severity") == "high")
    medium = sum(1 for f in findings if f.get("severity") == "medium")
    low = sum(1 for f in findings if f.get("severity") == "low")

    if high > 0:
        return f"Critical issues detected. {high} high severity issue(s) need immediate attention."
    if medium >= 2:
        return f"Multiple moderate issues found ({medium}). Code should be improved before production use."
    if medium == 1:
        return "One moderate issue detected. Code is functional but needs improvement."
    return f"Only minor issues detected ({low}). Code looks acceptable for basic use."


def calculate_smart_score(findings):
    score = 10

    for f in findings:
        sev = f.get("severity")
        if sev == "high":
            score -= 3
        elif sev == "medium":
            score -= 2
        elif sev == "low":
            score -= 1

    return max(1, min(10, score))
