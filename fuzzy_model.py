from text_preprocessing import*
from tools import*
import os

# docs_terms = [] # relación documentos términos
# docs_keys = [] # get for each doc_id the real doc name
# corpus_terms = [] # términos que hay en el corpus
# correlation_matrix = {} # matriz de factor de correlación normalizado entre dos terminos ki kl
degree_of_membership_matrix = {} # el grado de pertenencia de cada documento al conjunto difuso asociado a cada término ki

class Fuzzy:

    def __init__(self, corpus_term, documents, compute_fuzzy_data_required: bool = False):
        self.a = 0.5 # suavizado
        self.corpus_terms: List['str'] = corpus_term # list to store the terms present in the documents
        self.documents: List['Doc'] = documents # documents of the corpus of the form Doc()
        self.correlation_matrix = {}
        if compute_fuzzy_data_required:
            self.compute_fuzzy_data()
        else:
            self.deg_memb_matrix = unpick_pickle_file('./preprocessed/deg_memb_matrix.pickle')
            

    def correlation_factor(self, ki: str, kl: str):
        '''
            term-term correlation matriz
            a normalized correlation factor ci,l between
            between two terms ki and kl

            `c_i,l = n_i,l/(ni nl - n_i,l)` 
        '''
        if (ki,kl) in self.correlation_matrix:
            return self.correlation_matrix[(ki, kl)]
        if (kl, ki) in self.correlation_matrix:
            return self.correlation_matrix[(kl, ki)]
        n_i = 0  # number of documents which contains the term ki
        n_l = 0 #number of documents which contains the term kl
        n_i_l = 0  #number of documents which contains both terms

        for tokens in self.corpus_terms:
            if ki in tokens:
                n_i+=1
            if kl in tokens:
                n_l+=1
            if ki in tokens and kl in tokens:
                n_i_l +=1

        result = n_i_l/(n_i + n_l - n_i_l) # ci,l
        self.correlation_matrix[(ki, kl)] = result

        return result

        # We can use the term correlation matrix c to define a fuzzy set 
        # associated to each index term k_i. In this fuzzy set, a document d_j
        # has a degree of membership miu_i,j.

    def degree_of_membership(self, ki, dj): # degree of membership ki term and document dj
        if (ki, dj) in degree_of_membership_matrix:
            return degree_of_membership_matrix[(ki, dj)]
        result = 1
        for term in self.documents[dj].terms:
            result *= 1- self.correlation_factor(ki, term)
        result = 1 - result
        return result

    def compute_matriz_degree_for_all(self):
        degree_of_membership_matrix = {}
        for t in self.corpus_terms:
            print(f'Término {t} init')
            for doc_id, _ in enumerate(self.documents):
                print(f'Término {t},doc {doc_id}init')
                degree_of_membership_matrix[(t, doc_id)] = self.degree_of_membership(t, doc_id)
                print(f'Término {t},doc {doc_id}finished')
            print(f'Término {t} finished')
        return degree_of_membership_matrix

    def compute_fuzzy_data(self):
        degree_of_membership_m = self.compute_matriz_degree_for_all()
        make_pickle_file('./preprocessed/deg_memb_matrix', degree_of_membership_m)
        self.deg_memb_matrix = degree_of_membership_m

    def sim(self, q, dj): # similitud entre la query y un documento en el modelo fuzzy [0,1]
        result = 1

        for t in q:
            result *= 1 - self.deg_memb_matrix[(t, dj)]

        result = 1- result
        return result

    
     # obtener los resultados de búsqueda con los términos que estableció el usuario
    def get_search_results(self,*, query: str,
        filters: List[str] = ['PDF', 'TXT', 'PLAIN TEXT'],
        top10: bool = False):
        tokens = filter_and_tokenize_text(query)
        tokens = remove_terms_not_appear(tokens, self.corpus_terms) # quito los términos de la query que no me interesan porque no aparece en los términos del corpus

        results = []
        for doc_id, _ in enumerate():
            s = self.sim(tokens, doc_id)
            if s > 0:
                current_doc = self.documents[doc_id]
                if (current_doc.type == 'PDF' and 'PDF' in filters 
                    or current_doc.type == 'TXT' and 'TXT' in filters 
                    or current_doc.type == 'PLAIN_TEXT' and 'PLAIN TEXT' in filters):
                    results.append((current_doc, s))

        results.sort(key = lambda x:x[1], reverse=True)
        results = [doc for doc,_ in results]
        if top10:
            results = results[:10]
        return results

    


