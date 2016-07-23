# A simple parser for log files.
import sys
import os
import ntpath
import re
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
outputFile.write("\nParsed data: \n")

# The Initial regex 
logRegex = "\[(.*?)\] ([(\d\.)]+) ([(\d\.)]+) - - (\d*) (\S+) (\S*)(\s*)(\S*)(\s*)(\S*)(\s*)(\d*) (\w*)(\W*) (\w+)"
lineCount = 0
try:
	for eachLine in inputFile:
		lineCount+=1
		#print re.match(logRegex,eachLine).groups()
		extTuple = re.match(logRegex,eachLine).groups()
		extTupleLen = len(extTuple)
		for i in range(extTupleLen):
			outputFile.write(extTuple[i])
			outputFile.write("\t")
		outputFile.write("\n")
		
except Exception as e:
	print e
	print "Occured at line: " + str(lineCount)

inputFile.close()
outputFile.close()