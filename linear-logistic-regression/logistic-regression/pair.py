import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def main():
    X, y = make_classification(n_features=2, n_redundant=0, n_informative=2,
                               n_clusters_per_class=2, n_samples=1000)
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)[:, 1]

    tpr, fpr, thresholds = roc_curve(probabilities, y_test)

    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate (1 - Specificity)")
    plt.ylabel("True Positive Rate (Sensitivity, Recall)")
    plt.title("ROC plot of fake data")
    plt.show()


def roc_curve(probabilities, labels):
    '''
    INPUT: numpy array, numpy array
    OUTPUT: list, list, list

    Take a numpy array of the predicted probabilities and a numpy array of the
    true labels.
    Return the True Positive Rates, False Positive Rates and Thresholds for the
    ROC curve.
    '''
    probs_w_labels = pd.DataFrame({
        'probability': probabilities,
        'label': labels
    })
    probs_w_labels = probs_w_labels.sort_values(by='probability')

    TPRs = []
    FPRs = []
    thresholds = []

    for index, row in probs_w_labels.iterrows():
        threshold = row['probability']
        probs_w_labels['classification'] = probs_w_labels['probability'] > threshold

        true_positives = len(probs_w_labels[(probs_w_labels['label'] == True) & (probs_w_labels['classification'] == True)])
        false_positives = len(probs_w_labels[(probs_w_labels['label'] == False) & (probs_w_labels['classification'] == True)])

        true_negatives = len(probs_w_labels[(probs_w_labels['label'] == False) & (probs_w_labels['classification'] == False)])
        false_negatives = len(probs_w_labels[(probs_w_labels['label'] == True) & (probs_w_labels['classification'] == False)])

        tpr = float(true_positives) / (true_positives + false_negatives)
        fpr = float(false_positives) / (false_positives + true_negatives)

        TPRs.append(tpr)
        FPRs.append(fpr)
        thresholds.append(threshold)

    return TPRs, FPRs, thresholds


"""
function ROC_curve(probabilities, labels):
    Sort instances by their prediction strength (the probabilities)
    For every instance in increasing order of probability:
        Set the threshold to be the probability
        Set everything above the threshold to the positive class
        Calculate the True Positive Rate (aka sensitivity or recall)
        Calculate the False Positive Rate (1 - specificity)
    Return three lists: TPRs, FPRs, thresholds
"""


if __name__ == '__main__':
    main()
