from app.state import GraphState


def validate_sql(state: GraphState):
    """This node checks if the sql exists or not"""

    sql = state["sql_query"]

    if not sql or not sql.strip():
        return {"is_valid": False, "error": "Generated SQL is empty."}

    sql = sql.strip().upper()

    if not (
        sql.startswith("SELECT")
        or sql.startswith("WITH")
        or sql.startswith("INSERT")
        or sql.startswith("UPDATE")
        or sql.startswith("DELETE")
        or sql.startswith("DROP")
        or sql.startswith("ALTER")
        or sql.startswith("TRUNCATE")
    ):
        return {"is_valid": False, "error": "Generated output is not SQL."}

    return {"is_valid": True, "error": ""}
