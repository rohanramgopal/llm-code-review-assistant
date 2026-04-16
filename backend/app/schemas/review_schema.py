from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    title: str = Field(default="Untitled Review")
    code: str
    language: Optional[str] = None
    review_mode: Literal["quick", "deep", "security", "performance"] = "deep"


class RepoReviewRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = None
    review_mode: Literal["quick", "deep", "security", "performance"] = "deep"


class Finding(BaseModel):
    category: str
    severity: Literal["low", "medium", "high"]
    title: str
    explanation: str
    recommendation: str
    line_hint: Optional[str] = None


class ReviewResponse(BaseModel):
    title: str
    language: Optional[str]
    provider: str
    score: int
    summary: str
    strengths: List[str]
    findings: List[Finding]
    refactored_code: Optional[str] = None
    test_suggestions: List[str] = []
    architecture_notes: List[str] = []
