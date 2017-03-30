import numpy as np
from RandomForest import RandomForest
from DecisionTree import DecisionTree
from sklearn.model_selection import train_test_split
import pandas as pd


df = pd.read_csv('data/congressional_voting.csv')
y = df.pop('party').values

X = df.values

for t_cnt in [10, 100, 500, 5000]:
    for f_cnt in [2, 4, 8, 10, 14]:
        scores = []
        for trial in range(5):
            X_train, X_test, y_train, y_test = train_test_split(X, y)
            rf = RandomForest(num_trees=t_cnt, num_features=f_cnt)
            rf.fit(X_train, y_train)
            score = rf.score(X_test, y_test)
            scores.append(score)

        print "Trees: {}, Features: {}, Mean Score: {:.4f}".format(t_cnt, f_cnt, np.mean(scores))

single_tree = DecisionTree()
single_tree.fit(X_train, y_train)
print "Single Tree {}".format(single_tree.score(X_test, y_test))
