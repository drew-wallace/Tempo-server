from gmusicapi import Mobileclient
#from gmusicapi import Webclient
import json
import requests.packages.urllib3
import sys
import random
#from sklearn.cluster import KMeans
from clusters2list import *
requests.packages.urllib3.disable_warnings()

pid = sys.argv[1]
bpm = float(sys.argv[2])
cluster = int(sys.argv[3])

songs = []
for i, v in enumerate(clusters[cluster]):
    sbpm = float(clusters[cluster][i]['tempo'])
    if (bpm >= sbpm-5 and bpm <= sbpm+5) or (bpm*2 >= sbpm-5 and bpm*2 <= sbpm+5) or (bpm/2 >= sbpm-5 and bpm/2 <= sbpm+5):
	songs.append(clusters[cluster][i])

#webapi = Webclient()
#webapi.login('atyourtempo@gmail.com', 'musicatyourspeed')
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

errSong = None
try:
	guid = song['id']
except:
	#library = api.get_all_songs()
	errSong = clusters[cluster][random.randint(0, len(clusters[cluster])-1)]
	guid = errSong['id']

#device = webapi.get_registered_devices()
#print device[0]['id'][2:]
#streamURL = api.get_stream_url(guid, device[0]['id'][2:])
streamURL = api.get_stream_url(guid, '320b3128904ea650')
if errSong is None:
    #pid = api.create_playlist("Tempo: " + dt.datetime.now().strftime("%m-%d-%Y %I:%M:%S%p"))
    api.add_songs_to_playlist(pid, guid)
    print json.dumps({"streamURL": streamURL, "song": song}, indent=4, separators=(',', ': '))
else:
    api.add_songs_to_playlist(pid, guid)
    print json.dumps({"streamURL": streamURL, "song": errSong, "error": "true"}, indent=4, separators=(',', ': '))
