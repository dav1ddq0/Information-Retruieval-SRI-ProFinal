import os
from tools import *

def cran_separate_articles():
    with open('./test_documents/cran/cran.all.1400') as f:
        articles = f.read().split('\n.I')
    return articles

def save_cran_docs(text, number, path):
    with open(f'{path}/{number}', 'w') as newFile:
        newFile.write(text)


def process_article(article,i, path):
    article = article.split('\n.T\n')[1]

    _,_,article = article.partition('\n.W\n')
    save_cran_docs(article, i, path)
    return article

def make_cran_to_indepent_file():
    
    path = './system_docs'
    
    if os.path.exists(path):
        remove_all_from_a_path(path)
    else:
        os.mkdir(path)
    
    for i,article in enumerate(cran_separate_articles()):
        process_article(article, i+1, path)


def open_cran_qry(filename: str):
    with open(f'{filename}/cran.qry') as f:
        querys = f.read().split('\n.I')
    return querys

def process_1qry(query):
    query = query.split('\n.W\n')[1]
    return query

def process_cran_dot_qry(filename):
    return [process_1qry(query) for query in open_cran_qry(filename)]

def open_cran_qrel(filename: str):
    qrel = []
    with open(f"{filename}/cranqrel") as f:
        for line in f.readlines():
            line = line.split() 
            q = int(line[0])
            d = line[1]

            try:
                qrel[q-1].append(d)
            except IndexError:
                qrel.append([d])
            
           
    
    return qrel

def make_cran_query_qrel_files():
    '''

    '''
    cran_path = './test_documents/cran'
    qry = process_cran_dot_qry(cran_path)
    save_to_JSON('./preprocessed/qry', qry)
    qrel = open_cran_qrel(cran_path)
    save_to_JSON('./preprocessed/qrel', qrel)


    



    



