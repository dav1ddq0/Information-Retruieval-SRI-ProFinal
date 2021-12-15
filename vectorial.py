from typing import Dict,List
import spacy
import os
import math
from nltk.stem.snowball import SnowballStemmer


stemmer = SnowballStemmer(language='english')


nlp =  spacy.load('en_core_web_md')

# termino de suaviado
a = 0.5

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

def querytf(query: List[str]):
    querytf = {}
    maxfreq = 0
    freq = {}

    for token in query:
        if token not in freq.keys():
            freq[token] = 1
        else:
            freq[token] +=1
    
    for _, wfreq in freq.items():
        if wfreq > maxfreq:
            maxfreq = wfreq

   

    for token in query:
        querytf[token] = tf(freq[token], maxfreq)

    return querytf



def tftable(documents: Dict[str, List[str]]):
    tftable = {}
    freqt = freqtable(documents)

    for doc, tokens in documents.items():
        for token in tokens:
            tftable[doc, token] = tf(freqt[doc][token], maxfreq(freqt[doc]))
    
    return tftable

def ntable(documents: Dict[str, List[str]]):
    ntable = {}
    for doc, tokens in documents.items():
        visited = []
        for token in tokens:
            
            if token not in visited:
                visited.append(token)
                if token in ntable.keys():
                    ntable[token]+=1
                   
                else:
                    ntable[token] = 1

    return ntable

def idftable(documents: Dict[str, List[str]]):
    ntab = ntable(documents)
    N = len(documents)
    idftable = {}

    for doc, tokens in documents.items():
        for token in tokens:
            if token not in idftable.keys():
                idftable[token] = math.log(N/ntab[token])
    
    return idftable

# tf x idf
def weightTable(documents: Dict[str, List[str]]):
    tf = tftable(documents)
    idf = idftable(documents)
    wij = {}
    for doc, tokens in documents.items():
        for token in tokens:
            if (doc, token) not in wij.keys():
                wij[doc, token] = tf[doc, token]*idf[token]

    return wij      

def weightQuery(query: List[str], documents):
    weight = {}
    tf = querytf(query)
    
    

    for t in query:
        N = len(documents) + 1
        ni = 1
        for _, tokens in documents.items():
            if t in tokens:
                ni += 1
        weight[t]= (0.5 +0.5*(tf[t])) * math.log(N/ni)
    
    return weight

        

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


def process_query(query: str):
    #procesado del texto (tokenization,stopwords elimination y stemming)
    tokens=nlp(query)        
    tokens=[token for token in tokens if not token.is_stop and not token.is_punct and not token.is_space]
    tokens=[stemmer.stem(token.text) for token in tokens]
    
    return tokens



docs = preprocessing('./test_texts')
# b = freq(a['lordrings.txt'])
# c = maxfreq(b)
# d = freqtable(a)
# n = ntable(docs)
# tf = tftable(docs)
# idf = idftable(docs)
# w = weightTable(a)
# print(a)
# print(b)
# print(c)
# print(d)
w = weightQuery(process_query("Hello darkness to my friend"), docs)
print(w)
# print(idf)
# print(n)
