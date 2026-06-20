from app.state import GraphState


def validate_sql(state: GraphState):

    sql_query = state["sql_query"]

    if not sql_query:
        return {
            "validation_error": "Empty SQL query.",
            "is_valid": False,
        }

    sql_query = sql_query.upper()

    BLOCKED = {
        "DROP",
        "DELETE",
        "UPDATE",
        "ALTER",
        "TRUNCATE",
        "INSERT",
    }

    sql_words = sql_query.replace(";", " ").split()

    for block in BLOCKED:

        if block in sql_words:

            return {
                "validation_error": f"Query contains blocked operation: {block}",
                "is_valid": False,
            }

    return {
        "validation_error": "",
        "is_valid": True,
    }
