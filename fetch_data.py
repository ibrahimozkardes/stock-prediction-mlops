import os
import time
import datetime
import pandas as pd
import yfinance as yf
import certifi

DATA_FOLDER = "data"

def configure_certs() -> None:
    """C:\\cacert.pem varsa onu, yoksa certifi.where() kullan ve ortam değişkenlerini ayarla."""
    preferred = r"C:\cacert.pem"
    ca_path = preferred if os.path.isfile(preferred) else certifi.where()
    os.environ['SSL_CERT_FILE'] = ca_path
    os.environ['REQUESTS_CA_BUNDLE'] = ca_path
    os.environ['CURL_CA_BUNDLE'] = ca_path
    print(f"[INFO] Kullanılan CA: {ca_path}")

def download_with_retry(symbol: str, start: str, end: str, retries: int = 3, delay: float = 2.0) -> pd.DataFrame:
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            df = yf.download(symbol, start=start, end=end, progress=False, threads=False)
            if df is None or df.empty:
                raise ValueError("Boş veri döndü")
            return df.reset_index()
        except Exception as e:
            last_err = e
            print(f"[WARN] {symbol} deneme {attempt}/{retries} hata: {e}")
            if attempt < retries:
                time.sleep(delay)
    raise RuntimeError(f"{symbol} indirilemedi: {last_err}")

def fetch_or_load(symbol: str) -> pd.DataFrame:
    configure_certs()
    os.makedirs(DATA_FOLDER, exist_ok=True)
    today_str = datetime.date.today().isoformat()
    file_path = os.path.join(DATA_FOLDER, f"{symbol}_{today_str}.csv")

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, parse_dates=["Date"])
        if "Close" in df.columns and pd.api.types.is_numeric_dtype(df["Close"]):
            print(f"📂 Veri bulundu: {file_path}")
            return df
        else:
            print(f"⚠️ Bozuk veri bulundu, siliniyor: {file_path}")
            os.remove(file_path)

    # 1 yıl öncesinden bugüne
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)
    df = download_with_retry(symbol, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
    df.to_csv(file_path, index=False)
    print(f"⬇️ Veri çekildi ve kaydedildi: {file_path} satır={len(df)}")
    return df