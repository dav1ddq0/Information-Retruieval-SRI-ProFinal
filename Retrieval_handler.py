from doc_preprocessed import *
from tools import open_from_numpy_file, unpick_pickle_file
import numpy as np
from vectorial import *


class Retrieval_handler:

    def __init__(self, *, preprocess_required = False):
        self.preprocess_required = preprocess_required
        
        if preprocess_required:
            init_preprocessed('./system_docs')
        
        self.terms = unpick_pickle_file('./preprocessed/terms.pickle')
        self.docs_info = unpick_pickle_file('./preprocessed/docsinfo.pickle')
        self.docs_vectors = open_from_numpy_file('./preprocessed/vectors.npy')
        self.docs_tokens = unpick_pickle_file('./preprocessed/tokens.pickle')
        
    
    def SearchCoincidences(self, query: str, top: int):
        procquery = process_query(query)
        
        qvector = qVector(procquery, self.terms, len(self.docs_vectors), ni_table(self.docs_tokens, self.terms))

        search_results = getSimilarDocuments(self.docs_vectors, qvector)[:top]
        
        docsresult = getDocsFiles(search_results, self.docs_info)
        return docsresult

