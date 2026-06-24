import uuid
import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

st.set_page_config(page_title="NLP → SQL", layout="wide")


# -----------------------------
# Load graph
# -----------------------------
@st.cache_resource
def load_graph():
    from app.graph import graph

    return graph


graph = load_graph()

# -----------------------------
# Session state
# -----------------------------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None

# -----------------------------
# Suggested questions
# -----------------------------
SUGGESTIONS = [
    "What tables exist?",
    "Describe database schema",
    "Show all customers",
    "Top 5 products by sales",
    "Total revenue this month",
]


# -----------------------------
# Graph call
# -----------------------------
def ask_agent(question):
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    try:
        response = graph.invoke(
            {
                "messages": [HumanMessage(content=question)],
                "retry_count": 0,
            },
            config=config,
        )

        if "__interrupt__" in response:
            st.session_state.pending_approval = response["__interrupt__"][0].value
            return

        answer = ""

        for msg in reversed(response.get("messages", [])):
            if getattr(msg, "content", ""):
                answer = msg.content
                break

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    except Exception as e:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"Error: {e}",
            }
        )


def resume_agent(approved):
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    try:
        response = graph.invoke(
            Command(resume=approved),
            config=config,
        )

        st.session_state.pending_approval = None

        if not approved:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Query execution rejected.",
                }
            )
            return

        if "__interrupt__" in response:
            st.session_state.pending_approval = response["__interrupt__"][0].value
            return

        answer = ""

        for msg in reversed(response.get("messages", [])):
            if getattr(msg, "content", ""):
                answer = msg.content
                break

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    except Exception as e:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"Resume Error: {e}",
            }
        )


# -----------------------------
# Layout
# -----------------------------
left, center, right = st.columns([1, 4, 1])

# -----------------------------
# Left Sidebar
# -----------------------------
with left:
    st.title("NLP → SQL")

    if st.button("New Chat"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Center Chat
# -----------------------------
with center:

    st.subheader("Database Assistant")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if st.session_state.pending_approval:

        data = st.session_state.pending_approval

        risk = data.get("risk_level", "HIGH")

        if risk == "CRITICAL":
            st.error(f"{risk} Risk Query")
        elif risk == "HIGH":
            st.warning(f"{risk} Risk Query")
        else:
            st.info(f"{risk} Risk Query")

        st.write(data.get("message", "Approval Required"))

        st.code(
            data.get("sql", ""),
            language="sql",
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "Approve",
                type="primary",
                use_container_width=True,
            ):
                resume_agent(True)
                st.rerun()

        with col2:
            if st.button(
                "Reject",
                use_container_width=True,
            ):
                resume_agent(False)
                st.rerun()

# -----------------------------
# Right Suggestions
# -----------------------------
with right:

    st.subheader("Suggestions")

    for q in SUGGESTIONS:
        if st.button(q, use_container_width=True):
            ask_agent(q)
            st.rerun()

# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input(
    "Ask about database...",
    disabled=st.session_state.pending_approval is not None,
)

if prompt:
    ask_agent(prompt)
    st.rerun()
