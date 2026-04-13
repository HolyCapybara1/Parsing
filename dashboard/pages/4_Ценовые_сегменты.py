import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import plotly.express as px
from dashboard.components.charts import STORE_COLORS
from db.repository import get_all_products, init_db
from ml.clustering import train_kmeans, predict_segment, predict_segment_by_category
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

all_categories = sorted(df["category"].unique().tolist())

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

    # Фильтр по категории для карты и таблицы
    filter_cat = st.selectbox(
        "Показать категорию",
        ["Все категории"] + all_categories,
        key="seg_cat_filter",
    )
    view_df = seg_df if filter_cat == "Все категории" else seg_df[seg_df["category"] == filter_cat]

    st.subheader("Карта сегментов: Цена vs Рейтинг")
    if not view_df.empty:
        fig = px.scatter(
            view_df, x="price", y="rating",
            color="segment", symbol="source",
            title=f"Сегментация{' — ' + filter_cat if filter_cat != 'Все категории' else ''}",
            labels={
                "price": "Цена (₽)", "rating": "Рейтинг",
                "segment": "Сегмент", "source": "Магазин",
            },
            color_discrete_map={
                "Бюджетный": "#059669",
                "Средний": "#D97706",
                "Премиум": "#2563EB",
            },
            hover_data=["name", "brand", "category"],
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "Каждая точка — товар. "
            "Цвет = сегмент (Бюджетный / Средний / Премиум), форма = магазин."
        )
    else:
        st.info("По выбранной категории нет товаров с сегментами.")

    st.divider()

    st.subheader("Сводка по сегментам")
    summary = (
        view_df.groupby("segment")
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
    if not summary.empty:
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

# ── Пороги по категориям ───────────────────────────────────────────────────
st.subheader("Ценовые пороги по категориям")
st.caption("Границы сегментов рассчитаны на основе реальных данных для каждой категории отдельно.")

thresholds = []
for cat in all_categories:
    cat_df = df[df["category"] == cat]
    if len(cat_df) >= 3:
        p33 = cat_df["price"].quantile(0.33)
        p66 = cat_df["price"].quantile(0.66)
        thresholds.append({
            "Категория": cat,
            "Бюджетный (до)": f"{p33:,.0f} ₽",
            "Средний (до)": f"{p66:,.0f} ₽",
            "Премиум (от)": f"{p66:,.0f} ₽",
            "Товаров": len(cat_df),
        })

if thresholds:
    import pandas as pd
    st.dataframe(pd.DataFrame(thresholds), use_container_width=True, hide_index=True)

st.divider()

# ── Определить сегмент для нового товара ──────────────────────────────────
st.subheader("Определить сегмент нового товара")
st.caption(
    "Введите параметры товара — система скажет, к какому сегменту он относится "
    "**с учётом выбранной категории**."
)

with st.form("classify_form"):
    col0, col1, col2, col3 = st.columns([2, 2, 1, 1])
    category = col0.selectbox("Категория товара", all_categories)
    price = col1.number_input("Цена (₽)", min_value=0, value=15000, step=500)
    rating = col2.number_input("Рейтинг (0–5)", min_value=0.0, max_value=5.0, value=4.5, step=0.1)
    reviews = col3.number_input("Отзывов", min_value=0, value=200, step=10)
    submitted = st.form_submit_button("Определить сегмент", type="primary", use_container_width=True)

if submitted:
    result = predict_segment_by_category(float(price), float(rating), int(reviews), category, df)
    segment = result["segment"]
    budget_max = result["budget_max"]
    mid_max = result["mid_max"]
    cat_count = result["category_count"]

    seg_colors = {"Бюджетный": "green", "Средний": "orange", "Премиум": "blue"}
    color = seg_colors.get(segment, "blue")

    st.success(f"Категория **{category}** — сегмент: **:{color}[{segment}]**")

    # Пороги для этой категории
    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Бюджетный",
        f"до {budget_max:,.0f} ₽",
        delta="✓" if segment == "Бюджетный" else None,
        delta_color="normal",
    )
    c2.metric(
        "Средний",
        f"{budget_max:,.0f} – {mid_max:,.0f} ₽",
        delta="✓" if segment == "Средний" else None,
        delta_color="normal",
    )
    c3.metric(
        "Премиум",
        f"от {mid_max:,.0f} ₽",
        delta="✓" if segment == "Премиум" else None,
        delta_color="normal",
    )

    descriptions = {
        "Бюджетный": "Низкая цена для данной категории, ориентация на массовый спрос.",
        "Средний": "Оптимальное соотношение цены и качества в данной категории.",
        "Премиум": "Высокая цена для данной категории, акцент на качестве и статусе.",
    }
    if cat_count > 0:
        st.info(
            f"{descriptions.get(segment, '')} "
            f"Пороги рассчитаны по {cat_count} товарам категории «{category}»."
        )
    else:
        st.info(f"{descriptions.get(segment, '')} (использованы глобальные пороги — мало данных по категории)")
