import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

os.makedirs("ml/models", exist_ok=True)

RF_PATH = "ml/models/rf_classifier.pkl"
FEATURES = ["price", "rating", "reviews_count"]


def train_classifier() -> dict:
    """Обучить Random Forest на метках KMeans из БД."""
    from db.repository import get_all_products
    df = get_all_products()
    df = df.dropna(subset=FEATURES + ["segment"])

    if len(df) < 15:
        return {"error": "Недостаточно данных. Сначала запустите KMeans-кластеризацию."}

    X = df[FEATURES]
    y = df["segment"]

    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )
    cv = StratifiedKFold(n_splits=min(5, len(y.unique())), shuffle=True, random_state=42)
    cv_scores = cross_val_score(rf, X, y, cv=cv, scoring="accuracy")

    rf.fit(X, y)
    y_pred = rf.predict(X)

    acc = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred, average="macro")
    cm = confusion_matrix(y, y_pred)

    joblib.dump(rf, RF_PATH)

    return {
        "accuracy": round(acc, 4),
        "f1_macro": round(f1, 4),
        "cv_mean": round(cv_scores.mean(), 4),
        "cv_std": round(cv_scores.std(), 4),
        "confusion_matrix": cm.tolist(),
    }


def predict_segment(price: float, rating: float, reviews: int) -> str:
    """Предсказать сегмент для нового товара через Random Forest."""
    if not os.path.exists(RF_PATH):
        from ml.clustering import predict_segment as kmeans_predict
        return kmeans_predict(price, rating, reviews)

    rf = joblib.load(RF_PATH)
    X = pd.DataFrame([[price, rating, reviews]], columns=FEATURES)
    return rf.predict(X)[0]
