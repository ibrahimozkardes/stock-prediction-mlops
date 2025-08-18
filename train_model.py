from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
import argparse
import os

DEFAULT_MODEL_PATH = "model/model.pkl"

def train_or_update_model(df: pd.DataFrame, model_path: str = DEFAULT_MODEL_PATH):
    X = df[["Return", "MA5", "MA20"]]
    y = df["Target"]

    # Zaman serisi split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Model eğitimi
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Test doğruluğu
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model accuracy: {acc:.2f}")

    # Modeli kaydet
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"💾 Model kaydedildi: {model_path}")

    return model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default=DEFAULT_MODEL_PATH, help="Path to save trained model")
    args = parser.parse_args()

    from fetch_data import fetch_or_load
    from features import prepare_features

    SYMBOL = "AAPL"
    df = fetch_or_load(SYMBOL)
    df_feat = prepare_features(df)

    train_or_update_model(df_feat, args.output)