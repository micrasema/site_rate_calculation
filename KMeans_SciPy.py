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


inFile = open(sys.argv[1])
number_of_ks = int(sys.argv[2])

def kmeans(inFile, number_of_ks):
    list_of_rates = [line for line in inFile.readlines()]
    newest_list_of_rates = []
    for i in list_of_rates:
        newp = float(i.strip("\n"))
        newest_list_of_rates.append(newp)

    array = np.array(newest_list_of_rates, ndmin = 1)

    KMeans_out = cluster.vq.kmeans2(array, k = number_of_ks, \
        iter = 100, minit = 'points')

    all_rates = KMeans_out[1]

    centroids = KMeans_out[0]

    list_ks = range(number_of_ks)
    print list_ks
    count = 0
    number_in_rate_class = []
    for i in list_ks:
        numba = 0
        for p in all_rates:
            if p == list_ks[count]:
                numba += 1
        number_in_rate_class.append(numba)
        count += 1

    for i in list_ks:
        print "Rate class " + str(i + 1) + " has " \
        + str(number_in_rate_class[i]) + \
        " observations, centroid is " + str(centroids[i]) + "!"
    return all_rates, centroids

print kmeans(inFile, number_of_ks)
#pl.hist(newest_list_of_rates, bins = 100, facecolor = 'red')
#pl.title("Individual site CI's from insect transcriptome alignment")
#pl.xlabel("rates")
#pl.ylabel("Frequency")
#pl.show()
inFile.close()