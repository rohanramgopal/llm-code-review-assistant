# 🚀 LLM-Powered Code Review Assistant

![Python](https://img.shields.io/badge/Backend-Python-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?style=for-the-badge&logo=streamlit)
![Status](https://img.shields.io/badge/Status-Production--Ready-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 🧠 What is this?

**LLM Code Review Assistant** is an intelligent developer tool that analyzes code snippets and repositories, identifies issues, assigns severity levels, and generates structured review reports — all with a polished UI experience.

It mimics real-world tools like:
- GitHub PR reviews
- SonarQube
- AI-powered code analysis platforms

---

## ✨ Key Features

### 🔍 Smart Code Analysis
- Detects:
  - 🔴 Security issues (eval, hardcoded secrets)
  - 🟡 Code quality problems
  - 🟠 Performance bottlenecks
  - ⚠️ Logical flaws

---

### 📊 Intelligent Scoring System
- Scores code from **1 → 10**
- Based on severity of issues
- Realistic evaluation like senior engineers

---

### 🧠 Hybrid Review Engine
- Rule-based fast analysis (no lag)
- Optional LLM integration (OpenAI / Ollama)
- Smart fallback system

---

### 🎯 Line-Level Issue Detection
- Pinpoints exact problematic lines
- Example:

line 23: return eval(user_input)


---

### 🎨 Modern UI Dashboard
- Dark themed developer UI
- Severity badges (High / Medium / Low)
- Expandable issue cards
- Clean structured output

---

### 📁 Repository Analysis
- Analyze full GitHub repos
- Lightweight scanning (optimized for laptops)
- Multi-file insights

---

### 📄 Report Generation
- HTML Reports (beautiful view)
- JSON Reports (structured data)
- Stored locally for reuse

---


## 🏗️ Architecture

Frontend (Streamlit UI)  
⬇  
Backend (FastAPI)  
⬇  
Review Engine  
⬇  
Rule Engine  
⬇  
Smart Scoring  
⬇  
LLM Service (optional)  
⬇  
Repository Scanner  
⬇  
Report Generator
---


## 🏗️ Architecture Diagram

```mermaid
flowchart TD

A[User / Developer] --> B[Streamlit Frontend]

subgraph Frontend
    B --> F1[Code Input]
    B --> F2[Repository Input]
    B --> F3[Review Dashboard]
end

B -->|REST API Calls| C[FastAPI Backend]

subgraph Backend
    C --> D1[API Routes]
    D1 --> D2[Review Service]

    D2 --> S1[Rule Engine]
    D2 --> S2[Smart Scoring Engine]
    D2 --> S3[LLM Service (Optional)]
    D2 --> S4[Repository Scanner]
end

subgraph Processing
    S1 --> P1[Static Analysis]
    S2 --> P2[Score Calculation]
    S3 --> P3[LLM Insights]
    S4 --> P4[Multi-file Parsing]
end

P1 --> R[Review Generator]
P2 --> R
P3 --> R
P4 --> R

subgraph Output
    R --> O1[Summary]
    R --> O2[Findings]
    R --> O3[Severity Breakdown]
    R --> O4[Refactored Code]
end

O1 --> H[HTML Report Generator]
O2 --> H
O3 --> H
O4 --> H

O1 --> J[JSON Report Generator]
O2 --> J
O3 --> J
O4 --> J

H --> B
J --> B

```

---

## 📂 Project Structure 

```md



llm-code-review-assistant/
│
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── core/
│ │ ├── db/
│ │ ├── models/
│ │ ├── schemas/
│ │ ├── services/
│ │ ├── utils/
│ │ └── main.py
│ │
│ ├── reports/
│ └── requirements.txt
│
├── frontend/
│ └── app.py
│
└── README.md
---

## 🚀 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/rohanramgopal/llm-code-review-assistant.git
cd llm-code-review-assistant
2️⃣ Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3️⃣ Run backend
uvicorn app.main:app --reload

Backend runs on:
👉 http://127.0.0.1:8000

4️⃣ Run frontend
cd ../frontend
streamlit run app.py

Frontend runs on:
👉 http://localhost:8501

🧪 Example Test Code
def divide(a, b):
    try:
        return a / b
    except Exception:
        return 0

Output:
⚠️ Generic exception handling
⚠️ Silent failure logic
Score: 6/10

📊 Sample Outputs
🔴 Bad Code
Score: 1/10
High severity issues detected

🟢 Clean Code
Score: 9/10
Minimal issues

💡 Why This Project Stands Out
Combines AI + Software Engineering + UI
Designed like a real developer tool
Handles both snippets and repositories
Optimized for performance on local machines
Production-style architecture


🔮 Future Enhancements
🔍 GitHub PR integration
🧠 Advanced LLM reasoning mode
🎯 Inline code highlighting
☁️ Cloud deployment
🔐 Authentication system
📈 Analytics dashboard
👨‍💻 Author

Rohan Ramgopal
📍 Bengaluru, India
