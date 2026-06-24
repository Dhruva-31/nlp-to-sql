import re
from langchain_core.tools import tool
from app.db.build_schema_docs import build_schema_docs


@tool
def answer_schema_question(question: str) -> str:
    """Look up relevant database schema information for a question:
    what tables exist, what columns/types they have, and how tables
    relate to each other (foreign keys).

    Always call this FIRST before writing any SQL with
    execute_sql_query, so you know the real table and column names.
    Also use this on its own when the user is just asking what exists
    in the database and does not need actual row data back.

    Args:
        question: The user's question, verbatim or paraphrased -- used
            to retrieve the most relevant schema chunks.
    """
    return "\n\n".join(build_schema_docs())
