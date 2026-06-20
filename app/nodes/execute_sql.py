from datetime import datetime
from sqlalchemy import text
import time
from app.db.connection import engine
from app.state import GraphState
from app.utils.logger import log_query


def execute_sql(state: GraphState):
    """This node executes the SQL query"""

    start_time = time.perf_counter()

    sql = state["sql_query"]

    try:

        with engine.connect() as conn:

            result = conn.execute(text(sql))

            rows = result.fetchall()

    except Exception as e:

        log_query(
            {
                "timestamp": str(datetime.now()),
                "question": state["question"],
                "sql": sql,
                "status": "failed",
                "error": str(e),
            }
        )
        raise

    execution_time = time.perf_counter() - start_time

    log_query(
        {
            "timestamp": str(datetime.now()),
            "question": state["question"],
            "sql": sql,
            "retrieved_schema": state["schema"],
            "status": "success",
            "execution_time": round(
                execution_time,
                4,
            ),
            "row_count": len(rows),
        }
    )
    return {
        "result": rows,
        "execution_time": execution_time,
    }
