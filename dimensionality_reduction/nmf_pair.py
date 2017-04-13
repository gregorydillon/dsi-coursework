import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

articles = pd.read_pickle('data/articles.pkl')
article_texts = articles.content

vect = CountVectorizer(stop_words='english')
X = vect.fit_transform(article_texts)

vocab = vect.get_feature_names()

class NMF(object):

    def __init__(self, V, k, max_iter=10):
        self.V = V
        self.k = k
        self.max_iter = max_iter

        self.W = np.random.uniform(size = (V.shape[0], k), low=1, high=1000)
        self.H = np.random.uniform(size = (k, V.shape[1]), low=1, high=1000)

    def fit(self):
        dense_V = self.V.todense()
        for i in xrange(self.max_iter):
            print i
            # first hold W fixed...
            H, error, _, _ = np.linalg.lstsq(self.W, dense_V)
            H[H < 0] = 0
            self.H = H

            if np.sum(error) < 1:
                print "CONVERGED ITERATION: {}".format(i)
                break

            # Now hold H fixed
            W, error, _, _ = np.linalg.lstsq(self.H.T, dense_V.T)
            W[W < 0] = 0
            self.W = W.T

            if np.sum(error) < 1:
                print "CONVERGED ITERATION: {}".format(i)
                break

            print np.sum(error)

        return self.H, self.W


### Using Your NMF Function

#1 Write a method that uses W, H, and the document matrix (V) to calculate and return the mean-squared error (of V - WH).
def mse(V, H, W):
    abs_err_matrix = V - W.dot(H)
    return np.sum(np.square(abs_err_matrix))


nmf = NMF(X, 10)
H, W = nmf.fit()


#2 Using argsort on each topic in H, find the index values of the words most associated with that topic.
vocab_arr = np.array(vocab)
for latent_feature in H:
    latent_feature = latent_feature.tolist()[0]
    top_word_indicies = np.argsort(latent_feature)[-20:]
    print vocab_arr[top_word_indicies]


### Built-In NMF

#1 Use the scikit-learn NMF algorithm to compute the Non-Negative Matrix factorization of our documents. Explore what "topics" are returned.
from sklearn.decomposition import NMF

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

n_topics = 10
nmf = NMF(n_components=n_topics, random_state=1).fit(X)
n_top_words = 20
print_top_words(nmf, vocab, n_top_words)


#2 Run the code you wrote for the Using Your NMF Function section on the SKlearn classifier. How close is the output to what you found using your own NMF classifier?
'''
Remarkably close.
'''

#3 Can you add a title to each latent topic representing the words it contains?
'''
Yes..  (using scikit-learn list..)
0. top / news headlines
1. baseball
2. us political - healthcare bill
3. world news - US-Syria relations
4. us news - tragic
5. entertainment
 ...
'''

#4 Now that you have labeled the latent features with what topics they represent, explore strongest latent features for a few articles. Do these make sense given the article? You will have to go back to the raw data you read in to do this.
np.argmax(W[0])   # -> 6
article_texts[0]  # -> u'the original goal building model football .....etc
'''
looks good - the article is about football and so is our topic #6.
we confirmed the same for a few more examples.
'''

#5 How do the NYT sections compare to the topics from the unsupervised learning? What are the differences? Why do you think these differences exist?
'''
the topics are pretty similar to the NYT topics, however there are some differences.  specifically, the strongest topics (per the algorithm) can be pretty specific - such as US-Syria relations news.  This might not be good for business reasons, as maybe you want to fit news of this type into a more general category of World News.
'''
