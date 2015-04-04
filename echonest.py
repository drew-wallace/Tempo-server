#-*- coding: utf-8 -*-
import urllib, json, csv, time, io, sys
import pandas as pd

data = pd.read_csv("/home/drew/data.csv")
library = data[['song_id']].values
songs = {}
size = len(library)

sys.stderr = open("log.txt", "w")

for key, value in enumerate(library[0]):
    if songs.get('id') is None:
        songs['id'] = []

url = "http://developer.echonest.com/api/v4/song/search?api_key=NHSTSBEENVYUFRLY5&title=thunderstruck&artist=ac/dc&bucket=audio_summary&bucket=artist_discovery&bucket=artist_familiarity&bucket=artist_hotttnesss&bucket=artist_location&bucket=song_currency&bucket=song_discovery&bucket=song_hotttnesss&bucket=song_type"
response = urllib.urlopen(url);
data = json.loads(response.read())['response']['songs'][0]

for key, value in data.iteritems():
    if type(value) is dict:
        for key2, value2 in data[key].iteritems():
	    if songs.get(key2) is None:
                songs[key2] = []
    else:
        if songs.get(key) is None:
            songs[key] = []

#library = library[1585:]

for i in xrange(len(library)):
    libList = {}
    enid = library[i][0]
    print str(i) + ": " + enid + " <br>"

    url = "http://developer.echonest.com/api/v4/song/profile?api_key=NHSTSBEENVYUFRLY5&id="+enid+"&bucket=audio_summary&bucket=artist_discovery&bucket=artist_familiarity&bucket=artist_hotttnesss&bucket=artist_location&bucket=song_currency&bucket=song_discovery&bucket=song_hotttnesss&bucket=song_type"
    response = urllib.urlopen(url)
    data = json.loads(response.read())['response']['songs']
    if len(data) > 0:
	data = data[0]
    else:
	print "--skipped <br>"
	time.sleep(5)
	size -= 1
	continue
    #print json.dumps(data, indent=4, separators=(',', ': '))

    for key, value in enumerate(library[i]):
        libList['id'] = value

    for key, value in data.iteritems():
        if type(value) is dict:
            for key2, value2 in data[key].iteritems():
                libList[key2] = value2
        elif type(value) is list:
            temp = []
            sep = ','
            for key2, value2 in enumerate(value):
                temp.append(str(value2))
            libList[key] = sep.join(temp)
        else:
            libList[key] = value

    for key, value in songs.iteritems():
	if libList.get(key):
	    songs[key].append(libList[key])
	else:
	    songs[key].append("")
    time.sleep(3.2)

size = len(songs['id'])

libKeys = []
libVals = []
libSongs = []
temp = []

for key, value in songs.iteritems():
    if key not in libKeys:
        libKeys.append(key)
libSongs.append(libKeys)

for i in xrange(size):
    temp = []
    for key, value in songs.iteritems():
	temp.append(unicode(songs[key][i]).replace(',', ' '))
    libSongs.append([unicode(s).encode("utf-8") for s in temp])

with open('enmusic.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(libSongs)
