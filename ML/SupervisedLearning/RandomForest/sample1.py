# 07-04-2025

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

np.random.seed(42)

n_samples = 2000
area = np.random.randint(50, 250, n_samples)
rooms = np.random.randint(1, 6, n_samples)
age = np.random.randint(0, 50, n_samples)
location_score = np.random.uniform(0, 10, n_samples) # uniform - ondalıklı sayı

noise = np.random.normal(0, 20000, n_samples) # gürültü
price = (area * 3000) + (rooms * 50000) - (age * 1000) + (location_score * 10000) + noise

df = pd.DataFrame({

    "area": area,
    "rooms": rooms,
    "age": age,
    "location_score": location_score,
    "price": price   
})

print(df)

X = df[["area", "rooms", "age", "location_score"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

model = RandomForestRegressor(n_estimators=100,random_state=42) # n_estimators - ağaç sayısı
model.fit(X_train,y_train)
y_prediction = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test,y_prediction))
print("RMSE - Root Mean Squared Error : ", rmse) # kök ortalama kare hatası

# RMSE - Root Mean Squared Error :  26286.552054898704 - ortalama 26 bin liralık bir fark varmış bu da iyi bir hata oranı

# grafik kodu standart
plt.figure(figsize=(8,6))
plt.scatter(y_test, y_prediction, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Gerçek Fiyat')
plt.ylabel('Tahmin Edilen Fiyat')
plt.title('Gerçek vs Tahmin Edilen Ev Fiyatları')
plt.grid(True)
plt.show()