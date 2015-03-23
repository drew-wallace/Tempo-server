from operator import itemgetter
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

data = pd.read_csv("gpmusic_0.csv")
#print data.describe()
#for x in xrange(len(data.danceability)):
#    print x, data.danceability[x]

tempoCluster = data[['duration','danceability', 'liveness']].values
print tempoCluster

#km = KMeans(5, "k-means++", 10, 300, .0001, True, 1, None, True, 1)
km = KMeans(5)
km.fit(tempoCluster)

print "==================================="

#centers = km.cluster_centers_
#centers[centers<0] = 0
#centers = centers.round(2)
#print "Deal\t Cent1\t Cent2\t Cent3\t Cent4\t Cent5\t"
#for i in range(len(tempoCluster[0])):
#	print i+1, '\t', centers[0,i], '\t', centers[1,i], '\t', centers[2,i], '\t', centers[3,i], '\t', centers[4,i]

#print "==================================="

centers = km.labels_
print "Deal\t Cent1\t Cent2\t Cent3\t Cent4\t Cent5\t"
for i in range(len(tempoCluster[0])):
        print i+1, '\t', centers[i], '\t', centers[i], '\t', centers[i], '\t', centers[i], '\t', centers[i]

print "==================================="

print centers
print len(centers)

print "==================================="

print "Cluster\t Artist\t Title"

#for i in range(len(centers)):
#	print centers[i]+1, '\t', data.artist.values[i], '\t', data.title.values[i]

vals = []

for i in range(len(centers)):
        vals.append({"cluster": centers[i]+1, "artist": data.artist.values[i], "title": data.title.values[i]})

vals =  sorted(vals, key=itemgetter('cluster'))

for i in range(len(vals)):
#	if vals[i]['cluster'] == 1:
		print vals[i]['cluster'], '\t', vals[i]['artist'], '\t', vals[i]['title']
