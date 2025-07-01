import pandas as pd
import numpy as np
import requests

import calendar
from datetime import datetime

customer_url="http://localhost:3000/customers"
product_url="http://localhost:3000/products"
category_url="http://localhost:3000/categories"
order_url="http://localhost:3000/orders"
orderdetail_url="http://localhost:3000/orderDetails"

def getCustomers():  
    response=requests.get(customer_url)
    return response.json()
     
def getProducts():
    response=requests.get(product_url)
    return response.json()

def getCategories():
    response=requests.get(category_url)
    return response.json()

def getOrders():
    response=requests.get(order_url)
    return response.json()

def getOrderDetails():
    response=requests.get(orderdetail_url)
    return response.json()


#data_df=pd.read_json("C:\GYK\RunningApis\MEFSHOP.json")
#print(data_df)

customer_df=pd.DataFrame(getCustomers())
print(customer_df.isnull().sum())

product_df=pd.DataFrame(getProducts())
print(product_df.isnull().sum())

category_df=pd.DataFrame(getCategories())
print(category_df.isnull().sum())

order_df=pd.DataFrame(getOrders())
print(order_df.isnull().sum())

orderDetail_df=pd.DataFrame(getOrderDetails())
print(orderDetail_df.isnull().sum(), "\n")

# 2. VERI MANIPULASYONU

# Eksik verileri tespit edip doldurma veya kaldırma
print("Eksik verileri tespit edip doldurma veya kaldırma \n")
 
#'orderDetails' ve 'products' tablolarını 'productID' üzerinden birleştiriyoruz
orderDetail_df = orderDetail_df.merge(product_df[['id', 'categoryID']], on='id', how='left', suffixes=('', '_from_products'))

#Eksik categoryID'leri 'categoryID_from_products' ile dolduruyoruz
orderDetail_df['categoryID'] = orderDetail_df['categoryID'].fillna(orderDetail_df['categoryID_from_products'])

#Geçici olarak eklediğimiz 'categoryID_from_products' sütununu siliyoruz
orderDetail_df.drop(columns=['categoryID_from_products'], inplace=True)

print(orderDetail_df)
print(type(orderDetail_df), "\n")


# Tarih formatlarını uygun hale getirme
print("Tarih formatlarını uygun hale getirme \n")


def date_edit():
    return orderDetail_df.loc[orderDetail_df["orderDate"]!="INVALID_DATE"]
    #return orderDetail_df.loc[orderDetail_df["orderDate"]=="INVALID_DATE"] #where kosulu gibi

import json
import re

with open("mef_Shop_son.json", "r", encoding="utf-8") as file:
    data = json.load(file)

category_defaults = {c["categoryName"]: f"2025.{c['id']:02d}.01" for c in data["categories"]}
category_dates = {}

def fix_date(order):
    date=order.get("orderDate","INVALID_DATE")
    if date == "INVALID_DATE":
        return "2025.01.01"
    match = re.match(r"(\d{4})-.-.", date)
    if match:
        y, m, d = match.groups()
        return f"{y}.{d}.{m}" if int(m) > 12 else f"{y}.{m}.{d}"
    return date

for order in data.get("orders",[]):
    order["orderDate"] = fix_date(order)

with open("MEFSHOP_fixed.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("Düzeltilmiş dosya kaydedildi: MEFSHOP_fixed.json")


#print(date_edit())
#category_medians = orderDetail_df.groupby("categoryID")["orderDate"].transform(lambda x: x.fillna(x.median()))


# Belirli kategorilere gore fiyat degistirme
print("Belirli kategorilere gore fiyat degistirme \n")

product_df["price"] = product_df["price"].astype(float)

product_df.loc[product_df["categoryID"]==2,"price"]*=0.8
print(product_df, "\n")


# Müşteri memnuniyeti puanlarını analiz ederek en popüler ürünleri belirleme
print("Müşteri memnuniyeti puanlarını analiz ederek en popüler ürünleri belirleme \n")

pop_product=orderDetail_df.sort_values("customerSatisfiedScore",ascending=False)
pop_urun= pop_product.merge(product_df, left_on="categoryID", right_on="categoryID", how="left")
print(pop_urun[["productName", "customerSatisfiedScore"]], "\n")
#print(orderDetail_df["orderDate"][297])


# 3. VERI ANALIZI

# En cok satin alinan urunler
print("En cok satin alinan urunler \n")

totalSales=orderDetail_df.groupby('id')['quantity'].sum().reset_index()
top_selling_product=totalSales.sort_values(by="quantity",ascending=False)
print("en cok satin alinan urunler",top_selling_product, "\n")


# Fiyat ve satış miktarı arasındaki korelasyonu inceleyin
print("Fiyat ve satış miktarı arasındaki korelasyonu inceleyin \n")

cok_satanlar = orderDetail_df.groupby("id")["quantity"].sum().reset_index()
cok_satanlar = cok_satanlar.merge(product_df, on="id")

correlation = cok_satanlar[["price", "quantity"]].corr()
print("Fiyat ve satış miktarı arasındaki korelasyon:")
print(correlation, "\n")


# Kategorilere göre ortalama fiyatı hesapla
print("Kategorilere göre ortalama fiyatı hesapla \n")

# categoryID bir sayı ise float veya int türüne çevirmek daha uygun olur: (yukarıda float yaptık)
orderDetail_df["categoryID"] = pd.to_numeric(orderDetail_df["categoryID"], errors="coerce")
category_df["id"] = pd.to_numeric(category_df["id"], errors="coerce")

merged = orderDetail_df.merge(category_df, left_on='categoryID', right_on='id')
result = merged.groupby('categoryName')['unitPrice'].mean().reset_index()
print("resulttt:",result, "\n")


# Belirli bir zaman diliminde en çok satılan ürünleri bulun
print("Belirli bir zaman diliminde en çok satılan ürünleri bulun \n")

# top_selling_products = (
#     orderDetail_df[orderDetail_df["orderDate"].between("2023-01-01", "2023-01-31")]
#     .groupby("id", as_index=False)["quantity"].sum()
#     .sort_values(by="quantity", ascending=False)
# )
# print(" belirli zamanda toplam satilan urunler ", top_selling_products )


# orderID sütunlarının veri türünü kontrol et
print(orderDetail_df["orderID"].dtype)  # orderDetail_df'deki orderID'nin veri tipi
print(order_df["id"].dtype)             # order_df'deki id'nin veri tipi

# orderID'yi int64 türüne dönüştür
orderDetail_df["orderID"] = orderDetail_df["orderID"].astype(int)
order_df["id"] = order_df["id"].astype(int)

# orderDetail_df ile order_df'yi orderID ve id üzerinden birleştiriyoruz
merged_df = orderDetail_df.merge(order_df, left_on="orderID", right_on="id", how="inner")

# Belirli tarih aralığındaki satışları filtreliyoruz
top_selling_products = (
    merged_df[merged_df["orderDate"].between("2023-01-01", "2023-01-31")]
    .groupby("productId", as_index=False)["quantity"].sum()
    .sort_values(by="quantity", ascending=False)
)

print("Belirli zamanda toplam satılan ürünler:", top_selling_products)


# Müşteri harcama seviyelerine göre gruplama yapın
print("Müşteri harcama seviyelerine göre gruplama yapın \n")

# merged = orderDetail_df.merge(order_df, left_on='orderID', right_on='id') #Sipariş detaylarını siparişler ile birleştir

# merged = merged.merge(customer_df, left_on='customerID', right_on='id', suffixes=('_order', '_customer')) #Müşterileri detaylarla birleştir

# merged['totalSpent'] = merged['unitPrice'] * merged['quantity'] #Toplam harcamayı hesapla

# customer_spending = merged.groupby('customerName')['totalSpent'].sum().reset_index() #Müşteriye göre toplam harcamayı hesapla

# levels = [0, 1000, 15000, 30000] #Harcama seviyelerine göre gruplama yap
# labels = ['Düşük Harcama', 'Orta Harcama', 'Yüksek Harcama']
# customer_spending['spendingLevel'] = pd.cut(customer_spending['totalSpent'], bins=levels, labels=labels)

# print(customer_spending)


# 4. DINAMIK FIYATLANDIRMA

# Ürünlerin ortalama fiyatlarını hesaplayarak aşırı pahalı veya ucuz ürünleri belirleyin
# Piyasadan belirli bir oranda düşük fiyatlı ürünlerin fiyatını güncelleyin
print("Ürünlerin ortalama fiyatlarını hesaplayarak aşırı pahalı veya ucuz ürünleri belirleyin")
print("Piyasadan belirli bir oranda düşük fiyatlı ürünlerin fiyatını güncelleyin \n")

total_sales = orderDetail_df.groupby("id")["quantity"].sum().reset_index() #urun adet sayisi bul

top_selling_product = total_sales.sort_values(by="quantity", ascending=False)

top_selling_product = top_selling_product.merge(product_df, left_on="id", right_on="id", how="left")

ortalama_fiyat = top_selling_product["price"].mean()

ucuz_esik = ortalama_fiyat * 0.8  # %20 düşük olanlar
pahali_esik = ortalama_fiyat * 1.2  # %20 yüksek olanlar

ucuz_urunler = top_selling_product[top_selling_product["price"] < ucuz_esik]
pahali_urunler = top_selling_product[top_selling_product["price"] > pahali_esik]

top_selling_product.loc[top_selling_product["price"] < ucuz_esik, "price"] = ucuz_esik

print("Güncellenmiş fiyatlar:")
for row in top_selling_product[["productName", "price"]].itertuples(index=False):
    print(f"{row.productName}: {row.price} TL")


# 5. URUN ONERI SISTEMI

# Müşterilere, satın aldıkları ürünlere benzer en popüler ürünleri önerin Öneri sistemini kategori bazında geliştirin

kategori_satislari = orderDetail_df.groupby("categoryID", as_index=False)["quantity"].sum()
kategori_satislari = kategori_satislari.merge(product_df, on="categoryID", how="left")
kategori_satislari = kategori_satislari.sort_values(by=["categoryID", "quantity"], ascending=[True, False])

def urun_onerisi(urun): #Aynı kategorideki en çok satan ürünleri öner
# Aynı kategoride olup, kendisi olmayan ürünleri filtrele
    ayni_kategori_urunleri = kategori_satislari[(kategori_satislari["categoryID"] == product_df["categoryID"]) &
                                                (kategori_satislari["id"] != product_df["id"])]
    top_urunler = ayni_kategori_urunleri.nlargest(3, "quantity")["productName"].tolist()
    return top_urunler if top_urunler else ["Öneri bulunamadı"]


#satis_toplam["onerilen_urunler"] = satis_toplam.apply(urun_onerisi, axis=1)

#print("\nÜrün Önerileri:")
#for urun_adi, oneriler in zip(satis_toplam["productName"], satis_toplam["onerilen_urunler"]):
#print(f"{urun_adi} için önerilen ürünler: {', '.join(oneriler)}"
