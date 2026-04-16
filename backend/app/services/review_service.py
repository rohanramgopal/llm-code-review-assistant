import json
from typing import Any
from sqlalchemy.orm import Session
from app.schemas.review_schema import ReviewResponse, Finding
from app.services.llm_service import call_llm
from app.services.rule_engine import run_static_rules
from app.services.smart_enhancer import generate_smart_summary, calculate_smart_score
from app.services.cleaner import deduplicate_findings
from app.services.strengths_engine import generate_strengths
from app.models.review_models import ReviewRecord
from app.utils.code_parser import detect_language


PROMPT_TEMPLATE = """
You are a senior software engineer performing a practical code review.

Return ONLY valid JSON with these exact keys:
score, summary, strengths, findings, refactored_code, test_suggestions, architecture_notes

Rules:
- score must be an integer from 1 to 10
- strengths must be a list of short strings
- findings must be a list of objects
- each finding must contain:
  category, severity, title, explanation, recommendation, line_hint
- severity must be one of: low, medium, high
- keep the review concrete and developer-friendly
- do not include markdown fences
- do not include extra text outside JSON

Review mode: {review_mode}
Language: {language}

Code:
{code}
"""


class ReviewService:
    def __init__(self) -> None:
        pass

    def _normalize(self, data: dict[str, Any], title: str, language: str | None, provider: str) -> ReviewResponse:
        findings = []
        for item in data.get("findings", []):
            if isinstance(item, dict):
                try:
                    findings.append(Finding(**item))
                except Exception:
                    continue

        return ReviewResponse(
            title=title,
            language=language,
            provider=provider,
            score=int(data.get("score", 5)),
            summary=data.get("summary", "No summary generated."),
            strengths=data.get("strengths", []),
            findings=findings,
            refactored_code=data.get("refactored_code") or None,
            test_suggestions=data.get("test_suggestions", []),
            architecture_notes=data.get("architecture_notes", []),
        )

    def review_code(self, title: str, code: str, language: str | None, review_mode: str) -> ReviewResponse:
        language = language or detect_language(None, code)
        rule_findings = run_static_rules(code, language)

        prompt = PROMPT_TEMPLATE.format(
            review_mode=review_mode,
            language=language,
            code=code[:8000],
        )

        raw = call_llm(prompt)
        data = self._safe_json(raw)

        merged_findings = self._merge_findings(data.get("findings", []), rule_findings)
        cleaned_findings = deduplicate_findings(merged_findings)

        data["findings"] = cleaned_findings
        data["score"] = calculate_smart_score(data["findings"])
        data["summary"] = generate_smart_summary(data["findings"])
        data["strengths"] = generate_strengths(code)

        if not data.get("test_suggestions"):
            data["test_suggestions"] = [
                "Add tests for normal inputs.",
                "Add tests for failure cases and edge conditions."
            ]

        if not data.get("architecture_notes"):
            data["architecture_notes"] = [
                "Using lightweight local mode for fast feedback."
            ]

        return self._normalize(data, title, language, "local-fast-review")

    def review_repository(self, title: str, files: list[tuple[str, str]], review_mode: str) -> ReviewResponse:
        limited_files = files[:5]

        combined_code = "\n\n".join(
            f"# FILE: {name}\n{content[:1500]}" for name, content in limited_files
        )

        rule_findings = []
        for name, content in limited_files:
            findings = run_static_rules(content[:3000], None)
            for item in findings:
                if item.line_hint == "entire file":
                    item.line_hint = f"file: {name}"
            rule_findings.extend(findings)

        prompt = PROMPT_TEMPLATE.format(
            review_mode=review_mode,
            language="multi-file",
            code=combined_code[:10000],
        )

        raw = call_llm(prompt)
        data = self._safe_json(raw)

        merged_findings = self._merge_findings(data.get("findings", []), rule_findings)
        cleaned_findings = deduplicate_findings(merged_findings)

        data["findings"] = cleaned_findings
        data["score"] = calculate_smart_score(data["findings"])
        data["summary"] = generate_smart_summary(data["findings"])
        data["strengths"] = [
            "Repository scan completed on representative files",
            "Static checks were applied across sampled source files",
            "Review optimized for local laptop performance"
        ]

        if not data.get("test_suggestions"):
            data["test_suggestions"] = [
                "Add tests around changed modules.",
                "Validate edge cases and failure paths.",
                "Add regression tests for critical code paths."
            ]

        if not data.get("architecture_notes"):
            data["architecture_notes"] = [
                "Repository review is intentionally lightweight in local mode.",
                "Only a subset of files is scanned to avoid freezing the laptop."
            ]

        return self._normalize(data, title, "multi-file", "local-fast-review")

    def persist_review(self, db: Session, review: ReviewResponse) -> ReviewRecord:
        record = ReviewRecord(
            title=review.title,
            language=review.language,
            provider=review.provider,
            score=review.score,
            summary=review.summary,
            findings_json=review.model_dump_json(),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def _safe_json(self, raw: str) -> dict:
        try:
            return json.loads(raw)
        except Exception:
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(raw[start:end + 1])
                except Exception:
                    pass

        return {
            "score": 7,
            "summary": "Rule-based local review completed.",
            "strengths": [],
            "findings": [],
            "refactored_code": "",
            "test_suggestions": [
                "Add tests for normal inputs.",
                "Add tests for error conditions."
            ],
            "architecture_notes": [
                "Using lightweight local mode for better performance."
            ]
        }

    def _merge_findings(self, llm_findings: list[dict], rule_findings: list[Finding]) -> list[dict]:
        merged = list(llm_findings) if isinstance(llm_findings, list) else []
        existing_titles = {
            f.get("title", "").lower()
            for f in merged
            if isinstance(f, dict)
        }

        for rule in rule_findings:
            if rule.title.lower() not in existing_titles:
                merged.append(rule.model_dump())

        return merged
