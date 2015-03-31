import json, random
from clusters2list import *

randSongs = {'choices': []}
for i, v in enumerate(clusters):
    randSongs['choices'].append(clusters[i][random.randint(0, len(clusters[i])-1)])

print json.dumps(randSongs, indent=4, separators=(',', ': '))

#print json.dumps(ret, indent=4, separators=(',', ': '))

#add usable columns
#test http://scikit-learn.org/stable/modules/generated/sklearn.cluster.Ward.html#sklearn.cluster.Ward
#ask from tier 1 then ask from tier 2 (maybe include songs from other cluster in case they don't want the selected cluster)
