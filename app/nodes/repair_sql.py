from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from app.state import GraphState
from app.utils.sql_parser import extract_sql

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
)

prompt_template = Path("prompts/repair_prompt.txt").read_text()


def repair_sql(state: GraphState):
    """This node repairs the generated SQL query after execution"""

    prompt = prompt_template.format(
        question=state["question"],
        schema=state["schema"],
        sql=state["sql_query"],
        error=state["error"],
    )

    response = llm.invoke(prompt)

    repaired_sql = extract_sql(str(response.content))

    return {
        "sql_query": repaired_sql,
        "retry_count": state["retry_count"] + 1,
        "error": "",
    }
