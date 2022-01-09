from tools import *


def open_cran_qry():
    with open('./test_texts/cran/cran.qry') as f:
        querys = f.read().split('\n.I')
    return querys


def save(text, number):
    with open(f'./preprocessed/cran_1400_txt/doc{number}', 'w') as newFile:
        newFile.write(text)


def process(query):
    query = query.split('\n.W\n')[1]
    return query

qry = [process(query) for query in open_cran_qry()]


def open_qrel(filename: str):
    qrel = {}
    with open(filename) as f:
        for line in f.readlines():
            line = line.split() 
            q = int(line[0])
            d = int(line[1])
            if q in qrel:
                qrel[q].append(d)
            else:
                qrel[q] = [d]
    
    return qrel


qrel = open_qrel('./test_texts/cran/cranqrel')






make_pickle_file('./preprocessed/qry', qry)
make_pickle_file('./preprocessed/qrel', qrel)


