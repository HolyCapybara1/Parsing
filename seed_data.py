import sys
import os
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.dirname(__file__))

from db.repository import init_db, save_products, SessionLocal
from db.models import Collection

init_db()

# ─── Товары DNS ───────────────────────────────────────────────────────────────

dns_products = [
    # Оперативная память
    {"name": "Оперативная память Kingston FURY Beast Black 16 ГБ DDR5 5200 МГц DIMM CL40 KF552C40BB-16", "brand": "Kingston", "category": "Оперативная память", "price": 4299.0, "rating": 4.8, "reviews_count": 312, "url": "https://www.dns-shop.ru/product/kingston-fury-beast-16gb-ddr5"},
    {"name": "Оперативная память Kingston FURY Beast Black 32 ГБ DDR5 5600 МГц DIMM CL36 KF556C36BBE-32", "brand": "Kingston", "category": "Оперативная память", "price": 8190.0, "rating": 4.9, "reviews_count": 178, "url": "https://www.dns-shop.ru/product/kingston-fury-beast-32gb-ddr5"},
    {"name": "Оперативная память Crucial 16 ГБ DDR4 3200 МГц DIMM CL22 CT16G4DFRA32A", "brand": "Crucial", "category": "Оперативная память", "price": 2890.0, "rating": 4.7, "reviews_count": 524, "url": "https://www.dns-shop.ru/product/crucial-16gb-ddr4-3200"},
    {"name": "Оперативная память Crucial 32 ГБ DDR4 3200 МГц DIMM CL22 CT32G4DFD832A", "brand": "Crucial", "category": "Оперативная память", "price": 5490.0, "rating": 4.6, "reviews_count": 209, "url": "https://www.dns-shop.ru/product/crucial-32gb-ddr4-3200"},
    {"name": "Оперативная память G.Skill Trident Z5 RGB 32 ГБ DDR5 6000 МГц DIMM CL30 F5-6000J3038F16GX2-TZ5RK", "brand": "G.Skill", "category": "Оперативная память", "price": 14990.0, "rating": 4.9, "reviews_count": 87, "url": "https://www.dns-shop.ru/product/gskill-trident-z5-rgb-32gb-ddr5"},
    {"name": "Оперативная память Samsung 8 ГБ DDR4 3200 МГц DIMM M378A1K43EB2-CWE", "brand": "Samsung", "category": "Оперативная память", "price": 1790.0, "rating": 4.5, "reviews_count": 431, "url": "https://www.dns-shop.ru/product/samsung-8gb-ddr4-3200"},
    {"name": "Оперативная память Corsair Vengeance LPX 16 ГБ DDR4 3600 МГц DIMM CL18 CMK16GX4M2D3600C18", "brand": "Corsair", "category": "Оперативная память", "price": 3490.0, "rating": 4.7, "reviews_count": 267, "url": "https://www.dns-shop.ru/product/corsair-vengeance-lpx-16gb-ddr4"},
    {"name": "Оперативная память ADATA XPG Lancer RGB 32 ГБ DDR5 6400 МГц DIMM AX5U6400C3216G-DCLARBK", "brand": "ADATA", "category": "Оперативная память", "price": 12490.0, "rating": 4.6, "reviews_count": 53, "url": "https://www.dns-shop.ru/product/adata-xpg-lancer-32gb-ddr5"},

    # Видеокарты
    {"name": "Видеокарта NVIDIA GeForce RTX 4060 8 ГБ ASUS DUAL-RTX4060-O8G", "brand": "ASUS", "category": "Видеокарты", "price": 32990.0, "rating": 4.7, "reviews_count": 198, "url": "https://www.dns-shop.ru/product/asus-dual-rtx4060-o8g"},
    {"name": "Видеокарта NVIDIA GeForce RTX 4070 12 ГБ MSI GAMING X SLIM GeForce RTX 4070 12G", "brand": "MSI", "category": "Видеокарты", "price": 54990.0, "rating": 4.8, "reviews_count": 143, "url": "https://www.dns-shop.ru/product/msi-rtx4070-gaming-x-slim"},
    {"name": "Видеокарта NVIDIA GeForce RTX 4080 SUPER 16 ГБ Gigabyte AORUS MASTER GV-N408SAORUS M-16GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 109990.0, "rating": 4.9, "reviews_count": 61, "url": "https://www.dns-shop.ru/product/gigabyte-rtx4080s-aorus-master"},
    {"name": "Видеокарта AMD Radeon RX 7600 8 ГБ Sapphire PULSE RX 7600 8G GDDR6", "brand": "Sapphire", "category": "Видеокарты", "price": 27490.0, "rating": 4.6, "reviews_count": 112, "url": "https://www.dns-shop.ru/product/sapphire-pulse-rx7600-8g"},
    {"name": "Видеокарта AMD Radeon RX 7700 XT 12 ГБ PowerColor Hellhound RX 7700 XT 12GB", "brand": "PowerColor", "category": "Видеокарты", "price": 38990.0, "rating": 4.5, "reviews_count": 76, "url": "https://www.dns-shop.ru/product/powercolor-hellhound-rx7700xt"},
    {"name": "Видеокарта NVIDIA GeForce RTX 4090 24 ГБ ASUS ROG STRIX LC GeForce RTX 4090 24GB", "brand": "ASUS", "category": "Видеокарты", "price": 219990.0, "rating": 4.9, "reviews_count": 34, "url": "https://www.dns-shop.ru/product/asus-rog-strix-lc-rtx4090"},
    {"name": "Видеокарта NVIDIA GeForce RTX 4060 Ti 16 ГБ Palit JetStream RTX 4060 Ti 16G", "brand": "Palit", "category": "Видеокарты", "price": 44990.0, "rating": 4.6, "reviews_count": 89, "url": "https://www.dns-shop.ru/product/palit-jetstream-rtx4060ti-16g"},

    # Смартфоны
    {"name": "Смартфон Apple iPhone 15 128 ГБ черный", "brand": "Apple", "category": "Смартфоны", "price": 79990.0, "rating": 4.8, "reviews_count": 1243, "url": "https://www.dns-shop.ru/product/apple-iphone-15-128gb-black"},
    {"name": "Смартфон Apple iPhone 15 Pro 256 ГБ титановый черный", "brand": "Apple", "category": "Смартфоны", "price": 119990.0, "rating": 4.9, "reviews_count": 876, "url": "https://www.dns-shop.ru/product/apple-iphone-15-pro-256gb"},
    {"name": "Смартфон Samsung Galaxy S24 256 ГБ черный фантом", "brand": "Samsung", "category": "Смартфоны", "price": 74990.0, "rating": 4.7, "reviews_count": 654, "url": "https://www.dns-shop.ru/product/samsung-galaxy-s24-256gb"},
    {"name": "Смартфон Samsung Galaxy A55 256 ГБ темно-синий", "brand": "Samsung", "category": "Смартфоны", "price": 34990.0, "rating": 4.5, "reviews_count": 432, "url": "https://www.dns-shop.ru/product/samsung-galaxy-a55-256gb"},
    {"name": "Смартфон Xiaomi 14 256 ГБ черный", "brand": "Xiaomi", "category": "Смартфоны", "price": 59990.0, "rating": 4.7, "reviews_count": 321, "url": "https://www.dns-shop.ru/product/xiaomi-14-256gb"},
    {"name": "Смартфон Xiaomi Redmi Note 13 Pro+ 256 ГБ полуночный черный", "brand": "Xiaomi", "category": "Смартфоны", "price": 29990.0, "rating": 4.6, "reviews_count": 567, "url": "https://www.dns-shop.ru/product/xiaomi-redmi-note-13-pro-plus"},
    {"name": "Смартфон realme 12 Pro+ 256 ГБ навигаторский синий", "brand": "realme", "category": "Смартфоны", "price": 32990.0, "rating": 4.4, "reviews_count": 198, "url": "https://www.dns-shop.ru/product/realme-12-pro-plus-256gb"},
    {"name": "Смартфон HONOR 200 Pro 512 ГБ черный", "brand": "HONOR", "category": "Смартфоны", "price": 49990.0, "rating": 4.6, "reviews_count": 145, "url": "https://www.dns-shop.ru/product/honor-200-pro-512gb"},
]

# ─── Товары Ситилинк ──────────────────────────────────────────────────────────

citilink_products = [
    # Оперативная память
    {"name": "Оперативная память Patriot Viper Steel 16 ГБ DDR4 3600 МГц DIMM CL17 PVS416G360C7", "brand": "Patriot", "category": "Оперативная память", "price": 3190.0, "rating": 4.6, "reviews_count": 189, "url": "https://www.citilink.ru/product/patriot-viper-steel-16gb-ddr4"},
    {"name": "Оперативная память Crucial Pro 32 ГБ DDR5 5600 МГц DIMM CL46 CP2K16G56C46U5", "brand": "Crucial", "category": "Оперативная память", "price": 8490.0, "rating": 4.7, "reviews_count": 92, "url": "https://www.citilink.ru/product/crucial-pro-32gb-ddr5"},
    {"name": "Оперативная память Kingston FURY Renegade 16 ГБ DDR4 3600 МГц DIMM CL16 KF436C16RB/16", "brand": "Kingston", "category": "Оперативная память", "price": 3890.0, "rating": 4.8, "reviews_count": 234, "url": "https://www.citilink.ru/product/kingston-fury-renegade-16gb-ddr4"},
    {"name": "Оперативная память Corsair Dominator Platinum RGB 64 ГБ DDR5 5600 МГц DIMM CL36 CMT64GX5M2B5600C36", "brand": "Corsair", "category": "Оперативная память", "price": 24990.0, "rating": 4.8, "reviews_count": 41, "url": "https://www.citilink.ru/product/corsair-dominator-platinum-64gb-ddr5"},
    {"name": "Оперативная память Team T-Force Vulcan Z 16 ГБ DDR4 3200 МГц DIMM CL16 TLZGD416G3200HC16F01", "brand": "Team", "category": "Оперативная память", "price": 2790.0, "rating": 4.4, "reviews_count": 156, "url": "https://www.citilink.ru/product/team-t-force-vulcan-z-16gb"},
    {"name": "Оперативная память Hynix 8 ГБ DDR4 3200 МГц DIMM HMAA1GU6CJR6N-XN", "brand": "Hynix", "category": "Оперативная память", "price": 1590.0, "rating": 4.3, "reviews_count": 378, "url": "https://www.citilink.ru/product/hynix-8gb-ddr4-3200"},
    {"name": "Оперативная память G.Skill Ripjaws V 32 ГБ DDR4 3600 МГц DIMM CL18 F4-3600C18D-32GVK", "brand": "G.Skill", "category": "Оперативная память", "price": 6290.0, "rating": 4.7, "reviews_count": 143, "url": "https://www.citilink.ru/product/gskill-ripjaws-v-32gb-ddr4"},

    # Видеокарты
    {"name": "Видеокарта NVIDIA GeForce RTX 4070 SUPER 12 ГБ Gigabyte GAMING OC GV-N407SGAMING OC-12GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 64990.0, "rating": 4.8, "reviews_count": 97, "url": "https://www.citilink.ru/product/gigabyte-rtx4070s-gaming-oc"},
    {"name": "Видеокарта AMD Radeon RX 7800 XT 16 ГБ MSI Gaming Radeon RX 7800 XT 16G", "brand": "MSI", "category": "Видеокарты", "price": 48990.0, "rating": 4.7, "reviews_count": 68, "url": "https://www.citilink.ru/product/msi-rx7800xt-gaming-16g"},
    {"name": "Видеокарта NVIDIA GeForce RTX 3060 12 ГБ ASUS Phoenix RTX 3060 V2 OC 12G", "brand": "ASUS", "category": "Видеокарты", "price": 24990.0, "rating": 4.5, "reviews_count": 287, "url": "https://www.citilink.ru/product/asus-phoenix-rtx3060-v2-oc-12g"},
    {"name": "Видеокарта AMD Radeon RX 6600 8 ГБ Sapphire PULSE RX 6600 8G GDDR6", "brand": "Sapphire", "category": "Видеокарты", "price": 18990.0, "rating": 4.4, "reviews_count": 201, "url": "https://www.citilink.ru/product/sapphire-pulse-rx6600-8g"},
    {"name": "Видеокарта NVIDIA GeForce RTX 4080 16 ГБ MSI SUPRIM X GeForce RTX 4080 16G", "brand": "MSI", "category": "Видеокарты", "price": 99990.0, "rating": 4.9, "reviews_count": 45, "url": "https://www.citilink.ru/product/msi-rtx4080-suprim-x-16g"},
    {"name": "Видеокарта NVIDIA GeForce RTX 4060 8 ГБ Gigabyte WINDFORCE OC GV-N4060WF2OC-8GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 31490.0, "rating": 4.6, "reviews_count": 134, "url": "https://www.citilink.ru/product/gigabyte-rtx4060-windforce-oc"},
    {"name": "Видеокарта AMD Radeon RX 7900 GRE 16 ГБ PowerColor Hellhound RX 7900 GRE 16G OC", "brand": "PowerColor", "category": "Видеокарты", "price": 59990.0, "rating": 4.7, "reviews_count": 52, "url": "https://www.citilink.ru/product/powercolor-hellhound-rx7900gre"},

    # Смартфоны
    {"name": "Смартфон Samsung Galaxy S24 Ultra 256 ГБ титановый серый", "brand": "Samsung", "category": "Смартфоны", "price": 124990.0, "rating": 4.9, "reviews_count": 543, "url": "https://www.citilink.ru/product/samsung-galaxy-s24-ultra-256gb"},
    {"name": "Смартфон Xiaomi 14 Ultra 512 ГБ белый", "brand": "Xiaomi", "category": "Смартфоны", "price": 99990.0, "rating": 4.8, "reviews_count": 176, "url": "https://www.citilink.ru/product/xiaomi-14-ultra-512gb"},
    {"name": "Смартфон Google Pixel 8 128 ГБ черный обсидиан", "brand": "Google", "category": "Смартфоны", "price": 64990.0, "rating": 4.7, "reviews_count": 234, "url": "https://www.citilink.ru/product/google-pixel-8-128gb"},
    {"name": "Смартфон OnePlus 12 256 ГБ черный силикон", "brand": "OnePlus", "category": "Смартфоны", "price": 69990.0, "rating": 4.6, "reviews_count": 98, "url": "https://www.citilink.ru/product/oneplus-12-256gb"},
    {"name": "Смартфон HONOR 90 256 ГБ полночный черный", "brand": "HONOR", "category": "Смартфоны", "price": 24990.0, "rating": 4.4, "reviews_count": 312, "url": "https://www.citilink.ru/product/honor-90-256gb"},
    {"name": "Смартфон Xiaomi Redmi 13C 256 ГБ полуночный черный", "brand": "Xiaomi", "category": "Смартфоны", "price": 13990.0, "rating": 4.2, "reviews_count": 621, "url": "https://www.citilink.ru/product/xiaomi-redmi-13c-256gb"},
    {"name": "Смартфон vivo V30 256 ГБ розовое золото", "brand": "vivo", "category": "Смартфоны", "price": 34990.0, "rating": 4.3, "reviews_count": 87, "url": "https://www.citilink.ru/product/vivo-v30-256gb"},
    {"name": "Смартфон OPPO Reno12 Pro 256 ГБ серый", "brand": "OPPO", "category": "Смартфоны", "price": 39990.0, "rating": 4.4, "reviews_count": 143, "url": "https://www.citilink.ru/product/oppo-reno12-pro-256gb"},
]

# ─── Товары Regard ────────────────────────────────────────────────────────────

regard_products = [
    # Оперативная память
    {"name": "Оперативная память Kingston FURY Beast RGB 16 ГБ DDR4 3200 МГц DIMM CL16 KF432C16BB1A/16", "brand": "Kingston", "category": "Оперативная память", "price": 3590.0, "rating": 4.7, "reviews_count": 267, "url": "https://www.regard.ru/product/kingston-fury-beast-rgb-16gb"},
    {"name": "Оперативная память Crucial 16 ГБ DDR5 4800 МГц DIMM CL40 CT16G48C40S5", "brand": "Crucial", "category": "Оперативная память", "price": 4990.0, "rating": 4.5, "reviews_count": 134, "url": "https://www.regard.ru/product/crucial-16gb-ddr5-4800"},
    {"name": "Оперативная память Corsair Vengeance RGB 32 ГБ DDR5 5600 МГц DIMM CL36 CMH32GX5M2B5600C36", "brand": "Corsair", "category": "Оперативная память", "price": 11990.0, "rating": 4.8, "reviews_count": 78, "url": "https://www.regard.ru/product/corsair-vengeance-rgb-32gb-ddr5"},
    {"name": "Оперативная память ADATA 8 ГБ DDR4 3200 МГц DIMM CL22 AD4U32008G22-SGN", "brand": "ADATA", "category": "Оперативная память", "price": 1490.0, "rating": 4.2, "reviews_count": 312, "url": "https://www.regard.ru/product/adata-8gb-ddr4-3200"},
    {"name": "Оперативная память Team T-Force Delta RGB 32 ГБ DDR4 3600 МГц DIMM CL18 TF3D432G3600HC18JDC01", "brand": "Team", "category": "Оперативная память", "price": 6990.0, "rating": 4.6, "reviews_count": 89, "url": "https://www.regard.ru/product/team-delta-rgb-32gb-ddr4"},
    {"name": "Оперативная память G.Skill Trident Z5 Neo 32 ГБ DDR5 6000 МГц DIMM CL30 F5-6000J3038F16GX2-TZ5NR", "brand": "G.Skill", "category": "Оперативная память", "price": 15490.0, "rating": 4.9, "reviews_count": 56, "url": "https://www.regard.ru/product/gskill-trident-z5-neo-32gb"},
    {"name": "Оперативная память Patriot Signature 8 ГБ DDR4 3200 МГц DIMM CL22 PSD48G320081", "brand": "Patriot", "category": "Оперативная память", "price": 1390.0, "rating": 4.3, "reviews_count": 445, "url": "https://www.regard.ru/product/patriot-signature-8gb-ddr4"},

    # Видеокарты
    {"name": "Видеокарта NVIDIA GeForce RTX 4070 Ti SUPER 16 ГБ ASUS ROG STRIX RTX 4070 Ti SUPER OC GAMING 16G", "brand": "ASUS", "category": "Видеокарты", "price": 89990.0, "rating": 4.9, "reviews_count": 38, "url": "https://www.regard.ru/product/asus-rog-strix-rtx4070tis-oc"},
    {"name": "Видеокарта AMD Radeon RX 7600 XT 16 ГБ Gigabyte Gaming OC RX 7600 XT GAMING OC-16GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 35990.0, "rating": 4.5, "reviews_count": 61, "url": "https://www.regard.ru/product/gigabyte-rx7600xt-gaming-oc-16g"},
    {"name": "Видеокарта NVIDIA GeForce RTX 3070 8 ГБ MSI Gaming X Trio GeForce RTX 3070 8G LHR", "brand": "MSI", "category": "Видеокарты", "price": 34990.0, "rating": 4.6, "reviews_count": 178, "url": "https://www.regard.ru/product/msi-rtx3070-gaming-x-trio-lhr"},
    {"name": "Видеокарта NVIDIA GeForce RTX 4060 8 ГБ Palit Dual RTX 4060 8G", "brand": "Palit", "category": "Видеокарты", "price": 30990.0, "rating": 4.5, "reviews_count": 112, "url": "https://www.regard.ru/product/palit-dual-rtx4060-8g"},
    {"name": "Видеокарта AMD Radeon RX 7900 XT 20 ГБ Sapphire NITRO+ RX 7900 XT Vapor-X 20GB", "brand": "Sapphire", "category": "Видеокарты", "price": 79990.0, "rating": 4.8, "reviews_count": 29, "url": "https://www.regard.ru/product/sapphire-nitro-rx7900xt-20g"},
    {"name": "Видеокарта NVIDIA GeForce RTX 4070 12 ГБ Gigabyte AERO OC GV-N4070AERO OC-12GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 53490.0, "rating": 4.7, "reviews_count": 84, "url": "https://www.regard.ru/product/gigabyte-rtx4070-aero-oc-12g"},
    {"name": "Видеокарта NVIDIA GeForce RTX 4090 24 ГБ MSI SUPRIM LIQUID X GeForce RTX 4090 24G", "brand": "MSI", "category": "Видеокарты", "price": 229990.0, "rating": 5.0, "reviews_count": 18, "url": "https://www.regard.ru/product/msi-rtx4090-suprim-liquid-x"},

    # Смартфоны
    {"name": "Смартфон Apple iPhone 15 Pro Max 256 ГБ натуральный титан", "brand": "Apple", "category": "Смартфоны", "price": 134990.0, "rating": 4.9, "reviews_count": 432, "url": "https://www.regard.ru/product/apple-iphone-15-pro-max-256gb"},
    {"name": "Смартфон Samsung Galaxy S24+ 256 ГБ мраморный серый", "brand": "Samsung", "category": "Смартфоны", "price": 94990.0, "rating": 4.8, "reviews_count": 287, "url": "https://www.regard.ru/product/samsung-galaxy-s24-plus-256gb"},
    {"name": "Смартфон Apple iPhone 14 128 ГБ полуночный", "brand": "Apple", "category": "Смартфоны", "price": 62990.0, "rating": 4.7, "reviews_count": 876, "url": "https://www.regard.ru/product/apple-iphone-14-128gb"},
    {"name": "Смартфон Xiaomi Poco X6 Pro 256 ГБ черный", "brand": "Xiaomi", "category": "Смартфоны", "price": 27990.0, "rating": 4.6, "reviews_count": 345, "url": "https://www.regard.ru/product/xiaomi-poco-x6-pro-256gb"},
    {"name": "Смартфон Samsung Galaxy A35 256 ГБ темно-синий", "brand": "Samsung", "category": "Смартфоны", "price": 28990.0, "rating": 4.4, "reviews_count": 213, "url": "https://www.regard.ru/product/samsung-galaxy-a35-256gb"},
    {"name": "Смартфон HONOR Magic6 Pro 512 ГБ черный", "brand": "HONOR", "category": "Смартфоны", "price": 79990.0, "rating": 4.7, "reviews_count": 94, "url": "https://www.regard.ru/product/honor-magic6-pro-512gb"},
    {"name": "Смартфон Xiaomi Redmi Note 13 128 ГБ полночный черный", "brand": "Xiaomi", "category": "Смартфоны", "price": 16990.0, "rating": 4.3, "reviews_count": 534, "url": "https://www.regard.ru/product/xiaomi-redmi-note-13-128gb"},
    {"name": "Смартфон realme GT 6 256 ГБ серебристый", "brand": "realme", "category": "Смартфоны", "price": 44990.0, "rating": 4.5, "reviews_count": 67, "url": "https://www.regard.ru/product/realme-gt6-256gb"},
]

# ─── Запись в БД ──────────────────────────────────────────────────────────────

stores = [
    ("DNS", dns_products),
    ("Ситилинк", citilink_products),
    ("Regard", regard_products),
]

base_time = datetime.utcnow() - timedelta(days=1)

with SessionLocal() as s:
    col = Collection(
        started_at=base_time,
        finished_at=base_time + timedelta(minutes=14),
        status="success",
        total_records=sum(len(p) for _, p in stores),
    )
    s.add(col)
    s.commit()
    col_id = col.id

for source_name, products in stores:
    # Добавляем небольшой шум к ценам чтобы данные выглядели живее
    noisy = []
    for p in products:
        item = dict(p)
        item["price"] = round(p["price"] * random.uniform(0.97, 1.03) / 10) * 10
        noisy.append(item)
    save_products(noisy, source_name, col_id)

total = sum(len(p) for _, p in stores)
print(f"Загружено {total} товаров из {len(stores)} магазинов.")
