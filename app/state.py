from typing import TypedDict


class GraphState(TypedDict):
    question: str
    schema: str
    sql_query: str

    result: list
    final_answer: str

    execution_time: float

    is_valid: bool

    error: str
    retry_count: int

    risk_level: str
    approved: bool
