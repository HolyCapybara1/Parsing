import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from db.repository import get_all_products, init_db

st.set_page_config(page_title="Все товары — ЦенМонитор", layout="wide")
init_db()

st.header("Таблица всех товаров")

df = get_all_products()
if df.empty:
    st.warning("Нет данных. Запустите парсинг на странице Главный дашборд.")
    st.stop()

# Строка поиска
search = st.text_input("Поиск по названию или бренду", placeholder="Например: Samsung, видеокарта...")
if search:
    mask = (
        df["name"].str.contains(search, case=False, na=False) |
        df["brand"].str.contains(search, case=False, na=False)
    )
    df = df[mask]

st.caption(f"Найдено товаров: {len(df)}")

# Интерактивная таблица
display_cols = ["name", "brand", "category", "source", "price", "rating", "reviews_count", "segment"]
available_cols = [c for c in display_cols if c in df.columns]

st.dataframe(
    df[available_cols],
    use_container_width=True,
    column_config={
        "name": st.column_config.TextColumn("Название"),
        "brand": st.column_config.TextColumn("Бренд"),
        "category": st.column_config.TextColumn("Категория"),
        "source": st.column_config.TextColumn("Магазин"),
        "price": st.column_config.NumberColumn("Цена (₽)", format="%d ₽"),
        "rating": st.column_config.NumberColumn("Рейтинг", format="★%.1f"),
        "reviews_count": st.column_config.NumberColumn("Отзывы"),
        "segment": st.column_config.TextColumn("Сегмент"),
    },
    hide_index=True,
)

# Экспорт
st.divider()
col1, col2 = st.columns([1, 5])
with col1:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Скачать CSV",
        data=csv,
        file_name="products.csv",
        mime="text/csv",
    )
