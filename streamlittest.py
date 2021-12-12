import streamlit as st

st.title("Document Information Retrieval")
st.write("""
# Text Retrival *world!*
""")

raw_query = st.text_area("Write what you want to search", "Type here...")

if st.button("Submit"):
    result = raw_query.title()
    st.success(result)