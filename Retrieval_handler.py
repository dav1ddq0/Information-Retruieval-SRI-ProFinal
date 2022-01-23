from tools import *
from vectorial_model import Vectorial
from system_docs_processing import*
from fuzzy_model import Fuzzy
from performance import*
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
    
    def search(self, query: str, 
        filters: List[str] =  ['PDF', 'TXT', 'PLAIN TEXT'], 
        top10: bool= False):  
        return self.model.get_search_results(query = query, filters = filters, top10 = top10)

    def eval_model(self, corpus='cran'):
        qrels = open_JSON('./preprocessed/qrel.json')
        qrys = open_JSON('./preprocessed/qry.json') 
        name = corpus
        p_promedio = 0
        r_promedio = 0
        f1_promedio = 0
        fallout_promedio = 0
        not_relevant_documents_recovered = 0
        not_documents_recovered = 0
        all_documents = [doc.name for doc in self.documents]

        for query_id, query in enumerate(qrys):
            results = self.search(query)
            if not results:
                not_documents_recovered +=1

            docs_recovered = [doc.name for doc in  results]
            if all( d not in qrels[query_id] for d in docs_recovered):
                not_relevant_documents_recovered +=1

            p_promedio += precision(qrels[query_id], docs_recovered)
            r_promedio += recall(qrels[query_id], docs_recovered)
            f1_promedio += f1(qrels[query_id], docs_recovered)
            fallout_promedio += fallout(qrels[query_id], docs_recovered, all_documents)

        p_promedio = p_promedio/len(qrys)
        r_promedio = r_promedio/len(qrys)
        f1_promedio = f1_promedio/len(qrys)
        fallout_promedio = fallout_promedio/len(qrys)
        print(f'Evaluación general con el corpus {corpus}:')
        print(f'Cantidad de querys procesadas: {len(qrys)}')
        print(f'Ningún documento recuperado:{not_documents_recovered} ')
        print(f'Ningún documento relevante recuperado :{not_relevant_documents_recovered} ')
        print(f'Precisión  promedio: {p_promedio}')
        print(f'Recobrado promedio: {r_promedio}')
        print(f'Medida f1 promedio: {f1_promedio}')
        print(f'Fallout  promedio: {f1_promedio}')
           
    