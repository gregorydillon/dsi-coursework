import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import scipy.stats as spst

nyt_data = pd.read_csv('data/nyt1.csv')
nyt_data.info()

# We don't want to include users who have not had any impressions in our study
# Copy to avoid pandas warning -- we want to be absolutely sure we're not modifying
# our original dataset
nyt_filtered = nyt_data[nyt_data['Impressions'] != 0].copy()
nyt_filtered['CTR'] = nyt_filtered['Clicks'] / nyt_filtered['Impressions']


def plot_hists(series_a, series_b):
    fig, ax_list = plt.subplots(2)

    series_a.hist(color='r', normed=True, ax=ax_list[0])
    plt.tight_layout()
    series_b.hist(color='b', normed=True, ax=ax_list[1])
    plt.tight_layout()
    plt.show()

    t_score = spst.ttest_ind(series_a, series_b, equal_var=False)
    return t_score

def signed_in(data):
    '''
    Compare the groups signed in, or not. In this case we'll be comparing 2 groups. Our fixed
    group alpha is .05, our individual alpha is going to be .05/2 == .025.
    '''
    signed_in_df = data[data['Signed_In'] == 1].copy()['CTR']
    signed_out_df = data[data['Signed_In'] == 0].copy()['CTR']

    # There are some strange results that can be explained -- the signed out users
    # all appear to be the same age and gender (because we don't KNOW who they are)
    # In terms of CTR, our distributions LOOK quite similar in shape, but if you
    # look closely there are some interesting things, for example the 0 CTR column
    # for signed_in_df is ~9.3 and signed out is ~8.6. This may not seem like a lot,
    # but given that this is over several hundred thousand samples -- it's probably meaningful
    t_score = plot_hists(signed_in_df, signed_out_df)

    # This t_score + p_value confirms our suspicion of meaningfulness.
    # at -55 standard units, an a p=0.00 (SAY WHAT?!) we are very confident
    # that signed in users click through at a lower rate.
    print t_score


def male_female(data):
    signed_in = data[data['Signed_In'] == 1].copy()
    male = signed_in[signed_in['Gender'] == 1].copy()['CTR']
    female = signed_in[signed_in['Gender'] == 0].copy()['CTR']

    t_score = plot_hists(male, female)
    print t_score


# signed_in(nyt_filtered)
male_female(nyt_filtered)
