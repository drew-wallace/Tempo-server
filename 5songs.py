import json, random
from clusters2list import *

randSongs = {'choices': []}
for i, v in enumerate(clusters):
    randSongs['choices'].append(clusters[i][random.randint(0, len(clusters[i])-1)])

print json.dumps(randSongs, indent=4, separators=(',', ': '))

#for i,v in enumerate(allsongs):
#    if v['title'] == "Alone In Memphis":
#	print json.dumps(v, indent=4, separators=(',', ': '))

#print json.dumps(ret, indent=4, separators=(',', ': '))
