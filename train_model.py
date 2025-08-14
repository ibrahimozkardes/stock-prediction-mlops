from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

MODEL_PATH = "model.pkl"

def train_or_update_model(df: pd.DataFrame):
    X = df[["Return", "MA5", "MA20"]]
    y = df["Target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"✅ Model accuracy: {acc:.2f}")

    joblib.dump(model, MODEL_PATH)
    return model