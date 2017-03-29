from heapq import nlargest
import numpy as np
from sklearn.datasets import make_classification

X, y = make_classification(n_features=4, n_redundant=0, n_informative=1,
                           n_clusters_per_class=1, class_sep=5, random_state=5)


def eucledian_distance(a, b):
    return np.linalg.norm(a-b)


class KNearestNeighbors(object):
    def __init__(self, k=3, distance_fn=eucledian_distance):
        self.k = k
        self.distance_fn = distance

    def fit(self, X, y):
        self.training_data = X
        self.training_answers = y

    def predict(self, input_datapoint):
        knn = []
        for training_point in self.training_data.iterrows():
            distance = self.distance_fn(training_point, input_datapoint)
            index = self.training_data.get_loc(training_point.name)
            knn.append(HeapqNode(distance, index))

        k_nearest = nlargest(self.k, knn)
        labels = {}
        for neighbor in k_nearest:
            label = self.training_answers[neighbor.index]
            if labels.get(label):
                labels[label] += 1
            else:
                labels[label] = 1

        return max(labels.iteritems(), key=operator.itemgetter(1))[0]


class HeapqNode(object):
    def __init__(self, distance, datapoint_index):
        self.distance = distance
        self.index = datapoint_index

    def __cmp__(self, other):
        return self.distance < other.distance


def knn(X, y, distance_function):
    knn = []
    for datapoint in X.iterrows:

        sort the distances in increasing order
        take the k items with the smallest distances to x
        return the majority class among these items
