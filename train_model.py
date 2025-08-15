from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

MODEL_PATH = "model.pkl"

def train_or_update_model(df: pd.DataFrame):
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
    joblib.dump(model, MODEL_PATH)
    print(f"💾 Model kaydedildi: {MODEL_PATH}")

    return model

if __name__ == "__main__":
    from fetch_data import fetch_or_load
    from features import prepare_features

    SYMBOL = "AAPL"
    df = fetch_or_load(SYMBOL)
    df_feat = prepare_features(df)
    train_or_update_model(df_feat)