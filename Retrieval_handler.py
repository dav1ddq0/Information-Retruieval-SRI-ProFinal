from tools import *
from vectorial_model import Vectorial
from system_docs_processing import*
from fuzzy_model import Fuzzy
class Retrieval_handler:

    def __init__(self, *, system_docs_preprocess_required = False,
        model_preprocess_required = False, 
        retrieval_model_used: str ='vectorial'):

        
        
        if system_docs_preprocess_required:
            self.compute_and_save_corpus_data()
        else:
            self.corpus_terms = unpick_pickle_file('./preprocessed/terms.pickle')
            self.documents = unpick_pickle_file('./preprocessed/documents.pickle')
        if retrieval_model_used == 'vectorial':
            self.model: Vectorial = Vectorial(self.corpus_terms, self.documents, model_preprocess_required)
        if retrieval_model_used == 'fuzzy':
            self.model: Fuzzy = Fuzzy(self.corpus_terms, self.documents, model_preprocess_required)

    def compute_and_save_corpus_data(self, docs_path: str = './system_docs'):
        docs = libdocuments_processing(docs_path)
        terms = get_terms(docs) 
        make_pickle_file('./preprocessed/terms', terms)
        make_pickle_file('./preprocessed/documents', docs)
        self.corpus_terms = terms
        self.documents = docs
    
    def search(self, query: str, filters: List[str], top10: bool= False):  
        return self.model.get_search_results(query = query, filters = filters, top10 = top10)

    def eval_model(corpus='cran', model= 'vectorial'):
        if corpus == 'cran':
            pass
        