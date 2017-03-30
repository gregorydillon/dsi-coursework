import numpy as np
import scipy.stats as scs
import matplotlib.pyplot as plt


def main():
    visits_a = np.loadtxt('data/siteA.txt')
    visits_b = np.loadtxt('data/siteB.txt')
    # plot_many_a_visits(visits_a)

    x = np.arange(0, 1.01, 0.01)
    a_conversions = visits_a.sum()
    a_n = len(visits_a)
    a_beta = scs.beta(a_conversions, a_n - a_conversions)

    b_conversions = visits_b.sum()
    b_n = len(visits_b)
    b_beta = scs.beta(b_conversions, b_n - b_conversions)

    # plot_with_fill(x, a_beta.pdf(x), "Site A")
    # plot_with_fill(x, b_beta.pdf(x), "Site B")

    sample_size = 10000
    sample_a = a_beta.rvs(size=sample_size)
    sample_b = b_beta.rvs(size=sample_size)

    def sum_if_b_greater(accum, a_and_b):
        a, b = a_and_b
        print a, b
        return accum + 1 if b > a else accum

    count_b_higher = reduce(
        lambda accum, b_greater: accum+1 if b_greater else accum,
        sample_a < sample_b, 0
    )

    # Probability that B > A
    print "Prob B > A: ", count_b_higher, count_b_higher / float(sample_size)

    # Credible Interval for A
    lower = a_beta.ppf(.025)
    upper = a_beta.ppf(.975)
    print (lower, upper)  # (0.050079164645113493, 0.084472853496219802)

    b_greater_by_2pct = sample_b > .02 + sample_a
    count_b_greater_by2pct = reduce(
        lambda accum, b_greater: accum+1 if b_greater else accum,
        b_greater_by_2pct, 0
    )

    print "Prob B > A + .02", count_b_greater_by2pct, count_b_greater_by2pct / float(sample_size)

    # Roughly normal shape
    plt.hist(sample_b - sample_a - .02, alpha=.5)
    plt.hist(sample_b - sample_a, alpha=.5)

    # If we're frequentists:
    '''
    Null hyp is that A performs better.
    Altr Hyp is that site B performs better.

    We'll calculate a t-score assuming independence of the two results
    '''
    t_score = scs.ttest_ind(visits_a, visits_b)  # ASSUME EQUAL VARIANCE
    print t_score  # Ttest_indResult(statistic=-2.6123179484177212, pvalue=0.0090773452572910415)
    # This result is saying to us that our effect_size is about 2.6 std deviations with p~=.01
    # Which concludes in the same direction that our baysean hypothesis did!
    # We could dig in deeper here, compute conf-intervals or plot these as
    # binomial distributions etc. But even under the more restrictive t-test we
    # confirmed our Bayesean results -- so lets stick with confirmation bias or whatever ;)

    # To answer 12, lets make a chart real quick.
    x = np.arange(1000, 1000000, 10)  # thousand to million clicks
    profit_a = lambda x: x * 1.00  # one dollar per click avg
    profit_b = lambda x: x * 1.05  # one dollar per click avg

    plt.xlabel('clicks')
    plt.plot(x, profit_b(x) - profit_a(x), label='($) Value of Switching')
    # You can see here, for example, the value of switching reaches $50,000 at around
    # one million clicks. Knowing how much the engineering is going to cost is HARD.
    # Knowing the tradeoffs before hand is tricky too...
    # We don't have evidence of a slam dunk here




def plot_many_a_visits(visits_a):
    x = np.arange(0, 1.01, 0.01)
    alpha = 1
    beta = 1
    prior_y = scs.beta(alpha, beta).pdf(x)
    plot_with_fill(x, prior_y, 'prior')

    # Plotting many beta's
    for n in [50, 100, 200, 400, len(visits_a)]:
        first_n = visits_a[:n]
        conversions = first_n.sum()
        postiror_y = scs.beta(conversions, n - conversions).pdf(x)
        label = str("Posterior after {}".format(n))
        plot_with_fill(x, postiror_y, label)


def plot_with_fill(x, y, label):
    lines = plt.plot(x, y, label=label, lw=2)
    plt.fill_between(x, 0, y, alpha=0.2, color=lines[0].get_c())
    plt.legend()

if __name__ == '__main__':
    main()
    plt.show()
