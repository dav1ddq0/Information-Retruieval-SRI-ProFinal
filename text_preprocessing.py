import nltk 
import string
import re
import inflect
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import copy

porter_stemmer =  PorterStemmer()
snowball_stemmer = SnowballStemmer(language='english')
lancaster_stemmer = LancasterStemmer()
inflect_engine = inflect.engine()
lemmatizer = WordNetLemmatizer()

def text_to_lowercase(text: str):
    '''
        Dado un str de entrada devuelve el mismo en lowecase

        Parámetros:
        -----------
        text: str texto de entrada

        `Ponemos en minúsculas el texto para reducir el tamaño del vocabulario 
        de nuestros datos del texto.`
    '''
    return text.lower()

# remove numbers from text
def remove_numbers(text):
    '''
       Podemos usar expresiones regulares para remover los números


    '''
    return re.sub(r'\d+', '', text)

# convert number into words
def convert_numbers_into_words(text: str)-> str:
    '''

    '''
    result = []
    for word in text.split(): # split string into list of words
        
        if word.isdigit(): # if word is a digit, convert the digit
            result.append((inflect_engine.number_to_words(word)))
                 
        else:
            result.append(word)
    
    return ' '.join(result)
    


# remove punctuation
def remove_punctuation_marks(text: str):
    '''
        We remove punctuations so that we don’t have different forms of the same word. 
        If we don’t remove the punctuation, then been. been, been! will be treated separately.
    '''
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

# convert text to tokens
def text_tokenize(text: str):
    '''
    
    '''
    tokens = word_tokenize(text)
    return tokens

# remove stopwords
def text_remove_stopword(text: str):
    '''
        Stopwords are words that do not contribute to the meaning of a sentence. 
        Hence, they can safely be removed without causing any change in the 
        meaning of the sentence
    '''
    stop_words = set(stopwords.words("english"))
    
    return ' '.join([word for word in text_tokenize(text) if word not in stop_words])
    
def text_stem_words(text: str, stemmer: str):
    '''
        Stemming is the process of getting the root form of a word. Stem or root is the part to which inflectional affixes 
        (-ed, -ize, -de, -s, etc.) are added. The stem of a word is created by removing the 
        prefix or suffix of a word
    '''
    
    if text == 'porter':
        stemmer = porter_stemmer
    elif text == 'snowball':
        stemmer = snowball_stemmer
    else:
        stemmer = lancaster_stemmer
    
    stems = [stemmer.stem(word) for word in text_tokenize(text)]
    return ' '.join(stems)

def text_lemmatize_words(text: str):
    '''
        Like stemming, lemmatization also converts a word to its root form. The only difference is that 
        lemmatization ensures that the root word belongs to the language. 
        We will get valid words if we use lemmatization.
    '''
    # provide context i.e. part-of-speech
    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in text_tokenize(text)]
    return ' '.join(lemmas)

def remove_terms_not_appear(q_terms, terms): # elimna los términos que no estén el el vocabulario
    result = []
    for t in q_terms:
        if t in terms:
            result.append(t)
    return result

def text_preprocessing(*, text: str, 
    lowercase: bool = False, 
    remove_numbers: bool = False,
    convert_numbers: bool = False,
    remove_punctuation: bool = False,
    stopwords: bool = False,
    stem: str = None,
    lemmatize: bool = False):
    '''
        we need to apply several pre-processing steps to the data to transform words into numerical 
        features that work with machine learning algorithms. The pre-processing steps for a problem 
        depend mainly on the domain and the problem itself, hence, we don’t need to apply all 
        steps to every problem

        Params:
        --------
        text: str input text
        lowercase: bool 


    '''

    text_preprocessing = copy.deepcopy(text)
    if lowercase:
        text_preprocessing  = text_to_lowercase(text_preprocessing)
    if remove_numbers:
        text_preprocessing = remove_numbers(text_preprocessing)
    if convert_numbers:
        text_preprocessing = convert_numbers_into_words(text_preprocessing)
    if remove_punctuation:
        text_preprocessing = remove_punctuation_marks(text_preprocessing)
    if stopwords:
        text_preprocessing = text_remove_stopword(text_preprocessing)
    if stem:
        text_preprocessing = text_stem_words(text_preprocessing, stem)
    if lemmatize:
        text_preprocessing = text_lemmatize_words(text_preprocessing)
    
    tokens = text_tokenize(text_preprocessing)
    return tokens


def filter_and_tokenize_text(text: str):
    tokens = text_preprocessing(
                text=text,
                lowercase = True,
                convert_numbers= True,
                remove_punctuation=True,
                stopwords=True,
                lemmatize=True
                
            )
    
    return tokens


