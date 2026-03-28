import pandas as pd


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


def price_dynamics(df: pd.DataFrame) -> pd.DataFrame:
    """Динамика средней цены по дате сбора и магазину."""
    if df.empty or "collected_at" not in df.columns:
        return pd.DataFrame()
    df = df.copy()
    df["date"] = pd.to_datetime(df["collected_at"]).dt.date
    return df.groupby(["date", "source"])["price"].mean().reset_index()


def top_by_reviews(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Топ-N товаров по количеству отзывов."""
    if df.empty:
        return pd.DataFrame()
    return (
        df.nlargest(n, "reviews_count")
        [["name", "source", "price", "rating", "reviews_count"]]
        .reset_index(drop=True)
    )


def top_by_rating(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Топ-N товаров по рейтингу."""
    if df.empty:
        return pd.DataFrame()
    return (
        df[df["rating"] > 0]
        .nlargest(n, "rating")
        [["name", "source", "price", "rating", "reviews_count"]]
        .reset_index(drop=True)
    )


def cross_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Сводная таблица сравнения категорий."""
    if df.empty or "category" not in df.columns:
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
    )


def price_comparison_by_source(df: pd.DataFrame) -> pd.DataFrame:
    """Сравнение цен по магазинам для каждой категории."""
    if df.empty:
        return pd.DataFrame()
    return (
        df.groupby(["category", "source"])["price"]
        .agg(["mean", "min", "max", "count"])
        .round(2)
        .reset_index()
        .rename(columns={"mean": "avg_price", "min": "min_price",
                          "max": "max_price", "count": "total"})
    )
