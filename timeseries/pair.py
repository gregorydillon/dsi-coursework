import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm
import statsmodels.tsa.arima_model import ARIMA, ARIMAResults 
from statsmodels.tsa.arima_process import ArmaProcess
plt.ion()

ts = pd.read_json('logins.json')
ones = np.full(len(ts),1)
df =pd.DataFrame(index=pd.to_datetime(ts[0]),data=ones)

daily= df.resample('D').sum()
hourly= df.resample('H').sum()

daily['dayofweek'] = daily.index.dayofweek

def plot_acf_pacf(your_data, lags):
   fig = plt.figure(figsize=(12,8))
   ax1 = fig.add_subplot(211)
   fig = plot_acf(your_data, lags=lags, ax=ax1)
   ax2 = fig.add_subplot(212)
   fig = plot_pacf(your_data, lags=lags, ax=ax2)
   plt.show()


plot_acf_pacf(daily.index,lags=28)

first_order = daily['counts'].diff(periods=1)
sev_per = daily['counts'].diff(periods=7)
plot_acf_pacf(first_order[1:],lags=28)
plot_acf_pacf(sev_per[7:],lags=28)


pre_x = (np.arange(len(daily))+1).reshape(-1,1)
X = sm.add_constant(pre_x,prepend=False)
linear_model = sm.OLS(daily.counts,X).fit()
linear_trend = linear_model.predict(X)
detrended_series = daily.counts - linear_trend

arima_model = ARIMA(daily.counts,order=(5,7,1))
