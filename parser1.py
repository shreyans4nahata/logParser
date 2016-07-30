# A simple parser for log files.
import sys
import os
import ntpath
import re
import csv
# Getting file name from the command line argument
if len(sys.argv) != 2 :
	print "Usage: python parser1.py <input-log-file-name>"
	sys.exit()
inputFileName = sys.argv[1]

# Opening the file
inputFile = open(inputFileName,"r")

# Creating output file
outputDir = os.getcwd() + "/parsedOutput/"
outputFileName = outputDir + "Parsed_" + os.path.splitext(ntpath.basename(inputFileName))[0] + ".csv"

# Opening output file
outputFile = open(outputFileName,"w+")

#Row name fields (Currently settitng sample names)
fieldnames = ['f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12','f13','f14','f15']

#Defining the attributes for the csv file
writer = csv.DictWriter(outputFile,fieldnames=fieldnames)

writer.writeheader()

# The Initial regex 
logRegex = "\[(.*?)\] ([(\d\.)]+) ([(\d\.)]+) - - (\d*) (\S+) (\S*)(\s*)(\S*)(\s*)(\S*)(\s*)(\d*) (\w*)(\W*) (\w+)"

#To keep the count of line no.
lineCount = 0

try:
	for eachLine in inputFile:
		lineCount+=1
		extTuple = re.match(logRegex,eachLine).groups()
		extTupleLen = len(extTuple)
		#Creating a dictionary to store the current row values
		d1 = {}
		for i in range(extTupleLen):
			d1[fieldnames[i]] = extTuple[i]

		writer.writerow(d1)
		#Clear the dictionary
		d1.clear()
		
except Exception as e:
	print e
	print "Occured at line: " + str(lineCount)
inputFile.close()
outputFile.close()