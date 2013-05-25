#This program will split a list of rates into kmeans clusters
#and output the number of observations within each cluster, as
#well as a histogram representing the distribution of rates.
#To use, call python, enter the name of the program (KMeans_SciPy.py)
#then the name of your file containing rates separated by line breaks
#and the number of desired k's separated by spaces.

import sys
import numpy as np
from scipy import cluster
import pylab as pl

#assign file specified in argument to variable
inFile = open(sys.argv[1])
#assign number of k's specified in command to variable
number_of_ks = int(sys.argv[2])

def kmeans(inFile, number_of_ks, num_iters):
    '''
    returns an array of character classes in order of character number
    and an array of centroids, requires input of a file of rates separated
    by newline characters, the number of desired k's, and the number of
    iterations of the kmeans algorithm
    '''
    #make list of rates from rate file
    list_of_rates = [line for line in inFile.readlines()]
    #create empty list to append rates without newline characters
    rate_list = []
    #loop through list of rates and remove newline characters, append
    #rate represented as a float into empty rate list
    for i in list_of_rates:
        newp = float(i.strip("\n"))
        rate_list.append(newp)

    #create a one dimensional array for input into SciPy's implementation of kmeans
    array = np.array(rate_list, ndmin = 1)

    #performs kmeans clustering on array
    KMeans_out = cluster.vq.kmeans2(array, k = number_of_ks, \
        iter = num_iters, minit = 'points')

    #assign the rates to variable as array
    all_rates = KMeans_out[1]
    #assign centroids to variable as array
    centroids = KMeans_out[0]
    #make a list of the number of k's specified by user
    list_ks = range(number_of_ks)
    count = 0
    number_in_rate_class = []
    #loop through the number of user specified k's and determine how many characters
    #belong to each rate class
    for i in list_ks:
        total_char = 0
        for p in all_rates:
            if p == list_ks[count]:
                total_char += 1
        number_in_rate_class.append(total_char)
        count += 1

    #print the number of characters in each rate class followed by the centroid
    #for that rate class, (coded to check to ensure that rate classes and centroids
    #make sense in comparison to distribution of rates)
    for i in list_ks:
        print "Rate class " + str(i + 1) + " has " \
        + str(number_in_rate_class[i]) + \
        " observations, centroid is " + str(centroids[i]) + "!"
    return all_rates, centroids

print kmeans(inFile, number_of_ks, 100)

def histogram_generator(rate_list, num_bins, title):
    '''
    Plots histogram given a user defined rate list, user
    specified number of bins, and user specified title
    '''
    pl.hist(rate_list, bins = num_bins, facecolor = 'red')
    pl.title(title)
    pl.xlabel("rates")
    pl.ylabel("Frequency")
    pl.show()

inFile.close()