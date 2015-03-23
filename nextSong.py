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

pid = sys.argv[1]
bpm = float(sys.argv[2])
cluster = int(sys.argv[3])

data = pd.read_csv("/home/drew/gpmusic_fixed.csv")

rfcTitle = data[['artist','title','energy','tempo','danceability','artist_discovery','speechiness','year','duration','trackType','acousticness','liveness','loudness','time_signature','valence','id','albumArtRef']]
rfcTitle = rfcTitle.dropna(subset = filter(lambda x: x != "albumArtRef", rfcTitle.columns))
rfc = rfcTitle[['energy','tempo','danceability','artist_discovery','speechiness','year','trackType','acousticness','liveness','loudness','time_signature','valence']]

km = pickle.load(open("/home/drew/tempo_scripts/tempo_model.p", "rb" ))
klbls = km.labels_
rfcTitle['label'] = klbls

results = []

for index, value in enumerate(rfcTitle.values):
    results.append({'artist': value[0], 'title': value[1], 'energy': value[2], 'tempo': value[3], 'danceability': value[4], 'artist_discovery': value[5], 'speechiness': value[6], 'year': value[7], 'duration': value[8], 'trackType': value[9], 'acousticness': value[10], 'liveness': value[11], 'loudness': value[12], 'time_signature': value[13], 'valence': value[14], 'cluster': value[17], 'id': value[15], 'albumArtRef': value[16]})

clusters = [[],[],[],[],[]]
ret = {'choices': []}
for i, v in enumerate(results):
    clusters[int(v['cluster'])].append(v)

songs = []
for i, v in enumerate(clusters[cluster]):
    if bpm > float(clusters[cluster][i]['tempo'])*.9 and bpm < float(clusters[cluster][i]['tempo'])*1.1:
	songs.append(clusters[cluster][i])

webapi = Webclient()
webapi.login('atyourtempo@gmail.com', 'musicatyourspeed')
api = Mobileclient()
logged_in = api.login('atyourtempo@gmail.com', 'musicatyourspeed')

playlists = api.get_all_user_playlist_contents()
playlist = []
for i,v in enumerate(playlists):
    if v['id'] == pid:
	playlist = v['tracks']
	break

song = {}
tids = []

for i,v in enumerate(playlist):
    tids.append(v['trackId'])

for i,v in enumerate(songs):
    if v['id'] not in tids:
	song = v

guid = song['id']
device = webapi.get_registered_devices()
streamURL = api.get_stream_url(guid, device[0]['id'][2:])
#pid = api.create_playlist("Tempo: " + dt.datetime.now().strftime("%m-%d-%Y %I:%M:%S%p"))
api.add_songs_to_playlist(pid, guid)
print json.dumps({"streamURL": streamURL, "playlistId": pid, "song": song}, indent=4, separators=(',', ': '))
