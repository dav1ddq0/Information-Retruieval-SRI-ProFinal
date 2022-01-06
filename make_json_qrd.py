from tools import *


def open_cran_qry():
    with open('./test_texts/cran/cran.qry') as f:
        querys = f.read().split('\n.I')
    return querys


def save(text, number):
    with open(f'./preprocessed/cran_1400_txt/doc{number}', 'w') as newFile:
        newFile.write(text)


def process(query,i):
    query = query.split('\n.W\n')[1]
    return query

qry = {(i+1):process(query, i+1) for i,query in enumerate(open_cran_qry())}


def open_qrel(filename: str):
    qrel = {}
    with open(filename) as f:
        for line in f.readlines():
            line = line.split() 
            q = line[0]
            d = line[1]
            if q in qrel:
                qrel[q].append(d)
            else:
                qrel[q] = [d]
    
    return qrel


qrel = open_qrel('./test_texts/cran/cranqrel')






save_to_JSON('./preprocessed/qry', qry)
save_to_JSON('./preprocessed/qrel', qrel)


