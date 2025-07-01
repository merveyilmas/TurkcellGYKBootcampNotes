import pandas as pd
import numpy as np

import sys
import os
# Bir üst klasörü sys.path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

import joblib  # Eğittiğimiz modeli .pkl dosyası olarak kaydetmek için

from data_preprocessing_service import df  # df'yi içeri alacağız
demo = df[['product_id', 'unit_price', 'quantity', 'discount', 'order_date']]

#demo["total_price"] = demo["quantity"] * demo["unit_price"] * (1 - demo["discount"])
#demo["month"] = demo["order_date"].dt.month

#1: Winter (Dec-Feb), 2: Spring (Mar-May), 3: Summer (Jun-Aug), 4: Fall (Sep-Nov)
season_mapping = {
12: 1, 1: 1, 2: 1, # Winter
3: 2, 4: 2, 5: 2, # Spring
6: 3, 7: 3, 8: 3, # Summer
9: 4, 10: 4, 11: 4 # Fall
}
#month sütunu eklemeden ay bilgisi çekip mevsim çıkardık
demo['season'] = demo["order_date"].dt.month.map(season_mapping)
#print(demo.head(10))

# 3. X ve y
X = demo[["unit_price", "discount", "season", "product_id"]]
y = demo["quantity"]

# 4. Eğitim ve test verisi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Modeli eğit
model = LinearRegression()
model.fit(X_train, y_train)

# joblib.dump(model, "sales_prediction_model.pkl")
# print("Model başarıyla kaydedildi")

# 6. Tahmin yap & metrikleri hesapla
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("Tahmin sonucu:", y_pred)
print("R2 Score:", r2)
print("RMSE:", rmse)
# R2 score: 0.019, RMSE: 20.55
