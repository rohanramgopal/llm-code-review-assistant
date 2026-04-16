import requests
from app.core.config import get_settings

settings = get_settings()


def get_pull_request_files(repo_full_name: str, pr_number: int) -> list[dict]:
    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()


def post_pr_comment(repo_full_name: str, pr_number: int, comment: str) -> dict:
    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
    response = requests.post(url, headers=headers, json={"body": comment}, timeout=60)
    response.raise_for_status()
    return response.json()
