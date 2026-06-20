from langchain_core.documents import Document
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma
from app.rag.schema_docs import SCHEMA_DOCS

docs = [Document(page_content=text) for text in SCHEMA_DOCS]

embeddings = FastEmbedEmbeddings()

vectorstore = Chroma.from_documents(
    documents=docs, embedding=embeddings, persist_directory="./schema_db"
)
