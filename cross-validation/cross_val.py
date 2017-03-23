from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.datasets import load_boston


def main():
    boston = load_boston()
    X = boston.data  # housing features
    y = boston.target  # housing prices

    # Split our data into training and test -- 1/3rd of our data is test data in this case
    # random_state is used for determinism
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=60)

    # Fit your model using the training set
    linear = LinearRegression()
    linear.fit(X_train, y_train)

    # Call predict to get the predicted values for training and test set
    train_predicted = linear.predict(X_train)
    test_predicted = linear.predict(X_test)

    # Calculate RMSE for training and test set
    print 'RMSE for training set ', rmse(y_train, train_predicted), np.sqrt(mean_squared_error(y_train, train_predicted))
    print 'RMSE for test set ', rmse(y_test, test_predicted), np.sqrt(mean_squared_error(y_test, test_predicted))

    print "Cross Validation Score: " + str(cross_validate(X, y, k=30))


def cross_validate(X, y, k=5):
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    fold_errors = []

    for train_index, validation_index in kf.split(X):
        train_data = X[train_index]
        train_answers = y[train_index]

        linear = LinearRegression()
        linear.fit(train_data, train_answers)

        validation_data = X[validation_index]
        validation_answers = y[validation_index]

        y_hat = linear.predict(validation_data)
        error = rmse(validation_answers, y_hat)
        fold_errors.append(error)

    return np.mean(fold_errors)


def rmse(true, predicted):
    return np.sqrt(np.mean((true - predicted) ** 2))


if __name__ == '__main__':
    main()
