# Veriler arasındaki benzerliklere göre küme oluşturmak için kullanılır
# indirimi bekleyenler, pahalı ürün satın alanlar
# etiketleme yok

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator  # Dirsek tespiti için

# müşteri gelir ve harcama
X = np.array([
    [15,39], [16,87], [23,72], [41,99], [73,67], [23,11], [93,35], [11,78], [34,55], [32,49], [12,64], [72,34], [22,94],
])

kmeans = KMeans(n_clusters=3, random_state=42)

kmeans.fit(X)
labels = kmeans.labels_

plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='rainbow')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, marker='X', c='black')
plt.xlabel("Gelir")
plt.ylabel("Harcama")
plt.title("K-means ile Müşteri Segmentasyonu")
plt.show()


# Elbow yöntemi
wss = []  # her k için WSS değerleri

K = range(1, 10)  # 1'den 9'a kadar deniyoruz
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    wss.append(kmeans.inertia_)  # inertia_ = toplam küme içi hata kareleri (WSS)

# Elbow (dirsek) noktasını bul
knee = KneeLocator(K, wss, curve='convex', direction='decreasing')
optimal_k = knee.elbow
print("Optimal k (elbow noktası):", optimal_k)

# Grafiği çiz
plt.plot(K, wss, 'bo-')
plt.xlabel('Küme Sayısı (k)')
plt.ylabel('WSS (Toplam Hata)')
plt.title('Elbow Yöntemi ile Optimal k Değeri Seçimi')
plt.axvline(x=optimal_k, color='r', linestyle='--', label=f"Elbow Noktası: k={optimal_k}")
plt.legend()
plt.show()

