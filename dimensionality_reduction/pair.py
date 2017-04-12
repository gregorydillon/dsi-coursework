import pandas as pd
import numpy as np
from numpy.linalg import svd
import matplotlib.pyplot as plt

reviews = pd.read_csv('data/book_reviews.csv')
reviews['unknown_field'] = reviews.pop('Unnamed: 0')
user_book_matrix = reviews.pivot(index='User-ID', columns='ISBN', values='Book-Rating')
user_book_matrix = user_book_matrix.fillna(value=-1)

U, S, V = svd(user_book_matrix)
plt.plot(np.arange(len(S)), S) # Plot suggests elbow at ~10-20 features
plt.yscale('log')

cum_sum = np.cumsum(S ** 2)
plt.plot(np.arange(len(cum_sum)), cum_sum) # total power
plt.axhline(.9 * cum_sum[-1]) # 90% of total power line
# The intersection of the above two is at ~440 (value for S values to maintain)
# meaning we need to keep 440 vectors to maintain 90% of the power


meta_data = pd.read_csv('data/book_meta.csv', sep=";", error_bad_lines=False)

# Map names to isbn
for row in meta_data.iterrows():
    row = row[1]
    book_names_by_isbn[row['ISBN']] = row['Book-Title']

for i in xrange(20):
    print "\n=======TOPIC BREAK======"
    top_ten = sorted(zip(V[i], book_names_in_order))[:10]
    nearset_zero = sorted(zip(np.abs(V[i]), book_names_in_order))[:10]
    bot_ten = sorted(zip(V[i], book_names_in_order), reverse=True)[:10]

    for value, name in top_ten:
        print value, name
    for value, name in nearset_zero:
        print value, name
    for value, name in bot_ten:
        print value, name
