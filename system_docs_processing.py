import os
from model import *
from tools import *

def libdocuments_processing(path: str): # procesa todos los documentos que hay en el sistema
    result = []
    for doc_filename in os.listdir(path): # recorre cada archivo o carpeta en el directorio
        full_path = os.path.join(path, doc_filename)
        if os.path.isdir(full_path): # en caso que sea un directorio 
            result += libdocuments_processing(full_path)
            
        else:  
            if os.path.splitext(doc_filename)[1] == '.txt':
                with open(file = full_path, encoding="utf8", errors='ignore') as f:
                    text = f.read()
                    document = Doc(doc_filename, full_path, 'TXT', text)
                   
                    result.append(document)
            
            elif os.path.splitext(doc_filename)[1] == '.pdf':
                    text = convert_pdf_to_plane_text(full_path)
                    document = Doc(doc_filename, full_path, 'PDF', text)
                    result.append(document)
                
            else:
                
                with open(file = full_path, encoding="utf8", errors='ignore') as f:
                    text = f.read()
                    document = Doc(doc_filename, full_path, 'PLAIN_TEXT', text)
                    result.append(document)
            

    return result

def get_terms(docs: List[Doc]): # genera el vocabulario con todas las palabras que contienen los documentos que hay en el sistema
    terms=[]
    
    for doc in docs:
        for t in doc.terms:
            if t not in terms:
                terms.append(t)
    
    return terms

def compute_and_save_corpus_data(docs_path: str = './system_docs'):
    docs = libdocuments_processing(docs_path)
    terms = get_terms(docs) 
    make_pickle_file('./preprocessed/terms', terms)
    make_pickle_file('./preprocessed/documents', docs)