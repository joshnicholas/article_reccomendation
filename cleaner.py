from matplotlib.pyplot import title
import pandas as pd 
import numpy as np

from rake_nltk import Rake
rakers = Rake()

import re 
import string

import nltk
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

import spacy
nlp = spacy.load('en_core_web_sm')

import scipy
import statsmodels.formula.api as smf
import statsmodels.api as sm

from sklearn import model_selection, preprocessing, feature_selection, ensemble, linear_model, metrics, decomposition
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

cv = CountVectorizer(max_df=0.95, min_df=2, stop_words="english")

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
model = Doc2Vec.load("models/cosine_doc2vec.model")

def clean_string(text, stem="None"):

    final_string = ""

    # Make lower
    text = text.lower()

    # Remove line breaks
    text = re.sub('\n', '', text)

    # Remove puncuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)

    # Remove stop words
    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    useless_words = useless_words + ['hi', 'im']

    text_filtered = [word for word in text if not word in useless_words]

    # Remove numbers
    text_filtered = [re.sub('\w*\d\w*', '', w) for w in text_filtered]

    ## Remove special chars

    text_filtered = [re.sub(r"[^a-zA-Z0-9 ]", '', w) for w in text_filtered]

    # Stem or Lemmatize
    if stem == 'Stem':
        stemmer = PorterStemmer() 
        text_stemmed = [stemmer.stem(y) for y in text_filtered]
    elif stem == 'Lem':
        lem = WordNetLemmatizer()
        text_stemmed = [lem.lemmatize(y) for y in text_filtered]
    elif stem == 'Spacy':
        text_filtered = nlp(' '.join(text_filtered))
        text_stemmed = [y.lemma_ for y in text_filtered]
    else:
        text_stemmed = text_filtered

    final_string = ' '.join(text_stemmed)

    final_string = final_string.replace("  ", ' ')

    return final_string



# Load data 

read = pd.read_csv('https://raw.githubusercontent.com/joshnicholas/article_reccomendation/main/archive/read.csv')
unread = pd.read_csv('https://github.com/joshnicholas/article_reccomendation/blob/main/archive/unread.csv?raw=true')

combo = read.append(unread)

# print(combo.columns)
# 'status', 'time_added', 'resolved_title', 'resolved_url', 'excerpt',
#        'word_count'

### Create new features to help with machine learning

combo['title_count'] = combo['resolved_title'].str.split(" ").str.len()

# vectored = combo[:5]


listo = []
for index, row in combo.iterrows():

    texto = row['excerpt']

    cleaned = clean_string(texto)

    status =  row['status']
    titlo = row['resolved_title']
    title_count = row['title_count']
    urlo = row['resolved_url']

    excerpt = row['excerpt']

    a = rakers.extract_keywords_from_text(excerpt)
    keywords = rakers.get_ranked_phrases()
    keywords = " ".join(keywords)

    keywords = clean_string(keywords)

    data = [{'status':status,
    'resolved_title': titlo,
    'resolved_url': urlo,
    'keywords': keywords,
    'excerpt': texto,
    'cleaned_text': cleaned,
    'title_word_count': title_count,
    'word_count': row['word_count']
    }]

    inter = pd.DataFrame.from_records(data)

    print(inter)
    print(inter.columns)

    listo.append(inter)


fin = pd.concat(listo)

with open('archive/binary_cleaned.csv', 'w') as f:
    fin.to_csv(f, index=False, header=True)

p = combo

# print(p)
# print(p.columns)
# print(p['title_count'])