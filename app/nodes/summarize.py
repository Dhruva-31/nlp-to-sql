from pathlib import Path

from langchain_groq import ChatGroq
from app.state import GraphState
from app.utils.clean_response import remove_thinking

PROMPT_PATH = Path("prompts/summarize_prompt.txt")

try:
    prompt_template = PROMPT_PATH.read_text()
except FileNotFoundError:
    raise RuntimeError(f"Prompt file not found: {PROMPT_PATH}")

summary_llm = ChatGroq(model="llama-3.3-70b-versatile")


def summarize(state: GraphState):
    """This node summarizes the SQL result"""

    prompt = prompt_template.format(
        question=state["question"],
        result=state["result"],
    )
    response = summary_llm.invoke(prompt)
    answer = remove_thinking(str(response.content))

    return {"final_answer": answer}
