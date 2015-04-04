from operator import itemgetter
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import sys

data = pd.read_csv("enmusic.csv")
#data = pd.read_csv("/home/drew/gpmusic_fixed.csv")

#print data.describe()
for i,v in enumerate(data.columns):
    print v, ":", len(data[[v]].dropna().values)

rfcTitle = data[['title','energy','tempo','danceability','artist_discovery','speechiness','duration','acousticness','liveness','loudness','time_signature','valence','instrumentalness','id']]
rfcTitle = rfcTitle.dropna(subset = filter(lambda x: x != "albumArtRef", rfcTitle.columns))
rfc = rfcTitle[['energy','tempo','danceability','artist_discovery','speechiness','acousticness','liveness','loudness','time_signature','valence','instrumentalness']]

print len(rfc.values)
