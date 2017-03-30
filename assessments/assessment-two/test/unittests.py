'''
Unit tests for DSI Assessment 2.
Usage: from main assessment directory: make test
'''
import unittest as unittest
import numpy as np
import pandas as pd
import sqlite3 as sql
from src import assessment as a


def run_sql_query(command, db='data/housing.sql'):
    if not command:
        return []
    con = sql.connect(db)
    c = con.cursor()
    data = c.execute(command)
    return [d for d in data]
    con.close()


class TestAssessment2(unittest.TestCase):

    def test_max_lists(self):
        result = a.max_lists([5, 7, 2, 3, 6], [3, 9, 1, 2, 8])
        self.assertEqual(result, [5,9,2,3,8])


    def test_get_diagonal(self):
        result = a.get_diagonal([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
        self.assertEqual(result, [1, 6, 11])


    def test_merge_dictionaries(self):
        result = a.merge_dictionaries({"a": 1, "b": 5, "c": 1, "e": 8},
                                      {"b": 2, "c": 5, "d": 10, "f": 6})
        self.assertEqual(result, {"a": 1, "b": 7, "c": 6, "d": 10, "e": 8, "f": 6})


    def test_make_char_dict(self):
        result = a.make_char_dict('data/people.txt')
        self.assertEqual(result['j'], [2, 19, 20])
        self.assertEqual(result['g'], [3])


    def test_pandas_add_increase_column(self):
        df = pd.read_csv('data/rent.csv')
        a.pandas_add_increase_column(df)
        cols = ['Neighborhood', 'City', 'State', 'med_2011', 'med_2014', 'Increase']
        self.assertEqual(df.columns.tolist(), cols)
        answer = ['Green Run', 'Virginia Beach', 'VA', 1150.0, 1150.0, 0.0]
        self.assertEqual(df.loc[123].tolist(), answer)


    def test_pandas_only_given_state(self):
        df = a.pandas_only_given_state(pd.read_csv('data/rent.csv'), 'CA')
        cols = ['Neighborhood', 'City', 'med_2011', 'med_2014']
        self.assertEqual(df.columns.tolist(), cols)
        self.assertEqual(len(df), 762)
        self.assertEqual(len(df[df['City'] == 'San Francisco']), 62)


    def test_pandas_max_rent(self):
        df = a.pandas_max_rent(pd.read_csv('data/rent.csv')).reset_index()
        self.assertEqual(len(df), 177)
        cols = ['City', 'State', 'med_2011', 'med_2014']
        self.assertEqual(df.columns.tolist()[-4:], cols)
        sf_row = df[df['City'] == 'San Francisco']
        sf = (sf_row['med_2011'].tolist()[0], sf_row['med_2014'].tolist()[0])
        maine = df[df['State'] == 'ME']
        portland_row = maine[maine['City'] == 'Portland']
        portland = (portland_row['med_2011'].tolist()[0], portland_row['med_2014'].tolist()[0])
        self.assertEqual(sf, (3575., 4900.))
        self.assertEqual(portland, (1600., 1650.))


    def test_sql_count_neighborhoods(self):
        result = run_sql_query(a.sql_count_neighborhoods())
        self.assertEqual(len(result), 177)
        sf, portland = None, None
        for line in result:
            if line[0] == 'San Francisco':
                sf = int(line[2])
            elif line[0] == 'Portland' and line[1] == 'ME':
                portland = int(line[2])
        self.assertEqual(sf, 62)
        self.assertEqual(portland, 13)


    def test_sql_highest_rent_increase(self):
        result = run_sql_query(a.sql_highest_rent_increase())
        self.assertEqual(len(result), 5)
        answer = {'Duboce Triangle', 'North Beach', 'Lake', 'Alamo Square', 'Glen Park'}
        self.assertEqual(set(x[0] for x in result), answer)


    def test_sql_rent_and_buy(self):
        result = run_sql_query(a.sql_rent_and_buy())
        self.assertEqual(len(result), 25)
        mission = None
        marina = None
        for line in result:
            if line[0] == "Mission":
                mission = line[1:]
            elif line[0] == "Marina":
                marina = line[1:]
        self.assertEqual(mission, (3500, 654300))
        self.assertEqual(marina, (3950, 747300))


if __name__ == '__main__':
    unittest.main()
