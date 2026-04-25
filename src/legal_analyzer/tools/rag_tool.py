from crewai.tools import tool
from legal_analyzer.rag.retrieval_pipeline import retrieve_relevant_docs

@tool("RAG Contract Search Tool")
def rag_tool(query: str) -> str:
    """
    Use this tool to search the uploaded contract and retrieve the most
    relevant sections based on a user query. Input should be the user's
    question or a specific legal topic to search for. Always use this
    tool first before any analysis.
    """
    docs = retrieve_relevant_docs(query, k=5)

    if not docs:
        return "No relevant sections found in the contract for this query."

    chunks = [doc.page_content for doc in docs]
    joined = "\n---\n".join(chunks)
    return f"Relevant contract sections found:\n\n{joined}"