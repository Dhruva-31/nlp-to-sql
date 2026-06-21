from app.state import GraphState

READ_ONLY = {
    "SELECT",
    "WITH",
}

LOW_RISK = {
    "INSERT",
}

HIGH_RISK = {
    "UPDATE",
    "DELETE",
}

CRITICAL = {
    "DROP",
    "TRUNCATE",
    "ALTER",
}


def risk_check(state: GraphState):
    """This node evaluates the generated query and tag it with different level of risks"""

    sql = state["sql_query"].strip().upper()

    words = sql.replace(";", " ").split()

    for keyword in CRITICAL:

        if keyword in words:
            return {
                "risk_level": "CRITICAL",
                "error": f"Contains {keyword}",
            }

    for keyword in HIGH_RISK:

        if keyword in words:
            return {
                "risk_level": "HIGH",
                "error": f"Contains {keyword}",
            }

    for keyword in LOW_RISK:

        if keyword in words:
            return {
                "risk_level": "LOW",
                "error": f"Contains {keyword}",
            }

    return {
        "risk_level": "READ_ONLY",
        "error": "",
    }
