import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import statsmodels.api as sm


PRESTIGE = sm.datasets.get_rdataset("Duncan", "car", cache=True).data
CREDIT_CARD = sm.datasets.ccard.load_pandas().data
CREDIT_CARD.columns


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
    y_hat = est.predict(X)

    ax_list[0].axhline(0, linestyle='--')
    ax_list[0].scatter(y_hat, residuals, alpha=.2)
    ax_list[0].set_xlabel(dependent_name)
    ax_list[0].set_ylabel('student residuals')
    sm.qqplot(residuals, ax=ax_list[1], line='s')

    plt.tight_layout()


# PRESTIGE.info()
# CREDIT_CARD.info()
exp_plots(PRESTIGE)
exp_plots(CREDIT_CARD)
compute_reg_and_plt(PRESTIGE, ['education', 'income'], 'prestige')
compute_reg_and_plt(CREDIT_CARD, ['AGE', 'INCOME', 'INCOMESQ', 'OWNRENT'], 'AVGEXP')

# Now take log of AVGEXP
log_credit_card = CREDIT_CARD.copy()
log_credit_card['LOGAVGEXP'] = np.log(log_credit_card['AVGEXP'])
compute_reg_and_plt(log_credit_card, ['AGE', 'INCOME', 'INCOMESQ', 'OWNRENT'], 'LOGAVGEXP')
plt.show()
