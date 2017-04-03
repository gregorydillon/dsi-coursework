import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.base import clone
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier


class AdaBoostBinaryClassifier(object):
    '''
    INPUT:
    - n_estimator (int)
      * The number of estimators to use in boosting
      * Default: 50

    - learning_rate (float)
      * Determines how fast the error would shrink
      * Lower learning rate means more accurate decision boundary,
        but slower to converge
      * Default: 1
    '''

    def __init__(self,
                 n_estimator=50,
                 learning_rate=1):

        self.base_estimator = DecisionTreeClassifier(max_depth=1)
        self.n_estimator = n_estimator
        self.learning_rate = learning_rate

        # Will be filled-in in the fit() step
        self.estimators_ = []
        self.estimator_weight_ = np.zeros(self.n_estimator, dtype=np.float)

    def fit(self, x, y):
        '''
        INPUT:
        - x: 2d numpy array, feature matrix
        - y: numpy array, labels

        Build the estimators for the AdaBoost estimator.
        '''
        sample_weight = np.full(len(x), (1.0/(len(x))))
        for i in xrange(self.n_estimator):
            est, swt, ewt = self._boost(x,y, sample_weight)
            self.estimators_.append(est)
            self.estimator_weight_[i] = ewt
            sample_weight = swt

    def _boost(self, x, y, sample_weight):
        '''
        INPUT:
        - x: 2d numpy array, feature matrix
        - y: numpy array, labels
        - sample_weight: numpy array

        OUTPUT:
        - estimator: DecisionTreeClassifier
        - sample_weight: numpy array (updated weights)
        - estimator_weight: float (weight of estimator)

        Go through one iteration of the AdaBoost algorithm. Build one estimator.
        '''

        estimator = clone(self.base_estimator)

        ### YOUR CODE HERE ###
        estimator.fit(x, y, sample_weight=sample_weight)
        predictions = estimator.predict(x)
        indications = predictions != y
        indications = indications.astype(int)

        weighted_accuracy = np.sum(sample_weight * indications)
        weight_sum = np.sum(sample_weight)
        error = weighted_accuracy / weight_sum

        alpha = np.log((1 - error) / error)
        new_weights = sample_weight * np.exp(alpha * indications)

        return estimator, new_weights, alpha


    def predict(self, x):
        '''
        INPUT:
        - x: 2d numpy array, feature matrix

        OUTPUT:
        - labels: numpy array of predictions (0 or 1)
        '''

        sums = np.zeros(len(x))
        for estimator, alpha in zip(self.estimators_, self.estimator_weight_):
            predictions = estimator.predict(x)
            sums += alpha * ((predictions - 1) + predictions)  # Map 0 to -1 and 1 to 1

        return (sums > 0).astype(int)

    def score(self, x, y):
        '''
        INPUT:
        - x: 2d numpy array, feature matrix
        - y: numpy array, labels

        OUTPUT:
        - score: float (accuracy score between 0 and 1)
        '''
        y_hat = self.predict(x)
        prediction_correctness = y_hat == y
        score = float(np.sum(prediction_correctness)) / len(prediction_correctness)
        return score


if __name__=='__main__':
   data = np.genfromtxt('../data/spam.csv', delimiter=',')

   y = data[:, -1]
   x = data[:, 0:-1]

   train_x, test_x, train_y, test_y = train_test_split(x, y)

   my_ada = AdaBoostBinaryClassifier(n_estimator=50)
   my_ada.fit(train_x, train_y)

   their_ada = AdaBoostClassifier(n_estimators = 50)
   their_ada.fit(train_x, train_y)

   print "Our Accuracy:", my_ada.score(test_x, test_y)
   print "SKlearn Accuracy", their_ada.score(test_x, test_y)
