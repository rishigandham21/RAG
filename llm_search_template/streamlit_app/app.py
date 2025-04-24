import streamlit as st
import requests

st.set_page_config(page_title="LLM-based RAG Search", layout="centered")
st.title("🔍 LLM-based RAG Search")

query = st.text_input("Ask something:")

if st.button("Search"):
    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        with st.spinner("Searching the web and thinking..."):
            try:
                response = requests.post("http://localhost:5001/query", json={"query": query})
                if response.status_code == 200:
                    answer = response.json().get('answer', "No answer received.")
                    st.success("Answer:")
                    st.write(answer)
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
