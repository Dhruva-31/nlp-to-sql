from typing import Literal
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from app.nodes.agent import agent
from app.nodes.human_approval import human_approval
from app.nodes.tools import tools
from app.risk import classify_risk
from app.state import GraphState

MAX_RETRIES = 3


def route_after_agent(
    state: GraphState,
) -> Literal["tools", "human_approval", "__end__"]:
    """
    Replaces route_validation + route_risk + the success/failed branch
    of route_execution, combined into one routing function since
    validate_sql and risk_check are no longer separate nodes.
    """
    last = state["messages"][-1]

    if not getattr(last, "tool_calls", None):
        return "__end__"

    call = last.tool_calls[0]

    if call["name"] == "answer_schema_question":
        return "tools"

    if call["name"] == "execute_sql_query":

        if state.get("retry_count", 0) >= MAX_RETRIES:
            return "__end__"

        sql = call["args"].get("sql", "")
        risk_level = classify_risk(sql)
        if risk_level in {"HIGH", "CRITICAL"}:
            return "human_approval"
        return "tools"

    return "tools"


builder = StateGraph(GraphState)

builder.add_node("agent", agent)
builder.add_node("tools", tools)
builder.add_node("human_approval", human_approval)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {"tools": "tools", "human_approval": "human_approval", "__end__": END},
)

builder.add_edge("tools", "agent")

memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)

with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())
