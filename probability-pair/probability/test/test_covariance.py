import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.getcwd())
import probability.covariance as cv

ADMISSIONS = pd.read_csv(os.getcwd() + "/data/admissions.csv")

def test_covariance():
    computed = cv.covariance(ADMISSIONS)
    pandas = ADMISSIONS.cov()
    for i, row in enumerate(computed):
        for j, value in enumerate(row):
            assert np.isclose(value, pandas.iloc[i].iloc[j]), "got {} expected {}".format(value, pandas.iloc[i].iloc[j])

def test_correlation():
    computed = cv.correlation(ADMISSIONS)
    pandas = ADMISSIONS.corr()

    for i, row in enumerate(computed):
        for j, value in enumerate(row):
            assert np.isclose(value, pandas.iloc[i].iloc[j]), "got {} expected {}".format(value, pandas.iloc[i].iloc[j])
