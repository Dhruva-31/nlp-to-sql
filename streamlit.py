import uuid
import streamlit as st
from langchain_core.messages import HumanMessage

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

    st.session_state.messages.append({"role": "user", "content": question})

    response = graph.invoke(
        {
            "messages": [HumanMessage(content=question)],
            "retry_count": 0,
        },
        config=config,
    )

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
prompt = st.chat_input("Ask about database...")

if prompt:
    ask_agent(prompt)
    st.rerun()
