import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from roc import plot_roc

df = pd.read_csv('../data/churn.csv')

# drop state, area code, phone,
# convet int'l plan, vmail plan, churn to boolean

del df['State']
del df['Area Code']
del df['Phone']

df['Int\'l Plan'] = df['Int\'l Plan'] == 'yes'
df['VMail Plan'] = df['VMail Plan'] == 'yes'
df['Churn?'] = df['Churn?'] == 'True.'
y = df.pop('Churn?').values
X = df.values


def part_one():
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    eddy = RandomForestClassifier()
    eddy.fit(X_train,y_train)

    print "Mean accuracy score: ",eddy.score(X_test,y_test)
    y_pred = eddy.predict(X_test)
    print confusion_matrix(y_test,y_pred)


def part_two():
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    eddy = RandomForestClassifier(oob_score=True, n_estimators=100)
    eddy.fit(X_train,y_train)

    print "oob: {}".format(eddy.oob_score_)
    print "Mean accuracy score: ",eddy.score(X_test,y_test)
    y_pred = eddy.predict(X_test)
    print confusion_matrix(y_test,y_pred)
    print eddy.feature_importances_
    features_with_weights = zip(eddy.feature_importances_, df.columns)
    print "Sorted Feature Importance"
    for x in sorted(features_with_weights):
        print x
    return eddy


def plot_accuracy_for_trees():
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    accuracies = []
    # tree_cnts = [10, 50, 100, 1000, 5000]
    tree_cnts = [1, 2, 3, 10, 50, 100, 1000]
    for tree_cnt in tree_cnts:
        eddy = RandomForestClassifier(oob_score=True, n_estimators=tree_cnt)
        eddy.fit(X_train,y_train)
        accuracies.append(eddy.score(X_test,y_test))

    fig, ax = plt.subplots()
    width = .35
    plt.bar(np.array(range(len(accuracies))) + width, accuracies)
    ax.set_ylabel('accuracy')
    ax.set_title('number of trees')
    ax.set_xticks(np.array(range(len(accuracies))) + width / 2)
    ax.set_xticklabels(tree_cnts)
    plt.show()

def plot_accuracy_for_features():
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    accuracies = []
    # tree_cnts = [10, 50, 100, 1000, 5000]
    num_features = range(1, len(df.columns) + 1)
    for feature_count in num_features:
        eddy = RandomForestClassifier(oob_score=True, n_estimators=10, max_features=feature_count)
        eddy.fit(X_train,y_train)
        accuracies.append(eddy.score(X_test,y_test))

    fig, ax = plt.subplots()
    width = .35
    plt.bar(np.array(range(len(accuracies))) + width, accuracies)
    ax.set_ylabel('accuracy')
    ax.set_title('number of features')
    ax.set_xticks(np.array(range(len(accuracies))) + width / 2)
    ax.set_xticklabels(num_features)
    plt.show()

def every_classifier():
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    rf = RandomForestClassifier()
    knn = KNeighborsClassifier()
    dt = DecisionTreeClassifier()
    log_reg = LogisticRegression()

    classifiers = [rf, knn, dt, log_reg]
    for clss in classifiers:
        clss.fit(X_train, y_train)
        score = clss.score(X_test,y_test)
        y_pred = clss.predict(X_test)
        # mat = confusion_matrix(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        print "{}: precision: {}, recall: {}, accuracy: {}".format(clss.__class__.__name__, precision, recall, score)

        if clss is RandomForestClassifier:
            plot_roc(X, y, clss.__class__, n_estimators=20)
        else:
            plot_roc(X, y, clss.__class__)

        plt.subplots()
        plt.title(clss.__class__.__name__)
        plt.show()

    # y_meds = [np.median(y_test) for y in y_test]
    y_meds = [False] * len(y_test)
    precision = precision_score(y_test, y_meds)
    recall = recall_score(y_test,y_meds)
    score = (np.sum(y_meds == y_test)) / float(len(y_test))
    print "{}: precision: {}, recall: {}, accuracy: {}".format('median ML algo', precision, recall, score)


def importance_deviation():
    X_train, X_test, y_train, y_test = train_test_split(X,y)
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    importances_matrix = [tree.feature_importances_ for tree in rf.estimators_]
    importances_matrix = np.array(importances_matrix).T
    # print importances_matrix.shape
    deviations = np.std(importances_matrix, axis=1)
    names = df.columns

    fig, ax = plt.subplots()
    width = .35
    plt.bar(np.array(range(len(deviations))) + width, rf.feature_importances_ + deviations, alpha=.2, color='b')
    plt.bar(np.array(range(len(deviations))) + width, rf.feature_importances_ - deviations, alpha=.3, color='b')
    plt.bar(np.array(range(len(deviations))) + width, rf.feature_importances_, alpha=.5, color='r')

    ax.set_ylabel('accuracy')
    ax.set_title('number of features')
    ax.set_xticks(np.array(range(len(deviations))) + width / 2)
    ax.set_xticklabels(names)
    plt.show()


importance_deviation()
