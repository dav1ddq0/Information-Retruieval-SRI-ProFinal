import json
from typing import Dict, List
import spacy
from model import*
import pickle

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

# text processed (tokenization, remove stopwords and stemming)
def text_processed(text: str):
    tokens = nlp(text)
    tokens = [
        token for token in tokens if not token.is_stop and not token.is_punct and not token.is_space]
    tokens = [stemmer.stem(token.text) for token in tokens]
    return tokens

def from_docsl_to_dicc(docs: Dict[str, Doc]):
    return { doc: (docs[doc].path, docs[doc].type)  for doc in docs}

