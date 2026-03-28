import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from dashboard.components.filters import render_filters
from dashboard.components.stat_cards import render_stat_cards
from dashboard.components.charts import price_histogram, avg_price_by_brand, price_by_source
from db.repository import get_all_products, init_db

st.set_page_config(page_title="Главный дашборд — ЦенМонитор", layout="wide")
init_db()

st.header("Главный дашборд")

df = get_all_products()

if st.button("▶ Собрать данные сейчас", type="primary"):
    with st.spinner("Парсинг... Это займёт 3–10 минут. Не закрывайте страницу."):
        from scraper.runner import run_all
        from logger.logger import setup_all_loggers
        setup_all_loggers()
        result = run_all()
    st.success(
        f"Готово! Собрано **{result['total']}** товаров "
        f"из **{result['sources']}** магазинов. "
        f"Ошибок: {result.get('errors', 0)}"
    )
    df = get_all_products()
    st.rerun()

if df.empty:
    st.warning(
        "Данных пока нет. Нажмите кнопку **Собрать данные** выше, "
        "чтобы запустить парсинг."
    )
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
