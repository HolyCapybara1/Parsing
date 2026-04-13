import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import plotly.express as px
import pandas as pd
from db.repository import get_all_products, get_price_history, init_db
from analytics.analytics import (
    price_stats_market, price_stats_full,
    price_index, price_index_by_category,
    detect_anomalies, sentiment_analysis,
    top_by_reviews, top_by_rating,
    market_position, demand_structure, reviews_analysis,
    price_change_stats, price_change_frequency,
)
from dashboard.components.charts import (
    STORE_COLORS,
    price_histogram, avg_price_by_brand, price_by_source,
    mean_median_by_category, price_index_chart, price_index_by_category_chart,
    price_dynamics_chart, anomaly_boxplot, sentiment_chart,
    market_share_chart, demand_structure_chart, reviews_by_category_chart,
    rating_histogram_chart, price_range_distribution_chart,
    price_change_bar_chart, brand_price_chart, category_dynamics_chart,
    min_max_by_category,
)
from dashboard.components.stat_cards import render_stat_cards
from dashboard.components.pdf_export import export_to_pdf

st.set_page_config(page_title="Аналитика — ЦенМонитор", layout="wide")
init_db()

# ── Загрузка данных ────────────────────────────────────────────────────────
df_all = get_all_products()
history_df_all = get_price_history()

if df_all.empty:
    st.warning("Нет данных. Запустите парсинг на странице **Парсинг**.")
    st.stop()

# ── Боковая панель фильтров ────────────────────────────────────────────────
st.sidebar.header("Параметры анализа")

all_categories = sorted(df_all["category"].unique().tolist())
all_sources = sorted(df_all["source"].unique().tolist())

selected_categories = st.sidebar.multiselect(
    "Категории",
    all_categories,
    default=all_categories,
)
selected_sources = st.sidebar.multiselect(
    "Магазины",
    all_sources,
    default=all_sources,
)

# Применяем фильтры
df = df_all.copy()
if selected_categories:
    df = df[df["category"].isin(selected_categories)]
if selected_sources:
    df = df[df["source"].isin(selected_sources)]

history_df = history_df_all.copy()
if not history_df.empty:
    if selected_categories:
        history_df = history_df[history_df["category"].isin(selected_categories)]
    if selected_sources:
        history_df = history_df[history_df["source"].isin(selected_sources)]

if df.empty:
    st.warning("По выбранным фильтрам данных нет. Измените параметры в боковой панели.")
    st.stop()

# ── Заголовок ──────────────────────────────────────────────────────────────
st.header("Аналитика цен")
st.caption(
    f"Анализируется: **{len(df):,}** товаров | "
    f"**{df['source'].nunique()}** магазина | "
    f"**{df['category'].nunique()}** категории"
)

# ── Вкладки ────────────────────────────────────────────────────────────────
tab_market, tab_prices, tab_dynamics, tab_reviews, tab_compare = st.tabs([
    "Рынок",
    "Цены и аномалии",
    "Динамика",
    "Отзывы",
    "Сравнение",
])

# ══════════════════════════════════════════════════════════════════════════
# Вкладка 1: РЫНОК
# ══════════════════════════════════════════════════════════════════════════
with tab_market:
    # ── Ключевые метрики ──
    render_stat_cards(df)

    st.divider()

    # ── Обзорные графики ──
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(price_histogram(df), use_container_width=True)
    with col2:
        st.plotly_chart(avg_price_by_brand(df), use_container_width=True)
    with col3:
        st.plotly_chart(price_by_source(df), use_container_width=True)

    st.divider()

    st.subheader("Позиция компании на рынке")
    pos_df = market_position(df)
    if not pos_df.empty:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.plotly_chart(market_share_chart(pos_df), use_container_width=True)
        with col2:
            st.dataframe(
                pos_df.style.format({
                    "Средняя_цена": "{:,.0f} ₽",
                    "Средний_рейтинг": "{:.2f}",
                    "Отзывов": "{:,.0f}",
                    "Доля_рынка_%": "{:.1f}%",
                }),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Магазин": "Магазин",
                    "Товаров": "Товаров",
                    "Средняя_цена": "Ср. цена",
                    "Средний_рейтинг": "Рейтинг",
                    "Отзывов": "Отзывов",
                    "Доля_рынка_%": "Доля рынка",
                },
            )

    st.divider()

    st.subheader("Структура спроса")
    demand_df = demand_structure(df)
    if not demand_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(demand_structure_chart(demand_df), use_container_width=True)
            st.caption("Размер = кол-во отзывов, цвет = средняя цена")
        with col2:
            st.plotly_chart(price_range_distribution_chart(df), use_container_width=True)

    st.divider()

    st.subheader("Анализ брендов")
    st.plotly_chart(brand_price_chart(df), use_container_width=True)
    st.caption("Размер пузыря = кол-во товаров")

# ══════════════════════════════════════════════════════════════════════════
# Вкладка 2: ЦЕНЫ И АНОМАЛИИ
# ══════════════════════════════════════════════════════════════════════════
with tab_prices:
    st.subheader("Средняя и медианная цена по категориям")
    st.plotly_chart(mean_median_by_category(df), use_container_width=True)

    st.divider()

    st.subheader("Ценовой индекс относительно конкурентов")
    col1, col2 = st.columns(2)
    idx_df = price_index(df)
    idx_cat_df = price_index_by_category(df)
    with col1:
        if not idx_df.empty:
            st.plotly_chart(price_index_chart(idx_df), use_container_width=True)
            st.caption("Положительный = дороже рынка, отрицательный = дешевле")
    with col2:
        if not idx_cat_df.empty:
            st.plotly_chart(price_index_by_category_chart(idx_cat_df), use_container_width=True)

    st.divider()

    st.subheader("Минимальная и максимальная цена")
    st.plotly_chart(min_max_by_category(df), use_container_width=True)

    st.divider()

    st.subheader("Сводная таблица цен")
    stats_full = price_stats_full(df)
    if not stats_full.empty:
        st.dataframe(
            stats_full.style.format({
                "Среднее": "{:,.0f} ₽",
                "Медиана": "{:,.0f} ₽",
                "Минимум": "{:,.0f} ₽",
                "Максимум": "{:,.0f} ₽",
            }),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("Выявление демпинга и ценовых аномалий")
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
                    use_container_width=True,
                    hide_index=True,
                )
        with col2:
            st.plotly_chart(anomaly_boxplot(anomaly_df), use_container_width=True)

    st.divider()

    st.subheader("Экспорт раздела «Цены» в PDF")
    if st.button("Сформировать PDF", key="pdf_prices", type="primary"):
        charts_pdf = [("Srednyaya i medianaya tsena", mean_median_by_category(df))]
        if not idx_df.empty:
            charts_pdf.append(("Tsenovoy indeks", price_index_chart(idx_df)))
        if not anomaly_df.empty:
            charts_pdf.append(("Anomalii i demping", anomaly_boxplot(anomaly_df)))
        with st.spinner("Генерация PDF..."):
            pdf_bytes = export_to_pdf(charts_pdf)
        if pdf_bytes:
            st.download_button("Скачать PDF", pdf_bytes, "prices_report.pdf", "application/pdf")
        else:
            st.error("Установите kaleido и fpdf2: `pip install kaleido fpdf2`")

# ══════════════════════════════════════════════════════════════════════════
# Вкладка 3: ДИНАМИКА
# ══════════════════════════════════════════════════════════════════════════
with tab_dynamics:
    st.subheader("Динамика цен во времени")

    if history_df.empty or history_df["collected_at"].nunique() < 2:
        st.info(
            "Динамика появится после нескольких сеансов сбора данных. "
            "Запустите парсинг ещё раз позднее — и здесь появятся графики изменений."
        )
    else:
        history_df["collected_at"] = pd.to_datetime(history_df["collected_at"])
        min_date = history_df["collected_at"].min().date()
        max_date = history_df["collected_at"].max().date()

        col1, col2 = st.columns(2)
        start_date = col1.date_input("С", value=min_date, min_value=min_date, max_value=max_date)
        end_date = col2.date_input("По", value=max_date, min_value=min_date, max_value=max_date)

        hist_filtered = history_df[
            (history_df["collected_at"].dt.date >= start_date) &
            (history_df["collected_at"].dt.date <= end_date)
        ]

        if not hist_filtered.empty:
            st.plotly_chart(price_dynamics_chart(hist_filtered), use_container_width=True)
            st.caption("Средняя цена по магазинам за выбранный период")

            st.divider()
            st.subheader("Динамика по категориям")
            st.plotly_chart(category_dynamics_chart(hist_filtered), use_container_width=True)

        st.divider()

        st.subheader("Частота изменения цен")
        change_stats = price_change_stats(history_df)
        if not change_stats.empty:
            col1, col2 = st.columns([3, 2])
            with col1:
                st.plotly_chart(price_change_bar_chart(change_stats), use_container_width=True)
            with col2:
                st.dataframe(
                    change_stats.style.format({"Среднее_изменение_пct": "{:+.2f}%"}),
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            freq_df = price_change_frequency(history_df)
            if not freq_df.empty:
                st.dataframe(freq_df, use_container_width=True, hide_index=True)
            st.caption("Нужно минимум 2 сессии с одними и теми же товарами для расчёта изменений.")

# ══════════════════════════════════════════════════════════════════════════
# Вкладка 4: ОТЗЫВЫ
# ══════════════════════════════════════════════════════════════════════════
with tab_reviews:
    rev_info = reviews_analysis(df)
    if rev_info:
        c1, c2, c3 = st.columns(3)
        c1.metric("Средний рейтинг", f"★ {rev_info.get('avg_rating', 0):.2f}")
        c2.metric("Всего отзывов", f"{rev_info.get('total_reviews', 0):,}")
        c3.metric("Ср. отзывов на товар", f"{rev_info.get('avg_reviews', 0):.0f}")
        extra_c1, extra_c2 = st.columns(2)
        if "most_reviewed_brand" in rev_info:
            extra_c1.metric("Больше всего отзывов — бренд", rev_info["most_reviewed_brand"])
        if "top_rated_brand" in rev_info:
            extra_c2.metric("Лучший рейтинг — бренд", rev_info["top_rated_brand"])

    st.divider()

    st.subheader("Анализ тональности отзывов")
    sent_df = sentiment_analysis(df)
    if not sent_df.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(sentiment_chart(sent_df), use_container_width=True)
            st.caption(
                "Тональность по рейтингу: ≥ 4.5 — позитивная, 3.5–4.4 — нейтральная, < 3.5 — негативная"
            )
        with col2:
            st.dataframe(sent_df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Распределение рейтингов")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(rating_histogram_chart(df), use_container_width=True)
    with col2:
        st.plotly_chart(reviews_by_category_chart(df), use_container_width=True)

    st.divider()

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

    st.subheader("Экспорт раздела «Отзывы» в PDF")
    if st.button("Сформировать PDF", key="pdf_reviews", type="primary"):
        charts_pdf = []
        if not sent_df.empty:
            charts_pdf.append(("Tonalnost otzyvov", sentiment_chart(sent_df)))
        charts_pdf.append(("Raspredelenie reytingov", rating_histogram_chart(df)))
        if charts_pdf:
            with st.spinner("Генерация PDF..."):
                pdf_bytes = export_to_pdf(charts_pdf)
            if pdf_bytes:
                st.download_button("Скачать PDF", pdf_bytes, "reviews_report.pdf", "application/pdf")
            else:
                st.error("Установите kaleido и fpdf2: `pip install kaleido fpdf2`")

# ══════════════════════════════════════════════════════════════════════════
# Вкладка 5: СРАВНЕНИЕ
# ══════════════════════════════════════════════════════════════════════════
with tab_compare:
    comparison_mode = st.radio(
        "Режим сравнения",
        ["По магазинам", "По категориям", "По времени"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.divider()

    # ── По магазинам ──────────────────────────────────────────────────────
    if comparison_mode == "По магазинам":
        if len(all_sources) < 2:
            st.info("Для сравнения нужны данные минимум из 2 магазинов.")
        else:
            col1, col2 = st.columns(2)
            store1 = col1.selectbox("Магазин 1", all_sources, index=0)
            store2 = col2.selectbox(
                "Магазин 2",
                [s for s in all_sources if s != store1],
                index=0,
            )
            df1 = df[df["source"] == store1]
            df2 = df[df["source"] == store2]
            s1 = price_stats_market(df1)
            s2 = price_stats_market(df2)

            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric(f"Товаров ({store1})", f"{s1.get('total', 0):,}")
            mc2.metric(f"Товаров ({store2})", f"{s2.get('total', 0):,}")
            mc3.metric(f"Ср. цена ({store1})", f"{s1.get('mean', 0):,.0f} ₽")
            mc4.metric(
                f"Ср. цена ({store2})",
                f"{s2.get('mean', 0):,.0f} ₽",
                delta=f"{s2.get('mean', 0) - s1.get('mean', 0):+,.0f} ₽",
            )

            compare_df = df[df["source"].isin([store1, store2])]
            fig_hist = px.histogram(
                compare_df, x="price", color="source",
                title=f"Распределение цен: {store1} vs {store2}",
                labels={"price": "Цена (₽)", "source": "Магазин"},
                color_discrete_map=STORE_COLORS,
                barmode="overlay", opacity=0.7, nbins=30,
            )
            st.plotly_chart(fig_hist, use_container_width=True)

            cmp_cat = compare_df.groupby(["category", "source"])["price"].mean().reset_index()
            fig_cat = px.bar(
                cmp_cat, x="category", y="price", color="source",
                barmode="group",
                title=f"Средняя цена по категориям: {store1} vs {store2}",
                labels={"category": "Категория", "price": "Средняя цена (₽)", "source": "Магазин"},
                color_discrete_map=STORE_COLORS,
                text_auto=".0f",
            )
            fig_cat.update_traces(textposition="outside", texttemplate="%{y:,.0f}")
            st.plotly_chart(fig_cat, use_container_width=True)

    # ── По категориям ─────────────────────────────────────────────────────
    elif comparison_mode == "По категориям":
        selected_cats_cmp = st.multiselect(
            "Категории для сравнения",
            all_categories,
            default=all_categories[:min(3, len(all_categories))],
        )
        if selected_cats_cmp:
            cmp_df = df[df["category"].isin(selected_cats_cmp)]
            col1, col2 = st.columns(2)
            with col1:
                fig_box = px.box(
                    cmp_df, x="category", y="price", color="source",
                    title="Разброс цен по категориям",
                    labels={"category": "Категория", "price": "Цена (₽)", "source": "Магазин"},
                    color_discrete_map=STORE_COLORS,
                    points=False,
                )
                st.plotly_chart(fig_box, use_container_width=True)
            with col2:
                fig_violin = px.violin(
                    cmp_df, x="category", y="price", color="source",
                    title="Форма распределения по категориям",
                    labels={"category": "Категория", "price": "Цена (₽)", "source": "Магазин"},
                    color_discrete_map=STORE_COLORS,
                    box=True, points=False,
                )
                st.plotly_chart(fig_violin, use_container_width=True)

            cmp_stats = price_stats_full(cmp_df)
            if not cmp_stats.empty:
                st.dataframe(
                    cmp_stats.style.format({
                        "Среднее": "{:,.0f} ₽",
                        "Медиана": "{:,.0f} ₽",
                        "Минимум": "{:,.0f} ₽",
                        "Максимум": "{:,.0f} ₽",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )

    # ── По времени ────────────────────────────────────────────────────────
    elif comparison_mode == "По времени":
        if history_df.empty or history_df["collected_at"].nunique() < 2:
            st.info("Для сравнения по времени нужно несколько сеансов сбора данных.")
        else:
            history_df["collected_at"] = pd.to_datetime(history_df["collected_at"])
            dates = sorted(history_df["collected_at"].dt.date.unique())
            col1, col2 = st.columns(2)
            date1 = col1.selectbox("Период 1", dates, index=0)
            date2 = col2.selectbox("Период 2", dates, index=len(dates) - 1)

            df_t1 = history_df[history_df["collected_at"].dt.date == date1]
            df_t2 = history_df[history_df["collected_at"].dt.date == date2]

            avg1 = df_t1.groupby(["source", "category"])["price"].mean().reset_index()
            avg1["Период"] = str(date1)
            avg2 = df_t2.groupby(["source", "category"])["price"].mean().reset_index()
            avg2["Период"] = str(date2)

            combined = pd.concat([avg1, avg2])
            fig_time = px.bar(
                combined, x="category", y="price", color="Период",
                facet_col="source", barmode="group",
                title=f"Сравнение цен: {date1} vs {date2}",
                labels={"price": "Средняя цена (₽)", "category": "Категория"},
            )
            fig_time.update_layout(height=500)
            st.plotly_chart(fig_time, use_container_width=True)

            merged = avg1.merge(avg2, on=["source", "category"], suffixes=("_до", "_после"))
            if not merged.empty:
                merged["Изменение ₽"] = (merged["price_после"] - merged["price_до"]).round(0)
                merged["Изменение %"] = (
                    (merged["price_после"] - merged["price_до"]) / merged["price_до"] * 100
                ).round(2)
                merged = merged.rename(columns={"source": "Магазин", "category": "Категория"})
                st.subheader("Изменение цен между периодами")
                st.dataframe(
                    merged[["Магазин", "Категория", "price_до", "price_после", "Изменение ₽", "Изменение %"]]
                    .rename(columns={"price_до": f"Цена {date1}", "price_после": f"Цена {date2}"})
                    .style.format({
                        f"Цена {date1}": "{:,.0f} ₽",
                        f"Цена {date2}": "{:,.0f} ₽",
                        "Изменение ₽": "{:+,.0f} ₽",
                        "Изменение %": "{:+.2f}%",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )
