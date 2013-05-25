#import sys module to take command line arguments
import sys  
#import time to keep track of time analysis takes
import time

import numpy as np 
import pylab as pl

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale 

from collections import defaultdict


#open file with site rates, each rate must be separated by newline character "\n"
file1 = sys.argv[1]
#takes user input for number of desired clusters
number_of_ks = int(sys.argv[2])

#open file for reading and save in variable inFile to feed to function
inFile = open(file1)

def kmeans(inFile, number_of_ks):
    '''
    Takes, as input, a file with rates separated by newline characters, and
    the number of desired clusters, then performs kmeans clustering
    and returns a dictionary with character numbers as keys and
    rates as values
    '''
    #start clock to keep track of time
    start = time.clock()
    #read rates into list
    rate_list_lines = [line for line in inFile.readlines()]
    #create new list for rates without newline characters
    rate_list = []
    #remove newline characters and add to new list of rates
    for i in rate_list_lines:
        float_rate = float(i.strip("\n"))
        rate_list.append([float_rate])

    #create 1 dimensional array of rates for input into scikit_learn
    #implementation of kmeans
    array = np.array(rate_list, ndmin = 1)

    #print array

    #scale numbers in array
    #array = scale(array)

    #print array
    #create a KMeans object from scikit_learn
    KMeans_out = KMeans(init='k-means++', n_clusters = number_of_ks, \
        n_init = 10)

    #perform KMeans clustering on data array from site rates see functions of 
    #scikit learn KMeans class here: http://tinyurl.com/q3qjxly
    KMeans_out.fit(array)

    #store centroids
    centroids = KMeans_out.cluster_centers_
    #store individual rates in a list, should be in character order
    rate_categories = KMeans_out.labels_
    #create empty dictionary to store rates and associated characters
    dictionary_of_rates = {}
    char_number = 1    
    #loop through list of rate categories and add them to dictionary with associated character
    for i in rate_categories:
    	dictionary_of_rates[char_number] = i
    	char_number += 1
    #print centroid info to terminal window
    print "Centroids: " + str(centroids)
    #print list of categories to terminal
    print "All categories: " + str(rate_categories)

    #stop clock and output total time
    stop = time.clock()
    time_taken = "This analysis took " + str(stop - start) + "seconds!"
    print time_taken

    #return the dictionary with the rates
    return dictionary_of_rates

def RAxML_categories(inFile, number_of_ks):
    '''
    Takes as input the file with rates separated by newline characters
    and the desired number of rate categories, performs kmeans on the rates
    and outputs them into a RAxML partition scheme file called "RAxML_scheme.txt"
    '''
    #call kmeans function and assign variable to the dictionary of rate classes
	characters_and_rates = kmeans(inFile, number_of_ks)
    #make new dicitonary to assign characters to values
	output_dict = defaultdict(list)
    #loops through dicitonary of characters and rate classes and assign characters
    #to appropriate rate class in new dictionary
	for k, v in characters_and_rates.iteritems():
		output_dict[v].append(k)
    
    #creat new file to write RAxML partition scheme definition
	outFile = open("RAxML_scheme.txt", "a")
    #start counter for different partition numbers
	partition = 0
    #loops through dictionary of partitions and output information into
    #RAxML scheme definition
	for i in range(len(output_dict)):
		outFile.write("Partition " + str(partition) + ", DNA = " + \
            str(output_dict[partition]).strip("[]") + "\n")
		print "Partition " + str(partition) + ", DNA = " + str(output_dict[partition])
		partition += 1
	outFile.close()

RAxML_categories(inFile, number_of_ks)

inFile.close()




