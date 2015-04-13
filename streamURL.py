from gmusicapi import Mobileclient
#from gmusicapi import Webclient
import json
import requests.packages.urllib3
import sys
import datetime as dt
requests.packages.urllib3.disable_warnings()

#data = pd.read_csv("/home/drew/tempo_scripts/gpmusic_fixed.csv")

#webapi = Webclient()
#webapi.login('atyourtempo@gmail.com', 'musicatyourspeed')
api = Mobileclient()
logged_in = api.login('atyourtempo@gmail.com', 'musicatyourspeed')

#library = api.get_all_songs()

guid = sys.argv[1]
try:
    action = sys.argv[2]
except:
    action = ""

#library = api.get_track_info('Ttk6fmoytroyauv2simicl62hlu')
#print data[['storeId','id']]
#for i,v in data.iterrows():
#    for i2,v2 in enumerate(library):
#	if v2['storeId'] == data.loc[i, "storeId"]:
#	    print i
#	    data.loc[i, "id"] = v2['id']
#	    library.pop(i2)
#	    break

#data.to_csv("gpmusic_fixed.csv")

#print data.describe()

#print json.dumps(library[len(library)-1], indent=4, separators=(',', ': '))
#print json.dumps(library, indent=4, separators=(',', ': '))

#device = webapi.get_registered_devices()
#streamURL = api.get_stream_url(guid, device[0]['id'][2:])
streamURL = api.get_stream_url(guid, '320b3128904ea650')
if action == "":
    pid = api.create_playlist("Tempo: " + dt.datetime.now().strftime("%m-%d-%Y %I:%M:%S%p"))
    api.add_songs_to_playlist(pid, guid)
    #print json.dumps(device, indent=4, separators=(',', ': '))
    #print webapi.get_stream_urls(library['storeId'])
    print json.dumps({"streamURL": streamURL, "pid": pid}, indent=4, separators=(',', ': '))
else:
    print json.dumps({"streamURL": streamURL}, indent=4, separators=(',', ': '))
