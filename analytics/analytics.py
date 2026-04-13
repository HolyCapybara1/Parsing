import pandas as pd
import numpy as np


def price_stats_full(df: pd.DataFrame) -> pd.DataFrame:
    """Средняя, медианная, мин, макс цена по категории и магазину."""
    if df.empty:
        return pd.DataFrame()
    return (
        df.groupby(["category", "source"])["price"]
        .agg(
            Среднее=("mean"),
            Медиана=("median"),
            Минимум=("min"),
            Максимум=("max"),
            Товаров=("count"),
        )
        .round(0)
        .reset_index()
        .rename(columns={"category": "Категория", "source": "Магазин"})
    )


def price_stats_market(df: pd.DataFrame) -> dict:
    """Общие рыночные показатели."""
    if df.empty:
        return {}
    return {
        "mean": round(df["price"].mean(), 0),
        "median": round(df["price"].median(), 0),
        "min": round(df["price"].min(), 0),
        "max": round(df["price"].max(), 0),
        "std": round(df["price"].std(), 0),
        "total": len(df),
    }


def price_index(df: pd.DataFrame) -> pd.DataFrame:
    """Ценовой индекс: отклонение средней цены магазина от рыночной (%)."""
    if df.empty or "source" not in df.columns:
        return pd.DataFrame()
    avg_by_source = df.groupby("source")["price"].mean()
    market_avg = df["price"].mean()
    if market_avg == 0:
        return pd.DataFrame()
    index = ((avg_by_source - market_avg) / market_avg * 100).round(2)
    return index.reset_index().rename(columns={"price": "price_index_%"})


def price_index_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Ценовой индекс по категориям для каждого магазина."""
    if df.empty:
        return pd.DataFrame()
    result = []
    for cat in df["category"].unique():
        cat_df = df[df["category"] == cat]
        market_avg = cat_df["price"].mean()
        if market_avg == 0:
            continue
        for src in cat_df["source"].unique():
            src_avg = cat_df[cat_df["source"] == src]["price"].mean()
            idx = round((src_avg - market_avg) / market_avg * 100, 2)
            result.append({"Категория": cat, "Магазин": src, "Индекс (%)": idx})
    return pd.DataFrame(result)


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Выявление ценовых аномалий методом IQR по каждой категории."""
    if df.empty:
        return pd.DataFrame()
    result = []
    for cat in df["category"].unique():
        cat_df = df[df["category"] == cat].copy()
        Q1 = cat_df["price"].quantile(0.25)
        Q3 = cat_df["price"].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        cat_df["аномалия"] = cat_df["price"].apply(
            lambda p: "Демпинг" if p < lower else ("Завышена" if p > upper else "Норма")
        )
        cat_df["нижняя_граница"] = round(lower, 0)
        cat_df["верхняя_граница"] = round(upper, 0)
        result.append(cat_df)
    return pd.concat(result, ignore_index=True) if result else pd.DataFrame()


def sentiment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Анализ тональности на основе рейтинга товаров."""
    if df.empty or "rating" not in df.columns:
        return pd.DataFrame()
    df = df.copy()
    df["тональность"] = pd.cut(
        df["rating"],
        bins=[0, 3.4, 4.4, 5.0],
        labels=["Негативная (< 3.5)", "Нейтральная (3.5–4.4)", "Позитивная (≥ 4.5)"],
    )
    return (
        df.groupby(["source", "тональность"], observed=True)
        .size()
        .reset_index(name="Товаров")
        .rename(columns={"source": "Магазин"})
    )


def price_change_frequency(history_df: pd.DataFrame) -> pd.DataFrame:
    """Частота изменения цен по магазинам (требует нескольких сборов)."""
    if history_df.empty or "collected_at" not in history_df.columns:
        return pd.DataFrame()
    history_df = history_df.copy()
    history_df["collected_at"] = pd.to_datetime(history_df["collected_at"])
    sessions = history_df.groupby("source")["collected_at"].nunique().reset_index()
    sessions.columns = ["Магазин", "Сеансов"]
    return sessions


def price_dynamics(df: pd.DataFrame) -> pd.DataFrame:
    """Динамика средней цены по дате сбора и магазину."""
    if df.empty or "collected_at" not in df.columns:
        return pd.DataFrame()
    df = df.copy()
    df["date"] = pd.to_datetime(df["collected_at"]).dt.date
    return df.groupby(["date", "source"])["price"].mean().reset_index()


def top_by_reviews(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return (
        df.nlargest(n, "reviews_count")
        [["name", "source", "price", "rating", "reviews_count"]]
        .reset_index(drop=True)
    )


def top_by_rating(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return (
        df[df["rating"] > 0]
        .nlargest(n, "rating")
        [["name", "source", "price", "rating", "reviews_count"]]
        .reset_index(drop=True)
    )


def cross_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "category" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby("category")
        .agg(
            Товаров=("id", "count"),
            Средняя_цена=("price", "mean"),
            Медианная_цена=("price", "median"),
            Средний_рейтинг=("rating", "mean"),
            Всего_отзывов=("reviews_count", "sum"),
        )
        .round(2)
    )


def market_position(df: pd.DataFrame) -> pd.DataFrame:
    """Позиция магазина на рынке: доля, средняя цена, рейтинг, отзывы."""
    if df.empty:
        return pd.DataFrame()
    total = len(df)
    result = (
        df.groupby("source")
        .agg(
            Товаров=("id", "count"),
            Средняя_цена=("price", "mean"),
            Средний_рейтинг=("rating", "mean"),
            Отзывов=("reviews_count", "sum"),
        )
        .round(2)
        .reset_index()
        .rename(columns={"source": "Магазин"})
    )
    result["Доля_рынка_%"] = (result["Товаров"] / total * 100).round(1)
    return result.sort_values("Товаров", ascending=False).reset_index(drop=True)


def demand_structure(df: pd.DataFrame) -> pd.DataFrame:
    """Структура спроса по категориям: кол-во товаров, отзывов, рейтинг."""
    if df.empty:
        return pd.DataFrame()
    return (
        df.groupby("category")
        .agg(
            Товаров=("id", "count"),
            Средняя_цена=("price", "mean"),
            Средний_рейтинг=("rating", "mean"),
            Всего_отзывов=("reviews_count", "sum"),
        )
        .round(2)
        .reset_index()
        .rename(columns={"category": "Категория"})
        .sort_values("Всего_отзывов", ascending=False)
        .reset_index(drop=True)
    )


def reviews_analysis(df: pd.DataFrame) -> dict:
    """Сводные показатели по отзывам и рейтингам."""
    if df.empty or "rating" not in df.columns:
        return {}
    rated = df[df["rating"] > 0]
    result = {
        "avg_rating": round(rated["rating"].mean(), 2) if not rated.empty else 0,
        "total_reviews": int(df["reviews_count"].sum()),
        "avg_reviews": round(df["reviews_count"].mean(), 1),
    }
    if "brand" in df.columns and not df.empty:
        brand_reviews = df.groupby("brand")["reviews_count"].sum()
        if not brand_reviews.empty:
            result["most_reviewed_brand"] = brand_reviews.idxmax()
        if not rated.empty:
            brand_rating = rated.groupby("brand")["rating"].mean()
            if not brand_rating.empty:
                result["top_rated_brand"] = brand_rating.idxmax()
    return result


def price_change_stats(history_df: pd.DataFrame) -> pd.DataFrame:
    """Статистика изменений цен между сессиями сбора."""
    if history_df.empty or "collected_at" not in history_df.columns:
        return pd.DataFrame()
    h = history_df.copy()
    h["collected_at"] = pd.to_datetime(h["collected_at"])
    h = h.sort_values(["name", "source", "collected_at"])
    h["price_prev"] = h.groupby(["name", "source"])["price"].shift(1)
    h["price_change"] = h["price"] - h["price_prev"]
    h["price_change_pct"] = (h["price_change"] / h["price_prev"] * 100).round(2)
    changed = h[h["price_change"].abs() > 0].dropna(subset=["price_change"])
    if changed.empty:
        return pd.DataFrame()
    return (
        changed.groupby("source")
        .agg(
            Изменений=("price_change", "count"),
            Среднее_изменение_пct=("price_change_pct", "mean"),
            Снижений=("price_change", lambda x: (x < 0).sum()),
            Повышений=("price_change", lambda x: (x > 0).sum()),
        )
        .round(2)
        .reset_index()
        .rename(columns={"source": "Магазин"})
    )


def price_comparison_by_source(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    return (
        df.groupby(["category", "source"])["price"]
        .agg(["mean", "median", "min", "max", "count"])
        .round(0)
        .reset_index()
        .rename(columns={
            "category": "Категория", "source": "Магазин",
            "mean": "Среднее", "median": "Медиана",
            "min": "Минимум", "max": "Максимум", "count": "Товаров",
        })
    )
