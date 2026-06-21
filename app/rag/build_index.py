import shutil
from pathlib import Path
from app.rag.build_schema_docs import build_schema_docs
from langchain_core.documents import Document
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma


def build_index():

    db_path = Path("./schema_db")

    if db_path.exists():
        shutil.rmtree(db_path)

    schema_docs = build_schema_docs()

    docs = [Document(page_content=doc) for doc in schema_docs]

    embeddings = FastEmbedEmbeddings()

    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./schema_db",
    )

    print("Schema index rebuilt.")
