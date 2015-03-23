import pandas as pd
import json, random, pickle
from sklearn.cluster import KMeans

data = pd.read_csv("/home/drew/gpmusic_fixed.csv")
#print data[['id']].describe()

rfcTitle = data[['artist','title','energy','tempo','danceability','artist_discovery','speechiness','year','duration','trackType','acousticness','liveness','loudness','time_signature','valence','id','albumArtRef','storeId']]
rfcTitle = rfcTitle.dropna(subset = filter(lambda x: x != "albumArtRef", rfcTitle.columns))
rfc = rfcTitle[['energy','tempo','danceability','artist_discovery','speechiness','year','trackType','acousticness','liveness','loudness','time_signature','valence']]

#km = KMeans(5)
#km.fit(rfc.values)
#pickle.dump(km, open( "/home/drew/tempo_model.p", "wb" ))
km = pickle.load(open("/home/drew/tempo_scripts/tempo_model.p", "rb" ))
klbls = km.labels_
rfcTitle['label'] = klbls
#print rfcTitle[['artist','label']]

results = []

for index, value in enumerate(rfcTitle.values):
    results.append({'artist': value[0], 'title': value[1], 'energy': value[2], 'tempo': value[3], 'danceability': value[4], 'artist_discovery': value[5], 'speechiness': value[6], 'year': value[7], 'duration': value[8], 'trackType': value[9], 'acousticness': value[10], 'liveness': value[11], 'loudness': value[12], 'time_signature': value[13], 'valence': value[14], 'cluster': value[18], 'id': value[15], 'albumArtRef': value[16], 'storeId': value[17]})

#results = sorted(results, key=itemgetter('cluster'))

clusters = [[],[],[],[],[]]
#usedLabels = []
ret = {'choices': []}
for i, v in enumerate(results):
    #if v['cluster'] not in usedLabels:
	clusters[int(v['cluster'])].append(v)
	#usedLabels.append(v['cluster'])
	#ret['choices'].append(v)

randSongs = {'choices': []}
for i, v in enumerate(clusters):
    randSongs['choices'].append(clusters[i][random.randint(0, len(clusters[i])-1)])

print json.dumps(randSongs, indent=4, separators=(',', ': '))

#print json.dumps(ret, indent=4, separators=(',', ': '))

#add usable columns
#test http://scikit-learn.org/stable/modules/generated/sklearn.cluster.Ward.html#sklearn.cluster.Ward
#ask from tier 1 then ask from tier 2 (maybe include songs from other cluster in case they don't want the selected cluster)
