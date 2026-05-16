# NovaAssist Enterprise RAG 🛡️🧠

## 🚨 The Problem

At most growing enterprises, critical data is scattered across disconnected silos. HR policies live in PDFs, payroll and financial records sit in SQL databases, and IT security logs are buried in JSON files. Employees waste hours trying to track down information, and enforcing security across all these different formats is a massive headache.

**The Challenge:** How can we build a single, unified AI assistant that allows employees to ask natural language questions, intelligently routes those questions to the right data silo, and synthesizes an accurate answer—all while **strictly enforcing Role-Based Access Control (RBAC)** so nobody ever sees confidential data above their paygrade?

## 💡 The Solution

**NovaAssist** is a production-grade, context-aware Retrieval-Augmented Generation (RAG) pipeline designed to navigate highly fragmented data silos securely.

Instead of relying on a single vector database with no security, NovaAssist utilizes an LLM-based intelligent routing agent combined with strict database-level payload filtering to ensure every query is both highly accurate and cryptographically secure based on the user's role.

![Architecture Diagram](<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/de5da46e-0a74-4d86-b868-ed2c2d70b50f" />)
*(If you draw a quick flowchart of how the Router -> Retriever -> Generator works, put it here)*

---

## ✨ Key Features

- **Synthetic Data Factory:** Auto-generates a realistic, multi-format enterprise ecosystem using `Faker` and `pandas` (PDFs, SQLite, JSON), automatically mapping documents to `allowed_roles`.
- **Intelligent Query-Aware Routing:** An LLM routing agent intercepts queries and directs them to the exact data silo (`pdf`, `sqlite`, `json`), or triggers multi-silo retrieval for complex questions.
- **Database-Level RBAC Enforcement:** Security isn't left to the LLM. Using **Qdrant Payload Filtering**, unauthorized data is physically blocked from retrieval before the AI even sees it.
- **Zero-Hallucination Generation:** The generation prompt strictly bounds the LLM to the retrieved context. If the answer isn't in the allowed documents, it safely admits it.
- **Mandatory Citations:** Every claim the AI makes includes an inline citation mapping directly back to the original `doc_id` (e.g., `[Source: hr_doc_2]`).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | Python, LangChain Core |
| Vector Database | Qdrant (Local with Payload Filtering) |
| Embeddings | FastEmbed (`BAAI/bge-small-en-v1.5`) |
| LLM Inference | Groq API (`llama-3.3-70b-versatile`) |
| Frontend UI | Streamlit |

---

## 🚀 Installation & Setup

**1. Clone the repository:**
```bash
git clone https://github.com/YourUsername/nova-assist.git
cd nova-assist
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Set up your environment variables:**

Create a `.env` file in the root directory and add your Groq API Key:
```text
GROQ_API_KEY="your_api_key_here"
```

**4. Run the application:**
```bash
streamlit run app.py
```

---

## 📸 Role-Based Access Showcase

NovaAssist features a dynamic role-switching UI to easily test the security perimeter. Here is how the system handles the same data across different security clearances:

### 1. 👤 Standard Employee
Can access general HR handbooks, but is physically blocked from querying financial databases.

![Standard Employee View](docs/images/role_employee_placeholder.png)

### 2. 💰 Finance Analyst
Intelligently routes to the SQLite database to extract and summarize restricted salary records.

![Finance Analyst View](docs/images/role_finance_placeholder.png)

### 3. 🔒 IT Admin
Routes to semi-structured JSON logs to parse and identify sensitive server access/VPN events.

![IT Admin View](docs/images/role_it_admin_placeholder.png)

### 4. 🌐 Super Admin (Multi-Silo Reasoning)
Handles complex, multi-intent queries by routing to `ALL` silos and synthesizing a unified answer across isolated datasets.

![Super Admin View](docs/images/role_super_admin_placeholder.png)

---

## 📁 Repository Structure

```text
nova_assist/
│
├── data/                       # Generated synthetic mock data & Qdrant DB
├── src/
│   ├── data_factory/           # Scripts to generate mock PDFs, SQL, JSON
│   │   └── generate_mock_data.py
│   ├── ingestion/              # Document parsers and Qdrant Indexer
│   │   ├── parsers.py
│   │   └── qdrant_indexer.py
│   └── rag_engine/             # Core intelligence layer
│       ├── router.py           # LLM Intent Router
│       ├── retriever.py        # Qdrant search with RBAC payload filtering
│       └── generator.py        # Grounded generation with citations
│
├── .env                        # Environment variables (Ignored by Git)
├── app.py                      # Streamlit Frontend application
├── requirements.txt            # Python dependencies
└── README.md
```
