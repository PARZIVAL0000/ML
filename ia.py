#!/usr/bin/env python3
#_*_ coding:utf-8 _*_

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

datos = pd.read_csv('Book.csv')
df = pd.DataFrame(datos)

# de este "df" debemos sacarlos vlaores para x y para y
x = df['cast_total_facebook_likes'].values
y = df['imdb_score'].values


print("=====================================================================")
print("[*] Valor maximo de likes: ", df['cast_total_facebook_likes'].max())
print("[*] Valor minimo de likes: ", df['cast_total_facebook_likes'].min())
print("=====================================================================")
print("[**] El promedio total de los valores son: ", df['cast_total_facebook_likes'].mean())
print("=====================================================================")

# info = df[['cast_total_facebook_likes', 'imdb_score']]
X = np.array(list(zip(x, y)))


#agrupamiento o clustering.
kmeans = KMeans(n_clusters=2)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_

#vamos a ver en una grafica...
colors = ["m.", "r.", "c.", "y.", "b."]

for i in range(len(X)):
    print("Coordenada: ", X[i], " Label: ", labels[i])
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)


plt.scatter(centroids[:,0], centroids[:,1], marker='x', s=150, linewidths=5, zorder=10)

plt.show()