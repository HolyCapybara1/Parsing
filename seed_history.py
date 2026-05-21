"""
Заполняет базу данных историческими ценами с 1 апреля по вчерашний день.
Запустить один раз: python seed_history.py
"""
import sys
import os
import random
import hashlib
from datetime import date, timedelta, datetime

sys.path.insert(0, os.path.dirname(__file__))

from db.repository import init_db, save_products, SessionLocal
from db.models import Collection
from scraper.demo_catalog import PRODUCTS as CATALOG

DEMO_START = date(2026, 4, 1)
DEMO_END   = date(2026, 7, 1)


def demo_price(base_price: float, name: str, target_date: date) -> float:
    cap = min(target_date, DEMO_END)
    days = max((cap - DEMO_START).days, 0)
    name_hash = int(hashlib.sha1(name.encode()).hexdigest()[:8], 16)
    rng = random.Random(name_hash)
    price = base_price
    for _ in range(days):
        price *= rng.uniform(0.991, 1.009)
    return max(round(price / 10) * 10, base_price * 0.75)


def main():
    init_db()

    today = date.today()
    yesterday = today - timedelta(days=1)

    start = DEMO_START
    end = min(yesterday, DEMO_END)

    if start > end:
        print("История уже полностью загружена.")
        return

    total_days = (end - start).days + 1
    total_records = 0

    print(f"Загружаю историю с {start} по {end} ({total_days} дней)...")

    current = start
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

        day_total = 0
        for source_name, items in CATALOG.items():
            products = []
            for item in items:
                p = dict(item)
                p["price"] = demo_price(item["price"], item["name"], current)
                products.append(p)
            save_products(products, source_name, cid)
            day_total += len(products)

        with SessionLocal() as session:
            col = session.get(Collection, cid)
            col.total_records = day_total
            session.commit()

        total_records += day_total
        print(f"  {current}: {day_total} товаров", end="\r")
        current += timedelta(days=1)

    print(f"\nГотово! Загружено {total_records} записей за {total_days} дней.")


if __name__ == "__main__":
    main()
