from gmusicapi import Mobileclient
from gmusicapi import Webclient
import json
import requests
requests.packages.urllib3.disable_warnings()
api = Mobileclient()
logged_in = api.login('atyourtempo@gmail.com', 'musicatyourspeed')

playlists = api.get_all_playlists()

for i,v in enumerate(playlists):
    api.delete_playlist(v['id'])

print "All playlists deleted"
