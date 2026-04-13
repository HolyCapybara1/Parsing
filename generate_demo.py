"""
Генератор тестовых данных — 4 дня, все категории, все магазины.
Запуск: python generate_demo.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import random
from datetime import datetime, timedelta
from db.repository import init_db, SessionLocal
from db.models import Collection, Product, Price, Source

random.seed(42)

init_db()

# ── Продукты по категориям ─────────────────────────────────────────────────
PRODUCTS = {
    "Оперативная память": [
        ("Kingston Fury Beast 16GB DDR5-5200", "Kingston", {"DNS": 4990, "Ситилинк": 5199, "Regard": 4850}),
        ("Kingston Fury Beast 32GB DDR5-5200", "Kingston", {"DNS": 9490, "Ситилинк": 9799, "Regard": 9350}),
        ("Corsair Vengeance 16GB DDR5-6000", "Corsair", {"DNS": 6290, "Ситилинк": 6499, "Regard": 6150}),
        ("Corsair Vengeance 32GB DDR5-6000", "Corsair", {"DNS": 11990, "Ситилинк": 12299, "Regard": 11800}),
        ("G.Skill Trident Z5 32GB DDR5-6400", "G.Skill", {"DNS": 14990, "Ситилинк": 15499, "Regard": 14750}),
        ("G.Skill Trident Z5 16GB DDR5-6400", "G.Skill", {"DNS": 8490, "Ситилинк": 8799, "Regard": 8300}),
        ("Crucial Pro 16GB DDR5-5600", "Crucial", {"DNS": 4490, "Ситилинк": 4690, "Regard": 4350}),
        ("Crucial Pro 32GB DDR5-5600", "Crucial", {"DNS": 8290, "Ситилинк": 8590, "Regard": 8100}),
        ("Team T-Force Vulcan 16GB DDR5-5200", "Team", {"DNS": 4190, "Ситилинк": 4350, "Regard": 4090}),
        ("Team T-Force Delta RGB 32GB DDR5-6000", "Team", {"DNS": 10490, "Ситилинк": 10799, "Regard": 10300}),
        ("Kingston Fury Renegade 32GB DDR5-7200", "Kingston", {"DNS": 18490, "Ситилинк": 18999, "Regard": 18200}),
        ("Patriot Viper Venom 16GB DDR4-3600", "Patriot", {"DNS": 2990, "Ситилинк": 3199, "Regard": 2890}),
        ("Patriot Viper Venom 32GB DDR4-3600", "Patriot", {"DNS": 5490, "Ситилинк": 5699, "Regard": 5350}),
        ("HyperX Fury 16GB DDR4-3200", "HyperX", {"DNS": 2490, "Ситилинк": 2650, "Regard": 2390}),
        ("HyperX Fury 32GB DDR4-3200", "HyperX", {"DNS": 4690, "Ситилинк": 4890, "Regard": 4590}),
        ("Samsung M471A2K43EB1 16GB DDR4", "Samsung", {"DNS": 3190, "Ситилинк": 3390, "Regard": 3090}),
        ("Hynix 16GB DDR4-3200 SODIMM", "Hynix", {"DNS": 2890, "Ситилинк": 3050, "Regard": 2790}),
        ("ADATA XPG Lancer 32GB DDR5-6000", "ADATA", {"DNS": 9990, "Ситилинк": 10299, "Regard": 9800}),
        ("ADATA XPG Lancer 16GB DDR5-6000", "ADATA", {"DNS": 5290, "Ситилинк": 5499, "Regard": 5150}),
        ("Lexar Thor 32GB DDR5-5600", "Lexar", {"DNS": 8790, "Ситилинк": 9099, "Regard": 8600}),
        ("Kingston ValueRAM 8GB DDR4-3200", "Kingston", {"DNS": 1590, "Ситилинк": 1690, "Regard": 1520}),
        ("Kingston ValueRAM 16GB DDR4-3200", "Kingston", {"DNS": 2790, "Ситилинк": 2990, "Regard": 2690}),
        ("Corsair Dominator Platinum 32GB DDR5-6200", "Corsair", {"DNS": 19990, "Ситилинк": 20499, "Regard": 19700}),
        ("G.Skill Ripjaws 5 16GB DDR4-3600", "G.Skill", {"DNS": 3490, "Ситилинк": 3699, "Regard": 3350}),
        ("Crucial Ballistix 32GB DDR4-3600", "Crucial", {"DNS": 6490, "Ситилинк": 6790, "Regard": 6350}),
    ],
    "Видеокарты": [
        ("ASUS ROG Strix RTX 4090 24GB", "ASUS", {"DNS": 189990, "Ситилинк": 195000, "Regard": 187500}),
        ("MSI Gaming X Trio RTX 4090 24GB", "MSI", {"DNS": 184990, "Ситилинк": 189999, "Regard": 183000}),
        ("Gigabyte Eagle RTX 4080 Super 16GB", "Gigabyte", {"DNS": 89990, "Ситилинк": 92999, "Regard": 88500}),
        ("ASUS Dual RTX 4070 Ti Super 16GB", "ASUS", {"DNS": 72990, "Ситилинк": 75499, "Regard": 71800}),
        ("MSI Ventus RTX 4070 Super 12GB", "MSI", {"DNS": 54990, "Ситилинк": 56999, "Regard": 54200}),
        ("Gigabyte Windforce RTX 4070 12GB", "Gigabyte", {"DNS": 47990, "Ситилинк": 49499, "Regard": 47300}),
        ("ASUS Phoenix RTX 4060 Ti 16GB", "ASUS", {"DNS": 42990, "Ситилинк": 44499, "Regard": 42500}),
        ("MSI Ventus 2X RTX 4060 8GB", "MSI", {"DNS": 31990, "Ситилинк": 33299, "Regard": 31500}),
        ("Palit Dual RTX 4060 8GB", "Palit", {"DNS": 29990, "Ситилинк": 30999, "Regard": 29700}),
        ("PowerColor Red Devil RX 7900 XTX 24GB", "PowerColor", {"DNS": 104990, "Ситилинк": 108999, "Regard": 103500}),
        ("Sapphire Nitro+ RX 7900 XT 20GB", "Sapphire", {"DNS": 74990, "Ситилинк": 77499, "Regard": 73800}),
        ("XFX Speedster MERC RX 7800 XT 16GB", "XFX", {"DNS": 44990, "Ситилинк": 46499, "Regard": 44300}),
        ("Gigabyte Eagle RX 7700 XT 12GB", "Gigabyte", {"DNS": 37990, "Ситилинк": 39499, "Regard": 37400}),
        ("ASUS Dual RX 7600 8GB", "ASUS", {"DNS": 27990, "Ситилинк": 28999, "Regard": 27600}),
        ("Sapphire Pulse RX 7600 XT 16GB", "Sapphire", {"DNS": 33990, "Ситилинк": 35299, "Regard": 33500}),
        ("MSI Gaming RTX 3060 12GB", "MSI", {"DNS": 24990, "Ситилинк": 25999, "Regard": 24600}),
        ("ASUS Dual RTX 3060 Ti 8GB", "ASUS", {"DNS": 29990, "Ситилинк": 30999, "Regard": 29500}),
        ("Gigabyte Vision OC RTX 4080 16GB", "Gigabyte", {"DNS": 84990, "Ситилинк": 87999, "Regard": 83800}),
        ("Inno3D Twin X2 RTX 4070 12GB", "Inno3D", {"DNS": 45990, "Ситилинк": 47499, "Regard": 45400}),
        ("Zotac Trinity RTX 4070 Super 12GB", "Zotac", {"DNS": 52990, "Ситилинк": 54999, "Regard": 52300}),
    ],
    "Смартфоны": [
        ("Samsung Galaxy S24 Ultra 256GB", "Samsung", {"DNS": 109990, "Ситилинк": 114990, "Regard": 108500}),
        ("Samsung Galaxy S24+ 256GB", "Samsung", {"DNS": 84990, "Ситилинк": 88990, "Regard": 83800}),
        ("Samsung Galaxy S24 256GB", "Samsung", {"DNS": 69990, "Ситилинк": 72990, "Regard": 68900}),
        ("Samsung Galaxy A55 256GB", "Samsung", {"DNS": 34990, "Ситилинк": 36490, "Regard": 34500}),
        ("Samsung Galaxy A35 128GB", "Samsung", {"DNS": 24990, "Ситилинк": 25990, "Regard": 24600}),
        ("Apple iPhone 15 Pro Max 256GB", "Apple", {"DNS": 134990, "Ситилинк": 139990, "Regard": 133500}),
        ("Apple iPhone 15 Pro 128GB", "Apple", {"DNS": 109990, "Ситилинк": 114990, "Regard": 108700}),
        ("Apple iPhone 15 256GB", "Apple", {"DNS": 89990, "Ситилинк": 93990, "Regard": 88900}),
        ("Apple iPhone 15 128GB", "Apple", {"DNS": 79990, "Ситилинк": 83990, "Regard": 79200}),
        ("Apple iPhone 14 128GB", "Apple", {"DNS": 64990, "Ситилинк": 67990, "Regard": 64200}),
        ("Xiaomi 14 Pro 512GB", "Xiaomi", {"DNS": 74990, "Ситилинк": 77990, "Regard": 74200}),
        ("Xiaomi 14 256GB", "Xiaomi", {"DNS": 54990, "Ситилинк": 56990, "Regard": 54300}),
        ("Xiaomi Redmi Note 13 Pro 256GB", "Xiaomi", {"DNS": 22990, "Ситилинк": 23990, "Regard": 22700}),
        ("Xiaomi Poco X6 Pro 256GB", "Xiaomi", {"DNS": 31990, "Ситилинк": 33490, "Regard": 31600}),
        ("HONOR Magic6 Pro 512GB", "HONOR", {"DNS": 74990, "Ситилинк": 77990, "Regard": 74000}),
        ("HONOR 90 Pro 256GB", "HONOR", {"DNS": 39990, "Ситилинк": 41490, "Regard": 39500}),
        ("realme GT 6T 256GB", "realme", {"DNS": 34990, "Ситилинк": 36490, "Regard": 34600}),
        ("OnePlus 12 256GB", "OnePlus", {"DNS": 64990, "Ситилинк": 67490, "Regard": 64200}),
        ("Google Pixel 8 Pro 128GB", "Google", {"DNS": 79990, "Ситилинк": 82990, "Regard": 79200}),
        ("Vivo X100 Pro 256GB", "Vivo", {"DNS": 74990, "Ситилинк": 77990, "Regard": 74300}),
    ],
    "Процессоры": [
        ("Intel Core i9-14900K", "Intel", {"DNS": 44990, "Ситилинк": 46499, "Regard": 44400}),
        ("Intel Core i7-14700K", "Intel", {"DNS": 29990, "Ситилинк": 31299, "Regard": 29600}),
        ("Intel Core i5-14600K", "Intel", {"DNS": 21990, "Ситилинк": 22999, "Regard": 21700}),
        ("Intel Core i5-14400F", "Intel", {"DNS": 13990, "Ситилинк": 14499, "Regard": 13800}),
        ("Intel Core i3-14100F", "Intel", {"DNS": 8990, "Ситилинк": 9299, "Regard": 8850}),
        ("AMD Ryzen 9 7950X", "AMD", {"DNS": 47990, "Ситилинк": 49499, "Regard": 47500}),
        ("AMD Ryzen 9 7900X", "AMD", {"DNS": 33990, "Ситилинк": 35299, "Regard": 33600}),
        ("AMD Ryzen 7 7700X", "AMD", {"DNS": 22990, "Ситилинк": 23999, "Regard": 22700}),
        ("AMD Ryzen 5 7600X", "AMD", {"DNS": 15990, "Ситилинк": 16699, "Regard": 15800}),
        ("AMD Ryzen 5 7600", "AMD", {"DNS": 13990, "Ситилинк": 14599, "Regard": 13800}),
        ("Intel Core i9-14900KF", "Intel", {"DNS": 42990, "Ситилинк": 44499, "Regard": 42500}),
        ("Intel Core i7-14700KF", "Intel", {"DNS": 27990, "Ситилинк": 28999, "Regard": 27700}),
        ("AMD Ryzen 7 7700", "AMD", {"DNS": 20990, "Ситилинк": 21799, "Regard": 20700}),
        ("AMD Ryzen 5 7500F", "AMD", {"DNS": 12990, "Ситилинк": 13499, "Regard": 12800}),
        ("Intel Core Ultra 9 285K", "Intel", {"DNS": 54990, "Ситилинк": 56999, "Regard": 54300}),
        ("Intel Core Ultra 7 265K", "Intel", {"DNS": 36990, "Ситилинк": 38499, "Regard": 36500}),
    ],
    "Ноутбуки": [
        ("ASUS ROG Zephyrus G14 RTX 4060 14\"", "ASUS", {"DNS": 99990, "Ситилинк": 104990, "Regard": 98800}),
        ("MSI Raider GE78 HX RTX 4080 17\"", "MSI", {"DNS": 179990, "Ситилинк": 187990, "Regard": 177500}),
        ("Lenovo Legion Pro 7i RTX 4070 16\"", "Lenovo", {"DNS": 129990, "Ситилинк": 134990, "Regard": 128500}),
        ("HP Omen 16 RTX 4060 16\"", "HP", {"DNS": 84990, "Ситилинк": 88990, "Regard": 83800}),
        ("Acer Nitro 5 RTX 4050 15.6\"", "Acer", {"DNS": 59990, "Ситилинк": 62490, "Regard": 59200}),
        ("Dell XPS 15 OLED i7-13700H 15\"", "Dell", {"DNS": 134990, "Ситилинк": 139990, "Regard": 133500}),
        ("Apple MacBook Pro 16\" M3 Pro", "Apple", {"DNS": 219990, "Ситилинк": 229990, "Regard": 217500}),
        ("Apple MacBook Air 15\" M2", "Apple", {"DNS": 119990, "Ситилинк": 124990, "Regard": 118700}),
        ("Samsung Galaxy Book4 Pro 360 16\"", "Samsung", {"DNS": 124990, "Ситилинк": 129990, "Regard": 123500}),
        ("Lenovo ThinkPad X1 Carbon Gen 11 14\"", "Lenovo", {"DNS": 139990, "Ситилинк": 145990, "Regard": 138500}),
        ("ASUS ZenBook Pro 14 OLED i7 14\"", "ASUS", {"DNS": 79990, "Ситилинк": 83490, "Regard": 79000}),
        ("Gigabyte Aorus 15 RTX 4070 15.6\"", "Gigabyte", {"DNS": 114990, "Ситилинк": 119490, "Regard": 113800}),
        ("MSI Prestige 14 i7-1360P 14\"", "MSI", {"DNS": 69990, "Ситилинк": 72990, "Regard": 69200}),
        ("HP Pavilion 15 i5-1335U 15.6\"", "HP", {"DNS": 44990, "Ситилинк": 46990, "Regard": 44400}),
        ("Acer Swift Go 14 OLED i7-1355U 14\"", "Acer", {"DNS": 54990, "Ситилинк": 56990, "Regard": 54300}),
        ("Huawei MateBook X Pro 2023 i7 13.5\"", "Huawei", {"DNS": 99990, "Ситилинк": 103990, "Regard": 98800}),
    ],
    "SSD-накопители": [
        ("Samsung 990 Pro 2TB NVMe", "Samsung", {"DNS": 14990, "Ситилинк": 15499, "Regard": 14700}),
        ("Samsung 990 Pro 1TB NVMe", "Samsung", {"DNS": 8490, "Ситилинк": 8799, "Regard": 8300}),
        ("Samsung 870 EVO 2TB SATA", "Samsung", {"DNS": 12990, "Ситилинк": 13499, "Regard": 12700}),
        ("Samsung 870 EVO 1TB SATA", "Samsung", {"DNS": 6990, "Ситилинк": 7299, "Regard": 6850}),
        ("WD Black SN850X 2TB NVMe", "WD", {"DNS": 14990, "Ситилинк": 15499, "Regard": 14700}),
        ("WD Black SN850X 1TB NVMe", "WD", {"DNS": 8990, "Ситилинк": 9299, "Regard": 8800}),
        ("Seagate FireCuda 530 2TB NVMe", "Seagate", {"DNS": 13990, "Ситилинк": 14499, "Regard": 13700}),
        ("Seagate FireCuda 530 1TB NVMe", "Seagate", {"DNS": 7990, "Ситилинк": 8299, "Regard": 7800}),
        ("Kingston KC3000 2TB NVMe", "Kingston", {"DNS": 11990, "Ситилинк": 12499, "Regard": 11700}),
        ("Kingston KC3000 1TB NVMe", "Kingston", {"DNS": 6490, "Ситилинк": 6799, "Regard": 6350}),
        ("Crucial P5 Plus 2TB NVMe", "Crucial", {"DNS": 10990, "Ситилинк": 11499, "Regard": 10750}),
        ("Crucial MX500 2TB SATA", "Crucial", {"DNS": 8990, "Ситилинк": 9299, "Regard": 8800}),
        ("Silicon Power P34A80 1TB NVMe", "Silicon Power", {"DNS": 4990, "Ситилинк": 5199, "Regard": 4850}),
        ("A-Data XPG Gammix S70 Blade 2TB", "ADATA", {"DNS": 12490, "Ситилинк": 12999, "Regard": 12300}),
        ("ADATA Legend 960 2TB NVMe", "ADATA", {"DNS": 9990, "Ситилинк": 10299, "Regard": 9800}),
        ("Transcend MTE250S 1TB NVMe", "Transcend", {"DNS": 4490, "Ситилинк": 4699, "Regard": 4350}),
        ("Patriot P400 1TB NVMe", "Patriot", {"DNS": 3990, "Ситилинк": 4199, "Regard": 3890}),
        ("Plextor M10PGN 1TB NVMe", "Plextor", {"DNS": 6990, "Ситилинк": 7299, "Regard": 6850}),
    ],
    "Наушники": [
        ("Sony WH-1000XM5 Wireless ANC", "Sony", {"DNS": 27990, "Ситилинк": 28990, "Regard": 27600}),
        ("Sony WF-1000XM5 TWS ANC", "Sony", {"DNS": 21990, "Ситилинк": 22990, "Regard": 21700}),
        ("Apple AirPods Pro 2", "Apple", {"DNS": 19990, "Ситилинк": 20990, "Regard": 19700}),
        ("Apple AirPods 3", "Apple", {"DNS": 12990, "Ситилинк": 13490, "Regard": 12800}),
        ("Bose QuietComfort 45 Wireless ANC", "Bose", {"DNS": 24990, "Ситилинк": 25990, "Regard": 24700}),
        ("Bose QuietComfort Earbuds II TWS", "Bose", {"DNS": 18990, "Ситилинк": 19990, "Regard": 18700}),
        ("Samsung Galaxy Buds3 Pro TWS", "Samsung", {"DNS": 14990, "Ситилинк": 15490, "Regard": 14700}),
        ("Jabra Elite 10 TWS ANC", "Jabra", {"DNS": 16990, "Ситилинк": 17490, "Regard": 16700}),
        ("Sennheiser Momentum 4 Wireless", "Sennheiser", {"DNS": 26990, "Ситилинк": 27990, "Regard": 26700}),
        ("Audio-Technica ATH-M50xBT2 Wireless", "Audio-Technica", {"DNS": 12990, "Ситилинк": 13490, "Regard": 12800}),
        ("JBL Tour One M2 Wireless ANC", "JBL", {"DNS": 15990, "Ситилинк": 16490, "Regard": 15700}),
        ("Beats Studio Pro Wireless ANC", "Beats", {"DNS": 22990, "Ситилинк": 23990, "Regard": 22700}),
        ("Marshall Major V Bluetooth", "Marshall", {"DNS": 9990, "Ситилинк": 10490, "Regard": 9800}),
        ("Plantronics Voyager Focus 2 UC", "Plantronics", {"DNS": 18990, "Ситилинк": 19990, "Regard": 18700}),
        ("Razer BlackShark V2 HyperSpeed", "Razer", {"DNS": 8990, "Ситилинк": 9490, "Regard": 8800}),
        ("HyperX Cloud III Wireless", "HyperX", {"DNS": 10990, "Ситилинк": 11490, "Regard": 10800}),
        ("Xiaomi Buds 5 Pro TWS ANC", "Xiaomi", {"DNS": 9990, "Ситилинк": 10490, "Regard": 9800}),
        ("SteelSeries Arctis Nova Pro Wireless", "SteelSeries", {"DNS": 21990, "Ситилинк": 22990, "Regard": 21700}),
    ],
}

# Рейтинги по умолчанию для каждой категории (base, deviation)
RATINGS = {
    "Оперативная память": (4.5, 0.3),
    "Видеокарты":         (4.6, 0.25),
    "Смартфоны":          (4.4, 0.35),
    "Процессоры":         (4.7, 0.2),
    "Ноутбуки":           (4.3, 0.4),
    "SSD-накопители":     (4.5, 0.3),
    "Наушники":           (4.4, 0.35),
}

REVIEW_RANGES = {
    "Оперативная память": (50, 800),
    "Видеокарты":         (20, 400),
    "Смартфоны":          (100, 2000),
    "Процессоры":         (30, 600),
    "Ноутбуки":           (20, 500),
    "SSD-накопители":     (40, 700),
    "Наушники":           (30, 1500),
}


def rand_rating(category: str, seed_val: int) -> float:
    r = random.Random(seed_val)
    base, dev = RATINGS.get(category, (4.3, 0.4))
    v = base + r.uniform(-dev, dev)
    return round(max(1.0, min(5.0, v)), 1)


def rand_reviews(category: str, seed_val: int) -> int:
    r = random.Random(seed_val + 1000)
    lo, hi = REVIEW_RANGES.get(category, (20, 500))
    return r.randint(lo, hi)


def rand_price(base: float, day_idx: int, store: str) -> float:
    """Цена с небольшой вариацией по дням (+/-8%), округлённая до 10 ₽."""
    r = random.Random(hash((base, day_idx, store)))
    factor = 1.0 + r.uniform(-0.08, 0.08)
    return round(base * factor / 10) * 10


def main():
    base_date = datetime.utcnow().replace(hour=12, minute=0, second=0, microsecond=0)
    # 4 дня: 3 дня назад → сегодня
    dates = [base_date - timedelta(days=3 - i) for i in range(4)]

    with SessionLocal() as session:
        sources = {s.name: s for s in session.query(Source).all()}

    if not sources:
        print("Источники не найдены. Убедитесь, что init_db() выполнен.")
        return

    total_saved = 0

    for day_idx, date in enumerate(dates):
        print(f"\nДень {day_idx + 1}/4 — {date.strftime('%d.%m.%Y')} ...")

        with SessionLocal() as session:
            collection = Collection(
                started_at=date,
                finished_at=date,
                status="success",
                total_records=0,
            )
            session.add(collection)
            session.commit()
            cid = collection.id

            day_total = 0
            for category, products in PRODUCTS.items():
                for prod_name, brand, store_prices in products:
                    for store_name, base_price in store_prices.items():
                        source = session.query(Source).filter_by(name=store_name).first()
                        if source is None:
                            continue

                        # Найти или создать товар
                        product = session.query(Product).filter_by(
                            name=prod_name, source_id=source.id
                        ).first()
                        if not product:
                            product = Product(
                                name=prod_name,
                                brand=brand,
                                category=category,
                                source_id=source.id,
                            )
                            session.add(product)
                            session.flush()

                        seed = hash((prod_name, store_name))
                        price_val = rand_price(base_price, day_idx, store_name)
                        rating = rand_rating(category, seed + day_idx)
                        reviews = rand_reviews(category, seed)

                        price_rec = Price(
                            product_id=product.id,
                            price=price_val,
                            rating=rating,
                            reviews_count=reviews,
                            collected_at=date,
                            collection_id=cid,
                        )
                        session.add(price_rec)
                        day_total += 1

            collection.total_records = day_total
            session.commit()
            total_saved += day_total
            print(f"  Сохранено: {day_total} записей")

    print(f"\nГотово! Всего записей: {total_saved}")
    print(f"Охвачено категорий: {len(PRODUCTS)}, магазинов: 3, дней: 4")


if __name__ == "__main__":
    main()
