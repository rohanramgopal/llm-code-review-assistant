import shutil
from pathlib import Path
from uuid import uuid4
from git import Repo
from app.core.config import get_settings
from app.utils.file_utils import collect_code_files

settings = get_settings()


class RepoService:
    def __init__(self) -> None:
        self.root = Path(settings.REPOS_DIR)
        self.root.mkdir(parents=True, exist_ok=True)

    def clone_repo(self, repo_url: str, branch: str | None = None) -> Path:
        target = self.root / f"repo_{uuid4().hex[:10]}"
        if branch:
            Repo.clone_from(repo_url, target, branch=branch, depth=1)
        else:
            Repo.clone_from(repo_url, target, depth=1)
        return target

    def cleanup_repo(self, path: Path) -> None:
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)

    def load_code_files(self, repo_path: Path) -> list[Path]:
        return collect_code_files(repo_path, 20)
