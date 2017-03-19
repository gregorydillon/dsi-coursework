import numpy as np
from bandits import Bandits
from banditstrategy import BanditStrategy


def report(name, bandit_strat, true_probs):
    print "\n======={}========".format(name)
    print("  Number of trials: ", bandit_strat.trials)
    print("  Number of wins: ", bandit_strat.wins)
    print("  Conversion rates: ", bandit_strat.wins / bandit_strat.trials)
    print("  A total of %d wins of %d trials." % \
        (bandit_strat.wins.sum(), bandit_strat.trials.sum()))

    regret_over_time = regret(true_probs, bandit_strat.choices)
    # TODO: plot regret



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


sample_size = 1000
win_rates = np.array([.01, .03, .06, .12])
strategies = [
    'max_mean',
    'random_choice',
    'epsilon_greedy',
    'softmax',
    'ucb1',
    'bayesian_bandit'
]

for strat_name in strategies:
    bandits = Bandits(win_rates)
    strat = BanditStrategy(bandits, strat_name)
    strat.sample_bandits(sample_size)
    report(strat_name, strat, win_rates)
