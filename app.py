from fastapi import FastAPI
import joblib
import pandas as pd
import os
from features import prepare_features

MODEL_PATH = "model.pkl"

app = FastAPI()

# Modeli yükle
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    raise FileNotFoundError("Model bulunamadı. Önce run_pipeline.py ile eğitin.")

@app.get("/")
def root():
    return {"message": "Stock Predictor API çalışıyor"}

@app.get("/predict")
def predict(return_val: float, ma5: float, ma20: float):
    """Günlük özelliklerden tahmin döner"""
    X = pd.DataFrame([[return_val, ma5, ma20]], columns=["Return", "MA5", "MA20"])
    pred = model.predict(X)[0]
    return {"prediction": "artacak" if pred == 1 else "düşecek"}