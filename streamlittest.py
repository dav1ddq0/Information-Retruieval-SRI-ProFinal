from typing import TextIO
import streamlit as st
from streamlit.elements.button import DownloadButtonDataType
from vectorial import *
from PIL import Image


type_file_dicc = {
    DocType.PLAIN_TEXT : "./imgs/text-plane.jpeg",
    DocType.TXT : "./imgs/txt.jpeg",
}   

def buidlColFromDoc(doc: 'Doc'):
    
    
    with st.container():
        st.header(doc.name)
        st.image(loadImage(type_file_dicc[doc.type]))
        with open(doc.path, "rb") as file:
            st.download_button(
            label="Download",
            data=file,
            file_name=doc.name,
            mime = "text/plain_text"
            )
        


st.title("Document Information Retrieval")
def loadImage(path: str):
    img = Image.open(path)
    return img

raw_query = st.text_area("Write what you want to search", "Type here...")
menu = ["Home", "View", "Similarity", "About"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Home")
        
    if st.button("Submit"):
        query = raw_query.title()
        st.header("Resultados:\n")
        cols = st.columns(4)
        for i,doc in enumerate(SearchCoincidences(query)):
            with cols[i % 4]:
                buidlColFromDoc(doc)

    
    # query = process_query(query)
    # qvector = qVector(query, words, len(docs.keys()), ni_table(docs, words))
    # dvector = getDocsVectors(docs, words)
    # e = getSimilarDocuments(dvector, qvector)

    
   
        # st.success(e)

elif choice == "View":
    st.subheader("View")
    st.image(loadImage('./imgs/proof.jpeg'))
    
elif choice == "Similarity":
    st.subheader("Similarity")

else:
    st.subheader("About")
    with st.expander("Resultados:", True):
        submit = st.button("Submit")

        if submit:
            a= st.columns(4)
            

            with a[0]:
                st.header("Hola")
                st.image(loadImage('./imgs/proof.jpeg'))
            with a[0]:
                st.header("2")
            with a[1]:
                st.header("Hola")
                st.image(loadImage('./imgs/proof.jpeg'))

            with a[2]:
                st.header("Hola")
                st.image(loadImage('./imgs/proof.jpeg'))
                with open("./test_texts/dune.txt", "rb") as file:
                    btn = st.download_button(
                    label="Download",
                    data=file,
                    file_name="dune.txt",
                    mime="text/txt"
                    )


            with a[3]:
                st.header("Hola")
                st.image(loadImage('./imgs/proof.jpeg'))



    