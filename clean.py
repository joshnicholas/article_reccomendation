import pandas as pd
from wordcloud import WordCloud, STOPWORDS

import re
import string

# import nltk
# from nltk.corpus import stopwords
# from nltk import RegexpTokenizer
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import wordnet
# from textblob import TextBlob as tb


## Read in datasets

read = pd.read_csv('archive/read.csv')
read['word_count'] = pd.to_numeric(read['word_count'])

unread = pd.read_csv('archive/unread.csv')
unread['word_count'] = pd.to_numeric(unread['word_count'])

## Random samply just 7000 rows for each

read = read.sample(7000)
unread = unread.sample(7000)

## Combine

combo = read.append(unread)



### Start cleaning text

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')

## Construct a matrix 

tfidf_matrix = tfidf.fit_transform(combo['excerpt'])

print(tfidf_matrix.shape)

p = combo

# print(p)
# print(p.columns)