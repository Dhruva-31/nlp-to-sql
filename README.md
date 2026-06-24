# 🧠 NLP-to-SQL Agent

Convert natural language questions into SQL queries using an AI-powered agent built with LangGraph, LangChain, Groq LLMs, and PostgreSQL.

The system understands user questions, retrieves database schema information, generates SQL queries, executes them safely, and returns results through an interactive chat interface.

---

## 🚀 Features

### Natural Language to SQL
Ask questions in plain English and automatically generate SQL queries.

### Schema-Aware Query Generation
The agent first retrieves database schema information before generating SQL, reducing hallucinations and improving accuracy.

### Safe Query Execution
- Read-only queries execute automatically.
- Risky operations (`UPDATE`, `DELETE`, `DROP`, `ALTER`, etc.) require human approval before execution.

### LangGraph Workflow
Built using a stateful LangGraph pipeline with:
- Agent Node
- Tool Execution Node
- Human Approval Node
- Conditional Routing

### Query Logging
Every executed query is logged with:
- Timestamp
- Generated SQL
- Execution time
- Row count
- Success / Failure status

### Interactive Chat Interface
Simple Streamlit-based UI for chatting with the database.

---

## 🏗️ Architecture

```text
User Question
      │
      ▼
 AI Agent (Groq LLM)
      │
      ▼
 Schema Retrieval Tool
      │
      ▼
 SQL Generation
      │
      ▼
 Risk Classification
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Safe     High Risk
 │         │
 ▼         ▼
Execute  Human Approval
 │         │
 └────┬────┘
      ▼
 Results
```

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### AI & Agent Framework
- LangGraph
- LangChain
- Groq API
- Qwen 3 32B

### Database
- PostgreSQL
- SQLAlchemy
- Psycopg

### Backend
- Python

---

## 📂 Project Structure

```text
app/
│
├── db/
│   ├── connection.py
│   ├── seed.py
│   └── build_schema_docs.py
│
├── nodes/
│   ├── agent.py
│   ├── tools.py
│   └── human_approval.py
│
├── tools/
│   ├── schema_tool.py
│   └── sql_tool.py
│
├── utils/
│   └── logger.py
│
├── graph.py
├── state.py
└── risk.py

main.py
Dockerfile
docker-compose.yaml
requirements.txt
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd nlp-to-sql
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Linux / Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key

DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

---

## ▶️ Run Application

```bash
streamlit run main.py
```

Application will be available at:

```text
http://localhost:8501
```

---

## 💡 Example Queries

```text
What tables exist?

Describe the database schema.

Show all customers.

List all orders placed this month.

Top 5 products by sales.

What is the total revenue this year?
```

---

## 🔒 Safety Features

- Schema validation before SQL generation
- Risk classification for generated SQL
- Human approval workflow for destructive operations
- Execution logging and auditing
- Automatic retry on SQL errors

---

## 📈 Future Improvements

- Multi-database support
- Query result visualizations
- Role-based access control
- Vector-based schema retrieval
- Query explanation mode
- Conversational memory with persistent storage

---

## 👨‍💻 Author

**Dhruva**

Built as an AI-powered database assistant that bridges natural language and SQL through agentic workflows and safe query execution.
