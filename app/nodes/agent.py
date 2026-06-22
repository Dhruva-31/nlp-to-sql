from pathlib import Path
import re

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama

from app.state import GraphState
from app.tools.sql_tool import execute_sql_query
from app.tools.schema_tool import answer_schema_question

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

TOOLS = [execute_sql_query, answer_schema_question]
TOOL_NAMES = {t.name for t in TOOLS}

agent_llm = ChatOllama(
    model="qwen3:4b",
    temperature=0,
).bind_tools(TOOLS)

DEFAULT_SYSTEM_PROMPT = """\
You are a SQL assistant for a PostgreSQL database. Respond in English only. No thinking tags.
You have exactly two tools:

1. answer_schema_question
   - Use this to look up table names, column names, data types, and relationships.
   - Call this ONCE per user question. Do NOT call it multiple times for the same question.
   - After receiving the result, answer the user immediately. Do not call any tool again
     unless the user asks a follow-up question.
   - Use this alone when the user asks about structure: "what tables exist",
     "what columns does X have", "show me the schema", "describe the database".
   - NEVER call execute_sql_query for schema/structure questions.

2. execute_sql_query
   - Use this ONLY when the user wants actual data rows, counts, or aggregates,
     or wants to insert/update/delete/alter data.
   - Always call answer_schema_question FIRST (once) to get the correct table and
     column names, then call this tool with the SQL you write from that schema.
   - Pass: sql (the query), question (the user's original question),
     schema_context (the exact text returned by answer_schema_question).
   - If this returns an error, read it carefully and call this tool again ONCE with
     a corrected query. Do not retry more than once without explaining the problem.

Decision rules (follow these strictly):
- User asks about structure/schema → call answer_schema_question ONCE → answer.
- User wants data → call answer_schema_question ONCE → write SQL → call execute_sql_query ONCE → answer.
- Never call execute_sql_query for schema questions.
"""

SYSTEM_PROMPT = SystemMessage(content=DEFAULT_SYSTEM_PROMPT)

PYTHON_TAG_RE = re.compile(r"<\|python_tag\|>\s*(\{.*\})", re.DOTALL)


def agent(state: GraphState) -> dict:
    """Replaces generate_sql.py (SQL generation) and summarize.py
    (final answer generation) -- both are now just this same LLM
    reasoning over the message history with tools bound."""
    messages = [SYSTEM_PROMPT, *state["messages"]]
    if len(messages) > 3:
        messages = [messages[0]] + messages[-2:]
    response = agent_llm.invoke(messages)
    return {"messages": [response]}
