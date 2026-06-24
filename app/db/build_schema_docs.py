from sqlalchemy import inspect
from app.db.connection import engine


def build_schema_docs():

    inspector = inspect(engine)

    docs = []

    for table in inspector.get_table_names():

        columns = inspector.get_columns(table)

        foreign_keys = inspector.get_foreign_keys(table)

        text = f"Table: {table}\n\n"

        text += "Columns:\n"

        for column in columns:

            text += f"- {column['name']} " f"({column['type']})\n"

        if foreign_keys:

            text += "\nRelationships:\n"

            for fk in foreign_keys:

                constrained = fk["constrained_columns"][0]
                referred_table = fk["referred_table"]
                referred_column = fk["referred_columns"][0]

                text += (
                    f"- {table}.{constrained}"
                    f" -> "
                    f"{referred_table}.{referred_column}\n"
                )

        docs.append(text)

    return docs
