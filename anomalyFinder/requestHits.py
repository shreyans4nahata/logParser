import csv
import numpy as np
import os
import ntpath
import sys
import collections
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

inputCSVFile = '../parsedOutput/Parsed_localhost_access_log-1.csv' # file path
fileObject = open(inputCSVFile)
reader = csv.DictReader(fileObject)

outputDir = os.getcwd() + "/parsedOutput/"
outputFileName = os.getcwd() + "/par.csv"
a = input()
b = input()

outputFile = open(outputFileName,"w+")

fieldnames = ['f2']

writer = csv.DictWriter(outputFile,fieldnames=fieldnames)

writer.writeheader()
#print "DEBUgs"
timestamp = [] # list to store all timestamps includes duplicates
ip = [] # list to store all remote ip's

# storing timestamp and ip's in a list
for row in reader:
    timestamp.append(row['f1'])
    ip.append(row['f2'])

unique_ip = list(set(ip)) # contains unique ip's

unique_ip_len = len(unique_ip)
print unique_ip

# plotting of request hits against timestamps
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
#        print t,i
        #sp_dict = {}
        time,dis =t.split(' ')
        time_stamp = datetime.datetime.strptime(time,'%d/%b/%Y:%H:%M:%S')
        time_val = mdates.date2num(time_stamp)
        #sp_dict['f1'] = t
        #sp_dict['f2'] = i
        #writer.writerow(sp_dict)
        #sp_dict.clear()
        t_list.append(time_val)
        tr.append(i)

    diff_tim = []
    diff_tim.append(0)
    for x in range(1,len(t_list)):
        diff_tim.append(t_list[x] - t_list[0])
#    print sum(tr)
    print len(diff_tim)
    print tr
    print diff_tim
    for y in range(len(diff_tim)):
        sp_dict = {}
        sp_dict['f1'] = diff_tim[y]
        sp_dict['f2'] = tr[y]
        writer.writerow(sp_dict)
        sp_dict.clear()

    #plt.figure(figsize = ( ,250))
    print tr
    plt.plot(t_list[a:b],tr[a:b],lw = 2)
    plt.ylabel('time',fontsize = 20)
    plt.ylabel(unique_ip[k],fontsize = 18)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
    break

#Close file
fileObject.close()
