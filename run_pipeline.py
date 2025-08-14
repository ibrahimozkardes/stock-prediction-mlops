from fetch_data import fetch_or_load
from features import prepare_features
from train_model import train_or_update_model

SYMBOL = "AAPL"  # Örnek: Apple hissesi

if __name__ == "__main__":
    df = fetch_or_load(SYMBOL)
    df_feat = prepare_features(df)
    train_or_update_model(df_feat)