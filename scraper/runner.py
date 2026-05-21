import os
import random
import hashlib
import logging
from datetime import datetime, date, timedelta

from db.repository import save_products, SessionLocal, init_db
from db.models import Collection

logger = logging.getLogger("runner")

ALL_CATEGORIES = [
    "Оперативная память",
    "Видеокарты",
    "Смартфоны",
    "Процессоры",
    "Ноутбуки",
    "SSD-накопители",
    "Наушники",
]

ALL_SOURCES = ["DNS", "Ситилинк", "Regard"]

_DEMO_START = date(2026, 4, 1)
_DEMO_END   = date(2026, 7, 1)


def _demo_price(base_price: float, name: str, target_date: date) -> float:
    cap = min(target_date, _DEMO_END)
    days = max((cap - _DEMO_START).days, 0)
    name_hash = int(hashlib.sha1(name.encode()).hexdigest()[:8], 16)
    rng = random.Random(name_hash)
    price = base_price
    for _ in range(days):
        price *= rng.uniform(0.991, 1.009)
    return max(round(price / 10) * 10, base_price * 0.75)


def _run_demo(categories: list[str], sources: list[str]) -> dict:
    """Загрузить данные из demo_catalog для текущей даты."""
    from .demo_catalog import PRODUCTS as CATALOG

    today = date.today()
    init_db()

    with SessionLocal() as session:
        collection = Collection(
            started_at=datetime.utcnow(),
            status="running",
        )
        session.add(collection)
        session.commit()
        cid = collection.id

    total = 0
    active_sources = 0

    for source_name, catalog_items in CATALOG.items():
        if source_name not in sources:
            continue
        active_sources += 1

        to_save = []
        for item in catalog_items:
            if item["category"] not in categories:
                continue
            product = dict(item)
            product["price"] = _demo_price(item["price"], item["name"], today)
            to_save.append(product)

        if to_save:
            save_products(to_save, source_name, cid)
            total += len(to_save)
            logger.info(f"[DEMO] {source_name}: загружено {len(to_save)} товаров за {today}")

    with SessionLocal() as session:
        col = session.get(Collection, cid)
        col.finished_at = datetime.utcnow()
        col.status = "success"
        col.total_records = total
        session.commit()

    logger.info(f"[DEMO] Итого: {total} товаров из {active_sources} магазинов")
    return {
        "total": total,
        "sources": active_sources,
        "categories": len(categories),
        "errors": 0,
    }


def run_all(
    categories: list[str] = None,
    sources: list[str] = None,
) -> dict:
    """
    Запустить сбор данных.
    Если присутствует scraper/demo_catalog.py — используется демо-режим.
    Иначе — реальный парсинг сайтов.
    """
    if categories is None:
        categories = ALL_CATEGORIES
    if sources is None:
        sources = ALL_SOURCES

    demo_catalog = os.path.join(os.path.dirname(__file__), "demo_catalog.py")
    if os.path.exists(demo_catalog):
        return _run_demo(categories, sources)

    # ── Реальный парсинг ──────────────────────────────────────────────────
    from .dns_parser import DnsParser
    from .citilink_parser import CitilinkParser
    from .regard_parser import RegardParser

    init_db()

    with SessionLocal() as session:
        collection = Collection(started_at=datetime.utcnow(), status="running")
        session.add(collection)
        session.commit()
        cid = collection.id

    all_parsers = {
        "DNS": DnsParser(),
        "Ситилинк": CitilinkParser(),
        "Regard": RegardParser(),
    }
    active_parsers = [p for name, p in all_parsers.items() if name in sources]

    total = 0
    errors = 0

    for parser in active_parsers:
        for category in categories:
            try:
                logger.info(f">>> Парсинг: {parser.source_name} — {category}")
                products = parser.parse_category(category)
                if products:
                    save_products(products, parser.source_name, cid)
                    total += len(products)
                    logger.info(f"    Сохранено: {len(products)} товаров")
                else:
                    logger.warning(f"    Товары не найдены: {parser.source_name} / {category}")
            except Exception as e:
                errors += 1
                logger.error(f"Ошибка {parser.source_name} {category}: {e}")

    with SessionLocal() as session:
        col = session.get(Collection, cid)
        col.finished_at = datetime.utcnow()
        col.status = "success" if errors == 0 else "partial"
        col.total_records = total
        session.commit()

    logger.info(f"Парсинг завершён: {total} товаров, {errors} ошибок")
    return {
        "total": total,
        "sources": len(active_parsers),
        "categories": len(categories),
        "errors": errors,
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from logger.logger import setup_all_loggers
    setup_all_loggers()

    result = run_all(categories=["Смартфоны"], sources=["DNS"])
    print(f"Готово: {result}")
