import scipy.stats as scs
import numpy as np
import random


class BanditStrategy(object):
    '''
    Implements an online learning strategy to solve the Multi-Armed Bandit
      problem.

    Methods
    --------
    sample_bandits(n): sample and train on n pulls.

    Attributes
    -----------
    N : the cumulative number of samples
    choices : the historical choices as a (N,) array
    bb_score: the historical score as a (N,) array
    '''

    def __init__(self, bandits, choice_function, seed=None, **kwargs):
        '''
        Initializes the BanditStrategy given an instance of the Bandits class
          and a choice function.

        Parameters
        -----------
        bandits : a Bandits object with a .pull method
    	choice_function : str indicating the choice function or a custom
            choice fuction accepting a self argument (which gives access to
            all the BanditStrategy's attributes) which returns an int
            between 0 and n-1
            Accepted str inputs are 'max_mean', 'random_choice',
            'epsilon_greedy', 'softmax', 'ucb1', and 'bayesian_bandit'
        seed : int setting the random seed or None to not seed the random
            number generator
        Also supports passing keyword args which can be used in a
            particular choice function.  Namely 'epsilon_greedy' accepts
            epsilon=float and 'softmax' accepts tau=float
            e.g. strat = BanditStrategy(bandits, 'epsilon_greedy',
              epsilon=0.1)
        '''
        choice_dict = {'max_mean': self._max_mean,
                       'random_choice': self._random_choice,
                       'epsilon_greedy': self._epsilon_greedy,
                       'softmax': self._softmax,
                       'ucb1': self._ucb1,
                       'bayesian_bandit': self._bayesian_bandit}
        self.bandits = bandits
        n_bandits = len(self.bandits)
        self.wins = np.zeros(n_bandits)
        self.trials = np.zeros(n_bandits)
        self.N = 0
        self.choices = []
        self.score = []
        self.seed = seed
        self._kwargs = kwargs
        if isinstance(choice_function, str):
            if choice_function in choice_dict:
                self.choice_function = choice_dict[choice_function]
            else:
                raise ValueError("{0} not a valid choice function. Valid choices include {1}".format(choice_function, choice_dict.keys()))
        elif not hasattr(choice_function, '__call__'):
            raise ValueError("{0} is not a valid input. Must be str or callable function accepting self".format(choice_function))
        else:
            BanditStrategy.choice_function = choice_function

    def sample_bandits(self, n=1):
        ''' Simulate n rounds of running the bandit machine

        Parameters
        -----------
        n : int number of rounds
        '''
        score = np.zeros(n)
        choices = np.zeros(n)

        # seed the random number generators so you get the same results every
        # time.
        if self.seed:
            np.random.seed(self.seed)
            random.seed(self.seed)

        for k in range(n):
            #choose a bandit index according to the choice function
            choice = self.choice_function()

            #sample the chosen bandit
            result = self.bandits.pull(choice)

            #update priors and score
            self.wins[choice] += result
            self.trials[choice] += 1
            score[k] = result
            self.N += 1
            choices[k] = choice

        self.score = np.r_[self.score, score]
        self.choices = np.r_[self.choices, choices]

    def _max_mean(self):
        ''' Pick the bandit with the current best observed proportion of winning

        Returns
        --------
        int : index of the winning bandit
        '''
        # make sure to play each bandit at least once
        if self.trials.min() == 0:
            return np.argmin(self.trials)
        return np.argmax(self.wins / self.trials)

    def _random_choice(self):
        ''' Pick a bandit uniformly at random

        Returns
        --------
        int : index of the winning bandit
        '''
        return np.random.randint(0, len(self.wins))

    def _epsilon_greedy(self):
        '''
        Pick a bandit uniformly at random epsilon percent of the time.
        Otherwise pick the bandit with the best observed proportion of winning

        Returns
        --------
        int : index of the winning bandit
        '''
        # Set default value of epsilon if not provided in init
        epsilon = self._kwargs.get('epsilon', 0.1)
        explore = np.random.random() <= epsilon

        return self._random_choice() if explore else self._max_mean()

    def _softmax(self):
        ''' Pick a bandit according to the Boltzmann Distribution

        Returns
        --------
        int : index of the winning bandit
        '''
        # Set default value of tau if not provided in init
        tau = self._kwargs.get('tau', 0.01)

        # Compute the denominator
        win_rates = self.wins / self.trials
        win_rates = [0 if np.isnan(win_rate) else win_rate for win_rate in win_rates]  # TODO: better way to  do this?
        denom = reduce(lambda accum, win_rate: accum + (np.exp(win_rate / tau)), win_rates, 0)

        # Use that to compute the estimated values
        boltzman_estimates = [(np.exp(win_rate / tau)) / denom for win_rate in win_rates]

        return np.random.choice(len(self.wins), p=boltzman_estimates)

    def _ucb1(self):
        ''' Pick the bandit according to the UCB1 strategy

        Returns
        --------
        int : index of the winning bandit
        '''
        total_plays = np.sum(self.trials)
        win_rates = self.wins / self.trials
        win_rates = [0 if np.isnan(win_rate) else win_rate for win_rate in win_rates]  # TODO: better way to  do this?
        upper_conf_bounds = [
            win_rate + np.sqrt((2 * np.log(total_plays) / trials))
            for win_rate, trials in zip(win_rates, self.trials)
        ]

        return np.argmax(upper_conf_bounds)

    def _bayesian_bandit(self):
        '''
        Randomly sample from a beta distribution for each bandit and pick
        the one with the largest value

        Returns
        --------
        int : index of the winning bandit
        '''
        # THIS HACK COULD CHANGE THINGS -- using 1 when there is no data -- beta cannot take 0 as params
        samples = [scs.beta.rvs(max(wins, 1), max(1, trials - wins)) for wins, trials in zip(self.wins, self.trials)]
        return np.argmax(samples)
