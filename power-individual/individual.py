import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pylab as pl

# pl.ion()

# coke_data = np.loadtxt('data/coke_weights.txt')
coke_data = np.loadtxt('data/coke_weights_1000.txt')


def part_1():
    """
    My null hyp: Coke bottle, on average, do in fact weigh null_mean ounces.
    Alt Hyp: Coke bottles weight significantly more or less than null_mean oz (2 tailed


    In this case it seems like, we're actually hopeful that we can 'accept' the null
    hypothesis. The data we find might not prove significant, but it might show that
    our sampling distribution is signficant and centered on the null distribution.
    """

    """
    We know from the CLT that our sample means will be close to the true mean as
    we collect more samples. Our sample size (130) is fairly large -- we can easily
    sample from this data to create a sampling distribution which is normal (bootstrapping)
    which will give us fairly strong confidence bounds.
    """

    # We're creating a normal distribution to sample from, based on our experimental data
    mean = np.mean(coke_data)  # 20.519
    std = np.std(coke_data)    # .957
    std_er = std / np.sqrt(len(coke_data))

    null_mean = 20.4
    coke_null_dist = norm(null_mean, std_er)  # Assume our data is representative of true STD
    coke_exp_dist = norm(mean, std_er)

    plot_range = np.linspace(null_mean - (4 * std_er), null_mean + (4 * std_er))

    # Null with line at mean
    pl.plot(plot_range, coke_null_dist.pdf(plot_range), color='b', label="null hyp.")
    pl.axvline(null_mean, color='b', linestyle='--')

    # Experimental with line at mean
    pl.plot(plot_range, coke_exp_dist.pdf(plot_range), color='r', label="exp. distribution")
    pl.axvline(mean, color='r', linestyle='--')

    pl.xlabel('Bottle Weights')
    pl.xlim((null_mean - (5 * std_er), null_mean + (5 * std_er)))
    pl.legend()

    coke_exp_dist.interval(.95)  # (20.355235664241324, 20.684487217803888)

    """
    Our experimental data and distribution confidence interval includes the null hyp.
    In this case, we may want to fail to reject the null hyp (fail to prove that
    coke bottles do not weigh null_meanoz)

    A Type II error, false negative, would mean we "fail to reject that coke bottles
    weigh null_meanoz on average when in fact coke bottles weigh something else."
    """

    # computing power
    alpha = .025
    critical_value = coke_null_dist.ppf(1 - alpha)
    print critical_value

    pl.axvline(critical_value, color='y', alpha=.7, linestyle='--')

    power = coke_exp_dist.cdf(critical_value)
    power_lin_sp = np.linspace(critical_value, null_mean + (4 * std_er))
    pl.fill_between(power_lin_sp, coke_exp_dist.pdf(power_lin_sp))

    """
    Power ~= .41

    This means we are 41 % likely to find a false negative. The chance that we did not
    reject the null Hyp when in reality we should have. Our conf interval suggests that
    the null hyp is likely, but our study is underpowered -- we have reason to be skeptical
    of our findings.
    """
    print power
    pl.show()


def explore_power(null_mean, alpha):
    # We're creating a normal distribution to sample from, based on our experimental data
    mean = np.mean(coke_data)  # 20.519
    std = np.std(coke_data)    # .957
    std_er = std / np.sqrt(len(coke_data))

    # Distros
    coke_null_dist = norm(null_mean, std_er)  # Assume our data is representative of true STD
    coke_exp_dist = norm(mean, std_er)

    critical_value = coke_null_dist.ppf(1 - alpha)
    power = 1 - coke_exp_dist.cdf(critical_value)
    power_lin_sp = np.linspace(critical_value, null_mean + (4 * std_er))

    # PRINTING INTERESTING STUFF ###
    print """
    null mu: {}
    exp mu:  {}
    std:     {}
    std_er:  {}
    alpha:   {}
    power:   {}
    """.format(null_mean, mean, std, std_er, alpha, power)

    # Plotting Section
    plot_range = np.linspace(null_mean - (4 * std_er), null_mean + (4 * std_er))

    # Null with line at mean
    pl.plot(plot_range, coke_null_dist.pdf(plot_range), color='b', label="null hyp.")
    pl.axvline(null_mean, color='b', linestyle='--')

    # Experimental with line at mean
    pl.plot(plot_range, coke_exp_dist.pdf(plot_range), color='r', label="exp. distribution")
    pl.axvline(mean, color='r', linestyle='--')

    # Shade power
    pl.axvline(critical_value, color='y', alpha=.7, linestyle='--')
    pl.fill_between(power_lin_sp, coke_exp_dist.pdf(power_lin_sp))

    pl.xlim((null_mean - (5 * std_er), null_mean + (5 * std_er)))
    pl.xlabel('Bottle Weights')
    pl.legend()
    pl.show()


def compute_power(null_mean, alpha):
    # We're creating a normal distribution to sample from, based on our experimental data
    print null_mean
    mean = np.mean(coke_data)  # 20.519
    std = np.std(coke_data)    # .957
    std_er = std / np.sqrt(len(coke_data))

    # Distros
    coke_null_dist = norm(null_mean, std_er)  # Assume our data is representative of true STD
    coke_exp_dist = norm(mean, std_er)

    critical_value = coke_null_dist.ppf(1 - alpha)
    power = 1 - coke_exp_dist.cdf(critical_value)

    return power


def part_2():
    # explore_power(20.2, .05)
    """
    WOW, moving from 20.4 to 20.2 had a huge effect on power. We're now at .98 -- very powerful!
    """
    starting_mu = 20.519
    effect_range = np.linspace(0.0, 1.0)
    fx = compute_power(starting_mu - effect_range, .05)
    pl.plot(effect_range, fx)
    pl.show()

    """
    Std_Er decreases as sample size increase because the denominator in it's formula is the sqrt of the
    sample size. As sqrt(n) increase, of course s/sqrt(n) will increase.
    """


def exploring_alpha():
    # Increasing sample size resulted in a big increase in power. up to .82!

    # Increasing alpha increased power -- which makes intuitive sense
    # as we move alpha left (by increasing it) the space under our
    # experimental curve which is to the right of alpha of course increases
    a_range = np.linspace(0.1, .3)
    fx = compute_power(20.4, a_range)
    pl.plot(a_range, fx)
    pl.show()


if __name__ == '__main__':
    part_1()
    # exploring_alpha()
