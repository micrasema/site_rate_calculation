#import sys module to take command line arguments
import sys  
#import time to keep track of time analysis takes
import time

import numpy as np 
import pylab as pl

from sklearn import metrics
from sklearn.cluster import DBSCAN

from collections import defaultdict


def dbscan(inFile, epsilon, min_n):
	#start clock
	start = time.clock()
	#save site rates into list
	rate_list_lines = [line for line in inFile.readlines()]
	rate_list = []
	for i in rate_list_lines:
		float_rate = float(i.strip("\n"))
		rate_list.append([float_rate])
	#create one dimensional array from site rate list
	rate_array = np.array(rate_list, ndmin = 2)
	# Create instance of DBSCAN object from scikit_learn and fit DBSCAN on 
    # array
	DBSCAN_result = DBSCAN(epsilon, min_n, 'Euclidean').fit(rate_array)
	#retrieve cluster information for each site
	site_rate_categories = DBSCAN_result.labels_
	# print site_rate_categories
	# Add cluster information for each site to dictionary along with site 
    # number
	site = 1
	cluster_dictionary = {}
	for i in site_rate_categories:
		cluster_dictionary[site] = int(i)
		site += 1
	# print cluster_dictionary
	# Stop clock, print time taken for analysis
	stop = time.clock()
	print "The DBSCAN analysis took " + str(stop - start) + " seconds!"
	# Return dictionary of sites and site rates
	return cluster_dictionary

def get_rate_dictionary(inFile):
    # Read rates from file
    rate_list_lines = [line for line in inFile.readlines()]
    # Create new list for rates without newline characters
    rate_list = []
    # Remove newline characters and add to new list of rates
    for i in rate_list_lines:
        float_rate = float(i.strip("\n"))
        rate_list.append([float_rate])
    # Begin count for site numbers
    count = 1
    dictionary_of_rates = {}
    # Loop through list and add rates formatted as floats to dictionary with 
    # site numbers
    for i in rate_list:
        dictionary_of_rates[count] = float(str(i).strip("[]"))
        count += 1
    return dictionary_of_rates

def cluster_histogram(inFile, epsilon, min_n, num_bins):
    # Make call to kmeans function
    char_dict = dbscan(inFile, epsilon, min_n)
    # Create new dictionary with categories as keys and lists of sites as 
    # values
    cluster_dict = defaultdict(list)
    for k, v in char_dict.iteritems():
        cluster_dict[v].append(k)
    inFile.seek(0)
    # Retrieve dictionary of rates
    dictionary_of_rates = get_rate_dictionary(inFile)
    # Merge dictionaries so site rate values are stored as lists with their 
    # corresponding cluster number
    rate_dict = ({k: [dictionary_of_rates[i] for i in v] for k, v 
        in cluster_dict.items()}
    rate_list = []
    for i in rate_dict:
        rate_list.append(rate_dict[i])
    # print rate_list

    pl.hist(rate_list, bins = num_bins, histtype = 'stepfilled')
    pl.title("Site rates from clusters")
    pl.xlabel("rates")
    pl.ylabel("frequencies")
    # pl.yscale('log')
    pl.show()

if __name__ == '__main__':
	# Open file with site rates, each rate must be separated by newline character "\n"
	file1 = sys.argv[1]
	# Open file for reading and save in variable inFile to feed to function
	inFile = open(file1)
	cluster_histogram(inFile, 0.3, 5, 100)
	inFile.close()
