# Python imajı
FROM python:3.12-slim

# Çalışma dizinini oluştur
WORKDIR /app

# Gereken dosyaları kopyala
COPY . .

# Gerekli kütüphaneleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uvicorn ile uygulamayı başlat
CMD ["uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8000"]


