from RandomForest import RandomForest
from sklearn.cross_validation import train_test_split
import numpy as np
import pandas as pd

df = pd.read_csv('data/playgolf.csv')
y = df.pop('Result').values
X = df.values
X_train, X_test, y_train, y_test = train_test_split(X, y)

rf = RandomForest(num_trees=10, num_features=4)
rf.fit(X_train, y_train)
y_predict = rf.predict(X_test)
print y_predict
print "score:", rf.score(X_test, y_test)
