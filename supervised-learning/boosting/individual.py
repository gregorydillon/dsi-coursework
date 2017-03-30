from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np


def main():
    boston = load_boston()
    targets = boston.target  # House Prices
    housing_data_all = boston.data  # The other 13 features

    training_data, test_data, training_targets, test_targets = train_test_split(
        housing_data_all, targets,
        test_size=.2,
        random_state=1
    )

    regressors = instantiate_regressors()

    cross_v_scores(regressors, training_data, training_targets)
    plot_regressors_staged_error(regressors[1:], training_data, training_targets, test_data, test_targets)

    random_forest_grid = {
        'max_depth': [3, None],
        'max_features': ['sqrt', 'log2', None],
        'min_samples_split': [2, 4],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False],
        'n_estimators': [10, 20, 40],
        'random_state': [1]
    }

    grid_search(RandomForestRegressor(), random_forest_grid, training_data, training_targets)


def grid_search(model, feature_dict, train_x, train_y):
    rf_gridsearch = GridSearchCV(model,
                                 feature_dict,
                                 n_jobs=-1,
                                 verbose=True,
                                 scoring='neg_mean_squared_error')
    rf_gridsearch.fit(train_x, train_y)

    print "best parameters:", rf_gridsearch.best_params_

    best_rf_model = rf_gridsearch.best_estimator_
    return best_rf_model


def cross_v_scores(regressors, training_data, training_targets):
    for r in regressors:
        mse, r2 = cross_validate(r, training_data, training_targets)
        print("{} -- MSE: {}, R2: {}".format(r.__class__.__name__, mse, r2))


def plot_regressors_staged_error(regressors, training_data, training_targets, test_data, test_targets):
    for r in regressors:
        stage_score_plot(r, training_data, training_targets, test_data, test_targets)

    rf_mse, _ = cross_validate(regressors[0], training_data, training_targets)
    plt.axhline(np.mean(rf_mse), linestyle='--', label="Random Forest MSE", color='y')
    plt.xlabel("Iterations")
    plt.ylabel("MSE")
    plt.title("MSE Per Iteration")
    plt.legend()
    plt.show()

def instantiate_regressors():
    rf = RandomForestRegressor(
        n_estimators=100,
        n_jobs=-1,  # DANGER -- THIS WILL USE EVERY CORE YOU HAVE!
        random_state=1
    )

    gdbr_slow = GradientBoostingRegressor(
        learning_rate=0.1,
        loss='ls',
        n_estimators=100,
        random_state=1
    )

    gdbr_fast = GradientBoostingRegressor(
        learning_rate=1,
        loss='ls',
        n_estimators=100,
        random_state=1
    )

    abr = AdaBoostRegressor(
        DecisionTreeRegressor(),
        learning_rate=0.1,
        loss='linear',
        n_estimators=100,
        random_state=1
    )

    return rf, gdbr_slow, gdbr_fast, abr


def cross_validate(estimator, training_data, test_targets):
    mse = cross_val_score(estimator, X=training_data, y=test_targets, scoring='neg_mean_squared_error')
    r2 = cross_val_score(estimator, X=training_data, y=test_targets, scoring='r2')

    return (-1 * np.mean(mse), np.mean(r2))


def stage_score_plot(model, train_x, train_y, test_x, test_y):
    '''
    INPUT:
     model: GradientBoostingRegressor or AdaBoostRegressor
     train_x: 2d numpy array
     train_y: 1d numpy array
     test_x: 2d numpy array
     test_y: 1d numpy array

    Create a plot of the number of iterations vs the MSE for the model for
    both the training set and test set.
    '''
    model.fit(train_x, train_y)
    predictions_per_stage_train = model.staged_predict(train_x)
    predictions_per_stage_test = model.staged_predict(test_x)

    test_error_at_stage = []
    training_error_at_stage = []
    for train_y_hat, test_y_hat in zip(predictions_per_stage_train, predictions_per_stage_test):
        training_error_at_stage.append(mean_squared_error(train_y_hat, train_y))
        test_error_at_stage.append(mean_squared_error(test_y_hat, test_y))

    x_space = np.arange(0, len(training_error_at_stage))
    plt.plot(x_space, training_error_at_stage, label='{} training error'.format(model.__class__.__name__), linestyle='--')
    plt.plot(x_space, test_error_at_stage, label='{} testing error'.format(model.__class__.__name__), linestyle='-')


if __name__ == '__main__':
    main()
