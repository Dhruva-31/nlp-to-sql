from langchain_core.messages import ToolMessage

from app.state import GraphState
from app.tools.sql_tool import execute_sql_query
from app.tools.schema_tool import answer_schema_question

TOOLS_BY_NAME = {
    execute_sql_query.name: execute_sql_query,
    answer_schema_question.name: answer_schema_question,
}


def tools(state: GraphState) -> dict:
    last = state["messages"][-1]
    outputs = []
    retry_increment = 0

    for call in last.tool_calls:
        tool_fn = TOOLS_BY_NAME[call["name"]]
        result = tool_fn.invoke(call["args"])

        if call["name"] == "execute_sql_query" and str(result).startswith("Error"):
            retry_increment = 1

        outputs.append(
            ToolMessage(content=str(result), tool_call_id=call["id"], name=call["name"])
        )

    return {
        "messages": outputs,
        "retry_count": state.get("retry_count", 0) + retry_increment,
    }
