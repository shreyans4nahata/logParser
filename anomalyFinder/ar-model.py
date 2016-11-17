import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.seasonal import seasonal_decompose

df = pd.read_csv('/Users/raghav/Documents/OPEN_SOURCE/cisco/logParser/anomalyFinder/parsedOutputarima_model.csv', index_col=0)
df.columns= ['requestHits']
print(df.columns[0:])
print(len(df.requestHits))
req = df.as_matrix(columns = df.columns[0:1])
r = []
for i in range(1000,1350):
    r.append(req[i][0])
print(r)
tim = []
#for i in range(1700,8000):
 #   tim.append(pd.Period(str(i)+'-12-31','D'))
    #tim.append(i)
#print(tim)
plt.plot(r)
plt.show()
der = np.array(r)
print(type(der))
dates = sm.tsa.datetools.dates_from_range('1700', length=len(der))
print(len(dates))
endog = pd.Series(der, index=dates)
print(endog)
ar_model = sm.tsa.AR(endog, freq='A')
pandas_ar_res = ar_model.fit(maxlag=4, method='mle', disp=-1)
pred = pandas_ar_res.predict(start='2044-12-31', end='2049-12-31')
print(pred)
