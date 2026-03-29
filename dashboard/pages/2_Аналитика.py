import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from db.repository import get_all_products, get_price_history, init_db
from analytics.analytics import (
    price_stats_market, price_index, price_index_by_category,
    detect_anomalies, sentiment_analysis, price_dynamics, top_by_reviews, top_by_rating,
)
from dashboard.components.charts import (
    mean_median_by_category, price_index_chart, price_index_by_category_chart,
    price_dynamics_chart, anomaly_boxplot, anomaly_chart, sentiment_chart,
)
from dashboard.components.pdf_export import export_to_pdf

st.set_page_config(page_title="Аналитика — ЦенМонитор", layout="wide")
init_db()

st.header("Аналитика цен")

df = get_all_products()
if df.empty:
    st.warning("Нет данных. Запустите парсинг на странице Главный дашборд.")
    st.stop()

# ── Рыночные показатели ────────────────────────────────────────────────────
st.subheader("Рыночные показатели")
stats = price_stats_market(df)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Всего товаров", f"{stats.get('total', 0):,}")
c2.metric("Средняя цена", f"{stats.get('mean', 0):,.0f} ₽")
c3.metric("Медианная цена", f"{stats.get('median', 0):,.0f} ₽")
c4.metric("Мин. цена", f"{stats.get('min', 0):,.0f} ₽")
c5.metric("Макс. цена", f"{stats.get('max', 0):,.0f} ₽")

st.divider()

# ── Средняя vs Медианная ───────────────────────────────────────────────────
st.subheader("Средняя и медианная цена по категориям")
fig_mm = mean_median_by_category(df)
st.plotly_chart(fig_mm, use_container_width=True)

st.divider()

# ── Ценовой индекс ─────────────────────────────────────────────────────────
st.subheader("Ценовой индекс")
col1, col2 = st.columns(2)
with col1:
    idx_df = price_index(df)
    if not idx_df.empty:
        fig_idx = price_index_chart(idx_df)
        st.plotly_chart(fig_idx, use_container_width=True)
        st.caption("Положительный индекс = магазин дороже рынка, отрицательный = дешевле")

with col2:
    idx_cat_df = price_index_by_category(df)
    if not idx_cat_df.empty:
        fig_idx_cat = price_index_by_category_chart(idx_cat_df)
        st.plotly_chart(fig_idx_cat, use_container_width=True)

st.divider()

# ── Динамика цен ───────────────────────────────────────────────────────────
st.subheader("Динамика цен")
history_df = get_price_history()
if not history_df.empty and history_df["collected_at"].nunique() > 1:
    fig_dyn = price_dynamics_chart(history_df)
    st.plotly_chart(fig_dyn, use_container_width=True)
else:
    st.info("Динамика появится после нескольких сеансов сбора данных.")

st.divider()

# ── Аномалии ──────────────────────────────────────────────────────────────
st.subheader("Ценовые аномалии и демпинг")
anomaly_df = detect_anomalies(df)
if not anomaly_df.empty:
    col1, col2 = st.columns([1, 2])
    with col1:
        counts = anomaly_df["аномалия"].value_counts().reset_index()
        counts.columns = ["Статус", "Товаров"]
        st.dataframe(counts, use_container_width=True, hide_index=True)
        anomalies_only = anomaly_df[anomaly_df["аномалия"] != "Норма"]
        if not anomalies_only.empty:
            st.caption(f"Обнаружено аномалий: {len(anomalies_only)}")
            st.dataframe(
                anomalies_only[["name", "source", "category", "price", "аномалия"]]
                .sort_values("price"),
                use_container_width=True, hide_index=True,
            )
    with col2:
        st.plotly_chart(anomaly_boxplot(anomaly_df), use_container_width=True)

st.divider()

# ── Тональность отзывов ────────────────────────────────────────────────────
st.subheader("Анализ тональности отзывов")
sent_df = sentiment_analysis(df)
if not sent_df.empty:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(sentiment_chart(sent_df), use_container_width=True)
        st.caption(
            "Тональность определяется по рейтингу: "
            "≥ 4.5 — позитивная, 3.5–4.4 — нейтральная, < 3.5 — негативная"
        )
    with col2:
        st.dataframe(sent_df, use_container_width=True, hide_index=True)

st.divider()

# ── Топ товаров ────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.subheader("Топ-10 по отзывам")
    top_rev = top_by_reviews(df)
    if not top_rev.empty:
        st.dataframe(top_rev, use_container_width=True, hide_index=True)
with col2:
    st.subheader("Топ-10 по рейтингу")
    top_rat = top_by_rating(df)
    if not top_rat.empty:
        st.dataframe(top_rat, use_container_width=True, hide_index=True)

st.divider()

# ── Экспорт PDF ────────────────────────────────────────────────────────────
st.subheader("Экспорт в PDF")
if st.button("Сформировать PDF-отчёт", type="primary"):
    with st.spinner("Генерация PDF..."):
        charts_for_pdf = [
            ("Srednyaya i medianaya tsena po kategoriyam", fig_mm),
        ]
        if not idx_df.empty:
            charts_for_pdf.append(("Tsenovoy indeks", price_index_chart(idx_df)))
        if not idx_cat_df.empty:
            charts_for_pdf.append(("Tsenovoy indeks po kategoriyam", price_index_by_category_chart(idx_cat_df)))
        if not anomaly_df.empty:
            charts_for_pdf.append(("Tsenovye anomalii", anomaly_boxplot(anomaly_df)))
        if not sent_df.empty:
            charts_for_pdf.append(("Analiz tonalnosti otzyvov", sentiment_chart(sent_df)))

        pdf_bytes = export_to_pdf(charts_for_pdf)

    if pdf_bytes:
        st.download_button(
            label="Скачать PDF",
            data=pdf_bytes,
            file_name="analytics_report.pdf",
            mime="application/pdf",
        )
    else:
        st.error(
            "Не удалось создать PDF. Установите необходимые пакеты:\n"
            "```\npython -m pip install kaleido fpdf2\n```"
        )
