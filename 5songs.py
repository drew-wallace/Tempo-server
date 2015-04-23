import json, random
from clusters2list import *

randSongs = {'choices': []}
count = 0
usedClusters = []
for i in xrange(len(clusters)):
    randCluster = random.randint(0, len(clusters)-1)
    if len(clusters[randCluster]) > 0 and randCluster not in usedClusters:
    	randSongs['choices'].append(clusters[randCluster][random.randint(0, len(clusters[randCluster])-1)])
	usedClusters.append(randCluster)
	count+=1
	if count == 5:
	    break

print json.dumps(randSongs, indent=4, separators=(',', ': '))

#for i,v in enumerate(allsongs):
#    if v['title'] == "Alone In Memphis":
#	print json.dumps(v, indent=4, separators=(',', ': '))

#print json.dumps(ret, indent=4, separators=(',', ': '))
