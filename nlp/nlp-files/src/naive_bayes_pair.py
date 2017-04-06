import numpy as np
from pymongo import MongoClient
from nltk.tokenize import word_tokenize, wordpunct_tokenize, RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from naive_bayes import NaiveBayes
import string

from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

# Why? Because: http://stackoverflow.com/questions/26570944/resource-utokenizers-punkt-english-pickle-not-found
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')


def load_data():
    client = MongoClient()
    db = client.nyt_dump
    coll = db.articles

    articles = coll.find({'$or': [{'section_name':'Sports'},
                                  {'section_name': 'Fashion & Style'}]})

    article_text_labels =  [(' '.join(article['content']), article['section_name'])
                     for article in articles]
    tokenizer = RegexpTokenizer(r'\w+')
    article_text = [tokenizer.tokenize(x[0].lower()) for x in article_text_labels]
    sections = [x[1] for x in article_text_labels]

    return article_text, sections

def load_data_rt():
    client = MongoClient()
    db = client.nyt_dump
    coll = db.articles
    articles = coll.find()
    tokenized_documents = []
    labels = []
    for a in articles:
        text_list = a['content']
        text = ' '.join(text_list).lower()
        text = ''.join([t for t in text if t not in string.punctuation])
        # str(text).translate(None,string.punctuation)
        label = a['section_name']
        # import pdb; pdb.set_trace()
        tokens = word_tokenize(text)
        tokenized_documents.append(tokens)
        labels.append(label)

    stop_words = stopwords.words('english')
    for i, document in enumerate(tokenized_documents):
        new_words = [word for word in document if word not in stop_words and word.isalpha()]
        tokenized_documents[i] = new_words

    return tokenized_documents, labels

def stemmalemma(all_docs):
    porter = PorterStemmer()
    snowball = SnowballStemmer('english')
    wordnet = WordNetLemmatizer()
    porter_docs = []
    snow_docs = []
    wordnet_docs = []
    for document in all_docs:
        port_stem = [porter.stem(word) for word in document]
        snow_stem = [snowball.stem(word) for word in document]
        wordnet_lemm = [wordnet.lemmatize(word) for word in document]

        porter_docs.append(port_stem)
        snow_docs.append(snow_stem)
        wordnet_docs.append(wordnet_lemm)

    stemmalems = {
        'porter': porter_docs,
        'snowball': snow_docs,
        'wordnet': wordnet_docs
    }

    return stemmalems

def generate_vocabulary(stemmed_documents):
    bag_of_words = set()
    for doc in stemmed_documents:
        bag_of_words.update(doc)

    vocabulary = list(bag_of_words)
    vocab_lookup = {}
    for i, word in enumerate(vocabulary):
        vocab_lookup[word] = i

    return vocabulary, vocab_lookup

def generate_matrix(stemmed_documents, vocabulary, vocab_lookup):

    # Making a matrix, rows are stemmed_documents columns are word counts
    # Parallel to our 'vocabulary'
    matrix = np.zeros((len(stemmed_documents), len(vocabulary)))
    for row_i, doc in enumerate(stemmed_documents):
        for word in doc:
            col_i = vocab_lookup[word]
            matrix[row_i][col_i] += 1

    return matrix

docs, labels = load_data_rt()
stemmed_and_lemmed = stemmalemma(docs)
stemmed_documents = stemmed_and_lemmed['porter']
vocabulary, vocab_lookup = generate_vocabulary(stemmed_documents)
matrix = generate_matrix(stemmed_documents, vocabulary, vocab_lookup)

document_frequencies = (matrix>0).sum(axis=0)
idf = np.log(len(stemmed_documents) / (document_frequencies + 1))
normalized_term_freq = matrix / np.linalg.norm(matrix, axis=0)

tf_idf = idf * normalized_term_freq
