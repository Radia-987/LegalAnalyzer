# LegalAnalyzer CrewAI

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python) ![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-purple) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit) ![License](https://img.shields.io/badge/License-MIT-green)

**LegalAnalyzer CrewAI** is an AI-powered legal contract analysis tool that leverages Retrieval-Augmented Generation (RAG), ChromaDB, and CrewAI agent orchestration to answer legal questions, analyze contract clauses, and provide real case law citations.

---

## ✨ Features

- **Conversational Q&A** — Ask legal questions about your contracts and get structured, AI-generated answers.
- **RAG Pipeline** — Ingests and indexes all PDF contracts in your `knowledge/` folder using ChromaDB and OpenAI embeddings.
- **Multi-Agent Workflow**
  - 🔍 Agent 1 (`contract_analyst`) — Analyzes contract clauses, assigns risk levels, and calls the MCP tool for real case law.
  - 📝 Agent 2 (`report_writer`) — Writes a clean, structured JSON report from the analysis.
- **CourtListener Integration** — Fetches real legal case citations for high/medium risk clauses via MCP.
- **Streamlit UI** — Simple, interactive chat interface for legal Q&A with downloadable JSON reports.

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| [Python 3.11+](https://www.python.org/) | Core language |
| [CrewAI](https://github.com/joaomdmoura/crewAI) | Multi-agent orchestration |
| [LangChain](https://github.com/langchain-ai/langchain) | LLM chaining & tooling |
| [ChromaDB](https://www.trychroma.com/) | Vector store for RAG |
| [Streamlit](https://streamlit.io/) | Chat UI |
| [OpenAI API](https://platform.openai.com/) | LLM + embeddings |
| [CourtListener MCP](https://www.courtlistener.com/api/) | Real case law citations |

---

## 📁 Project Structure

```
LegalAnalyzer_CrewAI/
├── legal_analyzer/
│   ├── src/
│   │   └── legal_analyzer/
│   │       ├── app.py                  # Streamlit UI
│   │       ├── crew.py                 # CrewAI agents & tasks
│   │       ├── rag/
│   │       │   ├── ingestion_pipeline.py
│   │       │   └── rag_tool.py
│   │       └── config/
│   │           ├── agents.yaml
│   │           └── tasks.yaml
│   ├── knowledge/                      # Place your PDF contracts here
│   └── db/
│       └── chroma_db/                  # Auto-generated vector store
├── .env                                # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/LegalAnalyzer_CrewAI.git
cd LegalAnalyzer_CrewAI
```

### 2. Create & Activate a Virtual Environment

```sh
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

Install all required packages in one command:

```sh
pip install streamlit crewai crewai-tools langchain chromadb openai python-dotenv httpx pypdf mcp "crewai-tools[mcp]"
```

If you use unstructured PDF loading, also run:

```sh
pip install unstructured pdf2image
```

> 💡 Optional — for testing: `pip install pytest`

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Add Your Contract PDFs

Place all your contract/legal PDF files inside the `knowledge/` folder.

### 6. Ingest Documents into ChromaDB

```sh
cd legal_analyzer
python src/legal_analyzer/rag/ingestion_pipeline.py
```

You should see output like:
```
ChromaDB path: ...
Documents in store: 146
```

### 7. Run the Streamlit App

```sh
# From the project root:
streamlit run legal_analyzer/src/legal_analyzer/app.py
```

Open your browser at **http://localhost:8501**

---

## 💬 Usage

1. Open the Streamlit app in your browser.
2. Type your legal question in the chat box (e.g. *"Under what circumstances is a surety discharged?"*).
3. The AI agents will:
   - Retrieve relevant clauses from your ingested contracts
   - Fetch real case law citations from CourtListener
   - Generate a structured report with risk levels and recommendations
4. Download the full report as a JSON file using the **Download Report** button.

---

## ⚙️ Configuration

| Path | Description |
|------|-------------|
| `knowledge/` | Drop your PDF contracts here before ingestion |
| `db/chroma_db/` | ChromaDB vector store — auto-generated, do not edit |
| `.env` | Store your `OPENAI_API_KEY` and other secrets |
| `config/agents.yaml` | Agent roles, goals, and backstories |
| `config/tasks.yaml` | Task descriptions and expected outputs |

---

## 🧠 How It Works

```
User Question
      ↓
RAG Tool → ChromaDB → Retrieves relevant contract chunks
      ↓
MCP Tool → CourtListener → Fetches real case law citations
      ↓
contract_analyst agent → Analyzes clauses + assigns risk levels
      ↓
report_writer agent → Structures output as JSON report
      ↓
Streamlit UI → Renders Executive Summary, Clauses, Risks, Recommendations
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| ChromaDB / database errors | Delete `db/chroma_db/` folder and re-run the ingestion pipeline |
| Module import errors | Ensure you're running from the project root with the venv activated |
| `MCPServerAdapter` errors | Use positional arg: `MCPServerAdapter({"url": ..., "transport": "streamable-http"})` |
| `mcp` package missing | Run `pip install mcp` and `pip install "crewai-tools[mcp]"` |
| Torch warnings on startup | Safe to ignore — these are non-critical warnings from the `torch` library |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with ❤️ using CrewAI, ChromaDB, and Streamlit.
