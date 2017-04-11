import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram

articles = pd.read_pickle('articles.pkl')

def hierarchical_section():
    content_subset = pd.DataFrame(columns = articles.columns)
    for section in articles.section_name.unique()[:4]:
        twenty_articles = articles[articles.section_name == section][:30]
        print section, len(twenty_articles)
        content_subset = content_subset.append(twenty_articles)

    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(content_subset.content)
    # dist_matrix = pdist(X)
    dist_matrix = pdist(X.todense()) # ??? maybe ???
    y = squareform(dist_matrix) # just for humans, the linkage accepts dist_matrix format
    cluster = linkage(dist_matrix)
    dendrogram(cluster, labels=content_subset.headline.values)
    plt.show()

def k_means_section():
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(articles[articles.section_name == 'Sports'].content)
    km = KMeans(n_clusters=3)
    km.fit(X)
    km.cluster_centers_

    index_to_word = {}
    for word, index in vectorizer.vocabulary_.iteritems():
        index_to_word[index] = word

    for centroid in km.cluster_centers_:
        index_and_word = enumerate(centroid)
        sorted_centroid = sorted(index_and_word, key=lambda x: x[1], reverse=True)
        print '\n=====CENTROID BREAK====='
        for i, tfidf in sorted_centroid[:10]:
            if tfidf > 0:
                print index_to_word[i], tfidf
