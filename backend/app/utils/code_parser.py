import re
from typing import Optional


def detect_language(filename: Optional[str], code: str) -> str:
    if filename:
        lower = filename.lower()
        if lower.endswith(".py"):
            return "python"
        if lower.endswith(".js"):
            return "javascript"
        if lower.endswith(".ts"):
            return "typescript"
        if lower.endswith(".java"):
            return "java"
        if lower.endswith(".go"):
            return "go"
        if lower.endswith(".cpp") or lower.endswith(".cc") or lower.endswith(".cxx"):
            return "cpp"

    if re.search(r"def\s+\w+\(", code):
        return "python"
    if re.search(r"function\s+\w+\(|const\s+\w+\s*=\s*\(", code):
        return "javascript"
    if re.search(r"public\s+class\s+\w+", code):
        return "java"

    return "unknown"
