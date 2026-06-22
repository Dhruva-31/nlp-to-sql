READ_ONLY = {"SELECT", "WITH"}
LOW_RISK = {"INSERT"}
HIGH_RISK = {"UPDATE", "DELETE"}
CRITICAL = {"DROP", "TRUNCATE", "ALTER"}


def classify_risk(sql: str) -> str:
    """Same logic as the old risk_check_sql.py node, just operating
    directly on a SQL string instead of reading/writing GraphState."""
    sql_upper = sql.strip().upper()
    words = sql_upper.replace(";", " ").split()

    for keyword in CRITICAL:
        if keyword in words:
            return "CRITICAL"

    for keyword in HIGH_RISK:
        if keyword in words:
            return "HIGH"

    for keyword in LOW_RISK:
        if keyword in words:
            return "LOW"

    return "READ_ONLY"
