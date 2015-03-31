import pandas as pd
import pickle
from sklearn.cluster import KMeans

#data = pd.read_csv("/home/drew/enmusic.csv")
data = pd.read_csv("/home/drew/gpmusic_fixed.csv")

#print data[['id']].describe()

rfcTitle = data[['title','energy','tempo','danceability','artist_discovery','speechiness','duration','acousticness','liveness','loudness','time_signature','valence','id']]
rfcTitle = rfcTitle.dropna(subset = filter(lambda x: x != "albumArtRef", rfcTitle.columns))
rfc = rfcTitle[['energy','tempo','danceability','artist_discovery','speechiness','acousticness','liveness','loudness','time_signature','valence']]

km = KMeans(5)
km.fit(rfc.values)
pickle.dump(km, open( "/home/drew/tempo_scripts/tempo_model.p", "wb" ))
