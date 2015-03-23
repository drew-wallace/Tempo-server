from gmusicapi import Mobileclient
from gmusicapi import Webclient
import json
import requests
import sys
import pandas as pd
import datetime as dt
import pickle
from sklearn.cluster import KMeans
requests.packages.urllib3.disable_warnings()
api = Mobileclient()
logged_in = api.login('atyourtempo@gmail.com', 'musicatyourspeed')

sid = sys.argv[0]

data = pd.read_csv("/home/drew/gpmusic_fixed.csv")

rfcTitle = data[['artist','title','energy','tempo','danceability','artist_discovery','speechiness','year','duration','trackType','acousticness','liveness','loudness','time_signature','valence','id','albumArtRef','storeId']]
rfcTitle = rfcTitle.dropna(subset = filter(lambda x: x != "albumArtRef", rfcTitle.columns))
rfc = rfcTitle[['energy','tempo','danceability','artist_discovery','speechiness','year','trackType','acousticness','liveness','loudness','time_signature','valence']]

km = pickle.load(open("/home/drew/tempo_scripts/tempo_model.p", "rb" ))
klbls = km.labels_
rfcTitle['label'] = klbls

results = []

for index, value in enumerate(rfcTitle.values):
    results.append({'artist': value[0], 'title': value[1], 'energy': value[2], 'tempo': value[3], 'danceability': value[4], 'artist_discovery': value[5], 'speechiness': value[6], 'year': value[7], 'duration': value[8], 'trackType': value[9], 'acousticness': value[10], 'liveness': value[11], 'loudness': value[12], 'time_signature': value[13], 'valence': value[14], 'cluster': value[18], 'id': value[15], 'albumArtRef': value[16], 'storeId': value[17]})

#playlists = api.get_all_playlists()
#print json.dumps(playlists, indent=4, separators=(',', ': '))
plsongs = api.get_all_user_playlist_contents()
#print json.dumps(plsongs, indent=4, separators=(',', ': '))

data = pd.read_csv("/home/drew/gpmusic_fixed.csv")
ret = {'results': []}

for i,v in enumerate(plsongs[0]['tracks']):
    for i2,v2 in enumerate(results):
        #print v2['storeId'], "==", plsongs[i]['track']['storeId']
        if v2['id'] == v['trackId']:
            ret['results'].append(v2)
            break
print json.dumps(plsongs, indent=4, separators=(',', ': '))
print json.dumps(ret, indent=4, separators=(',', ': '))
