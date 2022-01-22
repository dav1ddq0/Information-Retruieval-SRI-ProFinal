import json
from typing import Dict, List
import spacy
from model import*
import pickle
import os
import io
import numpy as np
from PIL import Image
from fpdf import FPDF
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter,PDFResourceManager 
from pdfminer.pdfpage import PDFPage

from nltk.stem.snowball import SnowballStemmer

nlp = spacy.load('en_core_web_md')
stemmer = SnowballStemmer(language='english')

def make_pickle_file(filename, data):
    with open(f"{filename}.pickle", "wb") as outfile:
        pickle.dump(data, outfile)

def unpick_pickle_file(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    
    return data

def save_to_JSON(filename, data):
    with open(f"{filename}.json", "w") as outfile:
        json.dump(data, outfile)

def open_JSON(filename):
    with open(filename) as f:
       data=json.load(f)
    return data

def save_to_numpy_file(filename, data):
    np.save(filename, data)

def open_from_numpy_file(filename):
    data = np.load(filename)
    return data


def load_image(path: str): # dado un path de entrada te devuelve una imagen usando Pillow
    '''
    
    '''
    img = Image.open(path)
    return img

def convert_plane_text_to_pdf(filename: str):
    # save FPDF() class into 
    # a variable pdf
    pdf = FPDF()   
    
    # Add a page
    pdf.add_page()
    
    # set style and size of font 
    # that you want in the pdf
    pdf.set_font("Arial", size = 14)
    
    # open the text file in read mode
    f = open(filename, "r")
    
    # insert the texts in pdf
    for line in f:
        pdf.cell(200, 10, txt = line, ln = 1, align = 'C')
    
    _, tail = os.path.split(filename)
    name = os.path.splitext(tail)[0]
    # save the pdf with name .pdf
    pdf.output(f"{name}.pdf")


def convert_pdf_to_plane_text(pdf_filename: str): # convierte un PDF a un texto en  string
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_filename, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    if text:
        return text


# text processed (tokenization, remove stopwords and stemming)
def text_processed(text: str):
    tokens = nlp(text)
    tokens = [
        token for token in tokens if not token.is_stop and not token.is_punct and not token.is_space]
    tokens = [stemmer.stem(token.text) for token in tokens]
    return tokens

def from_docsl_to_dicc(docs: Dict[str, Doc]):
    return { doc: (docs[doc].path, docs[doc].type)  for doc in docs}

