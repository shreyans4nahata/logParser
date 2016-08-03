import csv
import collections
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

inputCSVFile = '../parsedOutput/Parsed_localhost_access_log-1.csv' # file path
fileObject = open(inputCSVFile)
reader = csv.DictReader(fileObject)

#Taking input to show formatted graphs
a = input()#starting index 
b = input()#Ending index

timestamp = [] # list to store all timestamps includes duplicates
ip = [] # list to store all remote ip's

# storing timestamp and ip's in a list
for row in reader:
    timestamp.append(row['f1'])
    ip.append(row['f2'])

unique_ip = list(set(ip)) # contains unique ip's

unique_ip_len = len(unique_ip)

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

    # sorting dictionary by keys
    od = collections.OrderedDict(sorted(temp_dict.items()))

    for t,i in od.iteritems():
        time,dis =t.split(' ')
        time_stamp = datetime.datetime.strptime(time,'%d/%b/%Y:%H:%M:%S')
        time_val = mdates.date2num(time_stamp)
        t_list.append(time_val)
        tr.append(i)

    #plt.figure(figsize = ( ,250))
    print len(tr),len(t_list)
    plt.plot(t_list[a:b],tr[a:b],lw = 2)
    plt.ylabel('time',fontsize = 20)
    plt.ylabel(unique_ip[k],fontsize = 18)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()

#Close file
fileObject.close()
