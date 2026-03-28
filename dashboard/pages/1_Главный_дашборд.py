import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from dashboard.components.filters import render_filters
from dashboard.components.stat_cards import render_stat_cards
from dashboard.components.charts import price_histogram, avg_price_by_brand, price_by_source
from db.repository import get_all_products, init_db
from scraper.runner import ALL_CATEGORIES, ALL_SOURCES

st.set_page_config(page_title="Главный дашборд — ЦенМонитор", layout="wide")
init_db()

st.header("Главный дашборд")

# ── Настройки сбора данных ─────────────────────────────────────────────────
with st.expander("Настройки сбора данных", expanded=True):
    col_cat, col_src = st.columns(2)

    with col_cat:
        st.subheader("Категории товаров")
        selected_categories = []
        for cat in ALL_CATEGORIES:
            if st.checkbox(cat, value=cat in ["Оперативная память", "Видеокарты", "Смартфоны"], key=f"cat_{cat}"):
                selected_categories.append(cat)

    with col_src:
        st.subheader("Магазины")
        selected_sources = st.multiselect(
            "Выберите магазины",
            options=ALL_SOURCES,
            default=ALL_SOURCES,
        )

    if not selected_categories:
        st.warning("Выберите хотя бы одну категорию.")
    elif not selected_sources:
        st.warning("Выберите хотя бы один магазин.")
    else:
        st.info(
            f"Будет собрано: **{len(selected_categories)}** категорий × "
            f"**{len(selected_sources)}** магазинов "
            f"≈ {len(selected_categories) * len(selected_sources) * 5} страниц. "
            f"Примерное время: **{len(selected_categories) * len(selected_sources) * 2}–"
            f"{len(selected_categories) * len(selected_sources) * 5} мин.**"
        )

        if st.button("▶ Собрать данные", type="primary", use_container_width=True):
            with st.spinner("Идёт парсинг... Не закрывайте страницу."):
                from scraper.runner import run_all
                from logger.logger import setup_all_loggers
                setup_all_loggers()
                result = run_all(
                    categories=selected_categories,
                    sources=selected_sources,
                )
            if result["total"] > 0:
                st.success(
                    f"Готово! Собрано **{result['total']}** товаров "
                    f"из **{result['sources']}** магазинов по **{result['categories']}** категориям."
                )
            else:
                st.error(
                    "Товары не найдены. Возможные причины:\n"
                    "- Сайты заблокировали запросы (попробуйте позже)\n"
                    "- Playwright не установлен (см. инструкцию ниже)\n"
                    "- Проблемы с интернетом"
                )
            st.rerun()

# ── Данные ─────────────────────────────────────────────────────────────────
st.divider()
df = get_all_products()

if df.empty:
    st.warning("Данных пока нет. Настройте параметры выше и нажмите **Собрать данные**.")

    st.markdown("""
    #### Если парсинг не работает — установите Playwright:
    В терминале VS Code выполните:
    ```
    pip install playwright
    playwright install chromium
    ```
    """)
    st.stop()

st.caption(f"Последнее обновление: {df['collected_at'].max()}")

filtered_df = render_filters(df)

if filtered_df.empty:
    st.warning("По выбранным фильтрам товары не найдены.")
    st.stop()

render_stat_cards(filtered_df)
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(price_histogram(filtered_df), use_container_width=True)
with col2:
    st.plotly_chart(avg_price_by_brand(filtered_df), use_container_width=True)
with col3:
    st.plotly_chart(price_by_source(filtered_df), use_container_width=True)
