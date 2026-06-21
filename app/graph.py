from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END
from app.nodes.human_approval import human_approval
from app.nodes.repair_sql import repair_sql
from app.nodes.risk_check_sql import risk_check
from app.nodes.schema_retriever import schema_retriever
from app.nodes.validate_sql import validate_sql
from app.nodes.generate_sql import generate_sql
from app.nodes.execute_sql import execute_sql
from app.nodes.summarize import summarize
from app.nodes.reject import rejection
from app.state import GraphState
from langgraph.checkpoint.memory import InMemorySaver


def route_validation(state: GraphState):

    if state["is_valid"]:
        return "valid"

    return "invalid"


def route_execution(state: GraphState):

    if state["error"] and state["retry_count"] < 3:
        return "repair"

    if state["error"]:
        return "failed"

    return "success"


def route_risk(state):

    risk = state["risk_level"]

    if risk in {"HIGH", "CRITICAL"}:
        return "approval"

    return "safe"


def route_approval(state: GraphState):

    if state["approved"]:
        return "execute"

    return "rejected"


builder = StateGraph(GraphState)

builder.add_node("retrieve_schema", schema_retriever)

builder.add_node("generate_sql", generate_sql)

builder.add_node("execute_sql", execute_sql)

builder.add_node("validate_sql", validate_sql)

builder.add_node("summarize", summarize)

builder.add_node("repair_sql", repair_sql)

builder.add_node("risk_check", risk_check)

builder.add_node("human_approval", human_approval)

builder.add_node("reject", rejection)

builder.add_edge(START, "retrieve_schema")

builder.add_edge("retrieve_schema", "generate_sql")

builder.add_edge("generate_sql", "validate_sql")

builder.add_conditional_edges(
    "validate_sql",
    route_validation,
    {"valid": "risk_check", "invalid": "reject"},
)

builder.add_conditional_edges(
    "risk_check",
    route_risk,
    {"approval": "human_approval", "safe": "execute_sql"},
)

builder.add_conditional_edges(
    "human_approval",
    route_approval,
    {"execute": "execute_sql", "rejected": "reject"},
)

builder.add_conditional_edges(
    "execute_sql",
    route_execution,
    {"success": "summarize", "repair": "repair_sql", "failed": "reject"},
)

builder.add_edge("repair_sql", "execute_sql")

builder.add_edge("summarize", END)

builder.add_edge("reject", END)

memory = InMemorySaver()

graph = builder.compile(checkpointer=memory)
with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())
