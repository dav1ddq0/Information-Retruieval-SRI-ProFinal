from random import choice

import streamlit as st
from streamlit.elements.button import DownloadButtonDataType
from Retrieval_handler import Retrieval_handler

from model import Doc
from tools import*

class UIStremlit:

    type_file_dicc = {
    'PLAIN_TEXT' : "./imgs/doc.jpg",
    'TXT' : "./imgs/txt.jpg",
    'PDF': "./imgs/pdf.jpg"
    }   

    def __init__(self, handler: Retrieval_handler):
        self.handler: Retrieval_handler = handler
        self.title = st.title("Document Information Retrieval")
        self.menu = ["Search Engine", "View", "Similarity", "About"]
        self.choice = st.sidebar.selectbox("Menu", self.menu)
        self.raw_query = None
        self._check_choice()
    
    def _update_sidebar(self):
        pass
        
    
    def _buidl_container_from_doc(self, doc: 'Doc'):
        container = st.container()
        image = load_image(UIStremlit.type_file_dicc[doc.type])
        container.image(image, width=60)
        container.markdown(f"**{doc.name}**")
        
        with open(doc.path, "rb") as file:
            container.download_button(
                label="⬇️",
                data=file,
                file_name=doc.name,
                mime = "text"
                )
       


        return container
   

    def update_menu(self, new_option: str):
        self.menu.append(new_option)
    
    def docs_results_component(self, query, filters: List[str], top10: bool = False):
        docs_founds = self.handler.search(query, filters, top10)
        if docs_founds:
            # st.success("Se encontraron resultados")
            st.markdown("**Resultados de la búsqueda:**")
            results_components = st.columns(6)
            for i,doc in enumerate(docs_founds):
                with results_components[i % 6]:
                    self._buidl_container_from_doc(doc)
        else:
            # st.error('')
            st.markdown("**No se encontraron resultados 😥**")

    
    def text_main(self):
        input_modes_names = ['Text', 'Upload Document File']
        page =  st.radio('Mode', input_modes_names)
        type_documents_multisect = st.multiselect(
        'What types of documents do you want to search',
        ['PDF', 'TXT', 'PLAIN TEXT'],
        ['TXT', 'PLAIN TEXT'])
        # st.write(a)
        # st.text
        # search_component = st.columns(2)

        top_check_box = st.checkbox('Top 10')
        onlytop10  = True if top_check_box else False
         
        if page == 'Text':
            search_component_text_input = st.text_input("Write what you want to search")
            search_component_search_menu = st.button('Search')
        
            if search_component_search_menu:
                query = search_component_text_input.title()
                self.docs_results_component(query, type_documents_multisect, onlytop10)
        
        if page == 'Upload Document File':
            uploaded_file  =  st.file_uploader("Upload Document", type=["pdf", "txt"])
            if uploaded_file:
                file_type = uploaded_file.name.split('.')[1]
                
                if file_type == 'pdf':
                    query =  get_pdf_from_upload_file(uploaded_file)
                else:
                    query = get_text_from_upload_file(uploaded_file)
                    
                
                self.docs_results_component(query, type_documents_multisect, onlytop10)
                

                    

    def _check_choice(self):

        if self.choice == "Search Engine":
            self.text_main()
            # self.raw_query = st.text_input("Write what you want to search")
            # st.subheader("Home")
            # button = st.button("Submit")
            # if button:
            #     query = self.raw_query.title()
            #     st.header("Resultados:\n")
            #     cols = st.columns(6)
            #     for i,doc in enumerate(self.handler.search(query)):
            #         with cols[i % 6]:
            #             self._buidl_container_from_doc(doc)


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


