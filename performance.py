from typing import List
from tools import *

# fraction of retrieved documents that are relevant
def precision(relevant_documents: List[str], recovered_documents: List[str]):
    '''
        Fraction of retrieved documents that are relevant
    '''
    if not recovered_documents:
        return 0
    # qrel = unpick_pickle_file(qrel_path)
    # relevant_documents = qrel[query]
    recovered_relevant_documents = 0
    
    for doc in recovered_documents:
        if doc  in relevant_documents:
            recovered_relevant_documents +=1
                  
    
    return recovered_relevant_documents/ len(recovered_documents)


# fraction of relevant documentos that were retrieved
def recall(relevant_documents: List[str], recovered_documents: List):
    '''
        Fraction of relevant documentos that were retrieved
    '''
  
    if not recovered_documents:
        return 0
    
    recovered_relevant_documents = 0
    
    for doc in recovered_documents:
        if doc  in relevant_documents:
            recovered_relevant_documents +=1
                  
    return recovered_relevant_documents/ len(relevant_documents)

# It is a measure that harmonizes precision and recovery taking both into account.
def f1 (relevant_documents: List[str], recovered_documents: List):
    if not recovered_documents:
        return 0
    '''
        It is a measure that harmonizes precision and recovery taking both into account.
    '''
    p = precision(relevant_documents, recovered_documents)
    r = recall(relevant_documents, recovered_documents)
    return (2*p*r)/(p+r)


def r_precision(relevant_documents: List[str], recovered_documents: List[str], n: int):
    return precision(relevant_documents, recovered_documents[:n])

def fallout(relevant_documents: List[str], recovered_documents: List[str], all_documents: List[str]):
    recovered_not_relevant_documents = 0
    not_relevant_documents = 0
    for doc in all_documents:
        if doc not in relevant_documents and doc in recovered_documents:
            not_relevant_documents +=1
            if doc in recovered_documents:
                recovered_not_relevant_documents+=1
    
    return  recovered_not_relevant_documents/not_relevant_documents

def r_fallout(relevant_documents: List[str], recovered_documents: List[str], all_documents: List[str], n: int):
    return fallout(relevant_documents, recovered_documents[:n], all_documents)
