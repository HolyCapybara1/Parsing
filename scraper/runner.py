from .dns_parser import DnsParser
from .citilink_parser import CitilinkParser
from .regard_parser import RegardParser
from db.repository import save_products, SessionLocal, init_db
from db.models import Collection
from datetime import datetime
import logging

logger = logging.getLogger("runner")

# Все доступные категории
ALL_CATEGORIES = [
    "Оперативная память",
    "Видеокарты",
    "Смартфоны",
    "Процессоры",
    "Ноутбуки",
    "SSD-накопители",
    "Наушники",
]

# Все доступные магазины
ALL_SOURCES = ["DNS", "Ситилинк", "Regard"]


def run_all(
    categories: list[str] = None,
    sources: list[str] = None,
) -> dict:
    """
    Запустить парсинг.

    :param categories: список категорий для сбора (None = все)
    :param sources:    список магазинов для сбора (None = все)
    :return: словарь с итогами
    """
    init_db()

    if categories is None:
        categories = ALL_CATEGORIES
    if sources is None:
        sources = ALL_SOURCES

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

    # Пример: только смартфоны с DNS
    result = run_all(categories=["Смартфоны"], sources=["DNS"])
    print(f"Готово: {result}")
