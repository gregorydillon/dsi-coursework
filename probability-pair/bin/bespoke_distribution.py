import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
import pylab as pl
from scipy.stats import linregress, spearmanr, pearsonr
from scipy.stats.kde import gaussian_kde
from scipy.stats import norm

import probability.lib.plot as plot

"""
Profit = Number of views * Conversion * (Wholesale_Proportion * 50 + (1-Wholesale_Proportion)*60)

Assumptions:

    Number of views is a uniform distribution over the range of 5000 and 6000
    Conversion is a binomial distribution where the probability of success is 0.12 for
    each sale among the Number of views made

    Profit per sale has 0.2 probability of taking the value 50 (for wholesale) and 0.8
    of taking the value 60 (non-wholesale) for each sale, so you should use a binomial
    to model the number of the total sales that happen at wholesale.

    Given the distributions of each of variables, use scipy to write a function that
    would draw random values from each of the distributions to simulate a distribution for profit

    Compute the range of values of profit where the middle 95% of the probability mass lies.
"""

def main():
    profit_data = sample_monthly_profit(100000)
    mean_profit = profit_data.mean().profit
    std_profit = profit_data.std().profit
    lower = mean_profit - (std_profit * 2)
    upper = mean_profit + (std_profit * 2)

    print "95% density range for profit: {}-{}".format(lower, upper)
    plot.plot_series_histo_fit(profit_data['profit'], 'g')


def sample_monthly_profit(samples):
    views = np.random.randint(5000, 6000, samples)
    conversions = np.random.binomial(views, 0.12, samples)
    num_wholesales = np.random.binomial(conversions, .2, samples)
    num_fullsales = conversions - num_wholesales
    profit = num_wholesales * 50 + num_fullsales * 60

    profit_data = pd.DataFrame({
        'views': views,
        'conversions': conversions,
        'num_wholesales': num_wholesales,
        'num_fullsales': num_fullsales,
        'profit': profit
    })

    return profit_data


if __name__ == '__main__':
    main()
