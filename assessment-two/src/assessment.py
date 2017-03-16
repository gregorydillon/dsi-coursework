## Fill each each function stub according to the docstring.
## To run the unit tests: Make sure you are in the root dir:assessment-2 Then run the tests with this command:
#  "make test"

import numpy as np
import pandas as pd


def max_lists(list1, list2):
    '''
    INPUT: list, list
    OUTPUT: list

    list1 and list2 have the same length. Return a list which contains the
    maximum element of each list for every index.
    '''
    return_list = []
    for idx, v1 in enumerate(list1):
        v2 = list2[idx]
        return_list.append(max(v1, v2))

    return return_list


def get_diagonal(mat):
    '''
    INPUT: 2 dimensional list
    OUTPUT: list

    Given a matrix encoded as a 2 dimensional python list, return a list
    containing all the values in the diagonal starting at the index 0, 0.

    E.g.
    mat = [[1, 2], [3, 4], [5, 6]]
    | 1  2 |
    | 3  4 |
    | 5  6 |
    get_diagonal(mat) => [1, 4]

    You may assume that the matrix is nonempty.
    '''
    # We can only loop over the smaller of height / width
    iteration_max = min(len(mat), len(mat[0]))
    diag = []
    for i in range(iteration_max):
        diag.append(mat[i][i])

    return diag


def merge_dictionaries(d1, d2):
    '''
    INPUT: dictionary, dictionary
    OUTPUT: dictionary

    Return a new dictionary which contains all the keys from d1 and d2 with
    their associated values. If a key is in both dictionaries, the value should
    be the sum of the two values.
    '''
    # Choosing to do 2 passes -- I think the code is actually a bit cleaner this way
    ret_dict = {}
    for key, value in d1.iteritems():
        ret_dict[key] = value

    for key, value in d2.iteritems():
        if ret_dict.get(key):
            ret_dict[key] += value
        else:
            ret_dict[key] = value

    return ret_dict



def make_char_dict(filename):
    '''
    INPUT: string
    OUTPUT: dictionary (string => list)

    Given a file containing rows of text, create a dictionary whose keys
    are single characters. The value associated with each key is a list of all
    the line numbers which start with that letter. The first line should have
    line number 1.  Characters which never are the first letter of a line do
    not need to be included in your dictionary.
    '''
    ret_dict = {}

    with open(filename) as f:
        line_number = 0
        for line in f:
            line_number += 1
            first_char = line[0]

            if ret_dict.get(first_char) == None:
                ret_dict[first_char] = [line_number]
            else:
                ret_dict[first_char].append(line_number)


    return ret_dict


### Pandas
# For each of these, you will be dealing with a DataFrame which contains median
# rental prices in the US by neighborhood. The DataFrame will have these
# columns:
# Neighborhood, City, State, med_2011, med_2014

def pandas_add_increase_column(df):
    '''
    INPUT: DataFrame
    OUTPUT: None

    Add a column to the DataFrame called 'Increase' which contains the
    amount that the median rent increased by from 2011 to 2014.
    '''
    df['Increase'] = df['med_2014'] - df['med_2011']


def pandas_only_given_state(df, state):
    '''
    INPUT: DataFrame, string
    OUTPUT: DataFrame

    Return a new pandas DataFrame which contains the entries for the given
    state. Only include these columns:
        Neighborhood, City, med_2011, med_2014
    '''
    return df.loc[df['State'] == state].filter(['Neighborhood', 'City', 'med_2011', 'med_2014'])


def pandas_max_rent(df):
    '''
    INPUT: DataFrame
    OUTPUT: DataFrame

    Return a new pandas DataFrame which contains every city and the highest
    median rent from that city for 2011 and 2014.

    Note that city names are not unique and you need to use the state as well
    so that Portland, ME and Portland, OR are recognized as different.

    Your DataFrame should contain these columns:
        City, State, med_2011, med_2014
    '''
    city_grouping = df.groupby(['City', 'State']).max().filter(['City', 'State', 'med_2011', 'med_2014'])
    return city_grouping

### SQL
# For each of these, your python function should return a string that is the
# SQL statement which answers the question.
# For example:
#    return '''SELECT * FROM rent;'''
# You may want to run "sqlite3 data/housing.sql" in the command line to test
# out your queries if the test is failing.
#
# There are two tables in the database with these columns:
# (this is the same data that you dealt with in the pandas questions)
#     rent: Neighborhood, City, State, med_2011, med_2014
#     buy:  Neighborhood, City, State, med_2011, med_2014
# The values in the date columns are integers corresponding to the price on
# that date.

def sql_count_neighborhoods():
    '''
    INPUT: None
    OUTPUT: string

    Return a SQL query that gives the number of neighborhoods in each city
    according to the rent table. Keep in mind that city names are not always
    unique unless you include the state as well, so your result should have
    these columns (though you do not need to name them): city, state, cnt
    '''
    return """
        SELECT city, state, count(1) as count
        from rent
        group by city, state
    """


def sql_highest_rent_increase():
    '''
    INPUT: None
    OUTPUT: string

    Return a SQL query that gives the 5 San Francisco neighborhoods with the
    highest rent increase.
    '''
    return """
        SELECT neighborhood
        from rent
        where city='San Francisco' and state='CA'
        group by city, state, neighborhood
        order by med_2014 - med_2011 desc
        limit 5
    """


def sql_rent_and_buy():
    '''
    INPUT: None
    OUTPUT: string

    Return a SQL query that gives the rent price and buying price for 2014 for
    all the neighborhoods in San Francisco.
    Your result should have these columns (though you do not need to name
    them): neighborhood, rent, buy
    '''
    return """
        SELECT rent.neighborhood, rent.med_2014, buy.med_2014
        from rent
        join buy on buy.neighborhood=rent.neighborhood
            and buy.city=rent.city and buy.state=rent.state
        where rent.city='San Francisco' and rent.state='CA'
    """
