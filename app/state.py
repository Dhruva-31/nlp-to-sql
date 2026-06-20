from typing import TypedDict


class GraphState(TypedDict):
    question: str
    schema: str
    sql_query: str
    result: list
    final_answer: str
    execution_time: float
    is_valid: bool
    validation_error: str
