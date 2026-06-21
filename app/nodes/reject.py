from app.state import GraphState


def rejection(state: GraphState):
    """
    Terminal node for all failures and rejections.
    """

    return {"final_answer": state["error"]}
