from sklearn.datasets import make_classification
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

X, y = make_classification(n_samples=100,
                            n_features=2,
                            n_informative=2,
                            n_redundant=0,
                            n_classes=2,
                            random_state=0)


data = np.column_stack((X, y))
xdf = pd.DataFrame(data)
positives = xdf[xdf[2] == 1]
negatives = xdf[xdf[2] == 0]


plt.scatter(positives[0], positives[1], color='b')
plt.scatter(negatives[0], negatives[1], color='r')
plt.show()
#print X[:, 0]

# As if we are here
