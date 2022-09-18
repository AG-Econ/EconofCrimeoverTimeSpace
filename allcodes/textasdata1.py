import os
import sys
from collections import Counter
from itertools import chain

import nltk
import numpy as np
import pandas as pd
import spacy
from nltk import word_tokenize, RegexpTokenizer, FreqDist, PorterStemmer
from nltk.corpus import stopwords

nltk.download('maxent_ne_chunker')
nltk.download('punkt')
nltk.download('stopwords')

NER = spacy.load("en_core_web_sm")

dat_dir = 'YOUR DIRECTORY'
dat_link = dat_dir + 'raw_data.csv'
scraped_data = pd.read_csv(dat_link)

print(scraped_data.head())
len(scraped_data.index)

'''Because we have studied the data to notice some specific irrelevant texts - can be done with regex'''
scraped_data = scraped_data.replace({"Text2": r"^Anyone with any information"}, {"Text2": np.nan}, regex=True)
scraped_data = scraped_data.replace({"Text2": r"^Anyone with information"}, {"Text2": np.nan}, regex=True)
scraped_data = scraped_data.replace({"Text2": r"^Contact the incident room"}, {"Text2": np.nan}, regex=True)
scraped_data = scraped_data.replace({"Text2": r"^Read the full"}, {"Text2": np.nan}, regex=True)
scraped_data = scraped_data.replace({"Text2": r"^\*Unsolved as in no"}, {"Text2": np.nan}, regex=True)
scraped_data = scraped_data[~scraped_data.Text1.str.startswith("The following unsolved")]
scraped_data = scraped_data[~scraped_data.Text1.str.startswith("Cases are included as unsolved")]
scraped_data = scraped_data[~scraped_data.Text1.str.startswith("Other cases:")]
len(scraped_data.index)

'''Replace the cases we noticed where there is a duplicate of text1 in text2 fields.'''
for index, val in scraped_data.Text2.items():
    if val in scraped_data.Text1.values:
        scraped_data.loc[index, 'Text2'] = pd.NA

print(scraped_data)

'''Make a single variable with the unstructured texts'''
scraped_data["Text"] = scraped_data["Text1"] + ' ' + scraped_data["Text2"]
len(scraped_data.index)
scraped_data["Text"] = scraped_data["Text"].fillna(scraped_data["Text1"])

scraped_data.drop(['Text1', 'Text2'], axis=1, inplace=True)

'''Keeping a copy of the raw data - will be used in the next script'''
scraped_data["Raw_Text"] = scraped_data["Text"]
print(scraped_data.head())

'''Having a unique ID for the observations'''
scraped_data['counter'] = scraped_data.groupby('Year')['Year'].rank(method='first')
scraped_data['ID'] = scraped_data.Year.astype(str) + scraped_data.counter.astype(str)

'''Some preprocessing (make all lower case)'''
scraped_data['Text'] = scraped_data['Text'].str.lower()
print(scraped_data.head())

'''Some preprocessing (remove extra white spaces if any)'''


def remove_whitespace(text):
    return " ".join(text.split())


scraped_data['Text'] = scraped_data['Text'].apply(remove_whitespace)

'''Some preprocessing (Tokenize words)'''
scraped_data['Text'] = scraped_data['Text'].apply(lambda X: word_tokenize(X))
print(scraped_data.head())

'''Some preprocessing (Remove stopwords)'''
en_stopwords = stopwords.words('english')


def remove_stopwords(text):
    result = []
    for token in text:
        if token not in en_stopwords:
            result.append(token)

    return result


scraped_data['Text'] = scraped_data['Text'].apply(remove_stopwords)
print(scraped_data.head())


'''Some preprocessing (Remove punctuations)'''
def remove_punct(text):
    tokenizer = RegexpTokenizer(r"\w+")
    lst = tokenizer.tokenize(' '.join(text))
    return lst


scraped_data['Text'] = scraped_data['Text'].apply(remove_punct)


'''Some preprocessing (Remove frequent words check)'''
def frequent_words(df):
    lst = []
    for text in df.values:
        lst += text[0]
    fdist = FreqDist(lst)
    return fdist.most_common(10)


print(frequent_words(scraped_data['Text']))
# In this case no frequent words that really need to be deleted.

'''Lemmatization process of grouping together the different inflected forms of a word so they can be analyzed as a single item.'''
'''
def lemmatization(text):
    result = []
    wordnet = WordNetLemmatizer()
    for token, tag in pos_tag(text):
        pos = tag[0].lower()

        if pos not in ['a', 'r', 'n', 'v']:
            pos = 'n'

        result.append(wordnet.lemmatize(token, pos))

    return result


scraped_data['Text'] = scraped_data['Text'].apply(lemmatization)
print(scraped_data['Text'])
'''


'''Some preprocessing (Stemming - either lemmatization or stemming (we used stemming for this data, to reduce 
words to the core terms; like runner, ran, running to run.))'''
def stemming(text):
    porter = PorterStemmer()

    result = []
    for word in text:
        result.append(porter.stem(word))
    return result


scraped_data['Text'] = scraped_data['Text'].apply(stemming)
scraped_data.head()

'''Can be also removal of url or tags (not going in that for now)'''

'''Let's count common words'''

Counter(chain(*scraped_data['Text'])).most_common(10)

'''Let's save our data'''
outfile_name = "raw_data.csv"
completeName = os.path.join(dat_dir, outfile_name)

scraped_data.to_csv(completeName, index=False)

'''
Cleaning text for recognizing topics in a collection of documents, and then automatically classify 
any individual document within the collection in terms of how "relevant" it is to each of the discovered topics. 
A topic is considered to be a set of terms (i.e., individual words or phrases) that, taken together, suggest a shared theme:
'''

stop_words = set(stopwords.words('english'))
crime_stopwords = ['Crimestoppers', 'Contact', 'incident room']


def clean_text(input_string):
    words = nltk.word_tokenize(input_string)
    alpha_tokens = [word for word in words if word.isalpha()]
    tokens_lower = [token.lower() for token in alpha_tokens]
    tokens_no_stopwords = [token for token in tokens_lower if token not in stop_words and token not in crime_stopwords]
    clean_sentence = ' '.join(tokens_no_stopwords)
    return clean_sentence


scraped_data['clean_text'] = scraped_data.apply(lambda x: clean_text(x['Raw_Text']), axis=1)

print(scraped_data['Raw_Text'][0:5])
print(scraped_data['clean_text'][0:5])

'''Bag of words approach'''
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(max_features=10000)
tf = vectorizer.fit_transform(scraped_data['clean_text'])
df_bow = pd.DataFrame(tf.toarray(), columns=vectorizer.get_feature_names_out())

#df_bow['total_tokens'] = df_bow.sum(axis=1)
print(df_bow.head())

'''
Topic Modelling: unsupervised learning
'''
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation

tfidf = TfidfTransformer()
tfidf_sparse = tfidf.fit_transform(df_bow)
df_tfidf = pd.DataFrame(tfidf_sparse.toarray(), columns=tfidf.get_feature_names_out())
print(df_tfidf)
'''Choosing 5 topics arbitrarily'''
lda = LatentDirichletAllocation(
    n_components=5,
    max_iter=5,
    learning_method="online",
    learning_offset=50.0,
    random_state=520,
)
lda.fit(tf)

tf_feature_names = vectorizer.get_feature_names_out()

'''Plotting top words'''
import matplotlib.pyplot as plt
import numpy as np


def plot_top_words(model, feature_names, n_top_words, title):
    fig, axes = plt.subplots(1, 5, figsize=(10, 5))
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[: -n_top_words - 1: -1]
        top_features = [feature_names[i] for i in top_features_ind]
        raw_weights = topic[top_features_ind]
        weights = raw_weights / np.mean(raw_weights)

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx}", fontdict={"fontsize": 15})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=10)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=0)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.show()


plot_top_words(lda, tf_feature_names, 10, "Topics in LDA model")

sys.exit(0)
