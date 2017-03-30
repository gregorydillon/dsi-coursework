import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plot
from scipy.stats import poisson

rainfall_data = pd.read_csv('data/rainfall.csv')


def show_all_hist():
    s = [rainfall_data[col] for col in rainfall_data]
    plot.plot_multi_hist(s[1::])


def show_jan_his():
    rainfall_data = pd.read_csv('data/rainfall.csv')
    rainfall_data.Jan.hist()
    plt.show()


show_all_hist()
# Based on the histogram I chose poisson and gamma to model rainfal.
# The January data (and indeed several other months) has a positive skew
# Many months have a small second peak in the long right skew.
# I still plotted the normal distribution, just to see. Binomial is right out.
