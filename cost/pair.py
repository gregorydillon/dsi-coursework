import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression as LR
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.svm import SVC

df = pd.read_csv('churn.csv')

df=df.drop(["State","Area Code","Phone"],axis=1)

df["Churn"] = df["Churn?"] =="True."

df['Churn']=df['Churn'].astype(int)

df=df.drop(['Churn?'],axis=1)



df["Int'l Plan"] = (df["Int'l Plan"] =="yes").astype(int)
df["VMail Plan"] = (df["VMail Plan"] =="yes").astype(int)

#2

# cost_mat = np.array([[-155,-55],[-300,0]]).reshape(2,2)

def standard_confusion_matrix(y_true,y_predict):
    TP = np.sum((y_true ==y_predict) & (y_true == 1))
    FP = np.sum((y_true !=y_predict) & (y_true == 0))
    FN = np.sum((y_true !=y_predict) & (y_true == 1))
    TN = np.sum((y_true ==y_predict) & (y_true == 0))
    mat = np.array([[TP,FP],[FN,TN]]).reshape(2,2)
    return mat


def profit_curve(cost_benefit, predicted_probs, labels):
    # Add one synthetic datapoint to have a threshold of ALL NEGATIVES
    sorted_probs = np.append(predicted_probs, 1.0)
    sorted_probs = sorted(predicted_probs, reverse=True)

    costs = []
    for thresh in sorted_probs:
        cur_stage_labels = [1 if p > thresh else 0 for p in predicted_probs]
        confusion_mat = standard_confusion_matrix(np.array(labels), np.array(cur_stage_labels))
        # real_costs = np.multiply(cost_benefit, confusion_mat)
        real_costs = cost_benefit * confusion_mat
        total_cost = np.sum(real_costs) / float(len(labels))

        costs.append(total_cost)

    return np.array(costs)


def plot_profit(profits, thresholds, label):

    # percentages = np.arange(0, 100, 100. / len(profits))
    plt.plot(thresholds, profits, label=label)
    plt.title("Profit Curve")
    plt.xlabel("Percentage of test instances (decreasing by score)")
    plt.ylabel("Profit")
    plt.legend(loc='best')


def plot_profit_curve(model, cost_benefit, X_train, X_test, y_train, y_test):
    mod = model.fit(X_train,y_train)
    test_proba = model.predict_proba(X_test)[:,1]

    profits = profit_curve(cost_benefit, test_proba, y_test)
    percentages = np.arange(0, 100, 100. / len(profits))
    plot_profit(profits, percentages, model.__class__.__name__)


X=df.drop('Churn',axis=1)

y=df['Churn']

X_train, X_test, y_train, y_test = train_test_split(X,y)


cost_benefit = np.array([[6, -3], [0, 0]])
models = [RF(), LR(), GBC(), SVC(probability=True)]
for model in models:
    plot_profit_curve(model, cost_benefit, X_train, X_test, y_train, y_test)
plt.title("Profit Curves")
plt.xlabel("Percentage of test instances (decreasing by score)")
plt.ylabel("Profit")
plt.legend(loc='best')
plt.show()
