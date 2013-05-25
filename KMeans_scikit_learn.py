import sys
import time

import numpy as np
import pylab as pl

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale

from collections import defaultdict

start = time.clock()
file1 = sys.argv[1]
number_of_ks = int(sys.argv[2])

inFile = open(file1)


def kmeans(inFile, number_of_ks):
    list_of_rates = [line for line in inFile.readlines()]
    newest_list_of_rates = []
    for i in list_of_rates:
        newp = float(i.strip("\n"))
        newest_list_of_rates.append([newp])

    array = np.array(newest_list_of_rates, ndmin = 1)

    print array

    #array = scale(array)

    #print array

    KMeans_out = KMeans(init='k-means++', n_clusters = number_of_ks, \
        n_init = 10)

    KMeans_out.fit(array)

    centroids = KMeans_out.cluster_centers_
    list_of_categories = KMeans_out.labels_
    char_number = 1
    dictionary_of_characters_and_rates = {}
    for i in list_of_categories:
    	dictionary_of_characters_and_rates[char_number] = i
    	char_number += 1

    print "Centroids: " + str(centroids)
    print "All categories: " + str(list_of_categories)

    stop = time.clock()
    time_taken = "This analysis took " + str(stop - start) + "seconds!"
    print time_taken

    return dictionary_of_characters_and_rates

def RAxML_categories(inFile, number_of_ks):
	characters_and_rates = kmeans(inFile, number_of_ks)
	output_dict = defaultdict(list)
	for k, v in characters_and_rates.iteritems():
		output_dict[v].append(k)

	outFile = open("RAxML_scheme.txt", "a")
	partition = 0
	for i in range(len(output_dict)):
		outFile.write("Partition " + str(partition) + ", DNA = " + str(output_dict[partition]).strip("[]") + "\n")
		print "Partition " + str(partition) + ", DNA = " + str(output_dict[partition])
		partition += 1
	outFile.close()

RAxML_categories(inFile, number_of_ks)

inFile.close()




