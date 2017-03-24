'''
* Fill each each function stub according to the docstring.
* To run the unit tests: Make sure you are in the root dir(assessment-3)
  Then run the tests with this command: "make test"
'''

from numpy.random import beta as beta_dist
import numpy as np
import scipy.stats as st
from sklearn.linear_model import LinearRegression
import pandas as pd
import random


# Probability

def roll_the_dice():
    '''
    INPUT: None
    OUTPUT: FLOAT

    Two unbiased dice are thrown once and the total score is observed. Use a
    simulation to find the estimated probability that the total score is even
    or greater than 7.
    '''
    simulated_rolls = 10000
    die_1_rolls = np.random.randint(1, 7, size=simulated_rolls)  # High is excluded.
    die_2_rolls = np.random.randint(1, 7, size=simulated_rolls)  # High is excluded.

    combined = die_1_rolls + die_2_rolls
    fit_criteria = 0
    for roll in combined:
        if roll > 7 or roll % 2 == 0:
            fit_criteria += 1

    return fit_criteria / float(simulated_rolls)

# A/B Testing


def calculate_clickthrough_prob(clicks_A, views_A, clicks_B, views_B):
    '''
    INPUT: INT, INT, INT, INT
    OUTPUT: FLOAT

    Calculate and return an estimated probability that SiteA performs better
    (has a higher click-through rate) than SiteB.

    Hint: Use Bayesian A/B Testing (multi-armed-bandit repo)
    '''
    # We're going to model CTR using a beta distribution b/c it's the conjugate
    # of the binomial distribution.
    a_beta = st.beta(clicks_A, views_A - clicks_A)  # a=successes, b=failures
    b_beta = st.beta(clicks_B, views_B - clicks_B)  # a=successes, b=failures

    # Now we're going to sample from these distributions to determine the probability
    # that our new site indeed outperforms our old site.
    sample_size = 10000
    sample_a = a_beta.rvs(size=sample_size)
    sample_b = b_beta.rvs(size=sample_size)

    # Now we're going to determine the number of times b out-performed a.
    count_a_higher = reduce(
        lambda accum, b_greater: accum+1 if b_greater else accum,
        sample_a > sample_b,  # passing a list with True/False comparing our samples
        0  # Starting value for the sum
    )

    # Sampling from our distributions should have told us how likely it is that
    # site a out-performed site b.
    return count_a_higher / float(sample_size)


# Statistics

def calculate_t_test(sample1, sample2, type_I_error_rate):
    '''
    INPUT: NUMPY ARRAY, NUMPY ARRAY
    OUTPUT: FLOAT, BOOLEAN

    You are asked to evaluate whether the two samples come from a population
    with the same population mean.
    Return a tuple containing the p-value for the pair of samples and True or
    False depending if the p-value is considered significant at the provided Type I Error Rate.
    '''
    t_stat = st.ttest_ind(sample1, sample2)
    p_score = t_stat[1]

    return p_score, p_score < type_I_error_rate


# Pandas and Numpy

def pandas_query(df):
    '''
    INPUT: DATAFRAME
    OUTPUT: DATAFRAME

    Given a DataFrame containing university data with these columns:
        name, address, Website, Type, Size

    Return the DataFrame containing the average size of the university for each
    type ordered by size in ascending order.
    '''
    return df.groupby(['Type']).mean().filter(['Size']).sort_values(by='Size')


def df_to_numpy(df, y_column):
    '''
    INPUT: DATAFRAME, STRING
    OUTPUT: 2 DIMENSIONAL NUMPY ARRAY, NUMPY ARRAY

    Make the column named y_column into a numpy array (y) and make the rest of
    the DataFrame into a 2 dimensional numpy array (X). Return (X, y).

    E.g.
                a  b  c
        df = 0  1  3  5
             1  2  4  6
        y_column = 'c'

        output: [[1, 3], [2, 4]],   [5, 6]
    '''
    y = np.array(df[y_column])
    del df[y_column]
    return df.as_matrix(), y


def only_positive(arr):
    '''
    INPUT: 2 DIMENSIONAL NUMPY ARRAY
    OUTPUT: 2 DIMENSIONAL NUMPY ARRAY

    Return a numpy array containing only the rows from arr where all the values
    are positive.

    E.g.  np.array([[1, -1, 2], [3, 4, 2], [-8, 4, -4]])
              ->  np.array([[3, 4, 2]])

    DO NOT use a for loop.
    '''
    return arr[np.all(arr > 0, axis=1)]


def add_column(arr, col):
    '''
    INPUT: 2 DIMENSIONAL NUMPY ARRAY, NUMPY ARRAY
    OUTPUT: 2 DIMENSIONAL NUMPY ARRAY

    Return a numpy array containing arr with col added as a final column. You
    can assume that the number of rows in arr is the same as the length of col.

    E.g.  [[1, 2], [3, 4]], [5, 6]  ->  [[1, 2, 5], [3, 4, 6]]
    '''
    # Not sure why this not working :(
    return np.column_stack((arr, col))


def size_of_multiply(A, B):
    '''
    INPUT: 2 DIMENSIONAL NUMPY ARRAY, 2 DIMENSIONAL NUMPY ARRAY
    OUTPUT: TUPLE

    If matrices A (dimensions m x n) and B (dimensions p x q) can be
    multiplied, return the shape of the result of multiplying them. Use the
    shape function. Do not actually multiply the matrices, just return the
    shape.

    If A and B cannot be multiplied, return None.
    '''
    if A.shape[1] != B.shape[0]:
        return None
    return A.shape[0], B.shape[1]


# Linear Regression

def linear_regression(X_train, y_train, X_test, y_test):
    '''
    INPUT: 2 DIMENSIONAL NUMPY ARRAY, NUMPY ARRAY
    OUTPUT: TUPLE OF FLOATS, FLOAT

    Use the sklearn LinearRegression to find the best fit line for X_train and
    y_train. Calculate the R^2 value for X_test and y_test.

    Return a tuple of the coefficients and the R^2 value. Should be in this form:
    (12.3, 9.5), 0.567
    '''
    model = LinearRegression()
    model.fit(X_train, y_train)

    test_score = model.score(X_test, y_test)
    return model.coef_, test_score


# SQL

def sql_query():
    '''
    INPUT: None
    OUTPUT: STRING

    sqlite> PRAGMA table_info(universities);
    0,name,string,0,,0
    1,address,string,0,,0
    2,url,string,0,,0
    3,type,string,0,,0
    4,size,int,0,,0

    Return a SQL query that gives the average size of each type of university
    in ascending order.
    Columns should be: type, avg_size
    '''
    # Your code should look like this:
    # return '''SELECT * FROM universities;'''
    return """
        select type, avg(size) as avg_size from universities group by type order by avg_size asc;
    """
