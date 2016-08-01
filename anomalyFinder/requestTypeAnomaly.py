#Detect Anomalyies in the GET and POST requests to a particular resource.

import matplotlib.pyplot as plt
import csv

#Input File
inputCSVFile = '../parsedOutput/Parsed_localhost_access_log-1.csv'
inputCSV = open(inputCSVFile)
reader = csv.DictReader(inputCSV)

#A set of all the different resources
res_set = set()

for each_row in reader:
	res_set.add(each_row['f6'])

res_set = list(res_set)

res_set_len = len(res_set)

xval = []
post_list = []
get_list = []
oth_list = []

#Hold on tight
print "Total resources: ",res_set_len

for i in range(res_set_len):
	#Point to start of file again
	inputCSV.seek(0)

	xval.append(i)
	#Initialize the no. of requests
	post_val = 0
	get_val = 0
	oth_val = 0
	
	for each_row in reader:
		#Check for the count
		if each_row['f6'] == res_set[i]:
			if each_row['f5'] == 'GET' :
				get_val+=1
			elif each_row['f5'] == 'POST' :
				post_val+=1
			else:
				oth_val+=1
	
	#Append all values
	post_list.append(post_val)
	get_list.append(get_val)
	oth_list.append(oth_val)
	#print 'progress'
	print "Completed : ",(i+1)

#Don't uncomment below line, it makes the plot xticks more gibberish!!
#plt.xticks(xval,res_set)

plt.title("Count of POST")
plt.plot(xval,post_list,'b')
plt.xlabel('Different resources')
plt.ylabel('Count of POST requests')
plt.show()

plt.title("Count of GET")
plt.plot(xval,get_list,'r')
plt.xlabel('Different resources')
plt.ylabel('Count of GET requests')
plt.show()

plt.title("Count of other")
plt.plot(xval,oth_list,'g')
plt.xlabel('Different resources')
plt.ylabel('Count of Other requests')
plt.show()

#Close file
inputCSV.close()