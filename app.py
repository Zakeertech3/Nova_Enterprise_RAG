import os
import sys
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'rag_engine')))
from generator import generate_answer

st.set_page_config(page_title="NovaAssist Enterprise AI", layout="wide")

st.title("NovaAssist Enterprise RAG")
st.markdown("Secure, Context-Aware AI Assistant for NovaCorp Employees.")

st.sidebar.header("Security & Access Control")
st.sidebar.markdown("Simulate different employee roles to test RBAC filtering.")

roles = ["Standard_Employee", "Finance_Analyst", "IT_Admin", "Super_Admin"]
selected_role = st.sidebar.selectbox("Current User Role:", roles)

if "current_role" not in st.session_state or st.session_state.current_role != selected_role:
    st.session_state.current_role = selected_role
    st.session_state.messages = []
    st.sidebar.success(f"Switched to {selected_role}. Chat cleared for security.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask NovaAssist a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing intent and searching enterprise data silos securely..."):
            try:
                response, docs, routing = generate_answer(prompt, selected_role)
                
                st.caption(f"Intelligent Routing: Routed to {routing['source_type'].upper()} silo. Reasoning: {routing['reasoning']}")
                
                st.markdown(response)
                
                if docs:
                    with st.expander("View Retrieved Sources & Access Logs"):
                        for i, doc in enumerate(docs):
                            st.markdown(f"**Source {i+1}:** `{doc.metadata.get('doc_id')}` (Silo: `{doc.metadata.get('source_type')}`)")
                            st.caption(f"Allowed Roles: {doc.metadata.get('allowed_roles')}")
                            st.text(doc.page_content[:200] + "...")
                            st.divider()
                            
            except Exception as e:
                response = f"An error occurred: {e}"
                st.error(response)
                
    st.session_state.messages.append({"role": "assistant", "content": response})