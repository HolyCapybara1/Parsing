from .dns_parser import DnsParser
from .citilink_parser import CitilinkParser
from .regard_parser import RegardParser
from db.repository import save_products, SessionLocal, init_db
from db.models import Collection
from datetime import datetime
import logging

logger = logging.getLogger("runner")

CATEGORIES = ["Оперативная память", "Видеокарты", "Смартфоны"]


def run_all() -> dict:
    """Запустить парсинг всех магазинов и категорий."""
    init_db()

    with SessionLocal() as session:
        collection = Collection(started_at=datetime.utcnow(), status="running")
        session.add(collection)
        session.commit()
        cid = collection.id

    total = 0
    errors = 0
    parsers = [DnsParser(), CitilinkParser(), RegardParser()]

    for parser in parsers:
        for category in CATEGORIES:
            try:
                logger.info(f"Парсинг {parser.source_name} — {category}...")
                products = parser.parse_category(category)
                if products:
                    save_products(products, parser.source_name, cid)
                    total += len(products)
                    logger.info(f"  Сохранено: {len(products)} товаров")
                else:
                    logger.warning(f"  Товары не найдены: {parser.source_name} {category}")
            except Exception as e:
                errors += 1
                logger.error(f"Ошибка {parser.source_name} {category}: {e}")

    with SessionLocal() as session:
        col = session.get(Collection, cid)
        col.finished_at = datetime.utcnow()
        col.status = "success" if errors == 0 else "error"
        col.total_records = total
        session.commit()

    logger.info(f"Парсинг завершён: {total} товаров, {errors} ошибок")
    return {"total": total, "sources": len(parsers), "errors": errors}


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from logger.logger import setup_logger
    setup_logger("runner")
    result = run_all()
    print(f"Готово: {result}")
