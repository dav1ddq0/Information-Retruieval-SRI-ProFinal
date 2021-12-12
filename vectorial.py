from typing import Dict,List
import spacy
import os

from nltk.stem.snowball import SnowballStemmer


stemmer = SnowballStemmer(language='english')


nlp =  spacy.load('en_core_web_md')


tf = lambda freqij, maxfreqlj  : freqij/maxfreqlj

# given a document returns the frequency of occurrence of each term in this

# A document is represented by the name of the document and a list of tokens 
# that are the result of having processed the document by removing the keywors and stemming.
def freq(document: List[str]):
    words = {}

    for word in document:
        if word not in words.keys():
            words[word] = 1
        else:
            words[word] +=1
    
    return words

def maxfreq(words: Dict[str, int]):
    maxfreq = 0
    
    for word in words.keys():
        maxfreq = words[word] if words[word] > maxfreq else maxfreq

    return maxfreq


def freqtable(documents: Dict[str, List[str]]):
    freqtable = {}
    for doc,tokens in documents.items():
            freqtable[doc] = freq(tokens)
    return freqtable

def tftable(documents: Dict[str, List[str]]):...
    



def preprocessing(path):
    
    processed_docs={}
    text=''
    for doc in os.listdir(path):
       
        if  os.path.splitext(doc)[1]=='.txt':
            text=open(os.path.join(path,doc)).read()
            #procesado del texto (tokenization,stopwords elimination y stemming)
            tokens=nlp(text)        
            tokens=[token for token in tokens if not token.is_stop and not token.is_punct and not token.is_space]
            tokens=[stemmer.stem(token.text) for token in tokens]
            processed_docs[doc]=tokens
        else:
            continue
           
    return processed_docs

a = preprocessing('./test_texts')
b = freq(a['lordrings.txt'])
c = maxfreq(b)
d = freqtable(a)
print(a)
print(b)
print(c)
print(d)

