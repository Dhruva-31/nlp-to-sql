from langgraph.types import Command

from app.graph import graph
from app.rag.build_index import build_index
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
        "execution_time": 0.0,
        "error": "",
        "retry_count": 0,
        "approved": False,
        "risk_level": "SAFE",
    }

    try:
        response = graph.invoke(state, config=config)
        if "__interrupt__" in response:

            interrupt_data = response["__interrupt__"][0].value

            print("\nApproval Required")
            print(f"Risk: {interrupt_data['risk_level']}")
            print(f"SQL: {interrupt_data['sql']}")

            user_choice = input("\nApprove? (y/n): ").strip().lower()

            approved = user_choice == "y"

            result = graph.invoke(
                Command(resume=approved),
                config=config,
            )

        print()
        print(response["final_answer"])

    except Exception as e:
        print(f"\nError: {e}")
