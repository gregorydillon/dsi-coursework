import numpy as np
import matplotlib.pylab as plt
from bandits import Bandits
from banditstrategy import BanditStrategy

def report(name, bandit_strat, true_probs, collector=None):
    print "\n======={}========".format(name)
    print("  Number of trials: ", bandit_strat.trials)
    print("  Number of wins: ", bandit_strat.wins)
    print("  Conversion rates: ", bandit_strat.wins / bandit_strat.trials)
    print("  A total of %d wins of %d trials." % \
        (bandit_strat.wins.sum(), bandit_strat.trials.sum()))

    regret_over_time = regret(true_probs, bandit_strat.choices)
    print "ultimate regret: {}".format(regret_over_time[-1])


def plot_all(bandit_strategy_dir, true_probs):
    plot_trials_per_machine(bandit_strategy_dir, true_probs)
    plt.tight_layout()
    plt.legend()

    plot_win_rate(bandit_strategy_dir, true_probs)
    plt.tight_layout()
    plt.legend()

    plt.show()


def plot_trials_per_machine(bandit_strategy_dir, true_probs):
    true_probs_as_strings = ["%.2f" % number for number in true_probs]
    fig, ax_list = plt.subplots(2,3)
    fig.suptitle("Trials Per Machine")

    for tup, ax in zip(bandit_strategy_dir.iteritems(), ax_list.flatten()):
        name, bs = tup
        # print name, len(bs.trials), true_probs_as_strings, plt
        ax.bar(range(len(true_probs)), bs.trials)
        ax.set_title(name)
        ax.set_xticklabels(true_probs_as_strings)


def plot_win_rate(bandit_strategy_dir, true_probs):
    true_probs_as_strings = ["%.2f" % number for number in true_probs]
    fig, ax_list = plt.subplots(2,3)
    fig.suptitle("Experimental Win Rates Per Machine")

    for tup, ax in zip(bandit_strategy_dir.iteritems(), ax_list.flatten()):
        name, bs = tup
        win_rate = bs.wins / bs.trials
        ax.bar(range(len(true_probs)), win_rate)
        ax.set_title(name)
        ax.set_xticklabels(true_probs_as_strings)


def plot_regret_over_time(bs, name, axes):
    pass



def regret(probabilities, choices):
    '''
    INPUT: array of floats (0 to 1), array of ints
    OUTPUT: array of floats

    Take an array of the true probabilities for each machine and an
    array of the indices of the machine played at each round.
    Return an array giving the total regret after each round.
    '''
    c = choices.astype(int)
    p_opt = np.max(probabilities)
    return np.cumsum(p_opt - probabilities[c])


sample_size = 100
win_rates = np.array([.01, .03, .05, .07, .09, .11])
# win_rates = np.array([.11, .09, .07, .05, .03, .01])

strategies = [
    # 'max_mean',
    # 'random_choice',
    # 'epsilon_greedy',
    'softmax',
    # 'ucb1',
    # 'bayesian_bandit'
]

strat_collector = {}

for strat_name in strategies:
    bandits = Bandits(win_rates)
    strat = BanditStrategy(bandits, strat_name)
    strat.sample_bandits(sample_size)

    # Collect and report
    strat_collector[strat_name] = strat
    report(strat_name, strat, win_rates)

plot_all(strat_collector, win_rates)
