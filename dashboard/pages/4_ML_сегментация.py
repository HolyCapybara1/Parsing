import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from dashboard.components.charts import cluster_scatter
from db.repository import get_all_products, init_db
from ml.clustering import train_kmeans, predict_segment
from ml.classifier import train_classifier

st.set_page_config(page_title="ML-сегментация — ЦенМонитор", layout="wide")
init_db()

st.header("ML-сегментация товаров")

df = get_all_products()
if df.empty:
    st.warning("Нет данных. Запустите парсинг на странице Главный дашборд.")
    st.stop()

# Кнопки обучения моделей
col_btn1, col_btn2, _ = st.columns([1, 1, 3])
with col_btn1:
    if st.button("Обучить KMeans", type="primary"):
        with st.spinner("Обучение KMeans..."):
            result = train_kmeans(df)
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(
                f"KMeans обучен! Silhouette Score: **{result['silhouette_score']}** "
                f"(на {result['n_samples']} товарах)"
            )
        st.rerun()

with col_btn2:
    if st.button("Обучить Random Forest"):
        with st.spinner("Обучение Random Forest..."):
            result = train_classifier()
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(
                f"RF обучен! Accuracy: **{result['accuracy']}**, "
                f"F1: **{result['f1_macro']}**, "
                f"CV: {result['cv_mean']} ± {result['cv_std']}"
            )

st.divider()

# Scatter-диаграмма кластеров
if "segment" in df.columns and df["segment"].notna().any():
    st.subheader("Кластеры: Цена vs Рейтинг")
    st.plotly_chart(cluster_scatter(df.dropna(subset=["segment"])), use_container_width=True)

    # Сводка по сегментам
    st.subheader("Сводка по сегментам")
    summary = (
        df.dropna(subset=["segment"])
        .groupby("segment")
        .agg(
            Товаров=("id", "count"),
            Средняя_цена=("price", "mean"),
            Средний_рейтинг=("rating", "mean"),
        )
        .round(2)
    )
    st.dataframe(summary, use_container_width=True)
else:
    st.info("Нажмите **Обучить KMeans** для сегментации товаров.")

st.divider()

# Форма классификации нового товара
st.subheader("Классифицировать новый товар")
with st.form("classify_form"):
    col1, col2, col3 = st.columns(3)
    price = col1.number_input("Цена (₽)", min_value=0, value=15000, step=500)
    rating = col2.number_input("Рейтинг", min_value=0.0, max_value=5.0, value=4.5, step=0.1)
    reviews = col3.number_input("Кол-во отзывов", min_value=0, value=200, step=10)
    submitted = st.form_submit_button("Определить сегмент")

if submitted:
    segment = predict_segment(float(price), float(rating), int(reviews))
    colors = {"Бюджетный": "green", "Средний": "orange", "Премиум": "red"}
    color = colors.get(segment, "blue")
    st.success(f"Сегмент товара: **:{color}[{segment}]**")
