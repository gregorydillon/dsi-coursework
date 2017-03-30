import numpy as np

prior = { np.round(bias, 2): .01 for bias in list(np.linspace(0, .99, num=100))}


def likelihood(head_or_tails, prob_bucket):
    if head_or_tails == 'H':
        return prob_bucket

    return 1 - np.float(prob_bucket)
