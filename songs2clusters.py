import pandas as pd
import pickle
from sklearn.cluster import KMeans

#data = pd.read_csv("/home/drew/enmusic.csv")
data = pd.read_csv("/home/drew/gpmusic_fixed.csv")

#print data[['id']].describe()

rfcTitle = data[['title','energy','tempo','danceability','artist_discovery','speechiness','duration','acousticness','liveness','loudness','time_signature','valence','id']]
rfcTitle = rfcTitle.dropna(subset = filter(lambda x: x != "albumArtRef", rfcTitle.columns))
rfc = rfcTitle[['energy','tempo','danceability','artist_discovery','speechiness','acousticness','liveness','loudness','time_signature','valence']]

km = pickle.load(open("/home/drew/tempo_scripts/tempo_model.p", "rb" ))
klbls = km.labels_
rfcTitle['label'] = klbls
#print rfcTitle[['artist','label']]

results = []

for index, value in enumerate(rfcTitle.values):
    results.append({'title': value[0], 'energy': value[1], 'tempo': value[2], 'danceability': value[3], 'artist_discovery': value[4], 'speechiness': value[5], 'duration': value[6], 'acousticness': value[7], 'liveness': value[8], 'loudness': value[9], 'time_signature': value[10], 'valence': value[11], 'id': value[12], 'cluster': value[13]})

#results = sorted(results, key=itemgetter('cluster'))

clusters = [[],[],[],[],[]]
#usedLabels = []
#ret = {'choices': []}
for i, v in enumerate(results):
    #if v['cluster'] not in usedLabels:
        clusters[int(v['cluster'])].append(v)
        #usedLabels.append(v['cluster'])
        #ret['choices'].append(v)

pickle.dump(clusters, open( "/home/drew/tempo_scripts/clusters.p", "wb" ))
pickle.dump(results, open( "/home/drew/tempo_scripts/songs.p", "wb" ))
