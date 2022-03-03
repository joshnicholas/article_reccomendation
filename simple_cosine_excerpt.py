import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity
# import re 
# import string

# import nltk
# from nltk.stem import PorterStemmer
# from nltk.stem.wordnet import WordNetLemmatizer


# import spacy
# nlp = spacy.load('en_core_web_sm')


######### Read in datasets

# read = pd.read_csv('archive/read.csv')
# read['word_count'] = pd.to_numeric(read['word_count'])

# unread = pd.read_csv('archive/unread.csv')
# unread['word_count'] = pd.to_numeric(unread['word_count'])

# combo = unread.append(read)

# # 'status', 'time_added', 'resolved_title', 'resolved_url', 'excerpt',
# #        'word_count'

# combo = combo[['status','resolved_title', 'resolved_url', 'excerpt']]



####### Cleaning

# def clean_string(text, stem="None"):

#     final_string = ""

#     # Make lower
#     text = text.lower()

#     # Remove line breaks
#     text = re.sub('\n', '', text)

#     # Remove puncuation
#     translator = str.maketrans('', '', string.punctuation)
#     text = text.translate(translator)

#     # Remove stop words
#     text = text.split()
#     useless_words = nltk.corpus.stopwords.words("english")
#     useless_words = useless_words + ['hi', 'im']

#     text_filtered = [word for word in text if not word in useless_words]

#     # Remove numbers
#     text_filtered = [re.sub('\w*\d\w*', '', w) for w in text_filtered]

#     # Stem or Lemmatize
#     if stem == 'Stem':
#         stemmer = PorterStemmer() 
#         text_stemmed = [stemmer.stem(y) for y in text_filtered]
#     elif stem == 'Lem':
#         lem = WordNetLemmatizer()
#         text_stemmed = [lem.lemmatize(y) for y in text_filtered]
#     elif stem == 'Spacy':
#         text_filtered = nlp(' '.join(text_filtered))
#         text_stemmed = [y.lemma_ for y in text_filtered]
#     else:
#         text_stemmed = text_filtered

#     final_string = ' '.join(text_stemmed)

#     return final_string

# combo['cleaned'] = combo['excerpt'].apply(lambda x: clean_string(x, stem='Stem'))
# combo['cleaned'] = combo['cleaned'].str.strip()

# with open('archive/cleaned.csv', 'w') as f:
#     combo.to_csv(f, index=False, header=True)


###### CREATE MODEL

# #tokenize and tag the card text
# card_docs = [TaggedDocument(doc.split(' '), [i]) 
#              for i, doc in enumerate(combo.cleaned)]

# #instantiate model
# model = Doc2Vec(vector_size=64, window=2, min_count=1, workers=8, epochs = 40)
# #build vocab
# model.build_vocab(card_docs)
# #train model
# model.train(card_docs, total_examples=model.corpus_count
#             , epochs=model.epochs)



# ## Save model
# model.save("models/cosine_doc2vec.model")



## Load model 

model = Doc2Vec.load("models/cosine_doc2vec.model")





# ###### Generator vectors

# combo = pd.read_csv('archive/cleaned.csv')

# combo['cleaned'] = combo['cleaned'].astype(str)

# card2vec = [model.infer_vector(combo.iloc[i]['cleaned'].split(' '))
#             for i in range(0,len(combo))]

# ## Add to dataframe

# import numpy as np
# #Create a list of lists
# dtv= np.array(card2vec).tolist()
# #set list to dataframe column
# combo['card2vec'] = dtv

# with open('archive/vectored.csv', 'w') as f:
#     combo.to_csv(f, index=False, header=True)


#### MAKE SIMILARITY SCORES

vec = pd.read_csv('archive/vectored.csv')
vec = vec.loc[~vec['resolved_url'].str.contains('https://twitter.com')]
# 'status', 'resolved_title', 'resolved_url', 'excerpt', 'cleaned',
#        'card2vec'

unread =  vec.loc[vec['status'] == 0].copy()
read = vec.loc[vec['status'] == 1].copy()

first = model.infer_vector(read.iloc[250]['cleaned'].split(' ')).tolist()

from scipy import spatial
# unread = unread.dropna()

unread['Similarity'] = 0

listo = []

for index, row in unread.iterrows():

    texto = row['card2vec'].replace("[", '').replace("]", '').split(",")

    first = [float(x) for x in first]
    texto = [float(x) for x in texto]

    titlo = row['resolved_title']
    urlo = row['resolved_url']

    sim = spatial.distance.cosine(first, texto)

    data = [{'resolved_title': titlo,
    'resolved_url': urlo,
    'Similarity': sim}]

    inter = pd.DataFrame.from_records(data)

    listo.append(inter)

    
fin = pd.concat(listo)

fin.sort_values(by=['Similarity'], inplace=True, ascending=True)

p = fin

print(p.head)
print(p.columns)
