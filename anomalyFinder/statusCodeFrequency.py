#Detect anomalies in the status code frequency for each resource

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import csv
import datetime

#Input File
inputCSVFile = '../parsedOutput/Parsed_localhost_access_log-1.csv'
inputCSV = open(inputCSVFile)
reader = csv.DictReader(inputCSV)

#A set of all the different resources
res_set = set()

#create a set of all the different resources.
for each_row in reader:
	res_set.add(each_row['f6'])

res_set = list(res_set)

res_set_len = len(res_set)

t_list = []
status_list =[]

#Run this if u r really bored
#It displays around 280 graphs for the current csv file
#Hold on tight!!
for i in range(res_set_len):
	#Set pointer again to the begining
	inputCSV.seek(0)
	reader.next()

	for each_row in reader:
		
		if each_row['f6'] == res_set[i]:
			
			time,dis =(each_row['f1']).split(' ')

			#Getting time stamp value
			time_stamp = datetime.datetime.strptime(time,'%d/%b/%Y:%H:%M:%S')

			#Time ticks
			#time_ticks.append(time)

			#Converting time to floating values for easy plotting
			time_val = mdates.date2num(time_stamp)
			t_list.append(time_val)

			#Creating status code list
			status_list.append(int(each_row['f10']))

	
	plt.plot(t_list,status_list)
	plt.xlabel('Timestamp')
	plt.ylabel('Status codes')
	plt.title('For resource '+str(res_set[i]))
	plt.show()
	#Clear list fix
	del status_list[:]
	del t_list[:]

#Close file
inputCSV.close()