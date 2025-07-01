# Customer Segmentation with DBSCAN

Bu proje, Northwind veritabanı üzerinde DBSCAN algoritması kullanarak farklı segmentasyon analizleri yapan bir API uygulamasıdır.

## Proje Yapısı

```
customerSegmentationWithDBSCAN/
├── problem1/                 # Müşteri segmentasyonu implementasyonu
│   └── customer_segmentation.py
├── problem2/                 # Ürün kümeleme implementasyonu
│   └── product_clustering.py
├── problem3/                 # Tedarikçi segmentasyonu implementasyonu
│   └── supplier_segmentation.py
├── problem4/                 # Ülkelere göre satış deseni analizi
│   └── country_analysis.py
├── utils/                    # Ortak kullanılan fonksiyonlar
│   └── database.py
├── main.py                  # FastAPI uygulaması
├── requirements.txt         # Proje bağımlılıkları
└── README.md               # Bu dosya
```

## Gereksinimler

- Python 3.8+
- PostgreSQL veritabanı
- Northwind veritabanı

## Kurulum

1. Sanal ortam oluşturun:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. `.env` dosyasını oluşturun:
```
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=your_database
```

## API Endpoints

### 2. Ürün Kümeleme
- **Endpoint**: `/api/v1/product-clusters`
- **Method**: POST
- **Açıklama**: Benzer sipariş geçmişine sahip ürünleri gruplandırır
- **Parametreler**:
  - `eps`: DBSCAN epsilon parametresi (varsayılan: 0.5)
  - `min_samples`: DBSCAN min_samples parametresi (varsayılan: 5)

### 3. Tedarikçi Segmentasyonu
- **Endpoint**: `/api/v1/supplier-clusters`
- **Method**: POST
- **Açıklama**: Tedarikçileri sağladıkları ürünlerin satış performansına göre gruplandırır
- **Parametreler**:
  - `eps`: DBSCAN epsilon parametresi (varsayılan: 0.5)
  - `min_samples`: DBSCAN min_samples parametresi (varsayılan: 5)

### 4. Ülkelere Göre Satış Deseni Analizi
- **Endpoint**: `/api/v1/country-clusters`
- **Method**: POST
- **Açıklama**: Farklı ülkelerden gelen siparişleri gruplandırır
- **Parametreler**:
  - `eps`: DBSCAN epsilon parametresi (varsayılan: 0.5)
  - `min_samples`: DBSCAN min_samples parametresi (varsayılan: 5)

## Örnek Kullanım

### cURL ile
```bash

# Ürün kümeleme
curl -X POST "http://localhost:8000/api/v1/product-clusters" \
     -H "Content-Type: application/json" \
     -d "{\"eps\": 0.5, \"min_samples\": 5}"

# Tedarikçi kümeleme
curl -X POST "http://localhost:8000/api/v1/supplier-clusters" \
     -H "Content-Type: application/json" \
     -d "{\"eps\": 0.5, \"min_samples\": 5}"

# Ülke analizi
curl -X POST "http://localhost:8000/api/v1/country-clusters" \
     -H "Content-Type: application/json" \
     -d "{\"eps\": 0.5, \"min_samples\": 5}"
```

### Python ile
```python
import requests
import json

# Müşteri segmentasyonu
response = requests.post(
    "http://localhost:8000/api/v1/customer-clusters",
    json={"eps": 0.5, "min_samples": 5}
)
print(json.dumps(response.json(), indent=2))
```

## API Dokümantasyonu

Uygulama çalışırken aşağıdaki adreslerden API dokümantasyonuna erişebilirsiniz:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Analiz Sonuçları

Her endpoint aşağıdaki bilgileri döndürür:
- Kümeleme sonuçları
- Her küme için ortalama değerler
- Küme büyüklükleri
- Sıra dışı örnekler (-1 kümesi)

## Notlar

- DBSCAN parametreleri (`eps` ve `min_samples`) veri setinize göre ayarlanmalıdır
- -1 kümesi, sıra dışı veya aykırı değerleri temsil eder
- Veritabanı bağlantı bilgileri `.env` dosyasında saklanmalıdır 