import pandas as pd
import pickle
from sklearn.cluster import KMeans
pd.options.mode.chained_assignment = None

data = pd.read_csv("enmusic.csv")
#data = pd.read_csv("/home/drew/gpmusic_fixed.csv")

#print data[['id']].describe()

rfcTitle = data[['title','energy','tempo','danceability','artist_discovery','speechiness','duration','acousticness','liveness','loudness','time_signature','valence','id','instrumentalness']]
rfcTitle.instrumentalness = rfcTitle.instrumentalness.fillna(rfcTitle.instrumentalness.mean())
rfcTitle = rfcTitle.dropna(subset = filter(lambda x: x != "albumArtRef", rfcTitle.columns))
rfc = rfcTitle[['energy','tempo','danceability','artist_discovery','speechiness','acousticness','liveness','loudness','time_signature','valence','instrumentalness']]

km = KMeans(5)
km.fit(rfc.values)
pickle.dump(km, open( "/home/drew/tempo_scripts/10ktempo_model.p", "wb" ))
