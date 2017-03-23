from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error as mse
import numpy as np
import matplotlib.pyplot as plt

# Part 1
diabetes = load_diabetes()
X = diabetes.data[:50]
y = diabetes.target[:50]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#normalize data
Xn_train = preprocessing.scale(X_train)
Xn_test = preprocessing.scale(X_test)

ridge = Ridge(alpha=0.5)
ridge.fit(Xn_train, y_train)

train_predicted = ridge.predict(Xn_train)
test_predicted = ridge.predict(Xn_test)

train_mse = mse(y_train, train_predicted)
test_mse = mse(y_test, test_predicted)

# Part 2
Xn_data = preprocessing.scale(X_train)
k = X_train.shape[1]
alphas = np.logspace(-5, 0)
params = np.zeros((len(alphas), k))
ridge_errors = np.zeros((len(alphas), 1))
ridge_errorst = np.zeros((len(alphas), 1))

for i,a in enumerate(alphas):
    fit = Ridge(alpha=a, normalize=True, random_state=3).fit(Xn_data, y_train)
    params[i] = fit.coef_
    train_predicted = fit.predict(Xn_data)
    train_rmse = np.sqrt(mse(y_train, train_predicted))
    ridge_errors[i] = train_rmse

    Xnt_data = preprocessing.scale(X_test)
    fit2 = Ridge(alpha=a, normalize=True).fit(Xnt_data, y_test)
    test_predicted = fit2.predict(Xnt_data)
    test_rmse = np.sqrt(mse(y_test, test_predicted))
    ridge_errorst[i] = test_rmse

    # plt.plot(np.linspace(np.min(Xn_data[0]), np.max(Xn_data[0]), len(train_predicted)), train_predicted, label=str(a))

# plt.scatter(np.linspace(np.min(Xn_data[0]), np.max(Xn_data[0]), len(train_predicted)), y_train, alpha=.2)
# plt.legend()
# plt.show()

plt.plot(alphas, ridge_errors, label='train data')
plt.plot(alphas, ridge_errorst, label='test data')
plt.xlabel('lambda')
plt.ylabel('RMSE')
plt.xscale('log')
plt.legend()
plt.show()

####### LASSO #########
alphas = np.linspace(0.00001, 3)
lasso_errors = np.zeros((len(alphas), 1))
lasso_errorst = np.zeros((len(alphas), 1))
for i,a in enumerate(alphas):
    fit = Lasso(alpha=a, normalize=True, random_state=3).fit(Xn_data, y_train)
    train_predicted = fit.predict(Xn_data)
    train_rmse = np.sqrt(mse(y_train, train_predicted))
    lasso_errors[i] = train_rmse

    Xnt_data = preprocessing.scale(X_test)
    fit2 = Lasso(alpha=a, normalize=True).fit(Xnt_data, y_test)
    test_predicted = fit2.predict(Xnt_data)
    test_rmse = np.sqrt(mse(y_test, test_predicted))
    lasso_errorst[i] = test_rmse

    # plt.plot(np.linspace(np.min(Xn_data[0]), np.max(Xn_data[0]), len(train_predicted)), train_predicted, label=str(a))

# plt.scatter(np.linspace(np.min(Xn_data[0]), np.max(Xn_data[0]), len(train_predicted)), y_train, alpha=.2)
# plt.legend()
# plt.show()

plt.plot(alphas, lasso_errors, label='train data')
plt.plot(alphas, lasso_errorst, label='test data')
plt.xlabel('lambda')
plt.ylabel('RMSE')
plt.legend()
plt.show()

### OLS ###
lin_errors = np.zeros((len(alphas), 1))
lin_errorst = np.zeros((len(alphas), 1))
for i,a in enumerate(alphas):
    fit = LinearRegression().fit(X_train, y_train)
    train_predicted = fit.predict(X_train)
    train_rmse = np.sqrt(mse(y_train, train_predicted))
    lin_errors[i] = train_rmse

    fit2 = LinearRegression().fit(X_test, y_test)
    test_predicted = fit2.predict(X_test)
    test_rmse = np.sqrt(mse(y_test, test_predicted))
    lin_errorst[i] = test_rmse

    # plt.plot(np.linspace(np.min(Xn_data[0]), np.max(Xn_data[0]), len(train_predicted)), train_predicted, label=str(a))

# plt.scatter(np.linspace(np.min(Xn_data[0]), np.max(Xn_data[0]), len(train_predicted)), y_train, alpha=.2)
# plt.legend()
# plt.show()

plt.plot(alphas, lin_errors, label='train data')
plt.plot(alphas, lin_errorst, label='test data')
plt.xlabel('lambda')
plt.ylabel('RMSE')
plt.legend()
plt.show()

# for param in params.T:
#     plt.plot(alphas, param)
# plt.xlabel('lambda')
# plt.ylabel('standardized coefficients')
# plt.show()

# Part 3
