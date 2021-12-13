import streamlit as st
from vectorial import *

st.title("Document Information Retrieval")
st.write("""
# Text Retrival *world!*
""")

raw_query = st.text_area("Write what you want to search", "Type here...")

if st.button("Submit"):
    query = raw_query.title()
    query = process_query(query)
    st.success(idf)