from gmusicapi import Mobileclient
from gmusicapi import Webclient
import json
import requests
import sys
from sklearn.cluster import KMeans
from clusters2list import *
requests.packages.urllib3.disable_warnings()

pid = sys.argv[1]
bpm = float(sys.argv[2])
cluster = int(sys.argv[3])

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

try:
	guid = song['id']
except:
	library = api.get_all_songs()
	errSong = library[len(library) - 7]
	guid = errSong['id']

device = webapi.get_registered_devices()
streamURL = api.get_stream_url(guid, device[0]['id'][2:])

if guid != 0:
    #pid = api.create_playlist("Tempo: " + dt.datetime.now().strftime("%m-%d-%Y %I:%M:%S%p"))
    api.add_songs_to_playlist(pid, guid)
    print json.dumps({"streamURL": streamURL, "song": song}, indent=4, separators=(',', ': '))
else:
    print json.dumps({"streamURL": streamURL, "song": errSong}, indent=4, separators=(',', ': '))
