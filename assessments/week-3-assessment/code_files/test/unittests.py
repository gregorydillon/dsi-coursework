'''Unit Tests for DS Assessment 3
To run the tests: go to the root directory, assessment-3
run `make test`
'''
from __future__ import division
import unittest as unittest
import numpy as np
import pandas as pd
import scipy.stats as st
import sqlite3 as sql
from src import assessment as a


def run_sql_query(command, db):
    '''to test sql commands'''
    if not command:
        return []
    con = sql.connect(db)
    c = con.cursor()
    data = c.execute(command)
    result = [d for d in data]
    con.close()
    return result


class TestAssessment3(unittest.TestCase):

    def test_roll_the_dice(self):
        result = a.roll_the_dice()
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 2 / 3, places=1)

    def test_calculate_clickthrough_prob(self):
        result = a.calculate_clickthrough_prob(450, 56000, 345, 49000)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 0.97, places=2)

    def test_calculate_t_test(self):
        data = np.genfromtxt('data/t_test.csv')
        results = a.calculate_t_test(data[:, 0], data[:, 1], 0.001)
        self.assertIsNotNone(results)
        self.assertTrue(len(results), 2)
        self.assertAlmostEqual(results[0], 0.00023790996, 10)
        self.assertTrue(results[1])

    def test_pandas_query(self):
        answer = [934.38, 1129.41, 2399.89, 3504.50, 6889.37, 11478.91]
        result = a.pandas_query(pd.read_csv('data/universities.csv'))
        if isinstance(result, pd.DataFrame):
            self.assertIn('Size', result.columns)
            series = result['Size']
        else:
            series = result
        self.assertIsInstance(series, pd.Series)
        lst = series.values.tolist()
        self.assertEqual(len(lst), 6)
        for x, y in zip(lst, answer):
            self.assertIsInstance(x, float)
            self.assertAlmostEqual(x, y, places=2)

    def test_df_to_numpy(self):
        df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8],
                           'c': [9, 10, 11, 12], 'd': [13, 14, 15, 16]})
        results = a.df_to_numpy(df, 'c')
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)
        X, y = results
        self.assertIsInstance(X, np.ndarray)
        self.assertIsInstance(y, np.ndarray)
        self.assertEqual(X.tolist(), [[1, 5, 13], [2, 6, 14], [3, 7, 15], [4, 8, 16]])
        self.assertEqual(y.tolist(), [9, 10, 11, 12])

    def test_only_positive(self):
        arr = np.array([[1, 2, 3], [4, -5, -6], [-7, 8, 9], [10, 11, 12]])
        result = a.only_positive(arr)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.tolist(), [[1, 2, 3], [10, 11, 12]])

    def test_add_column(self):
        arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        col = np.array([10, 11, 12])
        result = a.add_column(arr, col)
        answer = [[1, 2, 3, 10], [4, 5, 6, 11], [7, 8, 9, 12]]
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.tolist(), answer)

    def test_size_of_multiply(self):
        A = np.array([[1, 2]])
        B = np.array([[3, 4]])
        self.assertIsNone(a.size_of_multiply(A, B))
        A = np.array([[1, 2], [3, 4], [5, 6]])
        B = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
        self.assertEqual(a.size_of_multiply(A, B), (3, 4))
        self.assertIsNone(a.size_of_multiply(B, A))

    def test_linear_regression(self):
        df = pd.read_csv('data/lin_reg.csv')
        X = df[['A', 'B']].values
        y = df['C'].values
        X_train = X[:25]
        y_train = y[:25]
        X_test = X[25:]
        y_test = y[25:]
        results = a.linear_regression(X_train, y_train, X_test, y_test)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)
        coeffs, r2 = results
        self.assertAlmostEqual(r2, 0.773895, 6)
        self.assertAlmostEqual(coeffs[0], 13.815259, 6)
        self.assertAlmostEqual(coeffs[1], 85.435835, 6)

    def test_sql_query(self):
        result = run_sql_query(a.sql_query(), 'data/sqlite.db')
        self.assertEqual(len(result), 6)
        answer = [("4-year, primarily associate's, Private for-profit", 934.38),
                  ("4-year, primarily associate's, Private not-for-profit", 1129.41),
                  ("4-year, Private not-for-profit", 2326.93),
                  ("4-year, Private for-profit", 3319.40),
                  ("4-year, primarily associate's, Public", 6889.37),
                  ("4-year, Public", 11200.30)]
        for res, ans in zip(result, answer):
            self.assertEqual(len(res), 2)
            if type(res[1]) == int:
                type_index, size_index = 1, 0
            else:
                type_index, size_index = 0, 1
            self.assertEqual(res[type_index], ans[0])
            self.assertAlmostEqual(res[size_index], ans[1], 2)

if __name__ == '__main__':
    unittest.main()
