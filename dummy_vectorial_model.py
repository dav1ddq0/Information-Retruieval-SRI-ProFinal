import math
from typing import List
import numpy as np
import os
from text_preprocessing import*
from collections import Counter
import numpy as np
from tools import *
from tools import save_to_JSON

a = 0.5 # suavizado
# list to store the terms present in the documents
corpus_terms = unpick_pickle_file('./preprocessed/terms.pickle')



documents = unpick_pickle_file('./preprocessed/documents.pickle')

# # dictionary to store the term and the number of times of its occurrence 
# # in the documents
# term_freq = {}


# # dictionary to store the term and the inverse document frequency 

if os.path.exists('./preprocessed/idf.pickle'):
    rec_idf = unpick_pickle_file('./preprocessed/idf.pickle')

if os.path.exists('./preprocessed/d_vectors.pickle'):
    rec_d_vectors = unpick_pickle_file('./preprocessed/d_vectors.pickle')
    

# # dictionary to store the term and the weight which is the product of term
# # frequency and inverse document frequency
# weight = {}

def sim(v1: List[float], v2: List[float]) -> float:
    '''
        Computes the similarity between two vectors v1,v2
        
        Parameters
        ----------
        v1 : List[float]
        represents the vector v1

        v2 : List[float]
        represents the vector v2
        
        `sim(v1, v2) = v1 dot v2 /(|v1||v2|)`
    '''
    dotproduct = 0

    # compute dotproduct from v1 v2
    # dot = np.dot(v1, v2)
    for i in range(len(v1)):
        dotproduct += v1[i]*v2[i]

    # |V(d1 )|
    # norm1 = np.linalg.norm(v1)
    norm1 = 0
    for i in v1:
        norm1 += i*i
    norm1 = math.sqrt(norm1)

    # |V(q)|

    # norm2 = np.linalg.norm(v2)
    norm2 = 0
    for i in v2:
        norm2 += i*i
    norm2 = math.sqrt(norm2)

    # if norm1 or norm2 == 0:
    #     return 0
    # sim(d1, d2) = V(d1) dot V(d2) /(|V(d1)||V(d2)|)
    if norm1 == 0 or norm2 == 0:
        return 0
    return dotproduct/(norm1*norm2)









def compute_weight():
    '''
        Function to compute the weight for each of the terms in the document.
        Here the weight is calculated with the help of term frequency and
        inverse document frequency
    '''
    N = len(documents) # cantidad de documentos 
    
    d_vectors = [ len(corpus_terms)*[0] for _ in range(N) ] # cada documento va a tener un vector de 
    # número de componentes igual a la cantidad de términos
    tf = [N*[0] for _ in range(len(corpus_terms))] # tf table tfi,j term i document j
    idf = len(corpus_terms)*[0]
    # si el término no aparece en el documento entonces su tfi,j = 0
    
    # print(doc_terms[len(doc_terms)-1])
    for doc_id,doc in enumerate(documents):
        
        if doc.terms:
            freq_counter = Counter(doc.terms)
            max_freq_dj  = freq_counter.most_common(1)[0][1] # la máxima frecuencia de los términsos del documento
            for ti, term in enumerate(corpus_terms):
                freqij = freq_counter[term] # la frecuencia del término i en el documento j
                tf[ti][doc_id] = freqij/max_freq_dj 
    
    terms_appear = len(corpus_terms)*[0] # ni number of documents  in which a term appears
    
    for tp, t in enumerate(corpus_terms): # por cada término que hay en la bd
        for doc in documents: # por cada término que tiene cada documento
            if t in doc.terms:
                terms_appear[tp]+=1
    
    
    for tp,ti in enumerate(corpus_terms):
            idf[tp] =  math.log(N/terms_appear[tp])
    
    for dj in range(N):
        for tp, ti in enumerate(corpus_terms):
            d_vectors[dj][tp] = tf[tp][dj] * idf[tp]
    
    return d_vectors, idf
    

def compute_and_save_vectorial_data():
    d_vectors, idf = compute_weight()
    make_pickle_file('./preprocessed/d_vectors', d_vectors)
    make_pickle_file('./preprocessed/idf', idf)


# remove terms that do not appear in the corpus


def compute_query_weight(query: str):
    tokens = filter_and_tokenize_text(query)
    tokens = remove_terms_not_appear(tokens, corpus_terms) # quito los términos de la query que no me interesan porque no aparece en los términos del corpus

    tf = len(corpus_terms)*[0] # tf table tfi,j term i document j
    # si el término no aparece en el documento entonces su tfi,j = 0
    
    
    q_vector = len(corpus_terms)*[0]
    if tokens:
        freq_counter = Counter(tokens)
        max_freq_q  = freq_counter.most_common(1)[0][1] # la máxima frecuencia de los términsos del documento
        for ti, term in enumerate(corpus_terms):
            freqiq = freq_counter[term] # la frecuencia del término i en el documento j
            tf_ti_q = a + (1 - a)* (freqiq/max_freq_q) # frecuencia normalizada del término ti en la query q
            idf_ti = rec_idf[ti] # inverse document frecuency del término ti
            w_iq = tf_ti_q * idf_ti #peso del término ti en la query q
            q_vector[ti] = w_iq
    

    return q_vector


def get_search_results(*, query: str,
    pdf = True,
    txt = True,
    plane_text = True,
    top: int = 0):
    q_vector = compute_query_weight(query)
    results = []
    for doc_id, d_vector in enumerate(rec_d_vectors):
        s = sim(d_vector, q_vector)
        if s > 0:
            current_doc = documents[doc_id]
            if (current_doc.type == 'PDF' and pdf 
                or current_doc.type == 'TXT' and txt 
                or current_doc.type == 'PLAIN_TEXT' and plane_text):
                results.append((current_doc.name, s))

    results.sort(key = lambda x:x[1], reverse=True)
    if top:
        results = results[:top]
    return results


# filter_text('./system_docs')
# compute_weight()
