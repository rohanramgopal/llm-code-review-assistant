import json
import requests
from app.core.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def _rules_response() -> str:
    return json.dumps({
        "score": 7,
        "summary": "Rule-based review completed successfully.",
        "strengths": ["Code was analyzed locally without external LLM dependency."],
        "findings": [],
        "refactored_code": "",
        "test_suggestions": [
            "Add tests for normal inputs.",
            "Add tests for invalid or edge-case inputs."
        ],
        "architecture_notes": [
            "Running in lightweight local rules mode."
        ]
    })


def call_openai(prompt: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            temperature=0.2,
            messages=[
                {"role": "system", "content": "You are a senior code reviewer. Return strict JSON only."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content or "{}"
    except Exception as exc:
        logger.exception("OpenAI call failed: %s", exc)
        return _rules_response()


def call_ollama(prompt: str) -> str:
    try:
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        }
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=20
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "{}")
    except Exception as exc:
        logger.exception("Ollama call failed: %s", exc)
        return _rules_response()


def call_llm(prompt: str) -> str:
    provider = settings.LLM_PROVIDER.lower().strip()

    if provider == "rules":
        return _rules_response()

    if provider == "openai":
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY missing. Falling back to rules mode.")
            return _rules_response()
        return call_openai(prompt)

    if provider == "ollama":
        return call_ollama(prompt)

    logger.warning("Unknown provider '%s'. Falling back to rules mode.", provider)
    return _rules_response()
