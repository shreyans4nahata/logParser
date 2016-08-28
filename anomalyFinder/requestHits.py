import csv
import os
import ntpath
import sys
import collections
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
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
        if ip[j] == unique_ip[k]:
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
    #print t_list
    diff_tim = []
    diff_tim.append(0)
    for x in range(1,len(t_list)):
        diff_tim.append(t_list[x] - t_list[0])
#    print sum(tr)
    #print (diff_tim)
    #print tr

    q75, q25 = np.percentile(tr, [75 ,25])
    iqr = q75 - q25
    ul = q75 + 3.0*iqr
    ll = q25 - 3.0*iqr

    print q75,q25
    outlier = []
    outlier_x = []
    for h in range(len(tr)):
        if tr[h] < ll or tr[h] > ul:
            outlier.append(tr[h])
            outlier_x.append(t_list[h])
    print len(outlier), len(outlier_x)


    #plt.figure(figsize = ( ,250))
    # print tr
    #plt.plot(t_list,tr)
    #plt.plot(outlier_x,outlier,linestyle = '-',marker = 'o',color = 'r')
    # plt.ylabel('time',fontsize = 20)
    # plt.ylabel(unique_ip[k],fontsize = 18)
    # mng = plt.get_current_fig_manager()
    # mng.full_screen_toggle()
    #plt.show()

    #For median absolute deviation
    tuned_param = 4.5
    window = 500

    median_tr = np.median(tr[0:window])
    r_outlier = []
    r_outlier_x = []

    len_tr = len(tr)
    tot_dev = 0
    whole_median = np.median(tr)
    for i in range(1,(len_tr-window)):
        ch_tr = np.abs(tr[(window+i)]-median_tr)
        tot_dev+=ch_tr
        median_tr = np.median(tr[i:window+i])

    # ch_tr = np.abs(tr[i:window]-median_tr)
    # #print ch_tr
    # median_ch_tr = np.median(ch_tr)
    # const_b = 0.3495
    # #print const_b
    mad_val = abs(tot_dev/(len_tr-window))
    ul = tuned_param*mad_val + whole_median
    ll = whole_median - tuned_param*mad_val

    for h in range(len_tr):
        if tr[h] < ll or tr[h] > ul:
            r_outlier.append(tr[h])
            r_outlier_x.append(t_list[h])

    print len(r_outlier)
    plt.plot(t_list,tr)
    plt.plot(r_outlier_x,r_outlier,linestyle = '-',marker = 'o',color = 'r')
    plt.show()
#Close file
fileObject.close()
