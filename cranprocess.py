import os

def articles():
    with open('./test_texts/cran/cran.all.1400') as f:
        articles = f.read().split('\n.I')
    return articles

def save(text, number):
    with open(f'./test_texts/cran_1400_files/{number}', 'w') as newFile:
        newFile.write(text)


def process_article(article,i):
    article = article.split('\n.T\n')[1]

    _,_,article = article.partition('\n.W\n')
    save(article, i)
    return article

def cran_to_indepent_file():

    path = './test_texts/cran_1400_files'
    
    if os.path.exists(path):
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
    else:
        os.mkdir('./test_texts/cran_1400_files')
    
    for i,article in enumerate(articles()):
        process_article(article, i+1)


cran_to_indepent_file()



    



