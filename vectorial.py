from enum import Enum
from json import load
from typing import Callable, Dict, List, Tuple
from numpy import bool8, number, sqrt
import numpy as np
import os
import math
from model import*
from tools import*



# termino de suaviado
a = 0

tf : Callable[[int, int], float]  = lambda freqij, maxfreqlj: freqij/maxfreqlj
idf: Callable[[int, int], float]  = lambda N, ni: np.log(N/ni)
# given a document returns the frequency of occurrence of each term in this

# A document is represented by the name of the document and a list of tokens
# that are the result of having processed the document by removing the keywors and stemming.


def freq(document: List[str]):
    words = {}

    for word in document:
        if word not in words.keys():
            words[word] = 1
        else:
            words[word] += 1

    return words


def maxfreq(words: Dict[str, int]):
    maxfreq = 0

    for word in words.keys():
        maxfreq = words[word] if words[word] > maxfreq else maxfreq

    return maxfreq


def freqtable(documents: Dict[str, List[str]]):
    freqtable = {}
    for doc, tokens in documents.items():
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
            freq[token] += 1

    for _, wfreq in freq.items():
        if wfreq > maxfreq:
            maxfreq = wfreq

    for token in query:
        querytf[token] = tf(freq[token], maxfreq)

    return querytf


def tftable(documents: List[List[Token]], words: List[str]):
    tftable = {(w, dj): 0 for w in words for dj,_ in enumerate(documents)}

    for dj, tokens in enumerate(documents):

        for token in tokens:
            tftable[token.word, dj] = tf(token.freq, max(tokens).freq)

    return tftable


def ni_table(documents: List[List[Token]], words: List['Token']):
    
    ntable = {w: 0 for w in words}

    for tokens in documents:
        for token in tokens:
            ntable[token.word] += 1

    return ntable


def idf_table(documents: List[List[Token]], words: List[str]):
    N = len(documents)
    idftable = {w: 0 for w in words}
    nit = ni_table(documents, words)
    for w in words:
        idftable[w] = idf(N, nit[w])

    return idftable




def qVector(q: List[Token], words: List[str], N: int, nitable):
    vq = len(words)*[0]
    term_dic = {word: index for index, word in enumerate(words)}
    for word in words:
        tfiq = q.count(word)/max(q).freq
        idfi = idf(N, nitable[word])
        wiq = (a + (1-a)*tfiq)*idfi
        vq[term_dic[word]] = wiq
    
    return np.array(vq)









# All words in system documents




# Para cada termino i la cantidad de documentos  en los que aparece


# def n_i_table(docs: Dict[str, List[Token]], words):

#     n_i_t = {w: 0 for w in words}

#     for w in words:

#         for _, tokens in docs.items():

#             for token in tokens:
#                 if token.word == w:
#                     n_i_t[w] += 1

#     return n_i_t


def getDocsVectors(docs_tokens: List[List[Token]], words: List[str]):
    # vectors: Dict[str, List[number]] = {}
    vectors = []
    # N = len(docs.keys())
    # nit = ni_table(docs_tokens, words)
    tft = tftable(docs_tokens, words)
    
    idft = idf_table(docs_tokens, words)

    for dj, tokens in enumerate(docs_tokens):
        vj = len(words)*[0]

        for index, token in enumerate(tokens):
            
            tfij = tft[token.word, dj]
            idfi = idft[token.word]
            wij = tfij*idfi
            vj[index] = wij

        vectors.append(vj)

    return np.array(vectors)



def getSimilarDocuments(docs, q):
    result = []
    
    for doc, vj in enumerate(docs):
        s = sim(vj, q)
        result.append((doc, s))

    result.sort(key = lambda x:x[1], reverse=True)
    return result

#
def sim(v1: List[float], v2: List[float]) -> float:
    # dotproduct = 0

    # compute dotproduct from v1 v2
    dot = np.dot(v1, v2)
    # for i in range(len(v1)):
    #     dotproduct += v1[i]*v2[i]

    # |V(d1 )|
    norm1 = np.linalg.norm(v1)
    # norm1 = 0
    # for i in v1:
    #     norm1 += i*i
    # norm1 = sqrt(norm1)

    # |V(q)|

    norm2 = np.linalg.norm(v2)

    # for i in v2:
    #     norm2 += i*i
    # norm2 = sqrt(norm2)

    # sim(d1, d2) = V(d1) dot V(d2) /(|V(d1)||V(d2)|)
    return dot/(norm1*norm2)


def getDocsFiles(results:List[Tuple[int, float]], docdicc):
    return [docdicc[doc_id] for doc_id, sim in results]   









# preprocessed_required = True

# if preprocessed_required:
#     init_preprocessed('./test_texts/cran_1400_files')


# vectors  = np.load('./preprocessed/terms.npy')
# print(vectors)
# a = unpick_pickle_file('./preprocessed/docsinfo.pickle')

# for key, docfile in a.items():
#     print(docfile)



# def SearchCoincidences(query: str):
#     procquery = process_query(query)
#     docs_info = unpick_pickle_file('./preprocessed/docsinfo.pickle')
#     terms = unpick_pickle_file('./preprocessed/terms.pickle')
#     doc_vectors = np.load('./preprocessed/vectors.npy')
#     doc_tokens = unpick_pickle_file('./preprocessed/tokens.pickle')
#     qvector = qVector(procquery, terms, len(doc_vectors), ni_table(doc_tokens, terms))
    
#     e = getSimilarDocuments(doc_vectors, qvector, 50)
#     print(e)
#     docsresult = getDocsFiles(e, docs_info)
#     return docsresult




for doc in SearchCoincidences("what are the structural and aeroelastic problems associated with flight\nof high speed aircraft ."):
    print(doc)

# print(z)
# vectors = getDocsVectors(docs, getWords(docs))

# print(vectors)
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
