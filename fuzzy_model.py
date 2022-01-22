from text_preprocessing import*
from tools import*
import os

docs_terms = [] # relación documentos términos
docs_keys = [] # get for each doc_id the real doc name
corpus_terms = [] # términos que hay en el corpus
correlation_matrix = {} # matriz de factor de correlación normalizado entre dos terminos ki kl
degree_of_membership_matrix = {} # el grado de pertenencia de cada documento al conjunto difuso asociado a cada término ki

def correlation_factor(ki: str, kl: str):
    '''
        term-term correlation matriz
        a normalized correlation factor ci,l between
        between two terms ki and kl
        
        `c_i,l = n_i,l/(ni nl - n_i,l)` 
    '''
    if (ki,kl) in correlation_matrix:
        return correlation_matrix[(ki, kl)]
    if (kl, ki) in correlation_matrix:
        return correlation_matrix[(kl, ki)]
    n_i = 0  # number of documents which contains the term ki
    n_l = 0 #number of documents which contains the term kl
    n_i_l = 0  #number of documents which contains both terms

    for tokens in docs_terms:
        if ki in tokens:
            n_i+=1
        if kl in tokens:
            n_l+=1
        if ki in tokens and kl in tokens:
            n_i_l +=1
    
    result = n_i_l/(n_i + n_l - n_i_l) # ci,l
    correlation_matrix[(ki, kl)] = result

    return result

# We can use the term correlation matrix c to define a fuzzy set 
# associated to each index term k_i. In this fuzzy set, a document d_j
# has a degree of membership miu_i,j.

def degree_of_membership(ki, dj): # degree of membership ki term and document dj
    if (ki, dj) in degree_of_membership_matrix:
        return degree_of_membership_matrix[(ki, dj)]
    result = 1
    for term in docs_terms[dj]:
        result *= 1- correlation_factor(ki, term)
    result = 1 - result
    return result

def compute_matriz_degree_for_all():
    for t in corpus_terms:
        print(f'Término {t} init')
        for doc_id, _ in enumerate(docs_terms):
            print(f'Término {t},doc {doc_id}init')
            degree_of_membership_matrix[(t, doc_id)] = degree_of_membership(t, doc_id)
            print(f'Término {t},doc {doc_id}finished')
        print(f'Término {t} finished')
    save_to_JSON('fuzzy_membership.json', degree_of_membership_matrix)
    save_to_JSON('fuzzy_doc_keys.json', docs_keys)
    save_to_JSON('fuzzy_corpus_terms.json', corpus_terms)

    


def similarity(q, dj): # similitud entre la query y un documento en el modelo fuzzy [0,1]
    result = 1

    for t in q:
        result *= 1 - degree_of_membership_matrix[(t, dj)]
    
    return 1

def filter_text(docs_path):
    '''
        create a
        dictionary which has the name of the document as key and the terms present
        in it as the list of strings  which is the value of the key
        
    '''
    for doc in os.listdir(docs_path):
        full_path = os.path.join(docs_path, doc)
    
        with open(file = full_path, encoding="utf8", errors='ignore') as f:
            doc_text = f.read()
            tokens = text_preprocessing(
                text= doc_text,
                lowercase = True,
                convert_numbers= True,
                remove_punctuation=True,
                stopwords=True,
                lemmatize=True
                
            )
            for term in tokens:
                if term not in corpus_terms:
                    corpus_terms.append(term)

            docs_terms.append(tokens)
            docs_keys.append(doc)
        save_to_JSON('./preprocessed/corpues_t',corpus_terms)
    

# remove terms that do not appear in the corpus
def remove_terms_not_appear(terms):
    result = []
    for t in terms:
        if t in corpus_terms:
            result.append(t)
    return result

def get_search_results(query: str):
    tokens = filter_query(query)
    tokens = remove_terms_not_appear(tokens)
    results = []
    for doc_id, doc in enumerate(docs_keys):
        s = similarity(tokens, doc_id)
        if s > 0:
            results.append((docs_keys[doc_id], s))
    results.sort(key = lambda x:x[1], reverse=True)
    return results


