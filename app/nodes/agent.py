from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from app.state import GraphState
from app.tools.sql_tool import execute_sql_query
from app.tools.schema_tool import answer_schema_question

load_dotenv()

TOOLS = [execute_sql_query, answer_schema_question]
agent_llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
).bind_tools(TOOLS)

DEFAULT_SYSTEM_PROMPT = """\
You are a PostgreSQL database assistant.

Always call answer_schema_question once before generating SQL.

Default behavior: DATA RETRIEVAL.

If user asks to show, list, display, fetch, retrieve, or give records:
- Return records.
- No analysis.
- No summary.
- No insights.
- No aggregation.
- No LIMIT unless explicitly requested.

Only perform analysis if user explicitly asks for:
count, average, sum, total, trend, compare, ranking, report, summary, analysis.

Use only tables and columns from schema.

Retry SQL once on failure.

If unsure, return records, not analysis.
"""

SYSTEM_PROMPT = SystemMessage(content=DEFAULT_SYSTEM_PROMPT)


def agent(state: GraphState) -> dict:
    """Generates SQL query and summarizes the results and analytics based on the query result."""
    messages = [SYSTEM_PROMPT, *state["messages"]]
    if len(messages) > 3:
        messages = [messages[0]] + messages[-2:]

    response = agent_llm.invoke(messages)

    return {"messages": [response]}
