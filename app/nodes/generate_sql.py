from pathlib import Path
from langchain_groq import ChatGroq

from app.db.schema import get_schema
from app.graph import GraphState
from app.utils.sql_parser import extract_sql

PROMPT_PATH = Path("prompts/sql_prompt.txt")

try:
    prompt_template = PROMPT_PATH.read_text()
except FileNotFoundError:
    raise RuntimeError(f"Prompt file not found: {PROMPT_PATH}")


llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)


def generate_sql(state: GraphState):
    """This node generates the SQL equivalent of User request"""

    schema = get_schema()
    prompt = prompt_template.format(schema=schema, question=state["question"])

    response = llm.invoke(prompt)
    sql = extract_sql(str(response.content))

    return {
        "schema": schema,
        "sql_query": sql,
    }
