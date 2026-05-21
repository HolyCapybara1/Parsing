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
    st.warning("Нет данных. Запустите парсинг на странице **Парсинг**.")
    st.stop()

# Строка поиска и фильтры
col_search, col_cat, col_src = st.columns([3, 2, 2])
search = col_search.text_input(
    "Поиск по названию или бренду",
    placeholder="Например: Samsung, видеокарта...",
)
all_cats = sorted(df["category"].unique().tolist())
all_srcs = sorted(df["source"].unique().tolist())
filter_cats = col_cat.multiselect("Категория", all_cats, default=all_cats, label_visibility="visible")
filter_srcs = col_src.multiselect("Магазин", all_srcs, default=all_srcs, label_visibility="visible")

# Применяем фильтры
filtered = df.copy()
if search:
    mask = (
        filtered["name"].str.contains(search, case=False, na=False) |
        filtered["brand"].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]
if filter_cats:
    filtered = filtered[filtered["category"].isin(filter_cats)]
if filter_srcs:
    filtered = filtered[filtered["source"].isin(filter_srcs)]

st.caption(f"Найдено товаров: {len(filtered):,} из {len(df):,}")

# Таблица
display_cols = ["name", "brand", "category", "source", "price", "rating", "reviews_count", "segment", "collected_at"]
available_cols = [c for c in display_cols if c in filtered.columns]

st.dataframe(
    filtered[available_cols],
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
        "collected_at": st.column_config.DatetimeColumn("Дата загрузки", format="DD.MM.YYYY HH:mm"),
    },
    hide_index=True,
)

# Экспорт
st.divider()
col1, col2, _ = st.columns([1, 1, 4])
with col1:
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Скачать CSV",
        data=csv,
        file_name="products.csv",
        mime="text/csv",
    )
with col2:
    try:
        import io
        excel_buf = io.BytesIO()
        filtered.to_excel(excel_buf, index=False, engine="openpyxl")
        st.download_button(
            label="Скачать Excel",
            data=excel_buf.getvalue(),
            file_name="products.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception:
        pass
