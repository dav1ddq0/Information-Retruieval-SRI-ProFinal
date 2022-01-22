import os
from typing import Dict, List
from model import*
from tools import*
from vectorial_model import*

def getTokens(words: List[str]) -> List['Token']:
    '''

    '''
    tokens: List['Token'] = []
    dic = {}

    for w in words:
        if w not in dic.keys():
            dic[w] = words.count(w)

    for w, o in dic.items():
        tokens.append(Token(word=w, freq=o))

    return tokens


def getWords(docs: Dict[str, List[Token]]):
    '''
        Create a list with all the words that exist 
        between all the documents in the system
    '''
    words = []

    for _, tokens in docs.items():
        for token in tokens:
            if token.word not in words:
                words.append(token.word)

    return words

def process_query(query: str):
    tokens = text_processed(query)
    return getTokens(tokens)

def preprocessing(path: str):

    doc_tokens = []
    
    doc_info_files = []
    terms = []

    
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
                doc_info_files.append(Doc(doc, full_path, 'TXT'))
                text = open(full_path).read()
                tokens = text_processed(text)
                for t in tokens:
                    if t not in terms:
                        terms.append(t)
                doc_tokens.append(getTokens(tokens))
            else:
                doc_info_files.append(Doc(doc, full_path,'PLAIN_TEXT'))
                with open(file = full_path, encoding="utf8", errors='ignore') as f:
                    text = f.read()
                    tokens = text_processed(text)
                    for t in tokens:
                        if t not in terms:
                            terms.append(t)
                    doc_tokens.append(getTokens(tokens))
                    
            

    

    return doc_tokens, doc_info_files, terms

def init_preprocessed(filename):
    docs_tokens, docs_info, terms = preprocessing(filename)
    check_folder = os.path.isdir('preprocessed')
    if  check_folder:
        os.mkdir('preprocessed')
        
    make_pickle_file('./preprocessed/docsinfo', docs_info)
    make_pickle_file('./preprocessed/terms', terms)
    make_pickle_file('./preprocessed/tokens', docs_tokens)
    
    # save_to_JSON('./preprocessed/words', words)
    vectors = getDocsVectors(docs_tokens,terms)
    np.save('./preprocessed/vectors', vectors)
    # make_pickle_file('./preprocessed/vectors', dv)


