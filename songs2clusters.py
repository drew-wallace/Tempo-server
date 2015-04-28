import pandas as pd
import pickle, sys, math
from sklearn.cluster import KMeans
pd.options.mode.chained_assignment = None

#data = pd.read_csv("/home/drew/enmusic.csv")
data = pd.read_csv("/home/drew/gpmusic_fixed.csv")

#print data[['id']].describe()

rfcTitle = data[['artist','title','energy','tempo','danceability','artist_discovery','speechiness','year','duration','trackType','acousticness','liveness','loudness','time_signature','valence','instrumentalness','id','albumArtRef','storeId']]
rfcTitle.instrumentalness = rfcTitle.instrumentalness.fillna(rfcTitle.instrumentalness.mean())
rfcTitle = rfcTitle.dropna(subset = filter(lambda x: x != "albumArtRef", rfcTitle.columns))
rfc = rfcTitle[['energy','danceability','artist_discovery','speechiness','acousticness','liveness','loudness','time_signature','valence','instrumentalness']]

km = pickle.load(open("/home/drew/tempo_scripts/10ktempo_model.p", "rb" ))
klbls = km.predict(rfc.values)
rfcTitle['label'] = klbls
#print rfcTitle[['artist','label']]

results = []

for index, value in enumerate(rfcTitle.values):
    results.append({'artist': value[0], 'title': value[1], 'energy': value[2], 'tempo': value[3], 'danceability': value[4], 'artist_discovery': value[5], 'speechiness': value[6], 'year': value[7], 'duration': value[8], 'trackType': value[9], 'acousticness': value[10], 'liveness': value[11], 'loudness': value[12], 'time_signature': value[13], 'valence': value[14], 'instrumentalness': value[15], 'cluster': value[19], 'id': value[16], 'albumArtRef': "none" if type(value[17]) is float else value[17], 'storeId': value[18]})

#results = sorted(results, key=itemgetter('cluster'))

clusters = [[],[],[],[],[],[],[],[],[],[]]
#usedLabels = []
#ret = {'choices': []}
for i, v in enumerate(results):
    #if v['cluster'] not in usedLabels:
        clusters[int(v['cluster'])].append(v)
        #usedLabels.append(v['cluster'])
        #ret['choices'].append(v)

pickle.dump(clusters, open( "/home/drew/tempo_scripts/10kclusters.p", "wb" ))
pickle.dump(results, open( "/home/drew/tempo_scripts/10ksongs.p", "wb" ))
