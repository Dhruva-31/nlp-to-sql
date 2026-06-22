import shutil
from app.rag.build_schema_docs import build_schema_docs
from langchain_core.documents import Document
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma

from app.rag.config import SCHEMA_DB_PATH


def build_index():

    if SCHEMA_DB_PATH:
        shutil.rmtree(SCHEMA_DB_PATH)

    schema_docs = build_schema_docs()

    docs = [Document(page_content=doc) for doc in schema_docs]

    embeddings = FastEmbedEmbeddings()

    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=SCHEMA_DB_PATH,
    )

    print("Schema index rebuilt.")
