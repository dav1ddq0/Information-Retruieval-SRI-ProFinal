import spacy
import os

from nltk.stem.snowball import SnowballStemmer


stemmer = SnowballStemmer(language='english')


nlp =  spacy.load('en_core_web_md')


def preprocessing(path):
    
    processed_docs={}
    text=''
    for doc in os.listdir(path):
        if os.path.splitext(doc)[1]=='.txt':
            text=open(os.path.join(path,doc)).read()
            tokens=nlp(text)
            tokens=[token for token in tokens if not token.is_stop and not token.is_punct and not token.is_space]
            tokens=[stemmer.stem(token.text) for token in tokens]
            processed_docs[doc]=tokens
        else:
            continue
           
    return processed_docs
