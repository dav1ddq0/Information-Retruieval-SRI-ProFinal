from random import choice
import streamlit as st
from streamlit.elements.button import DownloadButtonDataType

from model import Doc
from tools import*

class UIStremlit:

    type_file_dicc = {
    'PLAIN_TEXT' : "./imgs/text-plane.jpeg",
    'TXT' : "./imgs/txt.png",
    'PDF': "./imags/pdf.jpeg"
    }   

    def __init__(self):
        self.title = st.title("Document Information Retrieval")
        self.menu = ["Home", "View", "Similarity", "About"]
        self.choice = st.sidebar.selectbox("Menu", self.menu)
        self.raw_query = None
        self._check_choice()
    
    def _update_sidebar(self):
        pass
        
    
    def _buidl_columns_from_doc(self, doc: 'Doc'):
        with st.container() as container:
            st.header(doc.name)
            st.image(load_image(UIStremlit.type_file_dicc[doc.type]))

            with open(doc.path, "rb") as file:
                st.download_button(
                label="Download",
                data=file,
                file_name=doc.name,
                mime = "text/plain_text"
                )




        return container
   

    def update_menu(self, new_option: str):
        self.menu.append(new_option)
    
    def _check_choice(self):

        if self.choice == "Home":
            self.raw_query = st.text_input("Write what you want to search")
            st.subheader("Home")
            if st.button("Submit"):
                query = self.raw_query.title()
                st.header("Resultados:\n")
                cols = st.columns(4)
                # for i,doc in enumerate(SearchCoincidences(query)):
                #     with cols[i % 4]:
                #         buidlColFromDoc(doc)


            # query = process_query(query)
            # qvector = qVector(query, words, len(docs.keys()), ni_table(docs, words))
            # dvector = getDocsVectors(docs, words)
            # e = getSimilarDocuments(dvector, qvector)



                # st.success(e)

        elif self.choice == "View":
            st.subheader("View")
            st.image(load_image('./imgs/proof.jpeg'))

        elif self.choice == "Similarity":
            st.subheader("Similarity")


        else:
            st.subheader("About")
            with st.expander("Resultados:", True):
                submit = st.button("Submit")

                if submit:
                    a= st.columns(4)


                    with a[0]:
                        st.header("Hola")
                        st.image(load_image('./imgs/proof.jpeg'))
                    with a[0]:
                        st.header("2")
                    with a[1]:
                        st.header("Hola")
                        st.image(load_image('./imgs/proof.jpeg'))

                    with a[2]:
                        st.header("Hola")
                        st.image(load_image('./imgs/proof.jpeg'))
                        with open("./test_texts/dune.txt", "rb") as file:
                            btn = st.download_button(
                            label="Download",
                            data=file,
                            file_name="dune.txt",
                            mime="text/txt"
                            )


                    with a[3]:
                        st.header("Hola")
                        st.image(load_image('./imgs/proof.jpeg'))


