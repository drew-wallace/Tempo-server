import pandas as pd
import pickle, sys, json
from sklearn.cluster import KMeans
pd.options.mode.chained_assignment = None

data = pd.read_csv("/home/drew/tempo_scripts/enmusic.csv")
#data = pd.read_csv("/home/drew/gpmusic_fixed.csv")

#print data[['id']].describe()

rfcTitle = data[['title','energy','tempo','danceability','artist_discovery','speechiness','duration','acousticness','liveness','loudness','time_signature','valence','instrumentalness','id','artist_name']]
rfcTitle.instrumentalness = rfcTitle.instrumentalness.fillna(rfcTitle.instrumentalness.mean())
rfcTitle = rfcTitle.dropna(subset = filter(lambda x: x != "albumArtRef", rfcTitle.columns))
rfc = rfcTitle[['energy','tempo','danceability','artist_discovery','speechiness','acousticness','liveness','loudness','time_signature','valence','instrumentalness']]

km = pickle.load(open("/home/drew/tempo_scripts/10ktempo_model.p", "rb" ))
klbls = km.predict(rfc.values)
rfcTitle['label'] = klbls
#print rfcTitle[['artist','label']]

results = []

for index, value in enumerate(rfcTitle.values):
    #results.append({'title': value[0], 'energy': value[1], 'tempo': value[2], 'danceability': value[3], 'artist_discovery': value[4], 'speechiness': value[5], 'duration': value[6], 'acousticness': value[7], 'liveness': value[8], 'loudness': value[9], 'time_signature': value[10], 'valence': value[11], 'instrumentalness': value[12], 'cluster': value[15], 'id': value[13], 'artist_name': value[14]})
    results.append({'title': value[0], 'artist': value[14], 'cluster': value[15]})

#results = sorted(results, key=itemgetter('cluster'))

clusters = [[],[],[],[],[]]
#usedLabels = []
#ret = {'choices': []}
for i, v in enumerate(results):
    #if v['cluster'] not in usedLabels:
        clusters[int(v['cluster'])].append(v)
        #usedLabels.append(v['cluster'])
        #ret['choices'].append(v)
print json.dumps(clusters, indent=4, separators=(',', ': '))
