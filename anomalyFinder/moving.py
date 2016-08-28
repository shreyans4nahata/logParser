from __future__ import division
import csv
import os
import ntpath
import sys
import collections
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid
from numpy import linspace, loadtxt, ones, convolve
import numpy as np

inputCSVFile = '../parsedOutput/Parsed_localhost_access_log-1.csv' # file path
fileObject = open(inputCSVFile)
reader = csv.DictReader(fileObject)

#print "DEBUgs"
timestamp = [] # list to store all timestamps includes duplicates
ip = [] # list to store all remote ip's

# storing timestamp and ip's in a list
for row in reader:
    timestamp.append(row['f1'])
    ip.append(row['f2'])

unique_ip = list(set(ip)) # contains unique ip's

unique_ip_len = len(unique_ip)

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

#plotting of request hits against timestamps
for k in range(unique_ip_len):
    temp_dict = {} # temporary dictinary
    final_dict = {}
    tr = [] # list containing request hits at particular ip
    t_list = [] #list containg formatted timestamp

    # initialization of request hit to 0 corresponding timestamp
    for j in range(len(timestamp)):
        temp_dict[timestamp[j]] = 0

    # incrementing the count for each ip
    for j in range(len(timestamp)):
        if ip[j] == "10.241.248.26":
            temp_dict[timestamp[j]]+=1

#    print temp_dict
    # sorting dictionary by keys
    od = collections.OrderedDict(sorted(temp_dict.items()))

    for t,i in od.iteritems():

        time,dis =t.split(' ')
        time_stamp = datetime.datetime.strptime(time,'%d/%b/%Y:%H:%M:%S')
        time_val = mdates.date2num(time_stamp)
        t_list.append(time_val)
        tr.append(i)

    x = t_list
    y = tr

    MOV = movingaverage(y,1000).tolist()
    STD = np.std(MOV)
    events= []
    ind = []
    t_events = []
    for ii in range(len(y)):
        if y[ii] > MOV[ii]+STD:
            events.append(y[ii])
            t_events.append(x[ii])
    plot(t_events,events,"k.")
    y_av = movingaverage(y, 1000)
    plot(x,y_av,"r")
    xlabel("time")
    ylabel("Request hits")
    #grid(True)
    show()
    break

    #movin average


fileObject.close()
