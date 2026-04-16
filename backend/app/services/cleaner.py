def deduplicate_findings(findings):
    seen = set()
    cleaned = []

    for f in findings:
        title = f.get("title", "").strip().lower()
        line_hint = f.get("line_hint", "").strip().lower()
        category = f.get("category", "").strip().lower()
        key = (title, line_hint, category)

        if key not in seen:
            seen.add(key)
            cleaned.append(f)

    return cleaned
