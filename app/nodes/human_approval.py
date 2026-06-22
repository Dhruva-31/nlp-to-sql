from typing import Literal

from langchain_core.messages import ToolMessage
from langgraph.types import interrupt, Command

from app.risk import classify_risk
from app.state import GraphState


def human_approval(state: GraphState) -> Command[Literal["tools", "agent"]]:
    """This node requires human approval for dangerous queries."""

    last = state["messages"][-1]
    call = last.tool_calls[0]
    sql = call["args"].get("sql", "")
    risk_level = classify_risk(sql)

    approval = interrupt(
        {
            "type": "approval",
            "risk_level": risk_level,
            "sql": sql,
            "message": "Approve execution?",
        }
    )

    if approval:
        return Command(goto="tools")

    rejection_msg = ToolMessage(
        content=f"The user rejected this {risk_level}-risk query. Do not "
        "attempt to run it again. Explain to the user that it was not "
        "approved and why it may have been considered risky.",
        tool_call_id=call["id"],
        name=call["name"],
    )
    return Command(goto="agent", update={"messages": [rejection_msg]})
