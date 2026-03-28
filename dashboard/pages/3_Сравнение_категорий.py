import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import plotly.express as px
from db.repository import get_all_products, init_db
from analytics.analytics import cross_category_summary, price_comparison_by_source

st.set_page_config(page_title="Сравнение категорий — ЦенМонитор", layout="wide")
init_db()

st.header("Сравнение категорий")

df = get_all_products()
if df.empty:
    st.warning("Нет данных. Запустите парсинг на странице Главный дашборд.")
    st.stop()

# Сводная таблица
st.subheader("Сводка по категориям")
summary = cross_category_summary(df)
if not summary.empty:
    st.dataframe(summary, use_container_width=True)

st.divider()

# Сравнение цен по магазинам в каждой категории
st.subheader("Средняя цена по категориям и магазинам")
fig = px.bar(
    df.groupby(["category", "source"])["price"].mean().reset_index(),
    x="category", y="price", color="source", barmode="group",
    title="Средняя цена по категориям",
    labels={"category": "Категория", "price": "Средняя цена (₽)", "source": "Магазин"},
    color_discrete_map={
        "DNS": "#2563EB",
        "Ситилинк": "#DC2626",
        "Regard": "#059669",
    },
)
st.plotly_chart(fig, use_container_width=True)

# Детальное сравнение
st.subheader("Детальное сравнение цен")
comp = price_comparison_by_source(df)
if not comp.empty:
    st.dataframe(
        comp.style.format({
            "avg_price": "{:.0f} ₽",
            "min_price": "{:.0f} ₽",
            "max_price": "{:.0f} ₽",
        }),
        use_container_width=True,
    )

# Боксплот
st.subheader("Распределение цен по категориям")
fig2 = px.box(
    df, x="category", y="price", color="source",
    title="Разброс цен по категориям и магазинам",
    labels={"category": "Категория", "price": "Цена (₽)", "source": "Магазин"},
)
st.plotly_chart(fig2, use_container_width=True)
