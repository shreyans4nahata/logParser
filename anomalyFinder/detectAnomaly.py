import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import datetime

#Input File
inputCSVFile = '../parsedOutput/Parsed_localhost_access_log-1.csv'
inputCSV = open(inputCSVFile)
reader = csv.DictReader(inputCSV)

#Lists to contain x and y values
ip1_list = []
t_list = []

#Lists to contain x and y ticks values 
time_ticks = []
ip_ticks = []

for each_row in reader:
	time,dis =(each_row['f1']).split(' ')

	#Getting time stamp value
	time_stamp = datetime.datetime.strptime(time,'%d/%b/%Y:%H:%M:%S')

	#Time ticks
	#time_ticks.append(time)

	#Converting time to floating values for easy plotting
	time_val = mdates.date2num(time_stamp)
	t_list.append(time_val)
	
	i1_val = str(each_row['f2'])
	i2_val = str(each_row['f3'])

	#IP ticks
	#ip_ticks.append(i1_val+i2_val)
	
	if i1_val==i2_val:
		ip1_list.append(0)
	else:
		i1_list = list(map(int,i1_val.split('.')))
		i2_list = list(map(int,i2_val.split('.')))
		diff = 0
		for ele in range(4):
			diff+=i1_list[i]-i2_list[i]
		ip1_list.append(diff)

# Setting tick Values
# plt.xticks(t_list,time_ticks)
# plt.yticks(ip1_list,ip_ticks)

plt.plot(t_list,ip1_list,'b')
plt.show()