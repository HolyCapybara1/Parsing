import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from .models import Base, Product, Price, Source, Collection, MLCluster

os.makedirs("data", exist_ok=True)
DATABASE_URL = "sqlite:///data/prices.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Создать все таблицы если не существуют."""
    Base.metadata.create_all(engine)
    _seed_sources()


def _seed_sources():
    """Добавить источники-магазины в БД при первом запуске."""
    with SessionLocal() as session:
        if session.query(Source).count() == 0:
            sources = [
                Source(name="DNS", base_url="https://www.dns-shop.ru"),
                Source(name="Ситилинк", base_url="https://www.citilink.ru"),
                Source(name="Regard", base_url="https://www.regard.ru"),
            ]
            session.add_all(sources)
            session.commit()


def save_products(products: list[dict], source_name: str, collection_id: int):
    """Сохранить список товаров из парсера в БД."""
    with SessionLocal() as session:
        source = session.query(Source).filter_by(name=source_name).first()
        if not source:
            return
        for item in products:
            product = session.query(Product).filter_by(
                name=item["name"], source_id=source.id).first()
            if not product:
                product = Product(
                    name=item["name"],
                    brand=item.get("brand", ""),
                    category=item["category"],
                    url=item.get("url", ""),
                    source_id=source.id
                )
                session.add(product)
                session.flush()

            price = Price(
                product_id=product.id,
                price=item["price"],
                rating=item.get("rating", 0.0),
                reviews_count=item.get("reviews_count", 0),
                collection_id=collection_id
            )
            session.add(price)
        session.commit()


def get_all_products() -> pd.DataFrame:
    """Вернуть все товары с последней ценой как DataFrame."""
    query = """
        SELECT p.id, p.name, p.brand, p.category,
               s.name as source, pr.price, pr.rating,
               pr.reviews_count, pr.collected_at,
               mc.segment
        FROM products p
        JOIN sources s ON p.source_id = s.id
        JOIN prices pr ON pr.product_id = p.id
        LEFT JOIN ml_clusters mc ON mc.product_id = p.id
        WHERE pr.collected_at = (
            SELECT MAX(collected_at) FROM prices
            WHERE product_id = p.id)
        ORDER BY pr.collected_at DESC
    """
    with engine.connect() as conn:
        try:
            return pd.read_sql(text(query), conn)
        except Exception:
            return pd.DataFrame()


def get_price_history() -> pd.DataFrame:
    """Вернуть всю историю цен для графика динамики."""
    query = """
        SELECT p.name, p.category, s.name as source,
               pr.price, pr.collected_at
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        JOIN sources s ON p.source_id = s.id
        ORDER BY pr.collected_at
    """
    with engine.connect() as conn:
        try:
            return pd.read_sql(text(query), conn)
        except Exception:
            return pd.DataFrame()


def get_collections() -> pd.DataFrame:
    """Вернуть историю сеансов парсинга."""
    query = """
        SELECT id, started_at, finished_at, status, total_records
        FROM collections
        ORDER BY started_at DESC
        LIMIT 20
    """
    with engine.connect() as conn:
        try:
            return pd.read_sql(text(query), conn)
        except Exception:
            return pd.DataFrame()
