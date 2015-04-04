from gmusicapi import Mobileclient
import json
import requests
import sys
from clusters2list import *
import pandas as pd
requests.packages.urllib3.disable_warnings()
api = Mobileclient()
logged_in = api.login('atyourtempo@gmail.com', 'musicatyourspeed')

pid = sys.argv[1]

#playlists = api.get_all_playlists()
#print json.dumps(playlists, indent=4, separators=(',', ': '))
plsongs = api.get_all_user_playlist_contents()
#print json.dumps(plsongs, indent=4, separators=(',', ': '))

#data = pd.read_csv("/home/drew/gpmusic_fixed.csv")

allpls = {"playlists": []}

for pi, plst in enumerate(plsongs):
    ret = {'name': "",'songs': []}
    if plst['id'] == pid or pid == "all":
	ret['name'] = plsongs[pi]['name']
        for i,v in enumerate(plsongs[pi]['tracks']):
	    for i2,v2 in enumerate(allsongs):
	        if v2['id'] == v['trackId']:
		    ret['songs'].append(v2)
		    break
    allpls['playlists'].append(ret)

print json.dumps(allpls, indent=4, separators=(',', ': '))
