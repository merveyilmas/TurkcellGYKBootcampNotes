# 20-03-2025

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# örnek verilerimiz
data = {
    'Yas': [1, 3, 5, 7, 10],
    'Km': [10, 50, 80, 120, 180],
    'Motor_Hacmi': [1600, 1600, 2000, 2000, 1400],
    'Fiyat': [600000, 400000, 350000, 250000, 150000]
}

df = pd.DataFrame(data)

# Rastgele veri üretimi için örüntüyü belirleyelim
np.random.seed(42)
n_samples = 1000

age = np.random.randint(1, 15, n_samples)  # Araç yaşı 1-15 yıl arasında olacak
km = np.random.randint(5, 250, n_samples)  # Kilometre 5-250 bin arasında olacak
engine_capacity = np.random.choice([1400, 1600, 2000], n_samples)  # Motor hacmi seçenekleri

# Fiyat formülünü basitleştirip örnek verilere göre oluşturalım:
fiyat = (
    600000
    - (age * 30000)   # Yaş arttıkça fiyat düşecek
    - (km * 1000)     # Kilometre arttıkça fiyat düşecek
    + (engine_capacity * 50)  # Motor hacmi yüksek olunca fiyat artsın
    + np.random.randint(-20000, 20000, n_samples)  # Biraz rastgelelik ekleyelim
)

# Üretilen verileri DataFrame'e çevir
generated_data = pd.DataFrame({
    'Yas': age,
    'Km': km,
    'Motor_Hacmi': engine_capacity,
    'Fiyat': fiyat
})

print(generated_data)

# Eğitim ve test setlerini ayır (80% eğitim, 20% test)
X = generated_data[['Yas', 'Km', 'Motor_Hacmi']]
y = generated_data['Fiyat']

print("Bağımsız değişkler: \n", X)
print("Bağımlı değişkler: \n", y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli oluştur ve eğit
model = LinearRegression()
model.fit(X_train, y_train)

# Tahmin yap
y_pred = model.predict(X_test)

print("")

# Model parametrelerini al
print(f"Eğimler (Coefficients): {model.coef_}")
print(f"Kesişme (Intercept): {model.intercept_}")

# Modelinizin doğruluğunu değerlendirmek için hangi metriği kullanırsınız? Açıklayın.

# Performansı ölç
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Ortalama Kare Hata (MSE): {mse:.2f}")
print(f"R² Skoru: {r2:.2f}")

# Modeli eğittikten sonra, 4 yaşında, 70 bin km kullanılmış ve 1600 cc motor hacmine sahip bir aracın fiyatını tahmin edin.

predict_age = 4
predict_km = 70
predict_engine_capacity = 1600

predicted_price = model.predict([[predict_age, predict_km, predict_engine_capacity]])
print(f"Tahmini Fiyat: {predicted_price[0]:,.2f} ₺")