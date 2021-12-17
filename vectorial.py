from typing import Callable, Dict,List
from numpy import bool8, number, sqrt
import spacy
import os
import math

from nltk.stem.snowball import SnowballStemmer


class Token:
    
    def __init__(self, word: str, freq: int) -> None:
        self.word = word
        self.freq = freq

    def __str__(self) -> str:
        return f"Token(word = {self.word}, freq = {self.freq})"
    
    def __ge__(self, other: 'Token'):
        return self.freq >= other.freq

    def __gt__(self, other: 'Token'):
        return self.freq > other.freq




stemmer = SnowballStemmer(language='english')


nlp =  spacy.load('en_core_web_md')

# termino de suaviado
a = 0.5

tf: Callable[[int, int], float]  = lambda freqij, maxfreqlj  : freqij/maxfreqlj
idf: Callable[[int, int], float] = lambda N, ni : math.log(N/ni)
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



def tftable(documents: Dict[str, List[Token]], words: List[str]):
    tftable = {(w,doc): 0  for w in words for doc in documents.keys()}
    
    for doc, tokens in documents.items():
        
        for token in tokens:
            tftable[token.word, doc] = tf(token.freq, max(tokens).freq)
    
    return tftable

def ni_table(documents: Dict[str, List[Token]], words: List['Token']):
    ntable = { w:0 for w in words }
    
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

def idftable(documents: Dict[str, List[str]], words: List[str]):
    N = len(documents.keys())
    idftable = {w: 0 for w in words}
    nit = ni_table(documents, words)
    for w in words:
        idftable[w] = idf(N, nit[w])

    return idftable

   

def getTokens(words: List[str]) -> List['Token']:
    tokens: List['Token'] = []
    dic = {}
    
    for w in words:
        if w not in dic.keys():
            dic[w] = words.count(w)
    
    for w,o in dic.items():
        tokens.append(Token(word = w, freq = o))
    
    return tokens

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
    
    result = { doc: getTokens(tokens) for doc, tokens in processed_docs.items()}
    

    return result




def process_query(query: str):
    #procesado del texto (tokenization,stopwords elimination y stemming)
    tokens=nlp(query)        
    tokens=[token for token in tokens if not token.is_stop and not token.is_punct and not token.is_space]
    tokens=[stemmer.stem(token.text) for token in tokens]
    
    return tokens

# All words in system documents
def getWords(docs: Dict[str, List[Token]]):
    words = []

    for _, tokens in docs.items():
        for token in tokens:
            if token.word  not in words:
                words.append(token.word)
    
    return words

# Para cada termino i la cantidad de documentos  en los que aparece 
def n_i_table(docs: Dict[str, List[Token]], words):
    
    n_i_t = {w: 0 for w in words}
    
    for w in words:
        
        for _, tokens in docs.items():

            for token in tokens:
                if token.word == w:
                    n_i_t[w] += 1
    
    return n_i_t


def getDocsVectors(docs: Dict[str, List[Token]], words: List[str]):
    vectors: Dict[str, List[number]] = {}
    N = len(docs.keys())
    nit = ni_table(docs, words) 
    tft = tftable(docs, words)
    term_dic = {word: index for index, word in enumerate(words) }
    idft = idftable(docs, words)

    for dj, tokens in docs.items():
        vj = len(words)*[0]

        for token in tokens:
            tindex = term_dic[token.word]
            tfij = tft[token.word, dj]
            idfi = idft[token.word]
            wij = tfij*idfi
            vj[tindex] = wij
        
        vectors[dj] = vj

    return vectors




     


def sim(dj: Dict, q: Dict):
    dotproduct = 0
    # From the form .. 'term': weight,.. =>  [weigh1, weight2,...]
    v1 = list(dj.values()) # vector from dj
    v2 = list(q.values())  # vector from q

    # compute dotproduct from v1 v2
    for i in  range(len(v1)):
        dotproduct+=v1[i]+v2[i]

    # |V(d1 )|
    norm1 = 0
    for i in v1:
        norm1 += i*i
    norm1 = sqrt(norm1)

    # |V(q)|

    norm2 = 0
    for i in v2:
        norm2 += i*i
    norm2 = sqrt(norm2)

    # sim(d1, d2) = V(d1) dot V(d2) /(|V(d1)||V(d2)|)
    return dotproduct/(norm1*norm2)


docs = preprocessing('./test_texts')
vectors = getDocsVectors(docs, getWords(docs))

print(vectors)
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
# w = weightQuery(process_query("Hello darkness to my friend"), docs)
# print(w)
# print(idf)
# print(n)
