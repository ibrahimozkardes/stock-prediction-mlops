import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import mlflow
import mlflow.sklearn

MODEL_PATH = "model.pkl"

def train_or_update_model(df: pd.DataFrame):
    X = df[["Return", "MA5", "MA20"]]
    y = df["Target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model accuracy: {acc:.2f}")

    # MLflow ile loglama
    with mlflow.start_run():
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")
    
    joblib.dump(model, MODEL_PATH)
    return model

if __name__ == "__main__":
    df = pd.read_csv("data/stock_data.csv")
    train_or_update_model(df)