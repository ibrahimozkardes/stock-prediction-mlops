# Base image
FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Gereksinimleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Model dosyasını image içine dahil et (eğitim sonrası Jenkins buraya koyacak)
COPY model/model.pkl /app/model/model.pkl

# FastAPI başlat
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]