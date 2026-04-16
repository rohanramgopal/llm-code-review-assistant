from app.schemas.review_schema import Finding


def run_static_rules(code: str, language: str | None):
    findings = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        l = line.lower()

        if "eval(" in line:
            findings.append(Finding(
                category="security",
                severity="high",
                title="Dynamic execution usage",
                explanation="eval() can execute arbitrary code.",
                recommendation="Avoid eval and use safe parsing.",
                line_hint=f"line {i}: {line.strip()}"
            ))

        if "api_key" in l or "secret" in l:
            findings.append(Finding(
                category="security",
                severity="high",
                title="Hardcoded secret",
                explanation="Sensitive data should not be hardcoded.",
                recommendation="Use environment variables.",
                line_hint=f"line {i}: {line.strip()}"
            ))

        if "except Exception" in line:
            findings.append(Finding(
                category="quality",
                severity="medium",
                title="Generic exception catch",
                explanation="Catching Exception hides real errors.",
                recommendation="Catch specific exceptions.",
                line_hint=f"line {i}"
            ))

        if "return 0" in line:
            findings.append(Finding(
                category="logic",
                severity="medium",
                title="Silent fallback return",
                explanation="Returning 0 hides failure.",
                recommendation="Raise explicit error.",
                line_hint=f"line {i}"
            ))

    if not findings:
        findings.append(Finding(
            category="quality",
            severity="low",
            title="No major issues",
            explanation="Code looks clean.",
            recommendation="Consider adding tests.",
            line_hint="entire file"
        ))

    return findings
