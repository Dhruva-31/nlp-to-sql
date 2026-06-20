from pathlib import Path
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from app.state import GraphState
from app.utils.sql_parser import extract_sql

load_dotenv()

PROMPT_PATH = Path("prompts/sql_prompt.txt")

try:
    prompt_template = PROMPT_PATH.read_text()
except FileNotFoundError:
    raise RuntimeError(f"Prompt file not found: {PROMPT_PATH}")


generate_sql_llm = ChatGroq(model="qwen/qwen3-32b")


def generate_sql(state: GraphState):
    """This node generates the SQL equivalent of User request"""

    schema = state["schema"]
    prompt = prompt_template.format(schema=schema, question=state["question"])

    response = generate_sql_llm.invoke(prompt)
    sql = extract_sql(str(response.content))

    return {
        "schema": schema,
        "sql_query": sql,
    }
