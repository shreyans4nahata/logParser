import os
import csv
import ntpath
import sys
import collections
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import json
import matplotlib.pylab as plt
import pandas as pd
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels import *


#Function to generate timeseries
def genTimeSeries(inputCSVFile):

	outputDir = os.getcwd() + "/parsedOutput/"
	fileObject = open(outputDir+inputCSVFile,"r")
	reader = csv.DictReader(fileObject)

	timestamp = [] # list to store all timestamps includes duplicates
	ip = [] # list to store all remote ip's

	for row in reader:
		timestamp.append(datetime.strptime(str(row['f1']), "%d/%b/%Y:%H:%M:%S +0200" ))
		ip.append(row['f2'])

	unique_ip = list(set(ip)) # contains unique ip's

	#Debug prints
	#print timestamp,ip,unique_ip

	unique_ip_len = len(unique_ip)
	temp_dict = {} # temporary dictinary

    # initialization of request hit to 0 corresponding timestamp
	for j in range(0,len(timestamp)):
		temp_dict[timestamp[j]] = 0

    #Debug prints
    #print "Before: ",temp_dict

	# incrementing the count for each ip
	dikha = 12121212
	for j in range(0,len(timestamp)):
		if ip[j] == unique_ip[7]:
			temp_dict[timestamp[j]]+=1
			dikha = j

	#Debug prints
	#print "After: ",temp_dict
	fileObject.close()

	outputFileName = outputDir + inputCSVFile.strip('.csv') + "rr.csv"

	# Opening output file
	outputFile = open(outputFileName,"w+")

	#Row name fields (Currently settitng sample names)
	fieldnames = ['f0','f1']

	#Defining the attributes for the csv file
	writer = csv.DictWriter(outputFile,fieldnames=fieldnames)

	writer.writeheader()
	d1 = {}
	od = collections.OrderedDict(sorted(temp_dict.items()))
	for k,v in od.iteritems():
		d1 = {}
		d1['f0'] = k
		d1['f1'] = float(v)
		writer.writerow(d1)
		d1.clear()

	outputFile.close()

	return outputFileName

#Create pandas timeseries object
def createTime(outputFileName):
	dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
	data = pd.read_csv( outputFileName, parse_dates=True, index_col='f0',date_parser=dateparse)
	return data

def test_stationarity(timeseries):

	isStationary = True
	#Determing rolling statistics
	rolmean = timeseries.rolling(window=60, center= False).mean()
	rolstd = timeseries.rolling(window=60, center= False).std()

	#Plot rolling statistics:
	orig = plt.plot(timeseries, color='blue',label='Original')
	mean = plt.plot(rolmean, color='red', label='Rolling Mean')
	std = plt.plot(rolstd, color='black', label = 'Rolling Std')
	plt.legend(loc='best')
	plt.title('Rolling Mean & Standard Deviation')
	plt.show()

	#Perform Dickey-Fuller test:
	print 'Results of Dickey-Fuller Test:'
	dftest = adfuller(timeseries, autolag='AIC')
	dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
	for key,value in dftest[4].items():
		dfoutput['Critical Value (%s)'%key] = value
		if dfoutput['Test Statistic'] > value:
			isStationary = False
	print dfoutput
	return isStationary

#Take the file name as input
inputFile = raw_input("Enter the log file name")
ts_file = genTimeSeries(inputFile)

data = createTime(ts_file)
#print data.index
ts = data['f1']
plt.plot(ts)
Stat_res = test_stationarity(ts)
#penalizing higher values
# Taking log,sqrt or  other transformations
ts_log = np.log(ts)
ts.replace([np.inf, -np.inf], 0.0)
print ts_log
# for j in range(len(ts_log)):
# 	if
#plt.plot(ts_log)

# expwighted_avg = pd.ewma(ts_log, halflife=60)
# plt.plot(ts_log)
# plt.plot(expwighted_avg, color='red')
# plt.show()

# ts_log_ewma_diff = ts_log - expwighted_avg
# ts_log_ewma_diff.dropna(inplace=True)
# test_stationarity(ts_log_ewma_diff)
print "The time series is Stationary: ",Stat_res

#Doing ACF and PACF
# lag_acf = acf(ts, nlags=5)
# lag_pacf = pacf(ts, nlags=5, method='ols')
#
# print "U have crossed the barrier :p"
# plt.subplot(121)
# plt.plot(lag_acf)
# plt.axhline(y=0,linestyle='--',color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(ts)),linestyle='--',color='gray')
# plt.axhline(y=1.96/np.sqrt(len(ts)),linestyle='--',color='gray')
# plt.title('Autocorrelation Function')
#
# plt.subplot(122)
# plt.plot(lag_pacf)
# plt.axhline(y=0,linestyle='--',color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(ts)),linestyle='--',color='gray')
# plt.axhline(y=1.96/np.sqrt(len(ts)),linestyle='--',color='gray')
# plt.title('Partial Autocorrelation Function')
# plt.tight_layout()

#ARIMA model (Both AR and MA)
model = ARIMA(ts, order=(2, 1, 2))  #Set the p,d,q vals
results_ARIMA = model.fit(disp=-4)
#plt.plot(ts)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.show()
#plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2))
