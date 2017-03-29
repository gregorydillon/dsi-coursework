import pandas as pd
import numpy as np
import math
from collections import Counter
from TreeNode import TreeNode


class DecisionTree(object):
    '''
    A decision tree class.
    '''

    def __init__(self, impurity_criterion='entropy'):
        '''
        Initialize an empty DecisionTree.
        '''

        self.root = None  # root Node
        self.feature_names = None  # string names of features (for interpreting
                                   # the tree)
        self.categorical = None  # Boolean array of whether variable is
                                 # categorical (or continuous)
        self.impurity_criterion = self._entropy \
                                  if impurity_criterion == 'entropy' \
                                  else self._gini

    def fit(self, X, y, feature_names=None):
        '''
        INPUT:
            - X: 2d numpy array
            - y: 1d numpy array
            - feature_names: numpy array of strings
        OUTPUT: None

        Build the decision tree.
        X is a 2 dimensional array with each column being a feature and each
        row a data point.
        y is a 1 dimensional array with each value being the corresponding
        label.
        feature_names is an optional list containing the names of each of the
        features.
        '''

        if feature_names is None or len(feature_names) != X.shape[1]:
            self.feature_names = np.arange(X.shape[1])
        else:
            self.feature_names = feature_names

        # Create True/False array of whether the variable is categorical
        is_categorical = lambda x: isinstance(x, str) or \
                                   isinstance(x, bool) or \
                                   isinstance(x, unicode)
        self.categorical = np.vectorize(is_categorical)(X[0])

        self.root = self._build_tree(X, y)

    def _build_tree(self, X, y):
        '''
        INPUT:
            - X: 2d numpy array
            - y: 1d numpy array
        OUTPUT:
            - TreeNode

        Recursively build the decision tree. Return the root node.
        '''

        node = TreeNode()
        index, value, splits = self._choose_split_index(X, y)

        if index is None or len(np.unique(y)) == 1:
            node.leaf = True
            node.classes = Counter(y)
            node.name = node.classes.most_common(1)[0][0]
        else:
            X1, y1, X2, y2 = splits
            node.column = index
            node.name = self.feature_names[index]
            node.value = value
            node.categorical = self.categorical[index]
            node.left = self._build_tree(X1, y1)
            node.right = self._build_tree(X2, y2)
        return node

    def _entropy(self, y):
        '''
        INPUT:
            - y: 1d numpy array
        OUTPUT:
            - float

        Return the entropy of the array y.
        '''
        all_vals, all_counts = np.unique(y, return_counts=True)
        term_sum = 0
        for val, count in zip(all_vals, all_counts):
            p = float(count) / len(y)
            term_sum += p * np.log2(p)

        entropy = -1 * term_sum

        return entropy

    def _gini(self, y):
        '''
        INPUT:
            - y: 1d numpy array
        OUTPUT:
            - float

        Return the gini impurity of the array y.
        '''
        all_vals, all_counts = np.unique(y, return_counts=True)
        term_sum = 0
        for val, count in zip(all_vals, all_counts):
            p = float(count) / len(y)
            term_sum += p ** 2

        return 1 - term_sum



    def _make_split(self, X, y, split_index, split_value):
        '''
        INPUT:
            - X: 2d numpy array
            - y: 1d numpy array
            - split_index: int (index of feature)
            - split_value: int/float/bool/str (value of feature)
        OUTPUT:
            - X1: 2d numpy array (feature matrix for subset 1)
            - y1: 1d numpy array (labels for subset 1)
            - X2: 2d numpy array (feature matrix for subset 2)
            - y2: 1d numpy array (labels for subset 2)

        Return the two subsets of the dataset achieved by the given feature and
        value to split on.

        Call the method like this:
        >>> X1, y1, X2, y2 = self._make_split(X, y, split_index, split_value)

        X1, y1 is a subset of the data.
        X2, y2 is the other subset of the data.
        '''

        ### YOUR CODE HERE
        feature_is_categorical = self.categorical[split_index]
        if feature_is_categorical:
            in_mask = X[:,split_index] == split_value
            not_in_mask = X[:,split_index] != split_value
        else:
            in_mask = X[:,split_index] < split_value
            not_in_mask = X[:,split_index] >= split_value

        x1 = X[in_mask]
        y1 = y[in_mask]

        x2 = X[not_in_mask]
        y2 = y[not_in_mask]


        return x1, y1, x2, y2

    def _information_gain(self, y, y1, y2):
        '''
        INPUT:
            - y: 1d numpy array
            - y1: 1d numpy array (labels for subset 1)
            - y2: 1d numpy array (labels for subset 2)
        OUTPUT:
            - float

        Return the information gain of making the given split.

        Use self.impurity_criterion(y) rather than calling _entropy or _gini
        directly.
        '''

        h_of_s = self.impurity_criterion(y)
        y1_term = (float(len(y1)) / len(y)) * self.impurity_criterion(y1)
        y2_term = (float(len(y2)) / len(y)) * self.impurity_criterion(y2)

        return h_of_s - (y1_term + y2_term)

    def _choose_split_index(self, X, y):
        '''
        INPUT:
            - X: 2d numpy array
            - y: 1d numpy array
        OUTPUT:
            - index: int (index of feature)
            - value: int/float/bool/str (value of feature)
            - splits: (2d array, 1d array, 2d array, 1d array)

        Determine which feature and value to split on. Return the index and
        value of the optimal split along with the split of the dataset.

        Return None, None, None if there is no split which improves information
        gain.

        Call the method like this:
        >>> index, value, splits = self._choose_split_index(X, y)
        >>> X1, y1, X2, y2 = splits
        '''
        max_split_choice = None
        for i, column in enumerate(X.T):
            vals_to_try = np.unique(column)
            feature_is_categorical = self.categorical[i]

            for split_val in vals_to_try:
                if feature_is_categorical:
                    in_mask = (column == split_val)
                else:
                    in_mask = column < split_val

                out_mask = ~in_mask
                y1 = y[in_mask]
                y2 = y[out_mask]

                print feature_is_categorical, y1, y2, type(y)
                gain = self._information_gain(y, y1, y2)
                if max_split_choice == None or gain > max_split_choice[0]:
                    max_split_choice = (gain, i, split_val)


        # Now max_split_choice has the gain, col_index, and split_val
        split_index = max_split_choice[1]
        split_value = max_split_choice[2]

        splits = self._make_split(X, y, split_index, split_value)

        return split_index, split_value, splits

    def predict(self, X):
        '''
        INPUT:
            - X: 2d numpy array
        OUTPUT:
            - y: 1d numpy array

        Return an array of predictions for the feature matrix X.
        '''

        return np.array([self.root.predict_one(row) for row in X])

    def __str__(self):
        '''
        Return string representation of the Decision Tree.
        '''
        return str(self.root)
