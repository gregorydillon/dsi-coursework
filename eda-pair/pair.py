import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#1
bike_data = pd.read_csv('data/201402_trip_data.csv', parse_dates=['start_date', 'end_date'])
bike_data['month'] = bike_data.start_date.dt.month
bike_data['hour'] = bike_data.start_date.dt.hour
bike_data['dayofweek'] = bike_data.start_date.dt.dayofweek
bike_data['date'] = bike_data.start_date.dt.date

#2 Monthly, looks like no data for months 3-7 (march-july)
by_month = bike_data.groupby('month').count()

#3
by_day= bike_data['date'].value_counts()
day_mean = np.mean(by_day)
day_std = np.std(by_day)

day_high = day_mean + 1.5*day_std
day_low = day_mean - 1.5*day_std


by_day.reset_index().plot(x='index',y=0)

d = by_day.reset_index()
d['count'] = d['date']
d['date'] = d['index']
d = d.drop('index', 1)
sept = d[ pd.to_datetime(d['date']).dt.month == 9].sort_values(by='date')
october = d[ pd.to_datetime(d['date']).dt.month == 10].sort_values(by='date')
nov = d[ pd.to_datetime(d['date']).dt.month == 11].sort_values(by='date')
dec = d[ pd.to_datetime(d['date']).dt.month == 12].sort_values(by='date')

months = [sept, october, nov, dec]
for month in months:
    plt.plot(month.date, month['count'],'--o--')

plt.axhline(y=day_mean,color='g')
plt.axhline(y=day_high,color='g')
plt.axhline(y=day_low,color='g')

'''
High days come in clusters of 5, low days clusters of 2. We believe this is due this is due to weekends, more people commute during the week therefore higher numbers of bike share users. Also, end of dec/beg of jan we see a drop off likely due to holidays
'''

# 4
d['count'].hist(color='y', alpha=.8, normed=True, bins=range(min(d['count']), max(d['count']) + 75, 75))
d['count'].plot.kde()
plt.xlim([0,1400])

#plt.show()

weekday = d[ (d['date'].dt.dayofweek >= 0) & (d['date'].dt.dayofweek <= 4)]
weekend = d[ (d['date'].dt.dayofweek >= 5)]

weekday['count'].hist(color='b', alpha=.5, normed=True,bins=range(min(weekday['count']), max(weekday['count']) + 75, 75))
weekday['count'].plot.kde(color='b',label='week')
weekend['count'].hist(color='g', alpha=.5, normed=True,bins=range(min(weekend['count']), max(weekend['count']) + 75, 75))
weekend['count'].plot.kde(color='g',label='weekend')
plt.xlim([0,1400])
plt.legend()
#plt.show()

#5
grouped = bike_data.groupby(['date', 'hour'])
by_hour_and_date = grouped.count()
good_data = by_hour_and_date['trip_id']
good_data = good_data.reset_index()
good_data.boxplot(column=['trip_id'], by='hour')


#6
"""
The data in the boxplots is more informative. It gives us information about how much
variance there is within a given time period -- for example from midnight to 7 there really ISN'T any usership essentially. However, while there is a lull in ridership in the middle of the day, that lull has a lot of variance meaning that we still do have users. We also see some infuential points on the boxplot which are not made apparent by the line graph such as hour 13 where the max value is an outlier.
"""
weekday = good_data[ (pd.to_datetime(good_data['date']).dt.dayofweek <= 4)]
weekend = good_data[ (pd.to_datetime(good_data['date']).dt.dayofweek >= 5)]

weekday.plot(kind='box', title='weekday', column=['trip_id'], by='hour')
weekend.boxplot(column=['trip_id'], by='hour')
