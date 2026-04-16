from pathlib import Path
from typing import List

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".java", ".go", ".cpp", ".c", ".cs",
    ".rb", ".php", ".swift", ".kt", ".rs", ".sql", ".html",
    ".css", ".jsx", ".tsx"
}

IGNORED_DIRS = {
    ".git", "node_modules", "dist", "build", "venv", ".venv",
    "__pycache__", ".idea", ".vscode", "coverage", "target", "out"
}


def is_code_file(path: Path) -> bool:
    return path.suffix.lower() in ALLOWED_EXTENSIONS


def should_ignore(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def collect_code_files(root: Path, max_files: int) -> List[Path]:
    files: List[Path] = []
    for file_path in root.rglob("*"):
        if file_path.is_file() and not should_ignore(file_path) and is_code_file(file_path):
            files.append(file_path)
            if len(files) >= max_files:
                break
    return files
