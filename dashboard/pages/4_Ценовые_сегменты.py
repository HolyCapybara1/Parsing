import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from dashboard.components.charts import cluster_scatter
from db.repository import get_all_products, init_db
from ml.clustering import train_kmeans, predict_segment
from ml.classifier import train_classifier

st.set_page_config(page_title="Ценовые сегменты — ЦенМонитор", layout="wide")
init_db()

st.header("Ценовые сегменты товаров")
st.markdown(
    "Система автоматически делит товары на **три группы** по цене, рейтингу и отзывам: "
    "**Бюджетный**, **Средний** и **Премиум**. "
    "Это помогает понять структуру рынка и найти своё ценовое позиционирование."
)

df = get_all_products()
if df.empty:
    st.warning("Нет данных. Запустите парсинг на странице **Парсинг**.")
    st.stop()

st.divider()

# ── Обучение моделей ───────────────────────────────────────────────────────
st.subheader("Шаг 1 — Обучить кластеризацию")
st.caption(
    "KMeans разбивает товары на 3 группы по признакам: цена, рейтинг, кол-во отзывов. "
    "Нужно минимум 10 товаров."
)

col_btn1, col_btn2, _ = st.columns([1, 1, 3])
with col_btn1:
    if st.button("Обучить (Шаг 1: KMeans)", type="primary", use_container_width=True):
        with st.spinner("Кластеризация товаров..."):
            result = train_kmeans(df)
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(
                f"Готово! Качество кластеризации (Silhouette): **{result['silhouette_score']}** "
                f"(чем ближе к 1 — тем лучше). Обработано: {result['n_samples']} товаров."
            )
        st.rerun()

with col_btn2:
    st.caption("Шаг 2 — уточнение прогноза")
    if st.button("Уточнить (Шаг 2: Random Forest)", use_container_width=True):
        with st.spinner("Обучение классификатора..."):
            result = train_classifier()
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(
                f"Классификатор обучен! "
                f"Точность: **{result['accuracy']}**, "
                f"F1: **{result['f1_macro']}**, "
                f"CV: {result['cv_mean']} ± {result['cv_std']}"
            )

st.divider()

# ── Результаты сегментации ─────────────────────────────────────────────────
if "segment" in df.columns and df["segment"].notna().any():
    seg_df = df.dropna(subset=["segment"])

    st.subheader("Карта сегментов: Цена vs Рейтинг")
    st.plotly_chart(cluster_scatter(seg_df), use_container_width=True)
    st.caption(
        "Каждая точка — товар. "
        "Цвет = сегмент (Бюджетный / Средний / Премиум), форма = магазин."
    )

    st.divider()

    st.subheader("Сводка по сегментам")
    summary = (
        seg_df.groupby("segment")
        .agg(
            Товаров=("id", "count"),
            Средняя_цена=("price", "mean"),
            Мин_цена=("price", "min"),
            Макс_цена=("price", "max"),
            Средний_рейтинг=("rating", "mean"),
            Всего_отзывов=("reviews_count", "sum"),
        )
        .round(2)
        .reset_index()
    )
    st.dataframe(
        summary.style.format({
            "Средняя_цена": "{:,.0f} ₽",
            "Мин_цена": "{:,.0f} ₽",
            "Макс_цена": "{:,.0f} ₽",
            "Средний_рейтинг": "{:.2f}",
            "Всего_отзывов": "{:,.0f}",
        }),
        use_container_width=True,
        hide_index=True,
        column_config={
            "segment": "Сегмент",
            "Товаров": "Товаров",
            "Средняя_цена": "Ср. цена",
            "Мин_цена": "Мин. цена",
            "Макс_цена": "Макс. цена",
            "Средний_рейтинг": "Рейтинг",
            "Всего_отзывов": "Отзывов",
        },
    )
else:
    st.info(
        "Сегменты пока не рассчитаны. "
        "Нажмите **Обучить (Шаг 1: KMeans)** выше, чтобы разбить товары по ценовым группам."
    )

st.divider()

# ── Определить сегмент для нового товара ──────────────────────────────────
st.subheader("Определить сегмент нового товара")
st.caption("Введите параметры товара — система скажет, к какому сегменту он относится.")

with st.form("classify_form"):
    col1, col2, col3 = st.columns(3)
    price = col1.number_input("Цена (₽)", min_value=0, value=15000, step=500)
    rating = col2.number_input("Рейтинг (от 0 до 5)", min_value=0.0, max_value=5.0, value=4.5, step=0.1)
    reviews = col3.number_input("Кол-во отзывов", min_value=0, value=200, step=10)
    submitted = st.form_submit_button("Определить сегмент", type="primary", use_container_width=True)

if submitted:
    segment = predict_segment(float(price), float(rating), int(reviews))
    colors = {"Бюджетный": "green", "Средний": "orange", "Премиум": "red"}
    color = colors.get(segment, "blue")
    st.success(f"Товар относится к сегменту: **:{color}[{segment}]**")
    descriptions = {
        "Бюджетный": "Низкая цена, ориентация на массовый спрос.",
        "Средний": "Оптимальное соотношение цены и качества.",
        "Премиум": "Высокая цена, акцент на качестве и статусе.",
    }
    st.info(descriptions.get(segment, ""))
