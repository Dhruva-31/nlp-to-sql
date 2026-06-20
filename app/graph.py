from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END
from app.nodes.generate_sql import generate_sql
from app.nodes.execute_sql import execute_sql
from app.nodes.summarize import summarize
from typing import TypedDict


class GraphState(TypedDict):
    question: str
    schema: str
    sql_query: str
    result: list
    final_answer: str


builder = StateGraph(GraphState)

builder.add_node("generate_sql", generate_sql)

builder.add_node("execute_sql", execute_sql)

builder.add_node("summarize", summarize)

builder.add_edge(START, "generate_sql")

builder.add_edge("generate_sql", "execute_sql")

builder.add_edge("execute_sql", "summarize")

builder.add_edge("summarize", END)

graph = builder.compile()
