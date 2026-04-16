from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.review_schema import ReviewRequest
from app.services.review_service import ReviewService
from app.services.report_service import save_html_report, save_json_report

router = APIRouter(prefix="/review", tags=["review"])
service = ReviewService()


@router.post("")
def review_code(payload: ReviewRequest, db: Session = Depends(get_db)):
    review = service.review_code(
        title=payload.title,
        code=payload.code,
        language=payload.language,
        review_mode=payload.review_mode,
    )
    service.persist_review(db, review)
    html_path = save_html_report(review.model_dump())
    json_path = save_json_report(review.model_dump())
    return {
        "review": review.model_dump(),
        "html_report": html_path,
        "json_report": json_path,
    }
