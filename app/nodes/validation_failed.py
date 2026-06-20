from app.state import GraphState


def validation_failed(state: GraphState):

    return {"final_answer": state["validation_error"]}
