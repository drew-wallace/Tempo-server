#-*- coding: utf-8 -*-
from gmusicapi import Mobileclient
import urllib, json, csv, time, io

api = Mobileclient()
logged_in = api.login('atyourtempo@gmail.com', 'musicatyourspeed')
# logged_in is True if login was successful

library = api.get_all_songs()
#print json.dumps(library[0], indent=4, separators=(',', ': '))

"""songs = {}
size = len(library)

for i in xrange(len(library)):
    for key, value in library[i].iteritems():
	if songs.get(key) is None:
	    songs[key] = []

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

for i in xrange(len(library)):
    libList = {}
    artist = library[i]['artist']
    title = library[i]['title']
    print str(i) + ": " + artist.encode('utf8') + " - " + title.encode('utf8') + " <br>"

    url = "http://developer.echonest.com/api/v4/song/search?api_key=NHSTSBEENVYUFRLY5&title="+urllib.quote(title.encode('utf8'))+"&artist="+urllib.quote(artist.encode('utf8'))+"&bucket=audio_summary&bucket=artist_discovery&bucket=artist_familiarity&bucket=artist_hotttnesss&bucket=artist_location&bucket=song_currency&bucket=song_discovery&bucket=song_hotttnesss&bucket=song_type"
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

    for key, value in library[i].iteritems():
        if type(value) is list:
            if type(value[0]) is dict:
                temp = value[0]['url']
            else:
                temp = value[0]
        else:
            temp = value
        libList[key] = temp

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
    time.sleep(5)"""

data = open("songs2.txt")
songs = json.load(data)
size = len(songs['title'])

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

with open('gpmusic.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(libSongs)
