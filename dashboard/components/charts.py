import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Цвета магазинов — используются на всех графиках
STORE_COLORS = {
    "DNS": "#2563EB",
    "Ситилинк": "#DC2626",
    "Regard": "#059669",
    "NIX": "#D97706",
}

SENTIMENT_COLORS = {
    "Позитивная (≥ 4.5)": "#059669",
    "Нейтральная (3.5–4.4)": "#D97706",
    "Негативная (< 3.5)": "#DC2626",
}

ANOMALY_COLORS = {
    "Норма": "#2563EB",
    "Демпинг": "#059669",
    "Завышена": "#DC2626",
}


# ── Главный дашборд ────────────────────────────────────────────────────────

def price_histogram(df: pd.DataFrame):
    fig = px.histogram(
        df, x="price", nbins=30, color="source",
        title="Распределение цен по магазинам",
        labels={"price": "Цена (₽)", "count": "Кол-во товаров", "source": "Магазин"},
        color_discrete_map=STORE_COLORS,
        barmode="overlay", opacity=0.7,
    )
    fig.update_layout(legend_title="Магазин")
    return fig


def avg_price_by_brand(df: pd.DataFrame):
    data = df.groupby("brand")["price"].mean().nlargest(10).reset_index()
    fig = px.bar(
        data, x="price", y="brand", orientation="h",
        title="Средняя цена по брендам (Топ-10)",
        labels={"price": "Средняя цена (₽)", "brand": "Бренд"},
        color="price", color_continuous_scale="Blues",
    )
    return fig


def price_by_source(df: pd.DataFrame):
    data = df.groupby("source")["price"].mean().reset_index()
    fig = px.bar(
        data, x="source", y="price",
        title="Средняя цена по магазинам",
        labels={"source": "Магазин", "price": "Средняя цена (₽)"},
        color="source", color_discrete_map=STORE_COLORS,
        text_auto=".0f",
    )
    fig.update_traces(textposition="outside")
    return fig


# ── Аналитика ──────────────────────────────────────────────────────────────

def mean_median_by_category(df: pd.DataFrame):
    """Сравнение средней и медианной цены по категориям."""
    data = df.groupby("category")["price"].agg(["mean", "median"]).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Средняя цена", x=data["category"], y=data["mean"],
        marker_color="#2563EB", text=data["mean"].round(0),
        textposition="outside", texttemplate="%{text:,.0f} ₽",
    ))
    fig.add_trace(go.Bar(
        name="Медианная цена", x=data["category"], y=data["median"],
        marker_color="#059669", text=data["median"].round(0),
        textposition="outside", texttemplate="%{text:,.0f} ₽",
    ))
    fig.update_layout(
        title="Средняя vs Медианная цена по категориям",
        barmode="group",
        xaxis_title="Категория",
        yaxis_title="Цена (₽)",
        legend_title="Показатель",
    )
    return fig


def price_index_chart(df: pd.DataFrame):
    """Ценовой индекс по магазинам."""
    fig = px.bar(
        df, x="source", y="price_index_%",
        title="Ценовой индекс (отклонение от среднерыночной цены, %)",
        labels={"source": "Магазин", "price_index_%": "Индекс (%)"},
        color="price_index_%",
        color_continuous_scale=["#059669", "#FBBF24", "#DC2626"],
        text="price_index_%",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.add_hline(y=0, line_dash="dash", line_color="gray",
                  annotation_text="Рынок", annotation_position="right")
    return fig


def price_index_by_category_chart(df: pd.DataFrame):
    """Ценовой индекс по категориям и магазинам."""
    fig = px.bar(
        df, x="Категория", y="Индекс (%)", color="Магазин",
        barmode="group",
        title="Ценовой индекс по категориям (отклонение от среднего, %)",
        color_discrete_map=STORE_COLORS,
        text="Индекс (%)",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(xaxis_title="Категория", yaxis_title="Отклонение (%)")
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
        title="Динамика средней цены по магазинам",
        labels={"collected_at": "Дата", "price": "Средняя цена (₽)", "source": "Магазин"},
        color_discrete_map=STORE_COLORS,
        markers=True,
    )
    return fig


def anomaly_chart(df: pd.DataFrame):
    """Scatter-диаграмма с выделением ценовых аномалий."""
    if df.empty or "аномалия" not in df.columns:
        return go.Figure()
    fig = px.scatter(
        df, x="name", y="price",
        color="аномалия", facet_col="category",
        title="Ценовые аномалии по категориям",
        labels={"price": "Цена (₽)", "name": "Товар", "аномалия": "Статус"},
        color_discrete_map=ANOMALY_COLORS,
        hover_data=["source", "brand"],
        facet_col_wrap=3,
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(height=500)
    return fig


def anomaly_boxplot(df: pd.DataFrame):
    """Boxplot с аномалиями — наглядно показывает выбросы."""
    if df.empty:
        return go.Figure()
    fig = px.box(
        df, x="category", y="price", color="source",
        title="Распределение цен и выбросы по категориям",
        labels={"category": "Категория", "price": "Цена (₽)", "source": "Магазин"},
        color_discrete_map=STORE_COLORS,
        points="outliers",
        hover_data=["name"],
    )
    fig.update_layout(xaxis_title="Категория", yaxis_title="Цена (₽)")
    return fig


def sentiment_chart(df: pd.DataFrame):
    """Тональность отзывов (на основе рейтинга) по магазинам."""
    if df.empty:
        return go.Figure()
    fig = px.bar(
        df, x="Магазин", y="Товаров", color="тональность",
        title="Тональность отзывов по магазинам (на основе рейтинга)",
        color_discrete_map=SENTIMENT_COLORS,
        barmode="stack",
        text="Товаров",
    )
    fig.update_traces(textposition="inside")
    fig.update_layout(
        xaxis_title="Магазин",
        yaxis_title="Кол-во товаров",
        legend_title="Тональность",
    )
    return fig


# ── Сравнение категорий ────────────────────────────────────────────────────

def avg_price_by_category_and_store(df: pd.DataFrame):
    """Средняя цена по категориям и магазинам — сгруппированные столбцы."""
    data = df.groupby(["category", "source"])["price"].mean().reset_index()
    fig = px.bar(
        data, x="category", y="price", color="source",
        barmode="group",
        title="Средняя цена по категориям и магазинам",
        labels={"category": "Категория", "price": "Средняя цена (₽)", "source": "Магазин"},
        color_discrete_map=STORE_COLORS,
        text_auto=".0f",
    )
    fig.update_traces(textposition="outside", texttemplate="%{y:,.0f}")
    fig.update_layout(xaxis_title="Категория", yaxis_title="Средняя цена (₽)")
    return fig


def price_distribution_by_store(df: pd.DataFrame):
    """Распределение цен по магазинам (violin plot)."""
    fig = px.violin(
        df, x="source", y="price", color="source",
        box=True, points="outliers",
        title="Распределение цен в магазинах",
        labels={"source": "Магазин", "price": "Цена (₽)"},
        color_discrete_map=STORE_COLORS,
        hover_data=["name", "category"],
    )
    fig.update_layout(showlegend=False)
    return fig


def price_heatmap(df: pd.DataFrame):
    """Тепловая карта: категория × магазин = средняя цена."""
    if df.empty:
        return go.Figure()
    pivot = df.pivot_table(
        index="category", columns="source", values="price", aggfunc="mean"
    ).round(0)
    fig = px.imshow(
        pivot,
        title="Средняя цена: категория × магазин (₽)",
        labels={"x": "Магазин", "y": "Категория", "color": "Средняя цена (₽)"},
        color_continuous_scale="Blues",
        text_auto=True,
        aspect="auto",
    )
    fig.update_traces(texttemplate="%{z:,.0f}")
    return fig


def min_max_by_category(df: pd.DataFrame):
    """Мин и макс цена по категориям и магазинам."""
    data = (
        df.groupby(["category", "source"])["price"]
        .agg(["min", "max"])
        .reset_index()
    )
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Минимальная цена", "Максимальная цена"),
    )
    for src in data["source"].unique():
        d = data[data["source"] == src]
        color = STORE_COLORS.get(src, "#888")
        fig.add_trace(
            go.Bar(name=src, x=d["category"], y=d["min"],
                   marker_color=color, legendgroup=src,
                   text=d["min"].round(0), texttemplate="%{text:,.0f}"),
            row=1, col=1,
        )
        fig.add_trace(
            go.Bar(name=src, x=d["category"], y=d["max"],
                   marker_color=color, legendgroup=src,
                   showlegend=False,
                   text=d["max"].round(0), texttemplate="%{text:,.0f}"),
            row=1, col=2,
        )
    fig.update_layout(
        title="Минимальная и максимальная цена по категориям",
        barmode="group",
        height=450,
    )
    fig.update_traces(textposition="outside")
    return fig


# ── ML ─────────────────────────────────────────────────────────────────────

def cluster_scatter(df: pd.DataFrame):
    """Scatter-диаграмма ML-кластеров: Цена vs Рейтинг."""
    fig = px.scatter(
        df, x="price", y="rating",
        color="segment", symbol="source",
        title="ML-сегментация: Цена vs Рейтинг",
        labels={
            "price": "Цена (₽)", "rating": "Рейтинг",
            "segment": "Сегмент", "source": "Магазин",
        },
        color_discrete_map={
            "Бюджетный": "#059669",
            "Средний": "#D97706",
            "Премиум": "#DC2626",
        },
        hover_data=["name", "brand", "category"],
    )
    return fig
