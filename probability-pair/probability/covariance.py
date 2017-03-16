import pandas as pd
import numpy as np

def covariance(data_frame):
    covariance_matrix = []
    for row_name in data_frame:
        row = []
        covariance_matrix.append(row)

        row_series = data_frame[row_name]

        for col_name in data_frame:
            col_series = data_frame[col_name]
            cov_val = _cov(row_series, col_series)
            row.append(cov_val)

    return covariance_matrix

def _cov(x_series, y_series):
    x_avg = x_series.mean()
    y_avg = y_series.mean()

    avgs = zip(x_series, y_series)

    def cov_reducer(accum, next):
        x_point = next[0] - x_avg
        y_point = next[1] - y_avg
        return accum + x_point * y_point

    numerator = reduce(cov_reducer, avgs, 0)

    return float(numerator)/(len(avgs) - 1)

def correlation(data_frame):
    correlation_matrix = []
    covariance_matrix = data_frame.cov() # Using pandas because it's better, mine works it's tested
    for row in data_frame:
        correlation_row = []
        correlation_matrix.append(correlation_row)
        std_x = data_frame[row].std()

        for col in data_frame:
            std_y = data_frame[col].std()
            cov = covariance_matrix.loc[row].loc[col]
            correlation_row.append(cov / (std_x * std_y))

    return correlation_matrix




"""
cor(x,y) = cov(x,y) / sd(x)sd(y)
"""
