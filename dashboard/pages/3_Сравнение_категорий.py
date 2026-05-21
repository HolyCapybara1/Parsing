import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from db.repository import get_all_products, init_db
from analytics.analytics import cross_category_summary, price_comparison_by_source
from dashboard.components.charts import (
    avg_price_by_category_and_store,
    price_distribution_by_store,
    price_heatmap,
    min_max_by_category,
)
from dashboard.components.pdf_export import export_to_pdf

st.set_page_config(page_title="Сравнение категорий — ЦенМонитор", layout="wide")
init_db()

st.header("Сравнение категорий")

df = get_all_products()
if df.empty:
    st.warning("Нет данных. Запустите парсинг на странице Главный дашборд.")
    st.stop()

# ── График 1: Средняя цена по категориям и магазинам ──────────────────────
st.subheader("Средняя цена по категориям и магазинам")
fig1 = avg_price_by_category_and_store(df)
st.plotly_chart(fig1, use_container_width=True)
st.caption("Цвет — магазин, группы — категории товаров")

st.divider()

# ── График 2: Распределение цен ────────────────────────────────────────────
st.subheader("Распределение цен в магазинах")
col1, col2 = st.columns(2)
with col1:
    fig2 = price_distribution_by_store(df)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Violin plot — форма показывает где сконцентрированы цены, точки — выбросы")
with col2:
    import plotly.express as px
    fig_box = px.box(
        df, x="category", y="price", color="source",
        title="Разброс цен по категориям",
        labels={"category": "Категория", "price": "Цена (₽)", "source": "Магазин"},
        color_discrete_map={"DNS": "#2563EB", "Ситилинк": "#7C3AED",
                             "Regard": "#059669", "NIX": "#D97706"},
        points=False,
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# ── График 3: Тепловая карта ───────────────────────────────────────────────
st.subheader("Тепловая карта: средняя цена")
fig3 = price_heatmap(df)
st.plotly_chart(fig3, use_container_width=True)
st.caption("Тёмнее = дороже. Позволяет сразу увидеть где самые высокие и низкие цены")

st.divider()

# ── График 4: Мин и Макс ───────────────────────────────────────────────────
st.subheader("Минимальная и максимальная цена")
fig4 = min_max_by_category(df)
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Сводная таблица ────────────────────────────────────────────────────────
st.subheader("Сводная таблица по категориям")
summary = cross_category_summary(df)
if not summary.empty:
    st.dataframe(
        summary.style.format({
            "Средняя_цена": "{:,.0f} ₽",
            "Медианная_цена": "{:,.0f} ₽",
            "Средний_рейтинг": "{:.2f}",
            "Всего_отзывов": "{:,.0f}",
        }),
        use_container_width=True,
    )

st.subheader("Детальное сравнение по магазинам")
comp = price_comparison_by_source(df)
if not comp.empty:
    st.dataframe(
        comp.style.format({
            "Среднее": "{:,.0f} ₽",
            "Медиана": "{:,.0f} ₽",
            "Минимум": "{:,.0f} ₽",
            "Максимум": "{:,.0f} ₽",
        }),
        use_container_width=True,
    )

st.divider()

# ── Экспорт PDF ────────────────────────────────────────────────────────────
st.subheader("Экспорт в PDF")
if st.button("Сформировать PDF-отчёт", type="primary"):
    with st.spinner("Генерация PDF..."):
        pdf_bytes = export_to_pdf([
            ("Srednyaya tsena po kategoriyam i magazinam", fig1),
            ("Raspredelenie tsen v magazinakh", fig2),
            ("Teplovaya karta sredney tseny", fig3),
            ("Minimalnaya i maximalnaya tsena", fig4),
        ])
    if pdf_bytes:
        st.download_button(
            label="Скачать PDF",
            data=pdf_bytes,
            file_name="categories_report.pdf",
            mime="application/pdf",
        )
    else:
        st.error(
            "Не удалось создать PDF. Установите пакеты:\n"
            "```\npython -m pip install kaleido fpdf2\n```"
        )
