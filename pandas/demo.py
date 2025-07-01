# 08-03-2025

import pandas as pd 

#Series -> 1D array
#DataFrame -> 2D array

#Series
dailySales = pd.Series([1500, 2500, 3500, 200, 1500, 1000, 6000])
print(dailySales)

print('Index:', dailySales.index)
print('Values:', dailySales.values)
print('Sum:', dailySales.sum())
print('Mean:', dailySales.mean())
print('Max:', dailySales.max())
print('Min:', dailySales.min())

print(dailySales[3])

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dailySales2 = pd.Series([1500, 2500, 3500, 200, 1500, 100, 600], index = days)
# print(dailySales2[3])
print(dailySales2["Tuesday"])

#DataFrame
salesData = {
    "ProductName": ["Elma", "Armut", "Üzüm", "İncir", "Postakal", "Elma", "Elma", "Portakal"],
    "Price": [200, 100, 500, 300, 40, 50, 120, 120],
    "QuantitySold": [20, 3, 5, 8, 9, 14, 26, 12],
}

df = pd.DataFrame(salesData)
print(df)

print(df["ProductName"])
# df["ProductName"] type ı series, dolayısıyla series fonksiyonlarını kullanabiliriz
print(type(df["ProductName"])) 

print(df["Price"].mean())

# sql deki gibi sorgular yazabiliriz, yani select sorgusunda 2 sütun listelemek istiyorsak aşağıdaki gibi listeleriz
print(df[["ProductName", "Price"]])

print(df.iloc[2]) # index location
print(df.loc[df["ProductName"] == "İncir"]) # location - where koşulu gibi

bestSales = df[df["QuantitySold"] > 10] # 10 dan fazla satanlar
print(bestSales)

df["TotalIncome"] = df["Price"] * df["QuantitySold"] # sql deki gibi yeni bir kolon açmış oluruz
print(df)

print(df.groupby("ProductName")["QuantitySold"].sum()) # sql deki groupBy gibi


# Eksik verilerde çalışmak
salesData2 = {
    "ProductName": ["Elma", "Armut", "Üzüm", "İncir", "Postakal", "Elma", "Elma", "Portakal"],
    "Price": [200, 100, 500, 300, None, 50, None, 120],
    "QuantitySold": [20, 3, None, 8, 9, 14, 26, 12],
}

df = pd.DataFrame(salesData2)

# isNull sayısı kaç diye bakarız, ona göre napacağımızı düşünürüz domaine göre veya iş ihtiyaçlarına göre
# veri çok önemli ise, olmadan ilerleyemezsek, banka uygulaması ile şube ile iletişime geçilir vs dataya ulaşılmaya çalışır
# eğer veriye ulaşılamıyorsa ortalama alınabilir
# eğer 5 veri var ise null olan ve 5 veri çok önemli değişlse siledebiliriz
print(df.isnull().sum())

# ortalama alınarak doldurulma
df["Price"].fillna(df["Price"].mean(), inplace = True)
print(df)

# null değerleri silme
df.dropna(inplace=True)
print(df)

print(df.sort_values("Price", ascending=True))
print(df.sort_values("Price", ascending=False)) # desc

df.to_csv("salesDataAnalysis.csv", index=False)
df.to_excel("salesDataAnalysis.xlsx", index=False)

