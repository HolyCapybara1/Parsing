import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def price_histogram(df: pd.DataFrame):
    """Гистограмма распределения цен."""
    fig = px.histogram(
        df, x="price", nbins=20,
        title="Распределение цен",
        labels={"price": "Цена (₽)", "count": "Кол-во товаров"},
        color_discrete_sequence=["#2563EB"],
    )
    fig.update_layout(bargap=0.1)
    return fig


def avg_price_by_brand(df: pd.DataFrame):
    """Средняя цена по брендам (топ-10)."""
    data = df.groupby("brand")["price"].mean().nlargest(10).reset_index()
    fig = px.bar(
        data, x="price", y="brand", orientation="h",
        title="Средняя цена по брендам (Топ-10)",
        labels={"price": "Средняя цена (₽)", "brand": "Бренд"},
        color="price",
        color_continuous_scale="Blues",
    )
    return fig


def price_by_source(df: pd.DataFrame):
    """Сравнение средних цен между магазинами."""
    data = df.groupby("source")["price"].mean().reset_index()
    fig = px.bar(
        data, x="source", y="price",
        title="Средняя цена по магазинам",
        labels={"source": "Магазин", "price": "Средняя цена (₽)"},
        color="source",
        color_discrete_map={
            "DNS": "#2563EB",
            "Ситилинк": "#DC2626",
            "Regard": "#059669",
        },
    )
    return fig


def price_dynamics_chart(df: pd.DataFrame):
    """Динамика средней цены по датам и магазинам."""
    if df.empty or "collected_at" not in df.columns:
        return go.Figure()
    data = df.copy()
    data["collected_at"] = pd.to_datetime(data["collected_at"])
    data = data.groupby(["collected_at", "source"])["price"].mean().reset_index()
    fig = px.line(
        data, x="collected_at", y="price", color="source",
        title="Динамика средней цены",
        labels={"collected_at": "Дата", "price": "Средняя цена (₽)"},
        markers=True,
    )
    return fig


def cluster_scatter(df: pd.DataFrame):
    """Scatter-диаграмма ML-кластеров: Цена vs Рейтинг."""
    fig = px.scatter(
        df, x="price", y="rating",
        color="segment", symbol="source",
        title="ML-сегментация: Цена vs Рейтинг",
        labels={
            "price": "Цена (₽)",
            "rating": "Рейтинг",
            "segment": "Сегмент",
            "source": "Магазин",
        },
        color_discrete_map={
            "Бюджетный": "#059669",
            "Средний": "#D97706",
            "Премиум": "#DC2626",
        },
        hover_data=["name", "brand"],
    )
    return fig


def price_index_chart(df: pd.DataFrame):
    """График ценового индекса по магазинам."""
    fig = px.bar(
        df, x="source", y="price_index_%",
        title="Ценовой индекс (отклонение от среднерыночной цены, %)",
        labels={"source": "Магазин", "price_index_%": "Индекс (%)"},
        color="price_index_%",
        color_continuous_scale=["#059669", "#FBBF24", "#DC2626"],
        text="price_index_%",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    return fig
