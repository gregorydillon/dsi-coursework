import numpy as np
import matplotlib.pylab as plt
from sklearn import datasets

def land_use():
    land_use_init = np.array([.25, .2, .55])

    trans_matrix = np.array([
        [.7, .1, 0],
        [.2, .9, .2],
        [.1, 0, .8]
    ])

    landuse_2009 = trans_matrix.dot(land_use_init)
    landuse_2014 = trans_matrix.dot(landuse_2009)

    print land_use_init, landuse_2009, landuse_2014
    '''
      C        I     R
    [ 0.25    0.2    0.55]
    [ 0.195   0.34   0.465]
    [ 0.1705  0.438  0.3915]

    Which makes sense to us given the transition matrix. Industrial grows
    the fastest (.2+.2+.9 = 1.1, largest share of all 'to' rows), residential
    gives up 20% of it's market to Industrial and never gets it back.
    Commercial and Industrial trade a bit, and commercial leaks some of that
    back into residential.
    '''

# land_use()


def iris():
    # The 1st column is sepal length and the 2nd column is sepal width
    sepalLength_sepalWidth = datasets.load_iris().data[:, :2]
    mean_len_by_wid = np.mean(sepalLength_sepalWidth, axis=0)
    # print sepalLength_sepalWidth,  mean_len_by_wid

    plt.scatter(sepalLength_sepalWidth[:, 1], sepalLength_sepalWidth[:, 0], alpha=.6)
    plt.plot([mean_len_by_wid[1]], [mean_len_by_wid[0]], marker='o', markersize=3, color="red")
    plt.xlabel("sepal width")
    plt.ylabel("sepal length")
    plt.show()


def euclidean_dist(a, b):
    if a.shape != b.shape:
        raise TypeError("a and b must have the same shape instead got: a{}, b{}".format(a.shape, b.shape))
    elif a.shape[1] != 1:
        raise TypeError("vectors must be column vectors, instead shape was: {}".format(a.shape))

    return np.linalg.norm(b - a)


def cosine_sim(a, b):
    if a.shape != b.shape:
        raise TypeError("a and b must have the same shape instead got: a{}, b{}".format(a.shape, b.shape))
    elif a.shape[1] != 1:
        raise TypeError("vectors must be column vectors, instead shape was: {}".format(a.shape))

    # DOT THOSE BAD BOYS
    numerator = a.T.dot(b)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    return numerator / denominator


a = np.array([[1], [0]])
b = np.array([[0], [1]])
print euclidean_dist(a, b)
print cosine_sim(a, b)


# iris()
