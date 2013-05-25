#parses output of site rates from RAxML file
#line_number and range number need to be adjusted
#the appropriate line of rates in the outfile
#and the total number of sites, respectively
import sys

inFile = open(sys.argv[1], 'r')

line_number = 1
for line in inFile:
	if line_number == 118:
		string_of_rates = line
	line_number += 1

list_of_rates = string_of_rates.split(" ")

count = 0
for i in range(539526):
	print list_of_rates[count]
	count += 1

inFile.close()




