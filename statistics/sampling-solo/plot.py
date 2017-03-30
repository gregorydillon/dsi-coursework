import numpy as np
import pylab as pl
from scipy.stats import poisson, norm, gamma


def plot_multi_hist(series_list):
    fix, ax_list = pl.subplots(3, 4)
    for series, axes in zip(series_list, ax_list.flatten()):
        plot_series_histo_fit(series, axes=axes, show=False)

    pl.autoscale()
    pl.tight_layout()
    pl.show()


def plot_series_histo_fit(series, axes=None, show=True):

    normal_dist = norm(series.mean(), series.var())
    pois_dist = poisson(series.mean())
    alpha = (series.mean() ** 2) / (series.std() ** 2)
    beta = series.mean() / (series.std() ** 2)
    gamma_d = gamma(alpha, scale=(1 / beta))

    x = np.arange(series.min(), series.max(), .1)
    pois_x = np.arange(int(series.min()), int(series.max()), 1)

    if axes is None:
        fig = pl.figure()
        axes = fig.add_subplot(111)

    axes.plot(x, normal_dist.pdf(x), color='k', label="normal")
    axes.plot(x, gamma_d.pdf(x), color='m', label="gamma")
    axes.plot(pois_x, pois_dist.pmf(pois_x), color='y', label="poisson")

    axes.hist(series, normed=True, alpha=.4)  # histogram
    axes.set_xlabel(series.name)
    axes.legend()

    if show:
        pl.autoscale()
        pl.show()
