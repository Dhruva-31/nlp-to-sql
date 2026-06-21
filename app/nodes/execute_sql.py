from datetime import datetime
import time

from sqlalchemy import text

from app.db.connection import engine
from app.rag.build_index import build_index
from app.state import GraphState
from app.utils.logger import log_query

DDL_COMMANDS = {
    "ALTER",
    "CREATE",
    "DROP",
    "TRUNCATE",
}


def execute_sql(state: GraphState):
    """This node executes SQL query."""

    start_time = time.perf_counter()

    sql = state["sql_query"]

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
                "question": state["question"],
                "sql": sql,
                "retrieved_schema": state["schema"],
                "status": "failed",
                "error": str(e),
            }
        )

        return {
            "error": str(e),
        }

    first_word = sql.strip().upper().split()[0]

    if first_word in DDL_COMMANDS:
        build_index()

    execution_time = time.perf_counter() - start_time

    log_query(
        {
            "timestamp": str(datetime.now()),
            "question": state["question"],
            "sql": sql,
            "retrieved_schema": state["schema"],
            "status": "success",
            "execution_time": round(execution_time, 4),
            "row_count": len(rows),
        }
    )

    return {
        "result": rows,
        "execution_time": execution_time,
        "error": "",
    }
