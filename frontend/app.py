import html
import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LLM Code Review Assistant",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .hero {
        padding: 1.4rem 1.6rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #0f172a 0%, #0b1220 45%, #1e293b 100%);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1.25rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
        color: white;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #cbd5e1;
        line-height: 1.5;
    }
    .metric-card {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        background: #0f172a;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        margin-bottom: 0.75rem;
        min-height: 120px;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.92rem;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        color: white;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
        word-break: break-word;
    }
    .section-card {
        padding: 1.15rem 1.25rem;
        border-radius: 20px;
        background: #081225;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.75rem;
    }
    .summary-text {
        color: #e2e8f0;
        font-size: 1rem;
        line-height: 1.7;
    }
    .strength-item, .test-note {
        padding: 0.75rem 0.95rem;
        border-radius: 14px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.55rem;
        color: #e5e7eb;
    }
    .badge {
        display: inline-block;
        padding: 0.32rem 0.72rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.02em;
    }
    .badge-high {
        background: rgba(239, 68, 68, 0.18);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }
    .badge-medium {
        background: rgba(245, 158, 11, 0.18);
        color: #fcd34d;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .badge-low {
        background: rgba(34, 197, 94, 0.18);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.35);
    }
    .badge-category {
        background: rgba(59, 130, 246, 0.16);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.35);
        margin-left: 0.45rem;
    }
    .small-muted {
        color: #94a3b8;
        font-size: 0.92rem;
    }
    .score-good {
        color: #22c55e;
    }
    .score-mid {
        color: #f59e0b;
    }
    .score-bad {
        color: #ef4444;
    }
    .repo-note {
        margin-top: 0.5rem;
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)


def severity_badge(severity: str) -> str:
    sev = (severity or "").lower()
    cls = "badge-low"
    if sev == "high":
        cls = "badge-high"
    elif sev == "medium":
        cls = "badge-medium"
    return f'<span class="badge {cls}">{html.escape(sev.upper())}</span>'


def category_badge(category: str) -> str:
    return f'<span class="badge badge-category">{html.escape((category or "general").upper())}</span>'


def score_class(score: int) -> str:
    if score >= 8:
        return "score-good"
    if score >= 5:
        return "score-mid"
    return "score-bad"


def render_metric(label: str, value: str, value_class: str = ""):
    cls = f"metric-value {value_class}".strip()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{html.escape(label)}</div>
        <div class="{cls}">{html.escape(value)}</div>
    </div>
    """, unsafe_allow_html=True)


def render_findings(findings):
    st.markdown('<div class="section-card"><div class="section-title">Key Findings</div>', unsafe_allow_html=True)

    for idx, finding in enumerate(findings, start=1):
        title = finding.get("title", "Finding")
        severity = finding.get("severity", "low")
        category = finding.get("category", "general")
        explanation = finding.get("explanation", "")
        recommendation = finding.get("recommendation", "")
        line_hint = finding.get("line_hint", "")

        emoji = "🔴" if severity == "high" else "🟡" if severity == "medium" else "🟢"

        with st.expander(f"{emoji} {title}", expanded=(idx == 1)):
            st.markdown(f"""
            <div style="margin-bottom:0.75rem;">
                {severity_badge(severity)} {category_badge(category)}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**What it means:** {explanation}")
            st.markdown(f"**Recommended fix:** {recommendation}")
            st.code(line_hint if line_hint else "No line hint available")

    st.markdown("</div>", unsafe_allow_html=True)


def render_review(review: dict, html_report: str | None = None, json_report: str | None = None, files_analyzed: int | None = None):
    score = review.get("score", 0)
    provider = review.get("provider", "unknown")
    findings = review.get("findings", [])
    summary = review.get("summary", "")
    strengths = review.get("strengths", [])
    tests = review.get("test_suggestions", [])
    notes = review.get("architecture_notes", [])
    refactored_code = review.get("refactored_code")

    high_count = sum(1 for f in findings if f.get("severity") == "high")
    medium_count = sum(1 for f in findings if f.get("severity") == "medium")
    low_count = sum(1 for f in findings if f.get("severity") == "low")

    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric("Score", f"{score}/10", score_class(score))
    with col2:
        render_metric("Provider", provider)
    with col3:
        render_metric("Findings", str(len(findings)))

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">Summary</div>
        <div class="summary-text">{html.escape(summary)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">Severity Breakdown</div>
        <div class="summary-text">
            🔴 High: <b>{high_count}</b> &nbsp;&nbsp;
            🟡 Medium: <b>{medium_count}</b> &nbsp;&nbsp;
            🟢 Low: <b>{low_count}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if strengths:
        st.markdown('<div class="section-card"><div class="section-title">Strengths</div>', unsafe_allow_html=True)
        for item in strengths:
            st.markdown(f'<div class="strength-item">• {html.escape(item)}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if findings:
        render_findings(findings)

    if tests:
        st.markdown('<div class="section-card"><div class="section-title">Suggested Tests</div>', unsafe_allow_html=True)
        for item in tests:
            st.markdown(f'<div class="test-note">• {html.escape(item)}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if notes:
        st.markdown('<div class="section-card"><div class="section-title">Architecture Notes</div>', unsafe_allow_html=True)
        for item in notes:
            st.markdown(f'<div class="test-note">• {html.escape(item)}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if refactored_code:
        st.markdown('<div class="section-card"><div class="section-title">Refactored Code Suggestion</div>', unsafe_allow_html=True)
        st.code(refactored_code, language="python")
        st.markdown("</div>", unsafe_allow_html=True)

    if html_report or json_report or files_analyzed is not None:
        st.markdown('<div class="section-card"><div class="section-title">Generated Reports</div>', unsafe_allow_html=True)
        if html_report:
            st.markdown(f'<div class="small-muted">HTML report: <code>{html.escape(html_report)}</code></div>', unsafe_allow_html=True)
        if json_report:
            st.markdown(f'<div class="small-muted">JSON report: <code>{html.escape(json_report)}</code></div>', unsafe_allow_html=True)
        if files_analyzed is not None:
            st.markdown(f'<div class="repo-note">Files analyzed: <b>{files_analyzed}</b></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <div class="hero-title">LLM-Powered Code Review Assistant</div>
    <div class="hero-subtitle">
        Analyze snippets and small repositories with cleaner findings, better summaries,
        severity tags, and a polished review experience.
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Snippet Review", "Repository Review"])

with tab1:
    left, right = st.columns([1.2, 1])

    with left:
        title = st.text_input("Review Title", value="Sample Review")
        language = st.selectbox(
            "Language",
            ["python", "javascript", "typescript", "java", "go", "cpp", "unknown"],
            index=0
        )
        review_mode = st.selectbox(
            "Review Mode",
            ["quick", "deep", "security", "performance"],
            index=1
        )

    with right:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Quick Test Ideas</div>
            <div class="small-muted">
                Try code with eval usage, hardcoded secrets, nested loops, weak exception handling,
                or silent fallback values to get richer findings.
            </div>
        </div>
        """, unsafe_allow_html=True)

    example_code = """import requests

API_KEY = "hardcoded-secret-key"

def fetch_user_data(user_id):
    url = "https://api.example.com/user/" + str(user_id)
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None

def divide(a, b):
    try:
        return a / b
    except Exception:
        return 0

def execute_code(user_input):
    return eval(user_input)
"""

    if "code_input" not in st.session_state:
        st.session_state["code_input"] = ""

    code = st.text_area(
        "Paste your code here",
        height=320,
        value=st.session_state["code_input"],
        placeholder="Paste your code snippet here..."
    )

    c1, c2, c3 = st.columns([1, 1, 3])

    if c1.button("Analyze Snippet", use_container_width=True):
        if not code.strip():
            st.warning("Paste a code snippet first.")
        else:
            try:
                with st.spinner("Reviewing snippet..."):
                    payload = {
                        "title": title,
                        "language": language,
                        "review_mode": review_mode,
                        "code": code,
                    }
                    response = requests.post(f"{API_BASE}/review", json=payload, timeout=120)
                    response.raise_for_status()
                    result = response.json()
                    render_review(
                        result["review"],
                        result.get("html_report"),
                        result.get("json_report")
                    )
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")

    if c2.button("Load Example", use_container_width=True):
        st.session_state["code_input"] = example_code
        st.rerun()

with tab2:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">Repository Review</div>
        <div class="small-muted">
            Use smaller repositories in local mode. Large repositories can still feel slow on a laptop.
        </div>
    </div>
    """, unsafe_allow_html=True)

    repo_url = st.text_input("GitHub Repository URL", value="")
    branch = st.text_input("Branch", value="")
    review_mode_repo = st.selectbox(
        "Repository Review Mode",
        ["quick", "deep", "security", "performance"],
        index=1,
        key="repo_mode"
    )

    if st.button("Analyze Repository", use_container_width=True):
        if not repo_url.strip():
            st.warning("Enter a repository URL first.")
        else:
            try:
                with st.spinner("Cloning and analyzing repository..."):
                    payload = {
                        "repo_url": repo_url,
                        "branch": branch or None,
                        "review_mode": review_mode_repo,
                    }
                    response = requests.post(f"{API_BASE}/repo/review", json=payload, timeout=300)
                    response.raise_for_status()
                    result = response.json()
                    render_review(
                        result["review"],
                        result.get("html_report"),
                        result.get("json_report"),
                        result.get("files_analyzed")
                    )
            except requests.RequestException as exc:
                st.error(f"Repository review failed: {exc}")
