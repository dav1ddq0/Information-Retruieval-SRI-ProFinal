from typing import List
from tools import *

# fraction of retrieved documents that are relevant
def precision(relevant_documents: List[str], recovered_documents: List[Doc]):
    '''
        Fraction of retrieved documents that are relevant
    '''
  
    # qrel = unpick_pickle_file(qrel_path)
    # relevant_documents = qrel[query]
    recovered_relevant_documents = 0
    
    for doc in recovered_documents:
        if doc.name  in relevant_documents:
            recovered_relevant_documents +=1
                  
    
    return recovered_relevant_documents/ len(recovered_documents)


# fraction of relevant documentos that were retrieved
def recall(qrel_path: str,query, recovered_documents: List):
    '''
        Fraction of relevant documentos that were retrieved
    '''
  
    qrel = unpick_pickle_file(qrel_path)
    relevant_documents = qrel[query]
    recovered_relevant_documents = 0
    
    for doc in recovered_documents:
        if doc  in relevant_documents:
            recovered_relevant_documents +=1
                  
    
    return recovered_relevant_documents/ len(relevant_documents)

# It is a measure that harmonizes precision and recovery taking both into account.
def f1 (qrel_path: str, query, recovered_documents: List):
    '''
        It is a measure that harmonizes precision and recovery taking both into account.
    '''
    p = precision(qrel_path, query, recovered_documents)
    r = recall(qrel_path, query, recovered_documents)
    return (2*p*r)/(p+r)


