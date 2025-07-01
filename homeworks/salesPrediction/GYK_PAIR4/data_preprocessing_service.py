from database import Database
import pandas as pd
from regions import cities_regions

db = Database()

# order ve order_details birleştiriliyor.
main_details = db.get_orders_with_details()
#print("\n--- MAIN---")
df = pd.DataFrame(main_details)
#print(df)

# Eksik veri olup olmadığını kontrol etmek için aşağıdaki satır aktif edilebilir:
# print(df.isnull().sum())

# şehir bilgisine göre her satıra manuel olarak bir "region"  atanmasını sağlıyor
df["region"] = df["city"].replace(cities_regions)

# Region atamaları sonrası kontrol etmek istersen:
# print(df)
# print(df.isnull().sum())
# df_exp=df[["city","region"]]
# print(df_exp.drop_duplicates())

# order_date sütunu, string (object) tipindeyse datetime tipine çevriliyor. defalult olarak yyyy-mm-dd formatında.
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# Tip dönüşüm sonrası kontrol etmek istersen:
# print(df.dtypes)
# print(df["order_date"].isnull().sum())

# Tarih dönüşümü sonrası verileri görmek istersen:
#print(df)


# Bağlantıyı kapat
db.close()
