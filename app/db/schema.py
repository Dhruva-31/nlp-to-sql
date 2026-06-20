from sqlalchemy import inspect
from app.db.connection import engine


def get_schema():

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    schema = []

    for table in tables:

        columns = inspector.get_columns(table)

        column_names = [column["name"] for column in columns]

        schema.append(f"{table}({', '.join(column_names)})")

    return "\n".join(schema)
