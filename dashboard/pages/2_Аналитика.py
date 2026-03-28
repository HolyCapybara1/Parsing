import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from dashboard.components.charts import price_dynamics_chart, price_index_chart
from db.repository import get_all_products, get_price_history, init_db
from analytics.analytics import price_index, price_dynamics, top_by_reviews, top_by_rating

st.set_page_config(page_title="Аналитика — ЦенМонитор", layout="wide")
init_db()

st.header("Аналитика цен")

df = get_all_products()
if df.empty:
    st.warning("Нет данных. Запустите парсинг на странице Главный дашборд.")
    st.stop()

# Ценовой индекс
st.subheader("Ценовой индекс по магазинам")
idx_df = price_index(df)
if not idx_df.empty:
    st.plotly_chart(price_index_chart(idx_df), use_container_width=True)
    st.dataframe(idx_df, use_container_width=True)

st.divider()

# Динамика цен
st.subheader("Динамика средней цены")
history_df = get_price_history()
if not history_df.empty:
    st.plotly_chart(price_dynamics_chart(history_df), use_container_width=True)
else:
    st.info("История цен появится после нескольких сеансов парсинга.")

st.divider()

# Топ товаров
col1, col2 = st.columns(2)
with col1:
    st.subheader("Топ-10 по отзывам")
    top_rev = top_by_reviews(df)
    if not top_rev.empty:
        st.dataframe(top_rev, use_container_width=True)

with col2:
    st.subheader("Топ-10 по рейтингу")
    top_rat = top_by_rating(df)
    if not top_rat.empty:
        st.dataframe(top_rat, use_container_width=True)
