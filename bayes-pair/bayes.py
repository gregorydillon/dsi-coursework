import matplotlib.pyplot as plt
import dice
import biased_coin
from coin import Coin

class Bayes(object):
    '''
    INPUT:
        prior (dict): key is the value (e.g. 4-sided die),
                      value is the probability

        likelihood_func (function):
                        INPUT: INT data--the value of the roll of a die
                               INT key--the maximum value of the die (ie pass
                                            4 to get the likelihood for a
                                            4-sided die)
    '''
    def __init__(self, prior, likelihood_func):
        self.prior = prior
        self.likelihood_func = likelihood_func

    def normalize(self):
        '''
        INPUT: None
        OUTPUT: None

        Makes the sum of the probabilities equal 1.
        '''
        n_const = sum(self.prior.values())
        self.prior = {sides: prior / n_const for sides, prior in self.prior.iteritems()}


    def update(self, data):
        '''
        INPUT:
            data (int or str): A single observation (data point)

        OUTPUT: None

        Conduct a bayesian update. Multiply the prior by the likelihood and
        make this the new prior.
        '''
        for die_sides, prior in self.prior.iteritems():
            self.prior[die_sides] *= self.likelihood_func(data, die_sides)
        self.normalize()


    def print_distribution(self):
        '''
        Print the current posterior probability.
        '''
        print self.prior

    def plot(self, color=None, title=None, label=None):
        '''
        Plot the current prior.
        '''
        plt.bar(self.prior.keys(), self.prior.values(), color='g', width=.01)

def dice_solution():
    b1 = Bayes(dice.prior_fair.copy(), dice.dice)
    b2 = Bayes(dice.prior_weight.copy(), dice.dice)

    # 2 we did this it works call update once!!! if below code works, you know.... we're good

    # 3
    roles = [8,2,1,2,5,8,2,4,3,7,6,5,1,6,2,5,8,8,5,3,4,2,4,3,8,8,7,8,8,8,5,5,1,3,8,7,8,5,2,5,1,4,1,2,1,3,1,3,1,5]

    for roll in roles:
        b1.update(roll)
        b2.update(roll)

    print "\nPart 3"
    b1.print_distribution()
    b2.print_distribution()

    # 4
    b3 = Bayes(dice.prior_fair.copy(), dice.dice)
    b4 = Bayes(dice.prior_fair.copy(), dice.dice)

    roll_set_1 = [1, 1, 1, 3, 1, 2]
    roll_set_2 = [10, 10, 10, 10, 8, 8]

    for set1, set2 in zip(roll_set_1, roll_set_2):
        b3.update(set1)
        b4.update(set2)

    print "\nPart 4"
    b3.print_distribution()
    b4.print_distribution()


def coin_solution():
    test_cases = [
        ['H'],
        ['T'],
        ['H', 'H'],
        ['T', 'H'],
        ['H', 'H', 'H'],
        ['T', 'H', 'T'],
        ['H', 'H', 'H', 'H'],
        ['T', 'H', 'T', 'H'],
        ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
    ]

    bayesian_dists = []
    for test_case in test_cases:
        b = Bayes(biased_coin.prior.copy(), biased_coin.likelihood)
        bayesian_dists.append(b)

        for flip in test_case:
            b.update(flip)

    # Now we have test_cases number of trained bayesian_dists
    # plt.subplots(1, 1, len(bayesian_dists))
    for i, b in enumerate(bayesian_dists):
        plt.subplot(3, 4, i+1)
        b.plot()
        plt.tight_layout()

    plt.show()

def coin_bonus():
    b = Bayes(biased_coin.prior.copy(), biased_coin.likelihood)
    for i in range(10000):
        my_coin=Coin()
        b.update(my_coin.flip())
        if i == 2:
            plt.subplot(2,3,1)
            b.plot()
        if i == 10:
            plt.subplot(2,3,2)
            b.plot()
        if i == 50:
            plt.subplot(2,3,3)
            b.plot()
        if i == 250:
            plt.subplot(2,3,4)
            b.plot()

        # WE REJECT YOUR ORDINAL NATURE
        if i == 9999:
            plt.subplot(2,3,5)
            b.plot()


    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    coin_bonus()
