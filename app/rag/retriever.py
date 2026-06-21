from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

embeddings = FastEmbedEmbeddings()


def retrieve_schema(question: str):

    vectorstore = Chroma(
        persist_directory="./schema_db",
        embedding_function=embeddings,
    )

    docs = vectorstore.similarity_search(
        question,
        k=3,
    )

    return "\n\n".join(doc.page_content for doc in docs)
