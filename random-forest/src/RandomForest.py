import numpy as np
from collections import Counter

from DecisionTree import DecisionTree


class RandomForest(object):
    '''A Random Forest class'''

    def __init__(self, num_trees, num_features):
        '''
           num_trees:  number of trees to create in the forest:
        num_features:  the number of features to consider when choosing the
                           best split for each node of the decision trees
        '''
        self.num_trees = num_trees
        self.num_features = num_features
        self.forest = None

    def fit(self, X, y):
        '''
        X:  two dimensional numpy array representing feature matrix
                for test data
        y:  numpy array representing labels for test data
        '''
        self.forest = self.build_forest(X, y, self.num_trees, X.shape[0], \
                                        self.num_features)

    def build_forest(self, X, y, num_trees, num_samples, num_features):
        '''
        Return a list of num_trees DecisionTrees.
        '''
        """Repeat num_trees times:
        Create a random sample of the data with replacement
        Build a decision tree with that sample
        Return the list of the decision trees created"""

        forest = []
        valid_index_choices = range(len(X))
        for _ in range(num_trees):
            sample_indicies = np.random.choice(valid_index_choices, num_samples)
            sub_X = X[sample_indicies]
            sub_y = y[sample_indicies]
            tree = DecisionTree(impurity_criterion='entropy', num_features=num_features)
            tree.fit(sub_X, sub_y)
            forest.append(tree)

        return forest

    def predict(self, X):
        '''
        Return a numpy array of the labels predicted for the given test data.
        '''
        y_hats = None
        for tree in self.forest:
            y_hat = tree.predict(X)
            if y_hats is None:
                y_hats = y_hat
            else:
                y_hats = np.column_stack((y_hats, y_hat))

        predictions = []
        for row in y_hats:
            counts = Counter(row)
            value, count = counts.most_common(1)[0]
            predictions.append(value)

        return np.array(predictions)

    def score(self, X, y):
        '''
        Return the accuracy of the Random Forest for the given test data and
        labels.
        '''
        predictions = self.predict(X)
        correctness = y == predictions
