import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
import json

from legal_analyzer.crew import LegalAnalyzer


st.set_page_config(
    page_title="Legal Contract Analyzer",
    page_icon="⚖",
    layout="wide"
)

st.title("Legal Contract Q&A Chatbot")
st.caption("Ask any legal question about your contracts — powered by AI agents")

with st.sidebar:
    st.header("How to use")
    st.markdown("""
    1. Type your legal question
    2. Press Enter or click Send
    3. Read the structured report
    """)
    st.divider()
    st.caption("Powered by CrewAI + OpenAI + ChromaDB")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# ── DISPLAY CHAT HISTORY ──────────────────────────────────
for idx, msg in enumerate(st.session_state["chat_history"]):
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        # Show each AI answer in an expander for toggling
        with st.chat_message("ai"):
            with st.expander(f"Show/Hide Answer #{idx//2 + 1}", expanded=False):
                st.markdown(msg["content"])

# ── CHAT INPUT ────────────────────────────────────────────
user_query = st.chat_input("Type your question and press Enter...")

if user_query:
    st.session_state["chat_history"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.spinner("Agents are analyzing..."):
        try:
            
            result = LegalAnalyzer().crew().kickoff(inputs={"user_query": user_query})
            raw = result.raw if hasattr(result, "raw") else str(result)

            # ── STRIP CODE FENCES ─────────────────────────
            raw = raw.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            # ── TRY PARSE JSON ────────────────────────────
            try:
                report = json.loads(raw)

                st.chat_message("ai").markdown("### Executive Summary")
                st.info(report.get("executive_summary", "No summary available."))

                st.markdown("### Clauses Found")
                for clause in report.get("clauses", []):
                    risk = clause.get("risk_level", "low").lower()
                    color = "🔴" if risk == "high" else "🟡" if risk == "medium" else "🟢"
                    with st.expander(f"{color} {clause.get('type', 'Clause')} — {risk.upper()} risk"):
                        st.markdown(f"> {clause.get('text', 'N/A')}")

                st.markdown("### Risks and Citations")
                risks = report.get("risks", [])
                if risks:
                    for risk in risks:
                        severity = risk.get("severity", "low").lower()
                        color = "🔴" if severity == "high" else "🟡"
                        with st.expander(f"{color} {risk.get('clause_type', 'Risk')} — {severity.upper()}"):
                            st.markdown(risk.get("explanation", "N/A"))
                            st.markdown(f"_Citation: {risk.get('citation', 'None')}_")
                else:
                    st.success("No significant risks identified.")

                st.markdown("### Recommendations")
                for i, rec in enumerate(report.get("recommendations", []), 1):
                    st.markdown(f"**{i}.** {rec}")

                st.divider()
                st.download_button(
                    label="Download Report (JSON)",
                    data=json.dumps(report, indent=2),
                    file_name="legal_report.json",
                    mime="application/json"
                )

                # Store only the nicely formatted markdown answer in chat history
                ai_answer = "### Executive Summary\n" + report.get("executive_summary", "No summary available.")
                if report.get("clauses"):
                    ai_answer += "\n\n### Clauses Found\n"
                    for clause in report.get("clauses", []):
                        risk = clause.get("risk_level", "low").lower()
                        color = "🔴" if risk == "high" else "🟡" if risk == "medium" else "🟢"
                        ai_answer += f"\n- {color} **{clause.get('type', 'Clause')}** — {risk.upper()} risk\n    > {clause.get('text', 'N/A')}"
                if report.get("risks"):
                    ai_answer += "\n\n### Risks and Citations\n"
                    for risk in report.get("risks", []):
                        severity = risk.get("severity", "low").lower()
                        color = "🔴" if severity == "high" else "🟡"
                        ai_answer += f"\n- {color} **{risk.get('clause_type', 'Risk')}** — {severity.upper()}\n    {risk.get('explanation', 'N/A')}\n    _Citation: {risk.get('citation', 'None')}_"
                if report.get("recommendations"):
                    ai_answer += "\n\n### Recommendations\n"
                    for i, rec in enumerate(report.get("recommendations", []), 1):
                        ai_answer += f"\n{i}. {rec}"
                st.session_state["chat_history"].append({"role": "ai", "content": ai_answer})

            except json.JSONDecodeError:
                st.chat_message("ai").write(raw)
                st.session_state["chat_history"].append({"role": "ai", "content": raw})

        except Exception as e:
            st.chat_message("ai").write(f"Error: {str(e)}")
            st.session_state["chat_history"].append({"role": "ai", "content": f"Error: {str(e)}"})