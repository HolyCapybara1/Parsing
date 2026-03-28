import os
import pandas as pd
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score

os.makedirs("ml/models", exist_ok=True)

MODEL_PATH = "ml/models/kmeans.pkl"
SCALER_PATH = "ml/models/scaler.pkl"
FEATURES = ["price", "rating", "reviews_count"]
SEGMENT_NAMES = {0: "Бюджетный", 1: "Средний", 2: "Премиум"}


def train_kmeans(df: pd.DataFrame = None) -> dict:
    """Обучить KMeans на текущих данных из БД."""
    if df is None:
        from db.repository import get_all_products
        df = get_all_products()

    if df.empty or len(df) < 10:
        return {"error": "Недостаточно данных для обучения (нужно минимум 10 товаров)"}

    X = df[FEATURES].dropna()
    if len(X) < 10:
        return {"error": "Недостаточно данных после очистки"}

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    score = silhouette_score(X_scaled, labels)

    # Сортировка кластеров по цене (0=бюджетный, 2=премиум)
    centers = kmeans.cluster_centers_
    order = np.argsort(centers[:, 0])  # по price (первый признак)
    label_map = {order[i]: i for i in range(3)}
    labels_named = [SEGMENT_NAMES[label_map[l]] for l in labels]

    joblib.dump(kmeans, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    _save_clusters(df.iloc[X.index], labels_named)

    return {"silhouette_score": round(score, 4), "n_samples": len(X)}


def _save_clusters(df: pd.DataFrame, segments: list[str]):
    from db.repository import SessionLocal
    from db.models import MLCluster

    with SessionLocal() as session:
        for idx, segment in zip(df.index, segments):
            product_id = int(df.loc[idx, "id"])
            existing = session.query(MLCluster).filter_by(product_id=product_id).first()
            if existing:
                existing.segment = segment
            else:
                session.add(MLCluster(
                    product_id=product_id,
                    segment=segment,
                    model_version="kmeans_v1"
                ))
        session.commit()


def predict_segment(price: float, rating: float, reviews: int) -> str:
    """Предсказать ценовой сегмент для нового товара через KMeans."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        # Простая эвристика если модель ещё не обучена
        if price < 5000:
            return "Бюджетный"
        elif price < 30000:
            return "Средний"
        else:
            return "Премиум"

    kmeans = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    X = np.array([[price, rating, reviews]])
    X_scaled = scaler.transform(X)
    label = int(kmeans.predict(X_scaled)[0])

    # Пересчитать маппинг по центрам
    centers = kmeans.cluster_centers_
    order = np.argsort(centers[:, 0])
    label_map = {order[i]: i for i in range(3)}
    return SEGMENT_NAMES[label_map[label]]


def load_kmeans():
    """Загрузить обученную модель."""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None
