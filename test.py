import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()

corpus = [ 'This is a sentence',
           'Another sentence is here',
           'Wait for another sentence',
           'The sentence is coming',
           'The sentence has come'
         ]

x = vectorizer.fit_transform(corpus)
print(pd.DataFrame(x.A, columns=vectorizer.get_feature_names()).to_string())