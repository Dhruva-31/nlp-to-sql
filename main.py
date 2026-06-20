from app.graph import GraphState, graph

question = input("Ask a question: ")

state: GraphState = {
    "question": question,
    "final_answer": "",
    "result": [],
    "schema": "",
    "sql_query": "",
}

response = graph.invoke(state)

print()
print(response["final_answer"])
