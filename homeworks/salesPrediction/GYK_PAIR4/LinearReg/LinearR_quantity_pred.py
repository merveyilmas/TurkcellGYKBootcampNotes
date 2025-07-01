import pandas as pd
import joblib

model = joblib.load("sales_prediction_model.pkl")

yeni_veri = pd.DataFrame({
    'unit_price': [13, 16, 22, 22],
    'discount': [0, 0, 0.05, 0.05],
    'season' : [3, 3, 3, 4],
    'product_id':[11, 11, 22, 22]
})
tahmin = model.predict(yeni_veri)
print("Tahmin sonucu:", tahmin)
#Tahmin sonucu: [21.04430006 21.06284431 22.52413304 22.12538503]
