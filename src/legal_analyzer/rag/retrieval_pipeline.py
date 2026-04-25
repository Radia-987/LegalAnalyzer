from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# rag/ → legal_analyzer/ → src/ → legal_analyzer/ → db/chroma_db
persistent_directory = os.path.normpath(
    os.path.join(BASE_DIR, "..", "..", "..", "db", "chroma_db")
)

print(f"ChromaDB path: {persistent_directory}")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space": "cosine"}
)

print(f"Documents in store: {db._collection.count()}")

def retrieve_relevant_docs(user_query, k=5):
    retriever = db.as_retriever(search_kwargs={"k": k})
    relevant_docs = retriever.invoke(user_query)
    return relevant_docs