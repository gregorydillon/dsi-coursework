import os
import sys
import pandas as pd
from scipy.stats import spearmanr, pearsonr
sys.path.append(os.getcwd())
import probability.lib.plot as plot

ADMISSIONS = pd.read_csv(os.getcwd() + "/data/admissions.csv")
STUDY_HRS = pd.read_csv(os.getcwd() + "/data/admissions_with_study_hrs_and_sports.csv")


def main():
    ADMISSIONS['income_group'] = ADMISSIONS['family_income'].apply(income_group)

    low_gpas = ADMISSIONS[ADMISSIONS['income_group'] == 0]
    mid_gpas = ADMISSIONS[ADMISSIONS['income_group'] == 1]
    high_gpas = ADMISSIONS[ADMISSIONS['income_group'] == 2]

    series = [low_gpas['gpa'], mid_gpas['gpa'], high_gpas['gpa']]
    colors = ['r', 'g', 'b']
    plot.plot_multi_hist(series, colors)

    print "======INCOME GROUPS======"
    print "LOW 90th Percentile Cuttoff: {}".format(low_gpas.quantile(.9).gpa)
    print "MID 90th Percentile Cuttoff: {}".format(mid_gpas.quantile(.9).gpa)
    print "HIGH 90th Percentile Cuttoff: {}".format(high_gpas.quantile(.9).gpa)

    print "\n========HOURS STUDIED======="
    spearman = spearmanr(STUDY_HRS['hrs_studied'], STUDY_HRS['gpa'])
    pearson = pearsonr(STUDY_HRS['hrs_studied'], STUDY_HRS['gpa'])
    print "Spearman: Coef: {} p-value: {}".format(*spearman)
    print "Pearson: Coef: {} p-value: {}".format(*pearson)

    print "\n========SPORTS PERFORMANCE======="
    spearman = spearmanr(STUDY_HRS['sport_performance'], STUDY_HRS['gpa'])
    pearson = pearsonr(STUDY_HRS['sport_performance'], STUDY_HRS['gpa'])
    print "Spearman: Coef: {} p-value: {}".format(*spearman)
    print "Pearson: Coef: {} p-value: {}".format(*pearson)

    xs = [STUDY_HRS['hrs_studied'], STUDY_HRS['sport_performance']]
    ys = [STUDY_HRS['gpa'], STUDY_HRS['gpa']]
    plot.plot_multi_scatter(xs, ys)


def income_group(income):
    if income < 26832:
        return 0
    elif income < 37510:
        return 1

    return 2


if __name__ == '__main__':
    main()
