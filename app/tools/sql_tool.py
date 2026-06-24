from datetime import datetime
import time
from langchain_core.tools import tool
from sqlalchemy import text
from app.db.connection import engine
from app.utils.logger import log_query

DDL_COMMANDS = {
    "ALTER",
    "CREATE",
    "DROP",
    "TRUNCATE",
}


@tool
def execute_sql_query(sql: str, question: str, schema_context: str) -> str:
    """Execute a SQL query against the database and return the results.

    Use this whenever the user wants actual data (rows, counts,
    aggregates) or wants to modify data. Read-only SELECT/WITH queries
    run immediately. Writes and DDL (INSERT/UPDATE/DELETE/DROP/ALTER/
    TRUNCATE) are routed through a human approval step automatically --
    you do not need to ask for approval yourself, just call this tool
    and the system will pause for approval if needed.

    If this returns an error, read the error message and call this tool
    again with a corrected query rather than giving up.

    Args:
        sql: A single SQL statement to run.
        question: The original user question, used for logging.
        schema_context: The schema text you used to write this query,
            used for logging.
    """

    if not sql or not sql.strip():
        return "Error: Generated SQL is empty."

    sql_upper = sql.strip().upper()

    if not (
        sql_upper.startswith("SELECT")
        or sql_upper.startswith("WITH")
        or sql_upper.startswith("INSERT")
        or sql_upper.startswith("UPDATE")
        or sql_upper.startswith("DELETE")
        or sql_upper.startswith("DROP")
        or sql_upper.startswith("ALTER")
        or sql_upper.startswith("TRUNCATE")
    ):
        return "Error: Generated output is not SQL."

    start_time = time.perf_counter()

    try:
        with engine.begin() as conn:
            result = conn.execute(text(sql))

            if result.returns_rows:
                rows = result.fetchall()
            else:
                rows = []

    except Exception as e:
        log_query(
            {
                "timestamp": str(datetime.now()),
                "question": question,
                "sql": sql,
                "retrieved_schema": schema_context,
                "status": "failed",
                "error": str(e),
            }
        )
        return f"Error executing query: {e}"

    execution_time = time.perf_counter() - start_time

    log_query(
        {
            "timestamp": str(datetime.now()),
            "question": question,
            "sql": sql,
            "retrieved_schema": schema_context,
            "status": "success",
            "execution_time": round(execution_time, 4),
            "row_count": len(rows),
        }
    )

    return str(
        {
            "result": [dict(row._mapping) for row in rows],
            "execution_time": round(execution_time, 4),
            "row_count": len(rows),
        }
    )
