def generate_strengths(code: str):
    strengths = []

    if "def " in code:
        strengths.append("Code is organized into reusable functions")

    if "if " in code:
        strengths.append("Conditional logic is clearly structured")

    if "for " in code or "while " in code:
        strengths.append("Control flow handles iterative processing")

    if "try:" in code and "except" in code:
        strengths.append("Basic exception handling is present")

    if not strengths:
        strengths.append("Code structure is simple and readable")

    # remove duplicates while preserving order
    unique = []
    seen = set()
    for item in strengths:
        if item not in seen:
            seen.add(item)
            unique.append(item)

    return unique[:3]
