import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from retriever import get_retriever
from router import route_query

load_dotenv()

def format_docs(docs):
    formatted_context = ""
    for doc in docs:
        source_id = doc.metadata.get("doc_id", "Unknown")
        formatted_context += f"[Source: {source_id}]\n{doc.page_content}\n\n"
    return formatted_context

def generate_answer(query: str, role: str):
    routing_decision = route_query(query)
    source_type = routing_decision.get("source_type", "all")
    
    retriever = get_retriever(role, source_type)
    retrieved_docs = retriever.invoke(query)
    
    if not retrieved_docs:
        return "I do not have access to any documents that can answer this query based on your current role permissions.", [], routing_decision

    context_str = format_docs(retrieved_docs)
    
    llm = ChatGroq(
        temperature=0, 
        model_name="llama-3.3-70b-versatile",
        api_key=os.environ.get("GROQ_API_KEY")
    )
    
    template = """You are NovaAssist, a highly secure enterprise AI assistant for NovaCorp.
Your primary directive is to answer the employee's query using strictly the provided context.
If the answer is not contained within the context, you must state that you do not have the information.
Do not hallucinate or use outside knowledge.
You must cite the Source ID for every claim you make in your answer. Use the format [Source: doc_id].

Context:
{context}

Employee Query: {query}

Answer:"""
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context_str, "query": query})
    
    return answer, retrieved_docs, routing_decision