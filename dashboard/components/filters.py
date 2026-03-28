import streamlit as st
import pandas as pd


def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Рендерит фильтры в боковой панели, возвращает отфильтрованный DataFrame."""
    with st.sidebar:
        st.subheader("Фильтры")

        categories = ["Все"] + sorted(df["category"].dropna().unique().tolist())
        selected_cat = st.selectbox("Категория", categories)

        sources = sorted(df["source"].dropna().unique().tolist())
        selected_src = st.multiselect("Магазин", sources, default=sources)

        brands = ["Все"] + sorted(df["brand"].dropna().unique().tolist())
        selected_brand = st.selectbox("Бренд", brands)

        min_p = int(df["price"].min()) if not df.empty else 0
        max_p = int(df["price"].max()) if not df.empty else 100000
        if min_p == max_p:
            max_p = min_p + 1
        price_range = st.slider("Диапазон цен (₽)", min_p, max_p, (min_p, max_p))

    filtered = df.copy()
    if selected_cat != "Все":
        filtered = filtered[filtered["category"] == selected_cat]
    if selected_src:
        filtered = filtered[filtered["source"].isin(selected_src)]
    if selected_brand != "Все":
        filtered = filtered[filtered["brand"] == selected_brand]
    filtered = filtered[
        (filtered["price"] >= price_range[0]) &
        (filtered["price"] <= price_range[1])
    ]
    return filtered
