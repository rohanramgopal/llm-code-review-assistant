from fastapi import APIRouter, Header, HTTPException, Request
from app.core.security import verify_signature
from app.services.github_service import get_pull_request_files, post_pr_comment
from app.services.review_service import ReviewService

router = APIRouter(prefix="/github", tags=["github"])
service = ReviewService()


@router.post("/webhook")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None),
    x_github_event: str | None = Header(default=None),
):
    payload = await request.body()

    if not verify_signature(payload, x_hub_signature_256 or ""):
        raise HTTPException(status_code=401, detail="Invalid GitHub signature")

    data = await request.json()

    if x_github_event == "pull_request" and data.get("action") in {"opened", "synchronize", "reopened"}:
        repo_full_name = data["repository"]["full_name"]
        pr_number = data["pull_request"]["number"]
        files = get_pull_request_files(repo_full_name, pr_number)

        review_inputs = []
        for item in files:
            patch = item.get("patch")
            filename = item.get("filename")
            if patch and filename:
                review_inputs.append((filename, patch))

        if review_inputs:
            review = service.review_repository(
                title=f"PR Review #{pr_number}",
                files=review_inputs,
                review_mode="deep",
            )
            comment_lines = [
                f"## Automated Review Score: {review.score}/10",
                "",
                f"**Summary:** {review.summary}",
                "",
                "### Key Findings",
            ]
            for finding in review.findings[:8]:
                comment_lines.append(
                    f"- **[{finding.severity.upper()}]** {finding.title}: {finding.recommendation}"
                )
            post_pr_comment(repo_full_name, pr_number, "\n".join(comment_lines))

    return {"status": "processed"}
