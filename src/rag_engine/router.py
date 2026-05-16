import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

def route_query(query: str) -> dict:
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.3-70b-versatile",
        api_key=os.environ.get("GROQ_API_KEY")
    )

    template = """You are the intelligent routing agent for an Enterprise RAG system.
Analyze the following employee query and determine which data silo contains the relevant information.

Available Data Silos:
1. "pdf" : HR policies, handbooks, contracts, general text documents.
2. "sqlite" : Financial data, payroll, salaries, employee database records.
3. "json" : IT security logs, VPN logins, server access records.
4. "all" : If the query spans multiple silos or is unclear.

Output your decision strictly in valid JSON format with two keys:
- "source_type": (must be exactly "pdf", "sqlite", "json", or "all")
- "reasoning": (a brief 1-sentence explanation of why you chose this silo)

Employee Query: {query}
"""

    prompt = PromptTemplate.from_template(template)
    parser = JsonOutputParser()

    chain = prompt | llm | parser

    try:
        decision = chain.invoke({"query": query})
        
        if decision.get("source_type") not in ["pdf", "sqlite", "json", "all"]:
            decision["source_type"] = "all"
        return decision
    except Exception as e:
        return {"source_type": "all", "reasoning": "Fallback routing due to parsing error."}

if __name__ == "__main__":
    queries = [
        "What is the company policy on remote work?",
        "Can you find the salary for employee ID 47795?",
        "Show me the recent failed VPN attempts.",
        "Did anyone log into the server on the day payroll was processed?"
    ]

    for q in queries:
        print(f"Query: {q}")
        decision = route_query(q)
        print(f"Routed to: {decision['source_type']}")
        print(f"Reasoning: {decision['reasoning']}\n")