import json
from pathlib import Path
from datetime import datetime
from jinja2 import Template
from app.core.config import get_settings

settings = get_settings()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Code Review Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 32px; }
        h1 { color: #222; }
        .badge { display:inline-block; padding:6px 10px; border-radius:8px; background:#efefef; margin-right:8px; }
        .finding { border:1px solid #ddd; border-radius:12px; padding:14px; margin:12px 0; }
        .sev-high { border-left:6px solid #d32f2f; }
        .sev-medium { border-left:6px solid #f57c00; }
        .sev-low { border-left:6px solid #388e3c; }
        pre { white-space: pre-wrap; word-wrap: break-word; background:#f8f8f8; padding:12px; border-radius:8px; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <div>
        <span class="badge">Language: {{ language }}</span>
        <span class="badge">Provider: {{ provider }}</span>
        <span class="badge">Score: {{ score }}/10</span>
    </div>
    <h2>Summary</h2>
    <p>{{ summary }}</p>
    <h2>Strengths</h2>
    <ul>{% for item in strengths %}<li>{{ item }}</li>{% endfor %}</ul>
    <h2>Findings</h2>
    {% for f in findings %}
        <div class="finding sev-{{ f.severity }}">
            <h3>{{ f.title }} ({{ f.severity }})</h3>
            <p><strong>Category:</strong> {{ f.category }}</p>
            <p><strong>Explanation:</strong> {{ f.explanation }}</p>
            <p><strong>Recommendation:</strong> {{ f.recommendation }}</p>
            <p><strong>Line Hint:</strong> {{ f.line_hint }}</p>
        </div>
    {% endfor %}
    <h2>Test Suggestions</h2>
    <ul>{% for item in test_suggestions %}<li>{{ item }}</li>{% endfor %}</ul>
    <h2>Architecture Notes</h2>
    <ul>{% for item in architecture_notes %}<li>{{ item }}</li>{% endfor %}</ul>
    {% if refactored_code %}
    <h2>Refactored Code</h2>
    <pre>{{ refactored_code }}</pre>
    {% endif %}
</body>
</html>
"""


def _reports_dir() -> Path:
    output_dir = Path(settings.REPORTS_DIR).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def save_html_report(review_data: dict) -> str:
    output_dir = _reports_dir()
    filename = f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    path = output_dir / filename

    html = Template(HTML_TEMPLATE).render(**review_data)
    path.write_text(html, encoding="utf-8")

    return str(path)


def save_json_report(review_data: dict) -> str:
    output_dir = _reports_dir()
    filename = f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = output_dir / filename

    path.write_text(json.dumps(review_data, indent=2), encoding="utf-8")

    return str(path)
