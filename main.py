from app.graph import graph
from app.state import GraphState

config = {"configurable": {"thread_id": "user-1"}}

while True:

    question = input("\nAsk a question (or 'exit'): ")

    if question.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    state: GraphState = {
        "question": question,
        "final_answer": "",
        "result": [],
        "schema": "",
        "sql_query": "",
        "is_valid": True,
        "validation_error": "",
        "execution_time": 0.0,
    }

    try:
        response = graph.invoke(state, config=config)

        print()
        print(response["final_answer"])

    except Exception as e:
        print(f"\nError: {e}")
