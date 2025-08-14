from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
import mlflow

MODEL_PATH = "model.pkl"

def train_or_update_model(df: pd.DataFrame):
    # MLflow tracking server ayarı
    mlflow.set_tracking_uri("http://localhost:5000")  # Docker’da çalıştırdığın MLflow
    mlflow.set_experiment("stock_prediction")

    X = df[["Return", "MA5", "MA20"]]
    y = df["Target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"✅ Model accuracy: {acc:.2f}")

        # MLflow'a logla
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", acc)

        # Modeli kaydet
        joblib.dump(model, MODEL_PATH)
        mlflow.log_artifact(MODEL_PATH)

    return model