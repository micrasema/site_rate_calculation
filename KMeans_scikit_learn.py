import sys  
import time

import numpy as np 
import pylab as pl
import matplotlib.pyplot as pyplot

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale 

from collections import defaultdict
from phyml_rate_cluster import rates_from_categories


def kmeans_multi_dim(dictionary, number_of_ks):
    '''
    Take as input a dictionary made up of site numbers as keys
    and lists of rates as values
    '''
    # Take start time
    start = time.clock()
    # Read rates into multidimensional list
    all_rates_list = []
    for i in range(1, (len(dictionary) + 1)):
        rate_cat_list = dictionary[i]
        all_rates_list.append(rate_cat_list)
    # print all_rates_list
    # Save the number of dimensions to a variable
    num_dim = len(dictionary[1])
    # print num_dim
    # Create and array with the appropriate number of dimensions
    array = np.array(all_rates_list)
    # print array
    kmeans_out = KMeans(init='k-means++', n_clusters = number_of_ks, 
        n_init = 100)
    kmeans_out.fit(array)
    centroids = kmeans_out.cluster_centers_
    # print centroids
    rate_categories = kmeans_out.labels_
    # print rate_categories
    cluster_dictionary = {}
    char_number = 1    
    # Loop through list of rate categories and add them to dictionary with associated character
    for i in rate_categories:
        cluster_dictionary[char_number] = i
        char_number += 1
    # Print centroid info to terminal window
    print "Centroids: " + str(centroids)
    # Print list of categories to terminal
    print "All categories: " + str(rate_categories)
    # Stop clock and output total time
    stop = time.clock()
    time_taken = "This analysis took " + str(stop - start) + "seconds!"
    # print time_taken
    # Loop through dictionary and output the site and rate class separated by a tab
    site_number = 1
    for i in range(len(cluster_dictionary)):
        print str(site_number) + '\t' + str(cluster_dictionary[site_number])
        site_number += 1
    # Return the dictionary with the rates
    return cluster_dictionary



def kmeans(inFile, number_of_ks):
    '''
    Takes, as input, a file with rates separated by newline characters, and
    the number of desired clusters, then performs kmeans clustering
    and returns a dictionary with character numbers as keys and
    rates as values
    '''
    # Start clock to keep track of time
    start = time.clock()
    # Read rates into list
    rate_list_lines = [line for line in inFile.readlines()]
    # Create new list for rates without newline characters
    rate_list = []
    # Remove newline characters and add to new list of rates
    for i in rate_list_lines:
        float_rate = float(i.strip("\n"))
        rate_list.append([float_rate])

    # Create 1 dimensional array of rates for input into scikit_learn
    # Implementation of kmeans
    array = np.array(rate_list, ndmin = 1)
    # print array
    # Scale numbers in array
    # array = scale(array)
    # print array
    # Create a KMeans object from scikit_learn
    KMeans_out = KMeans(init='k-means++', n_clusters = number_of_ks, \
        n_init = 10)
    # Perform KMeans clustering on data array from site rates see functions of 
    # Scikit learn KMeans class here: http://tinyurl.com/q3qjxly
    KMeans_out.fit(array)
    # Store centroids
    centroids = KMeans_out.cluster_centers_
    # Store individual rates in a list, should be in character order
    rate_categories = KMeans_out.labels_
    # Create empty dictionary to store rates and associated characters
    cluster_dictionary = {}
    char_number = 1    
    # Loop through list of rate categories and add them to dictionary with associated character
    for i in rate_categories:
    	cluster_dictionary[char_number] = i
    	char_number += 1
    # Print centroid info to terminal window
    print "Centroids: " + str(centroids)
    # Print list of categories to terminal
    print "All categories: " + str(rate_categories)
    # Stop clock and output total time
    stop = time.clock()
    time_taken = "This analysis took " + str(stop - start) + "seconds!"
    print time_taken
    # Return the dictionary with the rates
    return cluster_dictionary

def RAxML_categories(inFile, number_of_ks):
    '''
    Takes as input the file with rates separated by newline characters
    and the desired number of rate categories, performs kmeans on the rates
    and outputs them into a RAxML partition scheme file called "RAxML_scheme.txt"
    '''
    # Call kmeans function and assign variable to the dictionary of rate classes
    characters_and_rates = kmeans(inFile, number_of_ks)
    # Make new dicitonary to assign characters to values
    output_dict = defaultdict(list)
    # Loops through dicitonary of characters and rate classes and assign characters
    # To appropriate rate class in new dictionary
    for k, v in characters_and_rates.iteritems():
        output_dict[v].append(k)
    # Create new file to write RAxML partition scheme definition
    outFile = open("RAxML_scheme.txt", "a")
    # Start counter for different partition numbers
    partition = 0
    # Loops through dictionary of partitions and output information into
    # RAxML scheme definition
    for i in range(len(output_dict)):
        outFile.write("Partition " + str(partition) + ", DNA = " + \
            str(output_dict[partition]).strip("[]") + "\n")
        print "Partition " + str(partition) + ", DNA = " + str(output_dict[partition])
        partition += 1
    outFile.close()
    return output_dict

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
    # Loop through list and add rates formatted as floats to dictionary with site numbers
    for i in rate_list:
        dictionary_of_rates[count] = float(str(i).strip("[]"))
        count += 1
    return dictionary_of_rates

def rates_and_categories(inFile, number_of_ks):
    # Make call to kmeans function
    char_dict = kmeans(inFile, number_of_ks)
    # Create new dictionary with categories as keys and lists of sites as values
    cluster_dict = defaultdict(list)
    for k, v in char_dict.iteritems():
        cluster_dict[v].append(k)
    inFile.seek(0)
    # Retrieve dictionary of rates
    dictionary_of_rates = get_rate_dictionary(inFile)
    # Merge dictionaries so site rate values are stored as lists with their 
    # corresponding cluster number
    rate_dict = {k: [dictionary_of_rates[i] for i in v] for k, v in cluster_dict.items()}
    return rate_dict

def cluster_histogram(inFile, number_of_ks, num_bins):
    # Make call to kmeans function
    char_dict = kmeans(inFile, number_of_ks)
    # Create new dictionary with categories as keys and lists of sites as values
    cluster_dict = defaultdict(list)
    for k, v in char_dict.iteritems():
        cluster_dict[v].append(k)
    inFile.seek(0)
    # Retrieve dictionary of rates
    dictionary_of_rates = get_rate_dictionary(inFile)
    # Merge dictionaries so site rate values are stored as lists with their 
    # corresponding cluster number
    rate_dict = {k: [dictionary_of_rates[i] for i in v] for k, v in cluster_dict.items()}
    rate_list = []
    for i in rate_dict:
        rate_list.append(rate_dict[i])
    # print rate_list

    pl.hist(rate_list, bins = num_bins, histtype = 'stepfilled', log = 'true')
    # pl.hist(rate_list, bins = num_bins, histtype = 'stepfilled')
    pl.title("Site likelihoods as calculated in PhyML")
    pl.xlabel("likelihood")
    pl.ylabel("frequencies (log scale)")
    pl.show()

def output_site_and_rates(inFile, number_of_ks, which_cat):
    # Get dictionary of rates and categories
    rate_dict = rates_and_categories(inFile, number_of_ks)
    # Return list of rates associated with specified category
    if which_cat not in rate_dict.keys():
        raise ValueError("Specified category does not exist!")
    else:
        return rate_dict[which_cat]


if __name__ == '__main__':
    # file1 = sys.argv[1]
    # inFile = open(file1)
    # number_of_ks = int(sys.argv[2])
    # cluster_histogram(inFile, number_of_ks, 300)
    # # x = output_site_and_rates(inFile, number_of_ks, 0)
    # inFile.close()
    # file2 = open("output_of_first_cat.txt", "a")
    # for i in x:
    #     file2.write(str(i) + "\n")
    # file2.close()
    in_file = sys.argv[1]
    phyml_lk_file = open(in_file)
    rate_cat_dict = rates_from_categories(phyml_lk_file)
    kmeans_multi_dim(rate_cat_dict, 8)
    phyml_lk_file.close()
