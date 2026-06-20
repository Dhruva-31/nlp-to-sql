from sqlalchemy import text

from app.db.connection import engine
from app.graph import GraphState


def execute_sql(state: GraphState):
    """This node executes the SQL query"""

    sql = state["sql_query"]

    with engine.connect() as conn:

        result = conn.execute(text(sql))

        rows = result.fetchall()

    return {"result": rows}
