import sys
import os

# Добавляем корень проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

st.set_page_config(
    page_title="ЦенМонитор",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from db.repository import init_db
from sqlalchemy import text

init_db()


def _auto_seed():
    """Автоматически заполнить историю цен при первом запуске."""
    import sys
    import random
    import hashlib
    from datetime import date, timedelta, datetime
    from db.repository import SessionLocal, save_products
    from db.models import Collection

    with SessionLocal() as session:
        count = session.execute(text("SELECT COUNT(*) FROM prices")).scalar()
    if count and count > 0:
        return

    try:
        from scraper.demo_catalog import PRODUCTS as CATALOG
    except ImportError:
        return

    DEMO_START = date(2026, 4, 1)
    DEMO_END   = date(2026, 7, 1)

    def _price(base, name, d):
        cap = min(d, DEMO_END)
        days = max((cap - DEMO_START).days, 0)
        rng = random.Random(int(hashlib.sha1(name.encode()).hexdigest()[:8], 16))
        p = base
        for _ in range(days):
            p *= rng.uniform(0.991, 1.009)
        return max(round(p / 10) * 10, base * 0.75)

    today = date.today()
    end = min(today, DEMO_END)
    current = DEMO_START

    while current <= end:
        with SessionLocal() as session:
            col = Collection(
                started_at=datetime.combine(current, datetime.min.time()),
                finished_at=datetime.combine(current, datetime.min.time()) + timedelta(minutes=12),
                status="success",
            )
            session.add(col)
            session.commit()
            cid = col.id

        for source_name, items in CATALOG.items():
            products = [dict(p, price=_price(p["price"], p["name"], current)) for p in items]
            save_products(products, source_name, cid)

        current += timedelta(days=1)


_auto_seed()

st.title("📊 ЦенМонитор — Система мониторинга цен конкурентов")
st.markdown(
    """
    Добро пожаловать в **ЦенМонитор** — систему автоматического сбора и анализа цен
    интернет-магазинов электроники.

    **Выберите раздел в левом меню:**

    | Раздел | Что делает |
    |---|---|
    | **Парсинг** | Выбор категорий и запуск сбора данных с сайтов магазинов |
    | **Аналитика** | Полный анализ рынка, цен, отзывов и конкурентов |
    | **Сравнение категорий** | Сравнение товаров между категориями и магазинами |
    | **Ценовые сегменты** | Разбивка товаров на бюджетный / средний / премиум классы |
    | **Все товары** | Полная таблица товаров с поиском, фильтрами и экспортом |
    """
)

st.info(
    "Если данных ещё нет — перейдите на страницу **Парсинг** "
    "и нажмите кнопку **Собрать данные**."
)
