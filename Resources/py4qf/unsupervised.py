#
# Machine Learning
#
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=30, centers=3,
                  random_state=500, cluster_std=1.25) 
model = KMeans(n_clusters=3, random_state=0)
model.fit(X)
print(model.predict(X))
