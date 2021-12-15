import streamlit as st
from vectorial import *
from PIL import Image

st.title("Document Information Retrieval")
st.write("""
# Text Retrival *world!*
""")

def loadImage(path: str):
    img = Image.open(path)
    return img

raw_query = st.text_area("Write what you want to search", "Type here...")
menu = ["Home", "View", "Similarity", "About"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Home")

elif choice == "View":
    st.subheader("View")
    st.image(loadImage('./imgs/proof.jpeg'))
    
elif choice == "Similarity":
    st.subheader("Similarity")

else:
    st.subheader("About")


if st.button("Submit"):
    query = raw_query.title()
    query = process_query(query)
    w = weightQuery(query, docs)
   
    st.success(idf)
    st.success(w)