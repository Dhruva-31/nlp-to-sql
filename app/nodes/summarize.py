from pathlib import Path

from langchain_groq import ChatGroq
from app.graph import GraphState
from app.utils.clean_response import remove_thinking

PROMPT_PATH = Path("prompts/summarize_prompt.txt")

try:
    prompt_template = PROMPT_PATH.read_text()
except FileNotFoundError:
    raise RuntimeError(f"Prompt file not found: {PROMPT_PATH}")

llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)


def summarize(state: GraphState):
    """This node summarizes the SQL result"""

    response = llm.invoke(prompt_template)
    answer = remove_thinking(str(response.content))

    return {"final_answer": answer}
