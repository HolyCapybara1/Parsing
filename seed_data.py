import sys, os, random
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(".")))
from db.repository import init_db, save_products, SessionLocal
from db.models import Collection

init_db()

dns = [
    {"name":"Kingston FURY Beast 16GB DDR5 5200MHz","brand":"Kingston","category":"Оперативная память","price":4299.0,"rating":4.8,"reviews_count":312,"url":""},
    {"name":"Crucial 32GB DDR4 3200MHz DIMM","brand":"Crucial","category":"Оперативная память","price":5490.0,"rating":4.6,"reviews_count":209,"url":""},
    {"name":"G.Skill Trident Z5 RGB 32GB DDR5 6000MHz","brand":"G.Skill","category":"Оперативная память","price":14990.0,"rating":4.9,"reviews_count":87,"url":""},
    {"name":"Samsung 8GB DDR4 3200MHz DIMM","brand":"Samsung","category":"Оперативная память","price":1790.0,"rating":4.5,"reviews_count":431,"url":""},
    {"name":"Corsair Vengeance LPX 16GB DDR4 3600MHz","brand":"Corsair","category":"Оперативная память","price":3490.0,"rating":4.7,"reviews_count":267,"url":""},
    {"name":"ASUS DUAL RTX 4060 8GB","brand":"ASUS","category":"Видеокарты","price":32990.0,"rating":4.7,"reviews_count":198,"url":""},
    {"name":"MSI Gaming X Slim RTX 4070 12GB","brand":"MSI","category":"Видеокарты","price":54990.0,"rating":4.8,"reviews_count":143,"url":""},
    {"name":"Gigabyte AORUS Master RTX 4080 Super 16GB","brand":"Gigabyte","category":"Видеокарты","price":109990.0,"rating":4.9,"reviews_count":61,"url":""},
    {"name":"Sapphire PULSE RX 7600 8GB","brand":"Sapphire","category":"Видеокарты","price":27490.0,"rating":4.6,"reviews_count":112,"url":""},
    {"name":"ASUS ROG STRIX RTX 4090 24GB","brand":"ASUS","category":"Видеокарты","price":219990.0,"rating":4.9,"reviews_count":34,"url":""},
    {"name":"Apple iPhone 15 128GB черный","brand":"Apple","category":"Смартфоны","price":79990.0,"rating":4.8,"reviews_count":1243,"url":""},
    {"name":"Samsung Galaxy S24 256GB черный фантом","brand":"Samsung","category":"Смартфоны","price":74990.0,"rating":4.7,"reviews_count":654,"url":""},
    {"name":"Xiaomi 14 256GB черный","brand":"Xiaomi","category":"Смартфоны","price":59990.0,"rating":4.7,"reviews_count":321,"url":""},
    {"name":"Samsung Galaxy A55 256GB темно-синий","brand":"Samsung","category":"Смартфоны","price":34990.0,"rating":4.5,"reviews_count":432,"url":""},
    {"name":"HONOR 200 Pro 512GB черный","brand":"HONOR","category":"Смартфоны","price":49990.0,"rating":4.6,"reviews_count":145,"url":""},
    {"name":"Intel Core i9-14900K BOX","brand":"Intel","category":"Процессоры","price":44990.0,"rating":4.9,"reviews_count":234,"url":""},
    {"name":"AMD Ryzen 9 7950X BOX","brand":"AMD","category":"Процессоры","price":52990.0,"rating":4.9,"reviews_count":187,"url":""},
    {"name":"Intel Core i5-14600K BOX","brand":"Intel","category":"Процессоры","price":22990.0,"rating":4.7,"reviews_count":412,"url":""},
    {"name":"AMD Ryzen 5 7600X BOX","brand":"AMD","category":"Процессоры","price":18490.0,"rating":4.8,"reviews_count":356,"url":""},
    {"name":"Intel Core i7-14700KF BOX","brand":"Intel","category":"Процессоры","price":34990.0,"rating":4.8,"reviews_count":178,"url":""},
    {"name":"ASUS VivoBook 16 AMD Ryzen 5 7520U 16GB 512GB","brand":"ASUS","category":"Ноутбуки","price":54990.0,"rating":4.6,"reviews_count":312,"url":""},
    {"name":"Lenovo IdeaPad Slim 5 Intel Core i5-13420H 16GB 512GB","brand":"Lenovo","category":"Ноутбуки","price":64990.0,"rating":4.7,"reviews_count":198,"url":""},
    {"name":"Apple MacBook Air M2 8GB 256GB серый космос","brand":"Apple","category":"Ноутбуки","price":104990.0,"rating":4.9,"reviews_count":543,"url":""},
    {"name":"HP Laptop 15s Intel Core i3-1215U 8GB 256GB","brand":"HP","category":"Ноутбуки","price":39990.0,"rating":4.4,"reviews_count":267,"url":""},
    {"name":"MSI Thin GF63 Intel Core i5-12450H 8GB 512GB RTX 2050","brand":"MSI","category":"Ноутбуки","price":59990.0,"rating":4.5,"reviews_count":143,"url":""},
    {"name":"Samsung 980 Pro 1TB M.2 NVMe","brand":"Samsung","category":"SSD-накопители","price":8490.0,"rating":4.9,"reviews_count":876,"url":""},
    {"name":"WD Black SN850X 2TB M.2 NVMe","brand":"WD","category":"SSD-накопители","price":14990.0,"rating":4.8,"reviews_count":432,"url":""},
    {"name":"Kingston NV2 500GB M.2 NVMe","brand":"Kingston","category":"SSD-накопители","price":2990.0,"rating":4.5,"reviews_count":654,"url":""},
    {"name":"Crucial MX500 1TB SATA","brand":"Crucial","category":"SSD-накопители","price":5990.0,"rating":4.7,"reviews_count":543,"url":""},
    {"name":"Seagate BarraCuda Q5 500GB M.2 NVMe","brand":"Seagate","category":"SSD-накопители","price":3490.0,"rating":4.3,"reviews_count":312,"url":""},
    {"name":"Sony WH-1000XM5 черный","brand":"Sony","category":"Наушники","price":29990.0,"rating":4.9,"reviews_count":876,"url":""},
    {"name":"Apple AirPods Pro 2","brand":"Apple","category":"Наушники","price":24990.0,"rating":4.8,"reviews_count":1243,"url":""},
    {"name":"JBL Tune 770NC черный","brand":"JBL","category":"Наушники","price":8490.0,"rating":4.6,"reviews_count":432,"url":""},
    {"name":"Sennheiser HD 560S","brand":"Sennheiser","category":"Наушники","price":12990.0,"rating":4.7,"reviews_count":234,"url":""},
    {"name":"HyperX Cloud Alpha черный","brand":"HyperX","category":"Наушники","price":9990.0,"rating":4.7,"reviews_count":567,"url":""},
]

citilink = [
    {"name":"Patriot Viper Steel 16GB DDR4 3600MHz","brand":"Patriot","category":"Оперативная память","price":3190.0,"rating":4.6,"reviews_count":189,"url":""},
    {"name":"Corsair Dominator Platinum RGB 64GB DDR5 5600MHz","brand":"Corsair","category":"Оперативная память","price":24990.0,"rating":4.8,"reviews_count":41,"url":""},
    {"name":"Kingston FURY Renegade 16GB DDR4 3600MHz","brand":"Kingston","category":"Оперативная память","price":3890.0,"rating":4.8,"reviews_count":234,"url":""},
    {"name":"G.Skill Ripjaws V 32GB DDR4 3600MHz","brand":"G.Skill","category":"Оперативная память","price":6290.0,"rating":4.7,"reviews_count":143,"url":""},
    {"name":"Hynix 8GB DDR4 3200MHz","brand":"Hynix","category":"Оперативная память","price":1590.0,"rating":4.3,"reviews_count":378,"url":""},
    {"name":"Gigabyte Gaming OC RTX 4070 Super 12GB","brand":"Gigabyte","category":"Видеокарты","price":64990.0,"rating":4.8,"reviews_count":97,"url":""},
    {"name":"MSI Gaming RX 7800 XT 16GB","brand":"MSI","category":"Видеокарты","price":48990.0,"rating":4.7,"reviews_count":68,"url":""},
    {"name":"ASUS Phoenix RTX 3060 12GB","brand":"ASUS","category":"Видеокарты","price":24990.0,"rating":4.5,"reviews_count":287,"url":""},
    {"name":"MSI SUPRIM X RTX 4080 16GB","brand":"MSI","category":"Видеокарты","price":99990.0,"rating":4.9,"reviews_count":45,"url":""},
    {"name":"PowerColor Hellhound RX 7900 GRE 16GB","brand":"PowerColor","category":"Видеокарты","price":59990.0,"rating":4.7,"reviews_count":52,"url":""},
    {"name":"Samsung Galaxy S24 Ultra 256GB титановый серый","brand":"Samsung","category":"Смартфоны","price":124990.0,"rating":4.9,"reviews_count":543,"url":""},
    {"name":"Xiaomi 14 Ultra 512GB белый","brand":"Xiaomi","category":"Смартфоны","price":99990.0,"rating":4.8,"reviews_count":176,"url":""},
    {"name":"Google Pixel 8 128GB черный","brand":"Google","category":"Смартфоны","price":64990.0,"rating":4.7,"reviews_count":234,"url":""},
    {"name":"HONOR 90 256GB полночный черный","brand":"HONOR","category":"Смартфоны","price":24990.0,"rating":4.4,"reviews_count":312,"url":""},
    {"name":"Xiaomi Redmi 13C 256GB","brand":"Xiaomi","category":"Смартфоны","price":13990.0,"rating":4.2,"reviews_count":621,"url":""},
    {"name":"AMD Ryzen 7 7700X BOX","brand":"AMD","category":"Процессоры","price":28490.0,"rating":4.8,"reviews_count":298,"url":""},
    {"name":"Intel Core i3-14100F BOX","brand":"Intel","category":"Процессоры","price":8990.0,"rating":4.6,"reviews_count":534,"url":""},
    {"name":"AMD Ryzen 5 5600X BOX","brand":"AMD","category":"Процессоры","price":12490.0,"rating":4.8,"reviews_count":876,"url":""},
    {"name":"Intel Core i9-13900KS BOX","brand":"Intel","category":"Процессоры","price":54990.0,"rating":4.9,"reviews_count":143,"url":""},
    {"name":"AMD Ryzen 9 5900X BOX","brand":"AMD","category":"Процессоры","price":22990.0,"rating":4.8,"reviews_count":421,"url":""},
    {"name":"Acer Aspire 5 Intel Core i5-1335U 16GB 512GB","brand":"Acer","category":"Ноутбуки","price":59990.0,"rating":4.5,"reviews_count":234,"url":""},
    {"name":"ASUS ROG Strix G15 Ryzen 7 6800H 16GB 512GB RTX 3060","brand":"ASUS","category":"Ноутбуки","price":89990.0,"rating":4.7,"reviews_count":312,"url":""},
    {"name":"Lenovo Legion 5 Ryzen 5 7640H 16GB 512GB RTX 4060","brand":"Lenovo","category":"Ноутбуки","price":84990.0,"rating":4.8,"reviews_count":198,"url":""},
    {"name":"Dell Inspiron 15 Intel Core i5-1335U 8GB 512GB","brand":"Dell","category":"Ноутбуки","price":54990.0,"rating":4.4,"reviews_count":156,"url":""},
    {"name":"Apple MacBook Pro 14 M3 8GB 512GB","brand":"Apple","category":"Ноутбуки","price":164990.0,"rating":4.9,"reviews_count":432,"url":""},
    {"name":"Crucial P3 Plus 1TB M.2 NVMe","brand":"Crucial","category":"SSD-накопители","price":4990.0,"rating":4.6,"reviews_count":432,"url":""},
    {"name":"Samsung 870 EVO 1TB SATA","brand":"Samsung","category":"SSD-накопители","price":7990.0,"rating":4.8,"reviews_count":765,"url":""},
    {"name":"Kingston A2000 500GB M.2 NVMe","brand":"Kingston","category":"SSD-накопители","price":2490.0,"rating":4.4,"reviews_count":543,"url":""},
    {"name":"WD Blue SN570 1TB M.2 NVMe","brand":"WD","category":"SSD-накопители","price":5490.0,"rating":4.7,"reviews_count":387,"url":""},
    {"name":"Transcend MTE220S 2TB M.2 NVMe","brand":"Transcend","category":"SSD-накопители","price":9990.0,"rating":4.5,"reviews_count":198,"url":""},
    {"name":"Bose QuietComfort 45 черный","brand":"Bose","category":"Наушники","price":27990.0,"rating":4.8,"reviews_count":654,"url":""},
    {"name":"Samsung Galaxy Buds2 Pro черный","brand":"Samsung","category":"Наушники","price":12990.0,"rating":4.6,"reviews_count":432,"url":""},
    {"name":"Beats Studio Pro черный","brand":"Beats","category":"Наушники","price":29990.0,"rating":4.5,"reviews_count":198,"url":""},
    {"name":"Jabra Evolve2 55 стерео","brand":"Jabra","category":"Наушники","price":34990.0,"rating":4.7,"reviews_count":143,"url":""},
    {"name":"Audio-Technica ATH-M50x черный","brand":"Audio-Technica","category":"Наушники","price":14990.0,"rating":4.8,"reviews_count":876,"url":""},
]

regard = [
    {"name":"Kingston FURY Beast RGB 16GB DDR4 3200MHz","brand":"Kingston","category":"Оперативная память","price":3590.0,"rating":4.7,"reviews_count":267,"url":""},
    {"name":"Corsair Vengeance RGB 32GB DDR5 5600MHz","brand":"Corsair","category":"Оперативная память","price":11990.0,"rating":4.8,"reviews_count":78,"url":""},
    {"name":"G.Skill Trident Z5 Neo 32GB DDR5 6000MHz","brand":"G.Skill","category":"Оперативная память","price":15490.0,"rating":4.9,"reviews_count":56,"url":""},
    {"name":"ADATA 8GB DDR4 3200MHz","brand":"ADATA","category":"Оперативная память","price":1490.0,"rating":4.2,"reviews_count":312,"url":""},
    {"name":"Patriot Signature 8GB DDR4 3200MHz","brand":"Patriot","category":"Оперативная память","price":1390.0,"rating":4.3,"reviews_count":445,"url":""},
    {"name":"ASUS ROG STRIX RTX 4070 Ti Super OC 16GB","brand":"ASUS","category":"Видеокарты","price":89990.0,"rating":4.9,"reviews_count":38,"url":""},
    {"name":"Gigabyte Gaming OC RX 7600 XT 16GB","brand":"Gigabyte","category":"Видеокарты","price":35990.0,"rating":4.5,"reviews_count":61,"url":""},
    {"name":"Sapphire NITRO+ RX 7900 XT 20GB","brand":"Sapphire","category":"Видеокарты","price":79990.0,"rating":4.8,"reviews_count":29,"url":""},
    {"name":"Palit Dual RTX 4060 8GB","brand":"Palit","category":"Видеокарты","price":30990.0,"rating":4.5,"reviews_count":112,"url":""},
    {"name":"MSI SUPRIM LIQUID X RTX 4090 24GB","brand":"MSI","category":"Видеокарты","price":229990.0,"rating":5.0,"reviews_count":18,"url":""},
    {"name":"Apple iPhone 15 Pro Max 256GB натуральный титан","brand":"Apple","category":"Смартфоны","price":134990.0,"rating":4.9,"reviews_count":432,"url":""},
    {"name":"Samsung Galaxy S24+ 256GB мраморный серый","brand":"Samsung","category":"Смартфоны","price":94990.0,"rating":4.8,"reviews_count":287,"url":""},
    {"name":"Xiaomi Poco X6 Pro 256GB черный","brand":"Xiaomi","category":"Смартфоны","price":27990.0,"rating":4.6,"reviews_count":345,"url":""},
    {"name":"HONOR Magic6 Pro 512GB черный","brand":"HONOR","category":"Смартфоны","price":79990.0,"rating":4.7,"reviews_count":94,"url":""},
    {"name":"Xiaomi Redmi Note 13 128GB","brand":"Xiaomi","category":"Смартфоны","price":16990.0,"rating":4.3,"reviews_count":534,"url":""},
    {"name":"AMD Ryzen 9 7900X BOX","brand":"AMD","category":"Процессоры","price":38990.0,"rating":4.9,"reviews_count":198,"url":""},
    {"name":"Intel Core i5-13600K BOX","brand":"Intel","category":"Процессоры","price":19990.0,"rating":4.8,"reviews_count":345,"url":""},
    {"name":"AMD Ryzen 7 5800X3D BOX","brand":"AMD","category":"Процессоры","price":24990.0,"rating":5.0,"reviews_count":543,"url":""},
    {"name":"Intel Core i3-13100 BOX","brand":"Intel","category":"Процессоры","price":7990.0,"rating":4.5,"reviews_count":267,"url":""},
    {"name":"AMD Ryzen 5 7500F BOX","brand":"AMD","category":"Процессоры","price":14990.0,"rating":4.8,"reviews_count":312,"url":""},
    {"name":"Huawei MateBook D15 Intel Core i5-1155G7 8GB 512GB","brand":"Huawei","category":"Ноутбуки","price":49990.0,"rating":4.5,"reviews_count":312,"url":""},
    {"name":"MSI Katana GF66 Intel Core i7-12650H 16GB 512GB RTX 3060","brand":"MSI","category":"Ноутбуки","price":79990.0,"rating":4.6,"reviews_count":178,"url":""},
    {"name":"Gigabyte AORUS 15 Ryzen 7 7745HX 16GB 1TB RTX 4060","brand":"Gigabyte","category":"Ноутбуки","price":94990.0,"rating":4.7,"reviews_count":134,"url":""},
    {"name":"Samsung Galaxy Book3 Intel Core i5-1335U 8GB 256GB","brand":"Samsung","category":"Ноутбуки","price":69990.0,"rating":4.4,"reviews_count":98,"url":""},
    {"name":"Acer Nitro 5 Ryzen 5 7535HS 16GB 512GB RTX 4050","brand":"Acer","category":"Ноутбуки","price":74990.0,"rating":4.6,"reviews_count":234,"url":""},
    {"name":"Seagate FireCuda 530 1TB M.2 NVMe","brand":"Seagate","category":"SSD-накопители","price":9490.0,"rating":4.8,"reviews_count":312,"url":""},
    {"name":"Silicon Power P34A80 1TB M.2 NVMe","brand":"Silicon Power","category":"SSD-накопители","price":3990.0,"rating":4.5,"reviews_count":198,"url":""},
    {"name":"ADATA XPG GAMMIX S70 Blade 2TB M.2 NVMe","brand":"ADATA","category":"SSD-накопители","price":12990.0,"rating":4.7,"reviews_count":156,"url":""},
    {"name":"Crucial BX500 480GB SATA","brand":"Crucial","category":"SSD-накопители","price":2490.0,"rating":4.4,"reviews_count":543,"url":""},
    {"name":"Samsung 990 Pro 2TB M.2 NVMe","brand":"Samsung","category":"SSD-накопители","price":16990.0,"rating":4.9,"reviews_count":234,"url":""},
    {"name":"Razer BlackShark V2 Pro черный","brand":"Razer","category":"Наушники","price":19990.0,"rating":4.7,"reviews_count":312,"url":""},
    {"name":"Marshall Major IV черный","brand":"Marshall","category":"Наушники","price":11990.0,"rating":4.6,"reviews_count":198,"url":""},
    {"name":"Philips SHP9500 серебристый","brand":"Philips","category":"Наушники","price":7990.0,"rating":4.7,"reviews_count":432,"url":""},
    {"name":"Logitech G Pro X 2 Lightspeed черный","brand":"Logitech","category":"Наушники","price":24990.0,"rating":4.8,"reviews_count":267,"url":""},
    {"name":"ASUS ROG Strix Go 2.4 черный","brand":"ASUS","category":"Наушники","price":14990.0,"rating":4.6,"reviews_count":145,"url":""},
]

stores = [("DNS", dns), ("Ситилинк", citilink), ("Regard", regard)]
base_time = datetime.utcnow() - timedelta(days=1)

with SessionLocal() as s:
    col = Collection(started_at=base_time, finished_at=base_time+timedelta(minutes=14), status="success", total_records=sum(len(p) for _,p in stores))
    s.add(col); s.commit(); col_id = col.id

for source_name, products in stores:
    noisy = [{**p, "price": round(p["price"]*random.uniform(0.97,1.03)/10)*10} for p in products]
    save_products(noisy, source_name, col_id)

print(f"Готово! Загружено {sum(len(p) for _,p in stores)} товаров из {len(stores)} магазинов.")
