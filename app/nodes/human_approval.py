from langgraph.types import interrupt

from app.state import GraphState


def human_approval(state: GraphState):
    """This node requires human approval for dangerous queries"""

    approval = interrupt(
        {
            "type": "approval",
            "risk_level": state["risk_level"],
            "reason": state["error"],
            "sql": state["sql_query"],
            "message": "Approve execution?",
        }
    )

    return {"approved": approval}
