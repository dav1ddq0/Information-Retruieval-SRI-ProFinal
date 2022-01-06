from typing import List
from tools import *

# fraction of retrieved documents that are relevant
def precision(qrel_path: str,query, recovered_documents: List):
    
  
    qrel = open_JSON(qrel_path)
    relevant_documents = qrel[query]
    recovered_relevant_documents = 0
    
    for doc in recovered_documents:
        if doc  in relevant_documents:
            recovered_relevant_documents +=1
                  
    
    return recovered_relevant_documents/ len(recovered_documents)


# fraction of relevant documentos that were retrieved
def recall(qrel_path: str,query, recovered_documents: List):
    
  
    qrel = open_JSON(qrel_path)
    relevant_documents = qrel[query]
    recovered_relevant_documents = 0
    
    for doc in recovered_documents:
        if doc  in relevant_documents:
            recovered_relevant_documents +=1
                  
    
    return recovered_relevant_documents/ len(relevant_documents)