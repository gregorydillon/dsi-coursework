import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import statsmodels.api as sm
import statsmodels.formula.api as smf

cars_df = pd.read_csv('http://www-bcf.usc.edu/~gareth/ISL/Auto.csv')


def exp_plots(data):
    fig, ax_list = plt.subplots()
    scatter_matrix(data, alpha=.2, figsize=(6, 6), diagonal='kde', ax=ax_list)
    plt.tight_layout()

    fig, ax_list = plt.subplots()
    data.boxplot()


def compute_reg_and_plt(data, indepent_list, dependent_name):
    X = data.filter(indepent_list)
    X = sm.add_constant(X)
    y = data[dependent_name]

    est = sm.OLS(y, X)
    est = est.fit()

    print est.summary()
    fig, ax_list = plt.subplots(1, 2)
    residuals = est.outlier_test()['student_resid']

    ax_list[0].axhline(0, linestyle='--')
    ax_list[0].scatter(y, residuals, alpha=.2)
    ax_list[0].set_xlabel(dependent_name)
    ax_list[0].set_ylabel('student residuals')
    sm.qqplot(residuals, ax=ax_list[1], line='s')

    plt.tight_layout()


def compute_reg_and_plt_frm(data, formula, dependent_name):
    est = smf.ols(data=data, formula=formula)
    est = est.fit()
    y = data[dependent_name]

    print est.summary()
    fig, ax_list = plt.subplots(1, 2)
    residuals = est.outlier_test()['student_resid']

    ax_list[0].axhline(0, linestyle='--')
    ax_list[0].scatter(y, residuals, alpha=.2)
    ax_list[0].set_xlabel(dependent_name)
    ax_list[0].set_ylabel('student residuals')
    sm.qqplot(residuals, ax=ax_list[1], line='s')

    plt.tight_layout()


# Cleaning up
cars_df = cars_df[ cars_df['horsepower'] != '?']
cars_df['horsepower'] = cars_df['horsepower'].astype(int)
cars_df['origin'] = cars_df['origin'].astype(str)
cars_df['year'] = cars_df['year'].astype(str)
cars_df['cylinders'] = cars_df['cylinders'].astype(str)
cars_df.info()
# exp_plots(cars_df)

# compute_reg_and_plt_frm(cars_df, 'mpg ~ origin + weight + year', 'mpg')
compute_reg_and_plt_frm(cars_df, 'mpg ~ origin + weight*acceleration + year*horsepower + cylinders', 'mpg')


plt.show()
