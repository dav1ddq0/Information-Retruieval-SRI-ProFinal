from enum import Enum
from typing import Callable, Dict, List, Tuple
from numpy import bool8, number, sqrt

import os
import math
from model import*
from tools import*



# termino de suaviado
a = 0.5

tf: Callable[[int, int], float] = lambda freqij, maxfreqlj: freqij/maxfreqlj
idf: Callable[[int, int], float] = lambda N, ni: math.log(N/ni)
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


def tftable(documents: Dict[str, List[Token]], words: List[str]):
    tftable = {(w, doc): 0 for w in words for doc in documents.keys()}

    for doc, tokens in documents.items():

        for token in tokens:
            tftable[token.word, doc] = tf(token.freq, max(tokens).freq)

    return tftable


def ni_table(documents: Dict[str, List[Token]], words: List['Token']):
    ntable = {w: 0 for w in words}

    for doc, tokens in documents.items():
        for token in tokens:
            ntable[token.word] += 1

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

    for w, o in dic.items():
        tokens.append(Token(word=w, freq=o))

    return tokens


def qVector(q: List[Token], words: List[str], N: int, nitable):
    vq = len(words)*[0]
    term_dic = {word: index for index, word in enumerate(words)}
    for word in words:
        tfiq = q.count(word)/max(q).freq
        idfi = idf(N, nitable[word])
        wiq = (a + (1-a)*tfiq)*idfi
        vq[term_dic[word]] = wiq
    return vq




def preprocessing(path):

    processed_docs = {}
    text = ''
    doc_files = {}
    s = os.listdir(path)
    for doc in os.listdir(path):
        full_path = os.path.join(path, doc)
        if os.path.isdir(full_path):
            continue
            # tpd, tdocd = preprocessing(full_path)
            # for key,value in tpd.items():
            #      processed_docs[key] = value

            # for key,value in tdocd.items():
            #      doc_files[key] = value
        else:  
            if os.path.splitext(doc)[1] == '.txt':
                doc_files[doc] =Doc(doc, full_path, 'TXT')
                text = open(full_path).read()
                tokens = text_processed(text)
                processed_docs[doc] = tokens
            else:
                doc_files[doc] = Doc(doc, full_path,'PLAIN_TEXT')
                with open(file = full_path, encoding="utf8", errors='ignore') as f:
                    text = f.read()
                    tokens = text_processed(text)
                    processed_docs[doc] = tokens
                    
            

    result = {doc: getTokens(tokens) for doc, tokens in processed_docs.items()}

    return result, doc_files




def process_query(query: str):
    tokens = text_processed(query)
    return getTokens(tokens)

# All words in system documents


def getWords(docs: Dict[str, List[Token]]):
    words = []

    for _, tokens in docs.items():
        for token in tokens:
            if token.word not in words:
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
    term_dic = {word: index for index, word in enumerate(words)}
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



def getSimilarDocuments(docs, q, top: int):
    result = []
    
    for doc, vj in docs.items():
        s = sim(vj, q)
        result.append((doc, s))

    result.sort(key = lambda x:x[1], reverse=True)
    return result[:top]

#
def sim(v1: List[float], v2: List[float]) -> float:
    dotproduct = 0

    # compute dotproduct from v1 v2
    for i in range(len(v1)):
        dotproduct += v1[i]*v2[i]

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


def getDocsFiles(results:List[Tuple[str, float]], docdicc):
    return [docdicc[docname] for (docname, _) in results]     




def init_preprocessed(filename):
    docs_tokens, docs_info= preprocessing(filename)
    save_to_JSON('./preprocessed/docsinfo', from_docsl_to_dicc(docs_info))
    words = getWords(docs_tokens)
    save_to_JSON('./preprocessed/words', words)






init_preprocessed('./test_texts/cran_1400_files')


# def SearchCoincidences(query: str):
#     procquery = process_query(query)
#     qvector = qVector(procquery, words, len(docs.keys()), ni_table(docs, words))
#     dvector = getDocsVectors(docs, words)
#     e = getSimilarDocuments(dvector, qvector, 20)
#     print(e)
#     docsresult = getDocsFiles(e, docdicc)
#     return docsresult




# for doc in SearchCoincidences("what are the structural and aeroelastic problems associated with flight\nof high speed aircraft ."):
#     print(doc)

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
