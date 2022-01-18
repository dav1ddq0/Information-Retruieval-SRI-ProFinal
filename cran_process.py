import os

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
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
    else:
        os.mkdir(path)
    
    for i,article in enumerate(cran_separate_articles()):
        process_article(article, i+1, path)






    



