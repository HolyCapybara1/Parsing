"""
Симулятор парсинга — выводит реалистичные сообщения в терминал
и сохраняет данные в базу данных.
"""

import sys
import os
import time
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.repository import init_db, save_products, SessionLocal
from db.models import Collection

# ─── Цвета для терминала ─────────────────────────────────────────────────────
GREEN  = '\033[92m'
YELLOW = '\033[93m'
CYAN   = '\033[96m'
GRAY   = '\033[90m'
RESET  = '\033[0m'
BOLD   = '\033[1m'

def log(msg, color=RESET):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{GRAY}{now}{RESET} {color}{msg}{RESET}')
    sys.stdout.flush()

def fake_delay(lo=0.3, hi=0.9):
    time.sleep(random.uniform(lo, hi))

# ─── Данные товаров ───────────────────────────────────────────────────────────

STORE_DATA = {
    "DNS": [
        {"name": "Kingston FURY Beast 16GB DDR5 5200MHz DIMM KF552C40BB-16", "brand": "Kingston", "category": "Оперативная память", "price": 4299.0, "rating": 4.8, "reviews_count": 312, "url": "https://www.dns-shop.ru/product/kingston-fury-beast-16gb-ddr5"},
        {"name": "Crucial 32GB DDR4 3200MHz DIMM CT32G4DFD832A", "brand": "Crucial", "category": "Оперативная память", "price": 5490.0, "rating": 4.6, "reviews_count": 209, "url": "https://www.dns-shop.ru/product/crucial-32gb-ddr4-3200"},
        {"name": "G.Skill Trident Z5 RGB 32GB DDR5 6000MHz F5-6000J3038F16GX2-TZ5RK", "brand": "G.Skill", "category": "Оперативная память", "price": 14990.0, "rating": 4.9, "reviews_count": 87, "url": "https://www.dns-shop.ru/product/gskill-trident-z5-rgb-32gb-ddr5"},
        {"name": "Samsung 8GB DDR4 3200MHz DIMM M378A1K43EB2-CWE", "brand": "Samsung", "category": "Оперативная память", "price": 1790.0, "rating": 4.5, "reviews_count": 431, "url": "https://www.dns-shop.ru/product/samsung-8gb-ddr4-3200"},
        {"name": "Corsair Vengeance LPX 16GB DDR4 3600MHz CMK16GX4M2D3600C18", "brand": "Corsair", "category": "Оперативная память", "price": 3490.0, "rating": 4.7, "reviews_count": 267, "url": "https://www.dns-shop.ru/product/corsair-vengeance-lpx-16gb-ddr4"},
        {"name": "ADATA XPG Lancer RGB 32GB DDR5 6400MHz AX5U6400C3216G-DCLARBK", "brand": "ADATA", "category": "Оперативная память", "price": 12490.0, "rating": 4.6, "reviews_count": 53, "url": "https://www.dns-shop.ru/product/adata-xpg-lancer-32gb-ddr5"},
        {"name": "ASUS DUAL RTX 4060 OC 8GB GDDR6 DUAL-RTX4060-O8G", "brand": "ASUS", "category": "Видеокарты", "price": 32990.0, "rating": 4.7, "reviews_count": 198, "url": "https://www.dns-shop.ru/product/asus-dual-rtx4060-o8g"},
        {"name": "MSI Gaming X Slim GeForce RTX 4070 12G", "brand": "MSI", "category": "Видеокарты", "price": 54990.0, "rating": 4.8, "reviews_count": 143, "url": "https://www.dns-shop.ru/product/msi-rtx4070-gaming-x-slim"},
        {"name": "Gigabyte AORUS Master RTX 4080 Super 16G GV-N408SAORUS M-16GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 109990.0, "rating": 4.9, "reviews_count": 61, "url": "https://www.dns-shop.ru/product/gigabyte-rtx4080s-aorus-master"},
        {"name": "Sapphire PULSE RX 7600 8G GDDR6", "brand": "Sapphire", "category": "Видеокарты", "price": 27490.0, "rating": 4.6, "reviews_count": 112, "url": "https://www.dns-shop.ru/product/sapphire-pulse-rx7600-8g"},
        {"name": "PowerColor Hellhound RX 7700 XT 12GB GDDR6", "brand": "PowerColor", "category": "Видеокарты", "price": 38990.0, "rating": 4.5, "reviews_count": 76, "url": "https://www.dns-shop.ru/product/powercolor-hellhound-rx7700xt"},
        {"name": "ASUS ROG STRIX LC GeForce RTX 4090 24GB OC", "brand": "ASUS", "category": "Видеокарты", "price": 219990.0, "rating": 4.9, "reviews_count": 34, "url": "https://www.dns-shop.ru/product/asus-rog-strix-lc-rtx4090"},
        {"name": "Palit JetStream RTX 4060 Ti 16G NE6406T019T1-1061J", "brand": "Palit", "category": "Видеокарты", "price": 44990.0, "rating": 4.6, "reviews_count": 89, "url": "https://www.dns-shop.ru/product/palit-jetstream-rtx4060ti-16g"},
        {"name": "Apple iPhone 15 128GB черный A3090", "brand": "Apple", "category": "Смартфоны", "price": 79990.0, "rating": 4.8, "reviews_count": 1243, "url": "https://www.dns-shop.ru/product/apple-iphone-15-128gb-black"},
        {"name": "Apple iPhone 15 Pro 256GB титановый черный", "brand": "Apple", "category": "Смартфоны", "price": 119990.0, "rating": 4.9, "reviews_count": 876, "url": "https://www.dns-shop.ru/product/apple-iphone-15-pro-256gb"},
        {"name": "Samsung Galaxy S24 256GB черный фантом SM-S921B", "brand": "Samsung", "category": "Смартфоны", "price": 74990.0, "rating": 4.7, "reviews_count": 654, "url": "https://www.dns-shop.ru/product/samsung-galaxy-s24-256gb"},
        {"name": "Samsung Galaxy A55 5G 256GB темно-синий SM-A556E", "brand": "Samsung", "category": "Смартфоны", "price": 34990.0, "rating": 4.5, "reviews_count": 432, "url": "https://www.dns-shop.ru/product/samsung-galaxy-a55-256gb"},
        {"name": "Xiaomi 14 256GB черный 23127PN0CC", "brand": "Xiaomi", "category": "Смартфоны", "price": 59990.0, "rating": 4.7, "reviews_count": 321, "url": "https://www.dns-shop.ru/product/xiaomi-14-256gb"},
        {"name": "Xiaomi Redmi Note 13 Pro+ 256GB полуночный черный", "brand": "Xiaomi", "category": "Смартфоны", "price": 29990.0, "rating": 4.6, "reviews_count": 567, "url": "https://www.dns-shop.ru/product/xiaomi-redmi-note-13-pro-plus"},
        {"name": "HONOR 200 Pro 512GB черный", "brand": "HONOR", "category": "Смартфоны", "price": 49990.0, "rating": 4.6, "reviews_count": 145, "url": "https://www.dns-shop.ru/product/honor-200-pro-512gb"},
        {"name": "Intel Core i9-14900K BOX BX8071514900K", "brand": "Intel", "category": "Процессоры", "price": 44990.0, "rating": 4.9, "reviews_count": 234, "url": "https://www.dns-shop.ru/product/intel-core-i9-14900k"},
        {"name": "AMD Ryzen 9 7950X BOX 100-100000514WOF", "brand": "AMD", "category": "Процессоры", "price": 52990.0, "rating": 4.9, "reviews_count": 187, "url": "https://www.dns-shop.ru/product/amd-ryzen-9-7950x"},
        {"name": "Intel Core i5-14600K BOX BX8071514600K", "brand": "Intel", "category": "Процессоры", "price": 22990.0, "rating": 4.7, "reviews_count": 412, "url": "https://www.dns-shop.ru/product/intel-core-i5-14600k"},
        {"name": "AMD Ryzen 5 7600X BOX 100-100000593WOF", "brand": "AMD", "category": "Процессоры", "price": 18490.0, "rating": 4.8, "reviews_count": 356, "url": "https://www.dns-shop.ru/product/amd-ryzen-5-7600x"},
        {"name": "Intel Core i7-14700KF BOX BX8071514700KF", "brand": "Intel", "category": "Процессоры", "price": 34990.0, "rating": 4.8, "reviews_count": 178, "url": "https://www.dns-shop.ru/product/intel-core-i7-14700kf"},
        {"name": "ASUS VivoBook 16 AMD Ryzen 5 7520U 16GB 512GB M1605YA-MB026", "brand": "ASUS", "category": "Ноутбуки", "price": 54990.0, "rating": 4.6, "reviews_count": 312, "url": "https://www.dns-shop.ru/product/asus-vivobook-16-m1605ya"},
        {"name": "Lenovo IdeaPad Slim 5 Intel Core i5-13420H 16GB 512GB 82XF004VRK", "brand": "Lenovo", "category": "Ноутбуки", "price": 64990.0, "rating": 4.7, "reviews_count": 198, "url": "https://www.dns-shop.ru/product/lenovo-ideapad-slim-5-82xf004vrk"},
        {"name": "Apple MacBook Air 13 M2 8GB 256GB серый космос MLXW3", "brand": "Apple", "category": "Ноутбуки", "price": 104990.0, "rating": 4.9, "reviews_count": 543, "url": "https://www.dns-shop.ru/product/apple-macbook-air-m2-mlxw3"},
        {"name": "HP Laptop 15s Intel Core i3-1215U 8GB 256GB 7X9X8EA", "brand": "HP", "category": "Ноутбуки", "price": 39990.0, "rating": 4.4, "reviews_count": 267, "url": "https://www.dns-shop.ru/product/hp-laptop-15s-7x9x8ea"},
        {"name": "MSI Thin GF63 12VE-1032RU Intel Core i5-12450H 8GB 512GB RTX 4050", "brand": "MSI", "category": "Ноутбуки", "price": 59990.0, "rating": 4.5, "reviews_count": 143, "url": "https://www.dns-shop.ru/product/msi-thin-gf63-12ve"},
        {"name": "Samsung 980 Pro 1TB M.2 NVMe MZ-V8P1T0BW", "brand": "Samsung", "category": "SSD-накопители", "price": 8490.0, "rating": 4.9, "reviews_count": 876, "url": "https://www.dns-shop.ru/product/samsung-980-pro-1tb"},
        {"name": "WD Black SN850X 2TB M.2 NVMe WDS200T2X0E", "brand": "WD", "category": "SSD-накопители", "price": 14990.0, "rating": 4.8, "reviews_count": 432, "url": "https://www.dns-shop.ru/product/wd-black-sn850x-2tb"},
        {"name": "Kingston NV2 500GB M.2 NVMe SNV2S/500G", "brand": "Kingston", "category": "SSD-накопители", "price": 2990.0, "rating": 4.5, "reviews_count": 654, "url": "https://www.dns-shop.ru/product/kingston-nv2-500gb"},
        {"name": "Crucial MX500 1TB SATA CT1000MX500SSD1", "brand": "Crucial", "category": "SSD-накопители", "price": 5990.0, "rating": 4.7, "reviews_count": 543, "url": "https://www.dns-shop.ru/product/crucial-mx500-1tb"},
        {"name": "Sony WH-1000XM5 черный WH1000XM5/B", "brand": "Sony", "category": "Наушники", "price": 29990.0, "rating": 4.9, "reviews_count": 876, "url": "https://www.dns-shop.ru/product/sony-wh-1000xm5-black"},
        {"name": "Apple AirPods Pro 2 MQD83CH/A", "brand": "Apple", "category": "Наушники", "price": 24990.0, "rating": 4.8, "reviews_count": 1243, "url": "https://www.dns-shop.ru/product/apple-airpods-pro-2"},
        {"name": "JBL Tune 770NC черный JBLT770NCBLK", "brand": "JBL", "category": "Наушники", "price": 8490.0, "rating": 4.6, "reviews_count": 432, "url": "https://www.dns-shop.ru/product/jbl-tune-770nc-black"},
        {"name": "Sennheiser HD 560S 508825", "brand": "Sennheiser", "category": "Наушники", "price": 12990.0, "rating": 4.7, "reviews_count": 234, "url": "https://www.dns-shop.ru/product/sennheiser-hd-560s"},
        {"name": "HyperX Cloud Alpha черный 4P5L1AA", "brand": "HyperX", "category": "Наушники", "price": 9990.0, "rating": 4.7, "reviews_count": 567, "url": "https://www.dns-shop.ru/product/hyperx-cloud-alpha-black"},
    ],

    "Ситилинк": [
        {"name": "Patriot Viper Steel 16GB DDR4 3600MHz PVS416G360C7", "brand": "Patriot", "category": "Оперативная память", "price": 3190.0, "rating": 4.6, "reviews_count": 189, "url": "https://www.citilink.ru/product/patriot-viper-steel-16gb-ddr4"},
        {"name": "Corsair Dominator Platinum RGB 64GB DDR5 5600MHz CMT64GX5M2B5600C36", "brand": "Corsair", "category": "Оперативная память", "price": 24990.0, "rating": 4.8, "reviews_count": 41, "url": "https://www.citilink.ru/product/corsair-dominator-platinum-64gb-ddr5"},
        {"name": "Kingston FURY Renegade 16GB DDR4 3600MHz KF436C16RB/16", "brand": "Kingston", "category": "Оперативная память", "price": 3890.0, "rating": 4.8, "reviews_count": 234, "url": "https://www.citilink.ru/product/kingston-fury-renegade-16gb-ddr4"},
        {"name": "G.Skill Ripjaws V 32GB DDR4 3600MHz F4-3600C18D-32GVK", "brand": "G.Skill", "category": "Оперативная память", "price": 6290.0, "rating": 4.7, "reviews_count": 143, "url": "https://www.citilink.ru/product/gskill-ripjaws-v-32gb-ddr4"},
        {"name": "Hynix 8GB DDR4 3200MHz HMAA1GU6CJR6N-XN", "brand": "Hynix", "category": "Оперативная память", "price": 1590.0, "rating": 4.3, "reviews_count": 378, "url": "https://www.citilink.ru/product/hynix-8gb-ddr4-3200"},
        {"name": "Gigabyte Gaming OC RTX 4070 Super 12G GV-N407SGAMING OC-12GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 64990.0, "rating": 4.8, "reviews_count": 97, "url": "https://www.citilink.ru/product/gigabyte-rtx4070s-gaming-oc"},
        {"name": "MSI Gaming Radeon RX 7800 XT 16G RX 7800 XT GAMING 16G", "brand": "MSI", "category": "Видеокарты", "price": 48990.0, "rating": 4.7, "reviews_count": 68, "url": "https://www.citilink.ru/product/msi-rx7800xt-gaming-16g"},
        {"name": "ASUS Phoenix RTX 3060 V2 OC 12G PH-RTX3060-12G-V2", "brand": "ASUS", "category": "Видеокарты", "price": 24990.0, "rating": 4.5, "reviews_count": 287, "url": "https://www.citilink.ru/product/asus-phoenix-rtx3060-v2-oc-12g"},
        {"name": "MSI SUPRIM X GeForce RTX 4080 16G RTX 4080 16G SUPRIM X", "brand": "MSI", "category": "Видеокарты", "price": 99990.0, "rating": 4.9, "reviews_count": 45, "url": "https://www.citilink.ru/product/msi-rtx4080-suprim-x-16g"},
        {"name": "PowerColor Hellhound RX 7900 GRE 16GB OC AXRX 7900GRE 16GBD6-3DHLL/OC", "brand": "PowerColor", "category": "Видеокарты", "price": 59990.0, "rating": 4.7, "reviews_count": 52, "url": "https://www.citilink.ru/product/powercolor-hellhound-rx7900gre"},
        {"name": "Samsung Galaxy S24 Ultra 256GB титановый серый SM-S928B", "brand": "Samsung", "category": "Смартфоны", "price": 124990.0, "rating": 4.9, "reviews_count": 543, "url": "https://www.citilink.ru/product/samsung-galaxy-s24-ultra-256gb"},
        {"name": "Xiaomi 14 Ultra 512GB белый 23127PN0CC", "brand": "Xiaomi", "category": "Смартфоны", "price": 99990.0, "rating": 4.8, "reviews_count": 176, "url": "https://www.citilink.ru/product/xiaomi-14-ultra-512gb"},
        {"name": "Google Pixel 8 128GB черный обсидиан GX7AS", "brand": "Google", "category": "Смартфоны", "price": 64990.0, "rating": 4.7, "reviews_count": 234, "url": "https://www.citilink.ru/product/google-pixel-8-128gb"},
        {"name": "HONOR 90 256GB полночный черный REA-NX9", "brand": "HONOR", "category": "Смартфоны", "price": 24990.0, "rating": 4.4, "reviews_count": 312, "url": "https://www.citilink.ru/product/honor-90-256gb"},
        {"name": "Xiaomi Redmi 13C 256GB полночный черный 23100RN82L", "brand": "Xiaomi", "category": "Смартфоны", "price": 13990.0, "rating": 4.2, "reviews_count": 621, "url": "https://www.citilink.ru/product/xiaomi-redmi-13c-256gb"},
        {"name": "AMD Ryzen 7 7700X BOX 100-100000591WOF", "brand": "AMD", "category": "Процессоры", "price": 28490.0, "rating": 4.8, "reviews_count": 298, "url": "https://www.citilink.ru/product/amd-ryzen-7-7700x"},
        {"name": "Intel Core i3-14100F BOX BX8071514100F", "brand": "Intel", "category": "Процессоры", "price": 8990.0, "rating": 4.6, "reviews_count": 534, "url": "https://www.citilink.ru/product/intel-core-i3-14100f"},
        {"name": "AMD Ryzen 5 5600X BOX 100-100000065BOX", "brand": "AMD", "category": "Процессоры", "price": 12490.0, "rating": 4.8, "reviews_count": 876, "url": "https://www.citilink.ru/product/amd-ryzen-5-5600x"},
        {"name": "Intel Core i9-13900KS BOX BX8071513900KS", "brand": "Intel", "category": "Процессоры", "price": 54990.0, "rating": 4.9, "reviews_count": 143, "url": "https://www.citilink.ru/product/intel-core-i9-13900ks"},
        {"name": "AMD Ryzen 9 5900X BOX 100-100000061WOF", "brand": "AMD", "category": "Процессоры", "price": 22990.0, "rating": 4.8, "reviews_count": 421, "url": "https://www.citilink.ru/product/amd-ryzen-9-5900x"},
        {"name": "Acer Aspire 5 A515-58M Intel Core i5-1335U 16GB 512GB NX.KQ8CD.002", "brand": "Acer", "category": "Ноутбуки", "price": 59990.0, "rating": 4.5, "reviews_count": 234, "url": "https://www.citilink.ru/product/acer-aspire-5-a515-58m"},
        {"name": "ASUS ROG Strix G15 Ryzen 7 6800H 16GB 512GB RTX 3060 G513RM-HN167", "brand": "ASUS", "category": "Ноутбуки", "price": 89990.0, "rating": 4.7, "reviews_count": 312, "url": "https://www.citilink.ru/product/asus-rog-strix-g15-g513rm"},
        {"name": "Lenovo Legion 5 Ryzen 5 7640H 16GB 512GB RTX 4060 82YK00BGRK", "brand": "Lenovo", "category": "Ноутбуки", "price": 84990.0, "rating": 4.8, "reviews_count": 198, "url": "https://www.citilink.ru/product/lenovo-legion-5-82yk00bgrk"},
        {"name": "Apple MacBook Pro 14 M3 8GB 512GB серый MR7J3", "brand": "Apple", "category": "Ноутбуки", "price": 164990.0, "rating": 4.9, "reviews_count": 432, "url": "https://www.citilink.ru/product/apple-macbook-pro-14-m3-mr7j3"},
        {"name": "Crucial P3 Plus 1TB M.2 NVMe CT1000P3PSSD8", "brand": "Crucial", "category": "SSD-накопители", "price": 4990.0, "rating": 4.6, "reviews_count": 432, "url": "https://www.citilink.ru/product/crucial-p3-plus-1tb"},
        {"name": "Samsung 870 EVO 1TB SATA MZ-77E1T0BW", "brand": "Samsung", "category": "SSD-накопители", "price": 7990.0, "rating": 4.8, "reviews_count": 765, "url": "https://www.citilink.ru/product/samsung-870-evo-1tb"},
        {"name": "Kingston A2000 500GB M.2 NVMe SA2000M8/500G", "brand": "Kingston", "category": "SSD-накопители", "price": 2490.0, "rating": 4.4, "reviews_count": 543, "url": "https://www.citilink.ru/product/kingston-a2000-500gb"},
        {"name": "WD Blue SN570 1TB M.2 NVMe WDS100T3B0C", "brand": "WD", "category": "SSD-накопители", "price": 5490.0, "rating": 4.7, "reviews_count": 387, "url": "https://www.citilink.ru/product/wd-blue-sn570-1tb"},
        {"name": "Bose QuietComfort 45 черный 866724-0100", "brand": "Bose", "category": "Наушники", "price": 27990.0, "rating": 4.8, "reviews_count": 654, "url": "https://www.citilink.ru/product/bose-quietcomfort-45-black"},
        {"name": "Samsung Galaxy Buds2 Pro черный SM-R510NZAACIS", "brand": "Samsung", "category": "Наушники", "price": 12990.0, "rating": 4.6, "reviews_count": 432, "url": "https://www.citilink.ru/product/samsung-galaxy-buds2-pro-black"},
        {"name": "Audio-Technica ATH-M50x черный", "brand": "Audio-Technica", "category": "Наушники", "price": 14990.0, "rating": 4.8, "reviews_count": 876, "url": "https://www.citilink.ru/product/audio-technica-ath-m50x"},
        {"name": "Jabra Evolve2 55 стерео UC 26599-989-999", "brand": "Jabra", "category": "Наушники", "price": 34990.0, "rating": 4.7, "reviews_count": 143, "url": "https://www.citilink.ru/product/jabra-evolve2-55-stereo"},
    ],

    "Regard": [
        {"name": "Kingston FURY Beast RGB 16GB DDR4 3200MHz KF432C16BB1A/16", "brand": "Kingston", "category": "Оперативная память", "price": 3590.0, "rating": 4.7, "reviews_count": 267, "url": "https://www.regard.ru/product/kingston-fury-beast-rgb-16gb"},
        {"name": "Corsair Vengeance RGB 32GB DDR5 5600MHz CMH32GX5M2B5600C36", "brand": "Corsair", "category": "Оперативная память", "price": 11990.0, "rating": 4.8, "reviews_count": 78, "url": "https://www.regard.ru/product/corsair-vengeance-rgb-32gb-ddr5"},
        {"name": "G.Skill Trident Z5 Neo 32GB DDR5 6000MHz F5-6000J3038F16GX2-TZ5NR", "brand": "G.Skill", "category": "Оперативная память", "price": 15490.0, "rating": 4.9, "reviews_count": 56, "url": "https://www.regard.ru/product/gskill-trident-z5-neo-32gb"},
        {"name": "ADATA 8GB DDR4 3200MHz AD4U32008G22-SGN", "brand": "ADATA", "category": "Оперативная память", "price": 1490.0, "rating": 4.2, "reviews_count": 312, "url": "https://www.regard.ru/product/adata-8gb-ddr4-3200"},
        {"name": "Patriot Signature 8GB DDR4 3200MHz PSD48G320081", "brand": "Patriot", "category": "Оперативная память", "price": 1390.0, "rating": 4.3, "reviews_count": 445, "url": "https://www.regard.ru/product/patriot-signature-8gb-ddr4"},
        {"name": "Team T-Force Delta RGB 32GB DDR4 3600MHz TF3D432G3600HC18JDC01", "brand": "Team", "category": "Оперативная память", "price": 6990.0, "rating": 4.6, "reviews_count": 89, "url": "https://www.regard.ru/product/team-delta-rgb-32gb-ddr4"},
        {"name": "ASUS ROG STRIX RTX 4070 Ti Super OC GAMING 16G ROG-STRIX-RTX4070TIS-O16G-GAMING", "brand": "ASUS", "category": "Видеокарты", "price": 89990.0, "rating": 4.9, "reviews_count": 38, "url": "https://www.regard.ru/product/asus-rog-strix-rtx4070tis-oc"},
        {"name": "Gigabyte Gaming OC RX 7600 XT 16G GV-R76XTGAMING OC-16GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 35990.0, "rating": 4.5, "reviews_count": 61, "url": "https://www.regard.ru/product/gigabyte-rx7600xt-gaming-oc-16g"},
        {"name": "Sapphire NITRO+ RX 7900 XT Vapor-X 20GB 11325-02-20G", "brand": "Sapphire", "category": "Видеокарты", "price": 79990.0, "rating": 4.8, "reviews_count": 29, "url": "https://www.regard.ru/product/sapphire-nitro-rx7900xt-20g"},
        {"name": "Palit Dual RTX 4060 8G NE6406001T02-1060D", "brand": "Palit", "category": "Видеокарты", "price": 30990.0, "rating": 4.5, "reviews_count": 112, "url": "https://www.regard.ru/product/palit-dual-rtx4060-8g"},
        {"name": "MSI SUPRIM LIQUID X GeForce RTX 4090 24G RTX 4090 24G SUPRIM LIQUID X", "brand": "MSI", "category": "Видеокарты", "price": 229990.0, "rating": 5.0, "reviews_count": 18, "url": "https://www.regard.ru/product/msi-rtx4090-suprim-liquid-x"},
        {"name": "Gigabyte AERO OC RTX 4070 12G GV-N4070AERO OC-12GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 53490.0, "rating": 4.7, "reviews_count": 84, "url": "https://www.regard.ru/product/gigabyte-rtx4070-aero-oc-12g"},
        {"name": "Apple iPhone 15 Pro Max 256GB натуральный титан MU793", "brand": "Apple", "category": "Смартфоны", "price": 134990.0, "rating": 4.9, "reviews_count": 432, "url": "https://www.regard.ru/product/apple-iphone-15-pro-max-256gb"},
        {"name": "Samsung Galaxy S24+ 256GB мраморный серый SM-S926B", "brand": "Samsung", "category": "Смартфоны", "price": 94990.0, "rating": 4.8, "reviews_count": 287, "url": "https://www.regard.ru/product/samsung-galaxy-s24-plus-256gb"},
        {"name": "Apple iPhone 14 128GB полуночный MPUD3", "brand": "Apple", "category": "Смартфоны", "price": 62990.0, "rating": 4.7, "reviews_count": 876, "url": "https://www.regard.ru/product/apple-iphone-14-128gb"},
        {"name": "Xiaomi POCO X6 Pro 256GB черный 23122PCD1G", "brand": "Xiaomi", "category": "Смартфоны", "price": 27990.0, "rating": 4.6, "reviews_count": 345, "url": "https://www.regard.ru/product/xiaomi-poco-x6-pro-256gb"},
        {"name": "HONOR Magic6 Pro 512GB черный MGD-AL80", "brand": "HONOR", "category": "Смартфоны", "price": 79990.0, "rating": 4.7, "reviews_count": 94, "url": "https://www.regard.ru/product/honor-magic6-pro-512gb"},
        {"name": "AMD Ryzen 9 7900X BOX 100-100000589WOF", "brand": "AMD", "category": "Процессоры", "price": 38990.0, "rating": 4.9, "reviews_count": 198, "url": "https://www.regard.ru/product/amd-ryzen-9-7900x"},
        {"name": "Intel Core i5-13600K BOX BX8071513600K", "brand": "Intel", "category": "Процессоры", "price": 19990.0, "rating": 4.8, "reviews_count": 345, "url": "https://www.regard.ru/product/intel-core-i5-13600k"},
        {"name": "AMD Ryzen 7 5800X3D BOX 100-100000651WOF", "brand": "AMD", "category": "Процессоры", "price": 24990.0, "rating": 5.0, "reviews_count": 543, "url": "https://www.regard.ru/product/amd-ryzen-7-5800x3d"},
        {"name": "Intel Core i3-13100 BOX BX8071513100", "brand": "Intel", "category": "Процессоры", "price": 7990.0, "rating": 4.5, "reviews_count": 267, "url": "https://www.regard.ru/product/intel-core-i3-13100"},
        {"name": "AMD Ryzen 5 7500F BOX 100-100001489BOX", "brand": "AMD", "category": "Процессоры", "price": 14990.0, "rating": 4.8, "reviews_count": 312, "url": "https://www.regard.ru/product/amd-ryzen-5-7500f"},
        {"name": "Huawei MateBook D15 Intel Core i5-1155G7 8GB 512GB BohrD-WFH9A", "brand": "Huawei", "category": "Ноутбуки", "price": 49990.0, "rating": 4.5, "reviews_count": 312, "url": "https://www.regard.ru/product/huawei-matebook-d15-bohrd-wfh9a"},
        {"name": "MSI Katana GF66 12UE-1032RU Intel Core i7-12650H 16GB 512GB RTX 3060", "brand": "MSI", "category": "Ноутбуки", "price": 79990.0, "rating": 4.6, "reviews_count": 178, "url": "https://www.regard.ru/product/msi-katana-gf66-12ue"},
        {"name": "Gigabyte AORUS 15 Ryzen 7 7745HX 16GB 1TB RTX 4060 9MF-E2KZ354SD", "brand": "Gigabyte", "category": "Ноутбуки", "price": 94990.0, "rating": 4.7, "reviews_count": 134, "url": "https://www.regard.ru/product/gigabyte-aorus-15-9mf"},
        {"name": "Acer Nitro 5 AN515-58 Ryzen 5 7535HS 16GB 512GB RTX 4050 NH.QM0CD.001", "brand": "Acer", "category": "Ноутбуки", "price": 74990.0, "rating": 4.6, "reviews_count": 234, "url": "https://www.regard.ru/product/acer-nitro-5-an515-58"},
        {"name": "Seagate FireCuda 530 1TB M.2 NVMe ZP1000GM3A013", "brand": "Seagate", "category": "SSD-накопители", "price": 9490.0, "rating": 4.8, "reviews_count": 312, "url": "https://www.regard.ru/product/seagate-firecuda-530-1tb"},
        {"name": "Silicon Power P34A80 1TB M.2 NVMe SP001TBP34A80M28", "brand": "Silicon Power", "category": "SSD-накопители", "price": 3990.0, "rating": 4.5, "reviews_count": 198, "url": "https://www.regard.ru/product/silicon-power-p34a80-1tb"},
        {"name": "ADATA XPG GAMMIX S70 Blade 2TB M.2 NVMe AGAMMIXS70B-2T-CS", "brand": "ADATA", "category": "SSD-накопители", "price": 12990.0, "rating": 4.7, "reviews_count": 156, "url": "https://www.regard.ru/product/adata-xpg-gammix-s70-blade-2tb"},
        {"name": "Crucial BX500 480GB SATA CT480BX500SSD1", "brand": "Crucial", "category": "SSD-накопители", "price": 2490.0, "rating": 4.4, "reviews_count": 543, "url": "https://www.regard.ru/product/crucial-bx500-480gb"},
        {"name": "Samsung 990 Pro 2TB M.2 NVMe MZ-V9P2T0BW", "brand": "Samsung", "category": "SSD-накопители", "price": 16990.0, "rating": 4.9, "reviews_count": 234, "url": "https://www.regard.ru/product/samsung-990-pro-2tb"},
        {"name": "Razer BlackShark V2 Pro черный RZ04-03220100-R3M1", "brand": "Razer", "category": "Наушники", "price": 19990.0, "rating": 4.7, "reviews_count": 312, "url": "https://www.regard.ru/product/razer-blackshark-v2-pro-black"},
        {"name": "Marshall Major IV черный 1005765", "brand": "Marshall", "category": "Наушники", "price": 11990.0, "rating": 4.6, "reviews_count": 198, "url": "https://www.regard.ru/product/marshall-major-iv-black"},
        {"name": "Philips SHP9500 серебристый SHP9500/00", "brand": "Philips", "category": "Наушники", "price": 7990.0, "rating": 4.7, "reviews_count": 432, "url": "https://www.regard.ru/product/philips-shp9500"},
        {"name": "Logitech G Pro X 2 Lightspeed черный 981-001263", "brand": "Logitech", "category": "Наушники", "price": 24990.0, "rating": 4.8, "reviews_count": 267, "url": "https://www.regard.ru/product/logitech-g-pro-x-2-lightspeed"},
        {"name": "ASUS ROG Strix Go 2.4 черный 90YH02G1-B3UA00", "brand": "ASUS", "category": "Наушники", "price": 14990.0, "rating": 4.6, "reviews_count": 145, "url": "https://www.regard.ru/product/asus-rog-strix-go-2-4"},
    ],
}

CATEGORIES = [
    "Оперативная память", "Видеокарты", "Смартфоны",
    "Процессоры", "Ноутбуки", "SSD-накопители", "Наушники",
]

STORE_URLS = {
    "DNS":      "https://www.dns-shop.ru",
    "Ситилинк": "https://www.citilink.ru",
    "Regard":   "https://www.regard.ru",
}

# ─── Основной цикл симуляции ─────────────────────────────────────────────────

def main():
    print()
    print(f'{BOLD}{"="*60}')
    print(f'  ЦенМонитор — Запуск сбора данных')
    print(f'{"="*60}{RESET}')
    print()

    init_db()
    log('База данных инициализирована', GREEN)
    fake_delay(0.2, 0.5)

    base_time = datetime.utcnow()
    with SessionLocal() as s:
        col = Collection(
            started_at=base_time,
            status='running'
        )
        s.add(col)
        s.commit()
        col_id = col.id

    log(f'Сеанс #{col_id} создан', CYAN)
    print()

    total_saved = 0
    stores_data = list(STORE_DATA.items())

    for source_name, all_products in stores_data:
        url = STORE_URLS[source_name]
        print(f'{BOLD}{CYAN}┌─ Магазин: {source_name} ({url}){RESET}')

        store_total = 0

        # Группируем товары по категориям
        by_cat = {}
        for p in all_products:
            by_cat.setdefault(p['category'], []).append(p)

        for category in CATEGORIES:
            products_in_cat = by_cat.get(category, [])
            if not products_in_cat:
                continue

            # Сколько страниц симулируем
            pages = random.randint(1, 3)

            for page in range(1, pages + 1):
                log(f'│  {source_name} [{category}]: страница {page} — загрузка...', GRAY)
                fake_delay(0.4, 1.1)

                # Товаров на этой странице
                per_page = len(products_in_cat) if page == 1 else random.randint(0, 4)
                log(f'│  {source_name} [{category}]: стр.{page} — найдено {per_page} карточек', YELLOW)
                fake_delay(0.2, 0.5)

                if per_page == 0 or page > 1:
                    log(f'│  {source_name} [{category}]: следующая страница отсутствует — стоп', GRAY)
                    break

            # Добавляем лёгкий шум к ценам
            noisy = []
            for p in products_in_cat:
                item = dict(p)
                item['price'] = round(p['price'] * random.uniform(0.97, 1.03) / 10) * 10
                noisy.append(item)

            save_products(noisy, source_name, col_id)
            store_total += len(noisy)
            total_saved += len(noisy)

            log(f'│  {source_name} [{category}]: сохранено {len(noisy)} товаров ✓', GREEN)
            fake_delay(0.1, 0.3)

        print(f'{CYAN}└─ {source_name}: итого {store_total} товаров{RESET}')
        print()
        fake_delay(0.3, 0.7)

    # Закрываем сеанс
    with SessionLocal() as s:
        col = s.get(Collection, col_id)
        col.finished_at = datetime.utcnow()
        col.status = 'success'
        col.total_records = total_saved
        s.commit()

    print(f'{BOLD}{GREEN}{"="*60}')
    print(f'  Парсинг завершён успешно!')
    print(f'  Сохранено товаров: {total_saved}')
    print(f'  Магазинов обработано: {len(stores_data)}')
    print(f'  Категорий: {len(CATEGORIES)}')
    print(f'{"="*60}{RESET}')
    print()
    print(f'Запустите дашборд: {CYAN}streamlit run dashboard/Главная.py{RESET}')
    print()


if __name__ == '__main__':
    main()
