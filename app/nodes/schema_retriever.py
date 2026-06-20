from app.rag.retriever import retrieve_schema


def schema_retriever(state):
    """This node retrieves the schema from the vector chroma db"""

    schema = retrieve_schema(state["question"])

    return {"schema": schema}
