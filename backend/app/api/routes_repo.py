from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.review_schema import RepoReviewRequest
from app.services.repo_service import RepoService
from app.services.review_service import ReviewService
from app.services.report_service import save_html_report, save_json_report

router = APIRouter(prefix="/repo", tags=["repository"])
repo_service = RepoService()
review_service = ReviewService()


@router.post("/review")
def review_repository(payload: RepoReviewRequest, db: Session = Depends(get_db)):
    repo_path: Path | None = None
    try:
        repo_path = repo_service.clone_repo(payload.repo_url, payload.branch)
        code_files = repo_service.load_code_files(repo_path)

        if not code_files:
            raise HTTPException(status_code=400, detail="No supported code files found in repository.")

        file_payloads = []
        for file_path in code_files:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            file_payloads.append((str(file_path.relative_to(repo_path)), content))

        review = review_service.review_repository(
            title=payload.repo_url,
            files=file_payloads,
            review_mode=payload.review_mode,
        )
        review_service.persist_review(db, review)
        html_path = save_html_report(review.model_dump())
        json_path = save_json_report(review.model_dump())

        return {
            "review": review.model_dump(),
            "html_report": html_path,
            "json_report": json_path,
            "files_analyzed": len(file_payloads),
        }
    finally:
        if repo_path:
            repo_service.cleanup_repo(repo_path)
