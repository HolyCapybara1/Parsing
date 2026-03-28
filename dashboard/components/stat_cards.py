import streamlit as st
import pandas as pd


def render_stat_cards(df: pd.DataFrame):
    """Рендерит строку карточек с ключевыми метриками."""
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Всего товаров",
            f"{len(df):,}",
            delta=f"из {df['source'].nunique()} магазинов" if not df.empty else None,
        )
    with col2:
        avg = df["price"].mean() if not df.empty else 0
        st.metric("Средняя цена", f"{avg:,.0f} ₽")
    with col3:
        val = df["price"].min() if not df.empty else 0
        st.metric("Мин. цена", f"{val:,.0f} ₽")
    with col4:
        val = df["price"].max() if not df.empty else 0
        st.metric("Макс. цена", f"{val:,.0f} ₽")
    with col5:
        avg_rating = df["rating"].mean() if not df.empty else 0
        st.metric("Средний рейтинг", f"★ {avg_rating:.2f}")
