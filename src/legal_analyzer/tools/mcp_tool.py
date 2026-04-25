import httpx
from crewai.tools import tool

@tool("Legal Case Law Research Tool")
def mcp_tool(clause_description: str) -> str:
    """
    Use this tool to find relevant court cases and legal definitions for
    a specific clause or legal issue. Input should be a description of
    the clause or legal concept you want to research. Use this tool for
    every medium or high risk clause found in the contract.
    """
    try:
        response = httpx.get(
            "https://www.courtlistener.com/api/rest/v4/search/",
            params={
                "q": clause_description,
                "type": "o",
                "page_size": 3,
            },
            headers={"User-Agent": "LegalAnalyzerApp/1.0"},
            timeout=15.0
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])

        if not results:
            return f"No relevant case law found for: {clause_description}"

        formatted = []
        for case in results:
            case_name = case.get("caseName", "Unknown Case")
            court = case.get("court", "Unknown Court")
            date = case.get("dateFiled", "Unknown Date")
            snippet = case.get("snippet", "No excerpt available")
            formatted.append(
                f"Case: {case_name}\n"
                f"Court: {court} | Date: {date}\n"
                f"Excerpt: {snippet}"
            )

        return "Relevant case law found:\n\n" + "\n---\n".join(formatted)

    except httpx.TimeoutException:
        return "Request timed out. Try a simpler search term."
    except httpx.HTTPError as e:
        return f"Error reaching legal API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"