from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END
from app.nodes.schema_retriever import schema_retriever
from app.nodes.validate_sql import validate_sql
from app.nodes.generate_sql import generate_sql
from app.nodes.execute_sql import execute_sql
from app.nodes.summarize import summarize
from app.nodes.validation_failed import validation_failed
from app.state import GraphState
from langgraph.checkpoint.memory import InMemorySaver


def route_validation(state: GraphState):

    if state["is_valid"]:
        return "valid"

    return "invalid"


builder = StateGraph(GraphState)

builder.add_node("retrieve_schema", schema_retriever)

builder.add_node("generate_sql", generate_sql)

builder.add_node("execute_sql", execute_sql)

builder.add_node("validate_sql", validate_sql)

builder.add_node("validation_failed", validation_failed)

builder.add_node("summarize", summarize)

builder.add_edge(START, "retrieve_schema")

builder.add_edge("retrieve_schema", "generate_sql")

builder.add_edge("generate_sql", "validate_sql")

builder.add_conditional_edges(
    "validate_sql",
    route_validation,
    {"valid": "execute_sql", "invalid": "validation_failed"},
)

builder.add_edge("execute_sql", "summarize")

builder.add_edge("summarize", END)

builder.add_edge("validation_failed", END)

memory = InMemorySaver()

graph = builder.compile(checkpointer=memory)
# with open("graph.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())
