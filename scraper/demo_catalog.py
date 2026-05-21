"""
Демо-каталог товаров для всех 7 категорий × 3 магазина.
Используется runner.py когда реальный парсинг недоступен.
Цены для каждой даты вычисляются детерминировано (random walk с seed от имени товара),
поэтому одна и та же дата всегда даёт одинаковые цены.
"""

PRODUCTS: dict[str, list[dict]] = {

    # ─── DNS ─────────────────────────────────────────────────────────────────

    "DNS": [
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

        # Процессоры
        {"name": "Процессор Intel Core i5-14600K, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 22990.0, "rating": 4.8, "reviews_count": 423, "url": "https://www.dns-shop.ru/product/intel-core-i5-14600k"},
        {"name": "Процессор Intel Core i7-14700K, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 34990.0, "rating": 4.9, "reviews_count": 287, "url": "https://www.dns-shop.ru/product/intel-core-i7-14700k"},
        {"name": "Процессор Intel Core i9-14900K, LGA1700, BOX", "brand": "Intel", "category": "Процессоры", "price": 54990.0, "rating": 4.9, "reviews_count": 134, "url": "https://www.dns-shop.ru/product/intel-core-i9-14900k"},
        {"name": "Процессор AMD Ryzen 5 7600X, AM5, OEM", "brand": "AMD", "category": "Процессоры", "price": 18990.0, "rating": 4.7, "reviews_count": 356, "url": "https://www.dns-shop.ru/product/amd-ryzen-5-7600x"},
        {"name": "Процессор AMD Ryzen 7 7700X, AM5, OEM", "brand": "AMD", "category": "Процессоры", "price": 27490.0, "rating": 4.8, "reviews_count": 219, "url": "https://www.dns-shop.ru/product/amd-ryzen-7-7700x"},
        {"name": "Процессор AMD Ryzen 9 7950X, AM5, OEM", "brand": "AMD", "category": "Процессоры", "price": 49990.0, "rating": 4.9, "reviews_count": 98, "url": "https://www.dns-shop.ru/product/amd-ryzen-9-7950x"},
        {"name": "Процессор Intel Core i3-14100, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 9490.0, "rating": 4.6, "reviews_count": 541, "url": "https://www.dns-shop.ru/product/intel-core-i3-14100"},
        {"name": "Процессор AMD Ryzen 5 5600, AM4, OEM", "brand": "AMD", "category": "Процессоры", "price": 8990.0, "rating": 4.7, "reviews_count": 678, "url": "https://www.dns-shop.ru/product/amd-ryzen-5-5600"},

        # Ноутбуки
        {"name": "Ноутбук ASUS ROG Strix G16 G614JVR-N3116 16\" Intel Core i7-14650HX/16GB/512GB SSD/RTX 4060 8GB", "brand": "ASUS", "category": "Ноутбуки", "price": 109990.0, "rating": 4.7, "reviews_count": 87, "url": "https://www.dns-shop.ru/product/asus-rog-strix-g16-g614jvr"},
        {"name": "Ноутбук Lenovo IdeaPad Slim 5 16IAH8 16\" Intel Core i5-12450H/16GB/512GB SSD", "brand": "Lenovo", "category": "Ноутбуки", "price": 54990.0, "rating": 4.5, "reviews_count": 234, "url": "https://www.dns-shop.ru/product/lenovo-ideapad-slim-5-16iah8"},
        {"name": "Ноутбук MSI Thin 15 B12UC-1218RU 15.6\" Intel Core i5-1235U/8GB/512GB SSD/RTX 3050 4GB", "brand": "MSI", "category": "Ноутбуки", "price": 62990.0, "rating": 4.6, "reviews_count": 167, "url": "https://www.dns-shop.ru/product/msi-thin-15-b12uc"},
        {"name": "Ноутбук HP Victus 16-r0036ci 16\" Intel Core i7-13700H/16GB/512GB SSD/RTX 4060 8GB", "brand": "HP", "category": "Ноутбуки", "price": 99990.0, "rating": 4.6, "reviews_count": 143, "url": "https://www.dns-shop.ru/product/hp-victus-16-r0036ci"},
        {"name": "Ноутбук Acer Nitro 5 AN515-58-51SE 15.6\" Intel Core i5-12500H/16GB/512GB SSD/RTX 4060 8GB", "brand": "Acer", "category": "Ноутбуки", "price": 84990.0, "rating": 4.5, "reviews_count": 198, "url": "https://www.dns-shop.ru/product/acer-nitro-5-an515-58"},
        {"name": "Ноутбук Apple MacBook Air 13\" M2 8GB/256GB SSD Space Gray", "brand": "Apple", "category": "Ноутбуки", "price": 99990.0, "rating": 4.9, "reviews_count": 543, "url": "https://www.dns-shop.ru/product/apple-macbook-air-13-m2"},
        {"name": "Ноутбук Lenovo ThinkPad E14 Gen 5 14\" AMD Ryzen 5 7530U/16GB/512GB SSD", "brand": "Lenovo", "category": "Ноутбуки", "price": 69990.0, "rating": 4.7, "reviews_count": 112, "url": "https://www.dns-shop.ru/product/lenovo-thinkpad-e14-gen5"},
        {"name": "Ноутбук ASUS VivoBook 15 X1504ZA 15.6\" Intel Core i3-1215U/8GB/256GB SSD", "brand": "ASUS", "category": "Ноутбуки", "price": 34990.0, "rating": 4.4, "reviews_count": 321, "url": "https://www.dns-shop.ru/product/asus-vivobook-15-x1504za"},

        # SSD-накопители
        {"name": "SSD Samsung 970 EVO Plus 1 ТБ M.2 2280 MZ-V7S1T0BW", "brand": "Samsung", "category": "SSD-накопители", "price": 7990.0, "rating": 4.9, "reviews_count": 1243, "url": "https://www.dns-shop.ru/product/samsung-970-evo-plus-1tb"},
        {"name": "SSD WD Black SN850X 1 ТБ M.2 2280 WDS100T2X0E", "brand": "WD", "category": "SSD-накопители", "price": 8490.0, "rating": 4.8, "reviews_count": 567, "url": "https://www.dns-shop.ru/product/wd-black-sn850x-1tb"},
        {"name": "SSD Crucial P5 Plus 1 ТБ M.2 2280 CT1000P5PSSD8", "brand": "Crucial", "category": "SSD-накопители", "price": 6490.0, "rating": 4.7, "reviews_count": 432, "url": "https://www.dns-shop.ru/product/crucial-p5-plus-1tb"},
        {"name": "SSD Kingston NV2 1 ТБ M.2 2280 SNV2S/1000G", "brand": "Kingston", "category": "SSD-накопители", "price": 4990.0, "rating": 4.6, "reviews_count": 876, "url": "https://www.dns-shop.ru/product/kingston-nv2-1tb"},
        {"name": "SSD Samsung 870 EVO 500 ГБ SATA III 2.5\" MZ-77E500BW", "brand": "Samsung", "category": "SSD-накопители", "price": 4490.0, "rating": 4.8, "reviews_count": 1567, "url": "https://www.dns-shop.ru/product/samsung-870-evo-500gb"},
        {"name": "SSD Seagate Barracuda 510 1 ТБ M.2 2280 ZP1000CM3A001", "brand": "Seagate", "category": "SSD-накопители", "price": 5990.0, "rating": 4.5, "reviews_count": 234, "url": "https://www.dns-shop.ru/product/seagate-barracuda-510-1tb"},
        {"name": "SSD ADATA Legend 960 Max 2 ТБ M.2 2280 ALEG-960M-2TCS", "brand": "ADATA", "category": "SSD-накопители", "price": 12990.0, "rating": 4.7, "reviews_count": 178, "url": "https://www.dns-shop.ru/product/adata-legend-960-max-2tb"},
        {"name": "SSD Patriot P300 256 ГБ M.2 2280 P300P256GM28", "brand": "Patriot", "category": "SSD-накопители", "price": 1990.0, "rating": 4.3, "reviews_count": 654, "url": "https://www.dns-shop.ru/product/patriot-p300-256gb"},

        # Наушники
        {"name": "Наушники Sony WH-1000XM5, накладные, активное шумоподавление, черные", "brand": "Sony", "category": "Наушники", "price": 29990.0, "rating": 4.9, "reviews_count": 876, "url": "https://www.dns-shop.ru/product/sony-wh-1000xm5-black"},
        {"name": "Наушники Apple AirPods Pro (2-е поколение) MQD83LL/A", "brand": "Apple", "category": "Наушники", "price": 24990.0, "rating": 4.8, "reviews_count": 1243, "url": "https://www.dns-shop.ru/product/apple-airpods-pro-2"},
        {"name": "Наушники JBL Live 660NC, накладные, активное шумоподавление, черные", "brand": "JBL", "category": "Наушники", "price": 9990.0, "rating": 4.6, "reviews_count": 432, "url": "https://www.dns-shop.ru/product/jbl-live-660nc-black"},
        {"name": "Наушники Sennheiser Momentum 4 Wireless, накладные, черные", "brand": "Sennheiser", "category": "Наушники", "price": 34990.0, "rating": 4.8, "reviews_count": 234, "url": "https://www.dns-shop.ru/product/sennheiser-momentum-4-wireless"},
        {"name": "Наушники Xiaomi Redmi Buds 5 Pro, вставные, TWS, активное шумоподавление", "brand": "Xiaomi", "category": "Наушники", "price": 4990.0, "rating": 4.5, "reviews_count": 567, "url": "https://www.dns-shop.ru/product/xiaomi-redmi-buds-5-pro"},
        {"name": "Наушники Samsung Galaxy Buds2 Pro SM-R510NZAACIS, вставные, TWS, фиолетовые", "brand": "Samsung", "category": "Наушники", "price": 12990.0, "rating": 4.6, "reviews_count": 345, "url": "https://www.dns-shop.ru/product/samsung-galaxy-buds2-pro"},
        {"name": "Наушники Marshall Major IV, накладные, черные", "brand": "Marshall", "category": "Наушники", "price": 11990.0, "rating": 4.7, "reviews_count": 198, "url": "https://www.dns-shop.ru/product/marshall-major-iv-black"},
        {"name": "Наушники Jabra Evolve2 55, накладные, активное шумоподавление, черные", "brand": "Jabra", "category": "Наушники", "price": 19990.0, "rating": 4.7, "reviews_count": 87, "url": "https://www.dns-shop.ru/product/jabra-evolve2-55-black"},
    ],

    # ─── Ситилинк ────────────────────────────────────────────────────────────

    "Ситилинк": [
        # Оперативная память
        {"name": "Оперативная память Patriot Viper Steel 16 ГБ DDR4 3600 МГц DIMM CL17 PVS416G360C7", "brand": "Patriot", "category": "Оперативная память", "price": 3190.0, "rating": 4.6, "reviews_count": 189, "url": "https://www.citilink.ru/product/patriot-viper-steel-16gb-ddr4"},
        {"name": "Оперативная память Crucial Pro 32 ГБ DDR5 5600 МГц DIMM CL46 CP2K16G56C46U5", "brand": "Crucial", "category": "Оперативная память", "price": 8490.0, "rating": 4.7, "reviews_count": 92, "url": "https://www.citilink.ru/product/crucial-pro-32gb-ddr5"},
        {"name": "Оперативная память Kingston FURY Renegade 16 ГБ DDR4 3600 МГц DIMM CL16 KF436C16RB/16", "brand": "Kingston", "category": "Оперативная память", "price": 3890.0, "rating": 4.8, "reviews_count": 234, "url": "https://www.citilink.ru/product/kingston-fury-renegade-16gb-ddr4"},
        {"name": "Оперативная память Corsair Dominator Platinum RGB 64 ГБ DDR5 5600 МГц DIMM CMT64GX5M2B5600C36", "brand": "Corsair", "category": "Оперативная память", "price": 24990.0, "rating": 4.8, "reviews_count": 41, "url": "https://www.citilink.ru/product/corsair-dominator-platinum-64gb-ddr5"},
        {"name": "Оперативная память Team T-Force Vulcan Z 16 ГБ DDR4 3200 МГц DIMM CL16", "brand": "Team", "category": "Оперативная память", "price": 2790.0, "rating": 4.4, "reviews_count": 156, "url": "https://www.citilink.ru/product/team-t-force-vulcan-z-16gb"},
        {"name": "Оперативная память Hynix 8 ГБ DDR4 3200 МГц DIMM HMAA1GU6CJR6N-XN", "brand": "Hynix", "category": "Оперативная память", "price": 1590.0, "rating": 4.3, "reviews_count": 378, "url": "https://www.citilink.ru/product/hynix-8gb-ddr4-3200"},
        {"name": "Оперативная память G.Skill Ripjaws V 32 ГБ DDR4 3600 МГц DIMM CL18 F4-3600C18D-32GVK", "brand": "G.Skill", "category": "Оперативная память", "price": 6290.0, "rating": 4.7, "reviews_count": 143, "url": "https://www.citilink.ru/product/gskill-ripjaws-v-32gb-ddr4"},
        {"name": "Оперативная память ADATA XPG Spectrix D50 16 ГБ DDR4 3600 МГц DIMM CL18 AX4U360016G18I-ST50", "brand": "ADATA", "category": "Оперативная память", "price": 3590.0, "rating": 4.5, "reviews_count": 167, "url": "https://www.citilink.ru/product/adata-xpg-spectrix-d50-16gb"},

        # Видеокарты
        {"name": "Видеокарта NVIDIA GeForce RTX 4070 SUPER 12 ГБ Gigabyte GAMING OC GV-N407SGAMING OC-12GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 64990.0, "rating": 4.8, "reviews_count": 97, "url": "https://www.citilink.ru/product/gigabyte-rtx4070s-gaming-oc"},
        {"name": "Видеокарта AMD Radeon RX 7800 XT 16 ГБ MSI Gaming Radeon RX 7800 XT 16G", "brand": "MSI", "category": "Видеокарты", "price": 48990.0, "rating": 4.7, "reviews_count": 68, "url": "https://www.citilink.ru/product/msi-rx7800xt-gaming-16g"},
        {"name": "Видеокарта NVIDIA GeForce RTX 3060 12 ГБ ASUS Phoenix RTX 3060 V2 OC 12G", "brand": "ASUS", "category": "Видеокарты", "price": 24990.0, "rating": 4.5, "reviews_count": 287, "url": "https://www.citilink.ru/product/asus-phoenix-rtx3060-v2-oc-12g"},
        {"name": "Видеокарта AMD Radeon RX 6600 8 ГБ Sapphire PULSE RX 6600 8G GDDR6", "brand": "Sapphire", "category": "Видеокарты", "price": 18990.0, "rating": 4.4, "reviews_count": 201, "url": "https://www.citilink.ru/product/sapphire-pulse-rx6600-8g"},
        {"name": "Видеокарта NVIDIA GeForce RTX 4080 16 ГБ MSI SUPRIM X GeForce RTX 4080 16G", "brand": "MSI", "category": "Видеокарты", "price": 99990.0, "rating": 4.9, "reviews_count": 45, "url": "https://www.citilink.ru/product/msi-rtx4080-suprim-x-16g"},
        {"name": "Видеокарта NVIDIA GeForce RTX 4060 8 ГБ Gigabyte WINDFORCE OC GV-N4060WF2OC-8GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 31490.0, "rating": 4.6, "reviews_count": 134, "url": "https://www.citilink.ru/product/gigabyte-rtx4060-windforce-oc"},
        {"name": "Видеокарта AMD Radeon RX 7900 GRE 16 ГБ PowerColor Hellhound RX 7900 GRE 16G OC", "brand": "PowerColor", "category": "Видеокарты", "price": 59990.0, "rating": 4.7, "reviews_count": 52, "url": "https://www.citilink.ru/product/powercolor-hellhound-rx7900gre"},
        {"name": "Видеокарта NVIDIA GeForce RTX 4070 Ti 12 ГБ ASUS TUF Gaming RTX 4070 Ti OC 12GB", "brand": "ASUS", "category": "Видеокарты", "price": 79990.0, "rating": 4.8, "reviews_count": 73, "url": "https://www.citilink.ru/product/asus-tuf-rtx4070ti-oc"},

        # Смартфоны
        {"name": "Смартфон Samsung Galaxy S24 Ultra 256 ГБ титановый серый", "brand": "Samsung", "category": "Смартфоны", "price": 124990.0, "rating": 4.9, "reviews_count": 543, "url": "https://www.citilink.ru/product/samsung-galaxy-s24-ultra-256gb"},
        {"name": "Смартфон Xiaomi 14 Ultra 512 ГБ белый", "brand": "Xiaomi", "category": "Смартфоны", "price": 99990.0, "rating": 4.8, "reviews_count": 176, "url": "https://www.citilink.ru/product/xiaomi-14-ultra-512gb"},
        {"name": "Смартфон Google Pixel 8 128 ГБ черный обсидиан", "brand": "Google", "category": "Смартфоны", "price": 64990.0, "rating": 4.7, "reviews_count": 234, "url": "https://www.citilink.ru/product/google-pixel-8-128gb"},
        {"name": "Смартфон OnePlus 12 256 ГБ черный силикон", "brand": "OnePlus", "category": "Смартфоны", "price": 69990.0, "rating": 4.6, "reviews_count": 98, "url": "https://www.citilink.ru/product/oneplus-12-256gb"},
        {"name": "Смартфон HONOR 90 256 ГБ полночный черный", "brand": "HONOR", "category": "Смартфоны", "price": 24990.0, "rating": 4.4, "reviews_count": 312, "url": "https://www.citilink.ru/product/honor-90-256gb"},
        {"name": "Смартфон Xiaomi Redmi 13C 256 ГБ полуночный черный", "brand": "Xiaomi", "category": "Смартфоны", "price": 13990.0, "rating": 4.2, "reviews_count": 621, "url": "https://www.citilink.ru/product/xiaomi-redmi-13c-256gb"},
        {"name": "Смартфон vivo V30 256 ГБ розовое золото", "brand": "vivo", "category": "Смартфоны", "price": 34990.0, "rating": 4.3, "reviews_count": 87, "url": "https://www.citilink.ru/product/vivo-v30-256gb"},
        {"name": "Смартфон OPPO Reno12 Pro 256 ГБ серый", "brand": "OPPO", "category": "Смартфоны", "price": 39990.0, "rating": 4.4, "reviews_count": 143, "url": "https://www.citilink.ru/product/oppo-reno12-pro-256gb"},

        # Процессоры
        {"name": "Процессор Intel Core i5-13600K, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 19990.0, "rating": 4.7, "reviews_count": 512, "url": "https://www.citilink.ru/product/intel-core-i5-13600k"},
        {"name": "Процессор Intel Core i7-13700KF, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 31490.0, "rating": 4.8, "reviews_count": 312, "url": "https://www.citilink.ru/product/intel-core-i7-13700kf"},
        {"name": "Процессор AMD Ryzen 5 7600, AM5, OEM", "brand": "AMD", "category": "Процессоры", "price": 16990.0, "rating": 4.7, "reviews_count": 423, "url": "https://www.citilink.ru/product/amd-ryzen-5-7600"},
        {"name": "Процессор AMD Ryzen 7 7800X3D, AM5, OEM", "brand": "AMD", "category": "Процессоры", "price": 32990.0, "rating": 4.9, "reviews_count": 267, "url": "https://www.citilink.ru/product/amd-ryzen-7-7800x3d"},
        {"name": "Процессор AMD Ryzen 9 7900X, AM5, OEM", "brand": "AMD", "category": "Процессоры", "price": 39990.0, "rating": 4.8, "reviews_count": 134, "url": "https://www.citilink.ru/product/amd-ryzen-9-7900x"},
        {"name": "Процессор Intel Core i9-13900KS, LGA1700, BOX", "brand": "Intel", "category": "Процессоры", "price": 69990.0, "rating": 4.9, "reviews_count": 67, "url": "https://www.citilink.ru/product/intel-core-i9-13900ks"},
        {"name": "Процессор Intel Core i3-13100F, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 7990.0, "rating": 4.5, "reviews_count": 678, "url": "https://www.citilink.ru/product/intel-core-i3-13100f"},
        {"name": "Процессор AMD Ryzen 5 5500, AM4, OEM", "brand": "AMD", "category": "Процессоры", "price": 6990.0, "rating": 4.6, "reviews_count": 534, "url": "https://www.citilink.ru/product/amd-ryzen-5-5500"},

        # Ноутбуки
        {"name": "Ноутбук ASUS TUF Gaming F15 FX507ZU4-LP049 15.6\" Intel Core i7-12700H/16GB/512GB SSD/RTX 4050", "brand": "ASUS", "category": "Ноутбуки", "price": 89990.0, "rating": 4.7, "reviews_count": 134, "url": "https://www.citilink.ru/product/asus-tuf-f15-fx507zu4"},
        {"name": "Ноутбук Lenovo Legion 5 Pro 16ARH7H 16\" AMD Ryzen 7 6800H/16GB/512GB SSD/RTX 3070 Ti", "brand": "Lenovo", "category": "Ноутбуки", "price": 119990.0, "rating": 4.8, "reviews_count": 98, "url": "https://www.citilink.ru/product/lenovo-legion-5-pro-16arh7h"},
        {"name": "Ноутбук HP 15s-eq3022ur 15.6\" AMD Ryzen 5 5500U/8GB/256GB SSD", "brand": "HP", "category": "Ноутбуки", "price": 39990.0, "rating": 4.3, "reviews_count": 345, "url": "https://www.citilink.ru/product/hp-15s-eq3022ur"},
        {"name": "Ноутбук Acer Aspire 5 A515-58M 15.6\" Intel Core i5-1335U/16GB/512GB SSD", "brand": "Acer", "category": "Ноутбуки", "price": 54990.0, "rating": 4.4, "reviews_count": 267, "url": "https://www.citilink.ru/product/acer-aspire-5-a515-58m"},
        {"name": "Ноутбук MSI Raider GE68HX 13VG 16\" Intel Core i9-13980HX/32GB/1TB SSD/RTX 4070 8GB", "brand": "MSI", "category": "Ноутбуки", "price": 199990.0, "rating": 4.8, "reviews_count": 43, "url": "https://www.citilink.ru/product/msi-raider-ge68hx-13vg"},
        {"name": "Ноутбук Realme Book Prime 15.6\" Intel Core i5-11320H/16GB/512GB SSD", "brand": "Realme", "category": "Ноутбуки", "price": 49990.0, "rating": 4.2, "reviews_count": 178, "url": "https://www.citilink.ru/product/realme-book-prime"},
        {"name": "Ноутбук Honor MagicBook 16 Pro HYM-W56 16\" AMD Ryzen 7 5800H/16GB/512GB SSD/RTX 3050", "brand": "Honor", "category": "Ноутбуки", "price": 64990.0, "rating": 4.6, "reviews_count": 156, "url": "https://www.citilink.ru/product/honor-magicbook-16-pro"},
        {"name": "Ноутбук Infinix InBook Y2 Plus 15.6\" Intel Core i5-1155G7/8GB/512GB SSD", "brand": "Infinix", "category": "Ноутбуки", "price": 34990.0, "rating": 4.1, "reviews_count": 212, "url": "https://www.citilink.ru/product/infinix-inbook-y2-plus"},

        # SSD-накопители
        {"name": "SSD Samsung 980 Pro 1 ТБ M.2 2280 MZ-V8P1T0BW", "brand": "Samsung", "category": "SSD-накопители", "price": 8990.0, "rating": 4.9, "reviews_count": 876, "url": "https://www.citilink.ru/product/samsung-980-pro-1tb"},
        {"name": "SSD Crucial MX500 1 ТБ SATA III 2.5\" CT1000MX500SSD1", "brand": "Crucial", "category": "SSD-накопители", "price": 5990.0, "rating": 4.8, "reviews_count": 1123, "url": "https://www.citilink.ru/product/crucial-mx500-1tb"},
        {"name": "SSD WD Blue SN570 1 ТБ M.2 2280 WDS100T3B0C", "brand": "WD", "category": "SSD-накопители", "price": 5490.0, "rating": 4.7, "reviews_count": 654, "url": "https://www.citilink.ru/product/wd-blue-sn570-1tb"},
        {"name": "SSD Kingston A2000 1 ТБ M.2 2280 SA2000M8/1000G", "brand": "Kingston", "category": "SSD-накопители", "price": 5290.0, "rating": 4.6, "reviews_count": 432, "url": "https://www.citilink.ru/product/kingston-a2000-1tb"},
        {"name": "SSD Transcend MTE250H 2 ТБ M.2 2280 TS2TMTE250H", "brand": "Transcend", "category": "SSD-накопители", "price": 14990.0, "rating": 4.7, "reviews_count": 123, "url": "https://www.citilink.ru/product/transcend-mte250h-2tb"},
        {"name": "SSD Silicon Power UD90 1 ТБ M.2 2280 SP01KGBP44UD9005", "brand": "Silicon Power", "category": "SSD-накопители", "price": 4490.0, "rating": 4.4, "reviews_count": 345, "url": "https://www.citilink.ru/product/silicon-power-ud90-1tb"},
        {"name": "SSD Netac N600S 256 ГБ SATA III 2.5\" NT01N600S-256G-S3X", "brand": "Netac", "category": "SSD-накопители", "price": 1890.0, "rating": 4.2, "reviews_count": 567, "url": "https://www.citilink.ru/product/netac-n600s-256gb"},
        {"name": "SSD Gigabyte AORUS Gen4 7300 1 ТБ M.2 2280 AG4731TB", "brand": "Gigabyte", "category": "SSD-накопители", "price": 9490.0, "rating": 4.8, "reviews_count": 198, "url": "https://www.citilink.ru/product/gigabyte-aorus-gen4-7300-1tb"},

        # Наушники
        {"name": "Наушники Sony WF-1000XM5, вставные, TWS, активное шумоподавление, черные", "brand": "Sony", "category": "Наушники", "price": 22990.0, "rating": 4.9, "reviews_count": 654, "url": "https://www.citilink.ru/product/sony-wf-1000xm5-black"},
        {"name": "Наушники Bose QuietComfort 45, накладные, активное шумоподавление, черные", "brand": "Bose", "category": "Наушники", "price": 29990.0, "rating": 4.8, "reviews_count": 345, "url": "https://www.citilink.ru/product/bose-quietcomfort-45-black"},
        {"name": "Наушники Samsung Galaxy Buds3 Pro SM-R630NZAACIS, вставные, TWS, серебристые", "brand": "Samsung", "category": "Наушники", "price": 16990.0, "rating": 4.7, "reviews_count": 234, "url": "https://www.citilink.ru/product/samsung-galaxy-buds3-pro"},
        {"name": "Наушники Jabra Elite 4 Active, вставные, TWS, активное шумоподавление, темно-серые", "brand": "Jabra", "category": "Наушники", "price": 8990.0, "rating": 4.6, "reviews_count": 312, "url": "https://www.citilink.ru/product/jabra-elite-4-active"},
        {"name": "Наушники Bang & Olufsen Beoplay H95, накладные, активное шумоподавление, черные", "brand": "Bang & Olufsen", "category": "Наушники", "price": 59990.0, "rating": 4.9, "reviews_count": 67, "url": "https://www.citilink.ru/product/beoplay-h95-black"},
        {"name": "Наушники Xiaomi Redmi Buds 4 Pro, вставные, TWS, активное шумоподавление, белые", "brand": "Xiaomi", "category": "Наушники", "price": 3990.0, "rating": 4.4, "reviews_count": 876, "url": "https://www.citilink.ru/product/xiaomi-redmi-buds-4-pro"},
        {"name": "Наушники Philips TAH8507BK/00, накладные, активное шумоподавление, черные", "brand": "Philips", "category": "Наушники", "price": 11990.0, "rating": 4.5, "reviews_count": 178, "url": "https://www.citilink.ru/product/philips-tah8507-black"},
        {"name": "Наушники Anker Soundcore Liberty 4 NC, вставные, TWS, активное шумоподавление, белые", "brand": "Anker", "category": "Наушники", "price": 6990.0, "rating": 4.6, "reviews_count": 432, "url": "https://www.citilink.ru/product/anker-soundcore-liberty-4-nc"},
    ],

    # ─── Regard ──────────────────────────────────────────────────────────────

    "Regard": [
        # Оперативная память
        {"name": "Оперативная память Kingston FURY Beast RGB 16 ГБ DDR4 3200 МГц DIMM CL16 KF432C16BB1A/16", "brand": "Kingston", "category": "Оперативная память", "price": 3590.0, "rating": 4.7, "reviews_count": 267, "url": "https://www.regard.ru/product/kingston-fury-beast-rgb-16gb"},
        {"name": "Оперативная память Crucial 16 ГБ DDR5 4800 МГц DIMM CL40 CT16G48C40S5", "brand": "Crucial", "category": "Оперативная память", "price": 4990.0, "rating": 4.5, "reviews_count": 134, "url": "https://www.regard.ru/product/crucial-16gb-ddr5-4800"},
        {"name": "Оперативная память Corsair Vengeance RGB 32 ГБ DDR5 5600 МГц DIMM CL36 CMH32GX5M2B5600C36", "brand": "Corsair", "category": "Оперативная память", "price": 11990.0, "rating": 4.8, "reviews_count": 78, "url": "https://www.regard.ru/product/corsair-vengeance-rgb-32gb-ddr5"},
        {"name": "Оперативная память ADATA 8 ГБ DDR4 3200 МГц DIMM CL22 AD4U32008G22-SGN", "brand": "ADATA", "category": "Оперативная память", "price": 1490.0, "rating": 4.2, "reviews_count": 312, "url": "https://www.regard.ru/product/adata-8gb-ddr4-3200"},
        {"name": "Оперативная память Team T-Force Delta RGB 32 ГБ DDR4 3600 МГц DIMM CL18", "brand": "Team", "category": "Оперативная память", "price": 6990.0, "rating": 4.6, "reviews_count": 89, "url": "https://www.regard.ru/product/team-delta-rgb-32gb-ddr4"},
        {"name": "Оперативная память G.Skill Trident Z5 Neo 32 ГБ DDR5 6000 МГц DIMM CL30 F5-6000J3038F16GX2-TZ5NR", "brand": "G.Skill", "category": "Оперативная память", "price": 15490.0, "rating": 4.9, "reviews_count": 56, "url": "https://www.regard.ru/product/gskill-trident-z5-neo-32gb"},
        {"name": "Оперативная память Patriot Signature 8 ГБ DDR4 3200 МГц DIMM CL22 PSD48G320081", "brand": "Patriot", "category": "Оперативная память", "price": 1390.0, "rating": 4.3, "reviews_count": 445, "url": "https://www.regard.ru/product/patriot-signature-8gb-ddr4"},
        {"name": "Оперативная память Samsung 16 ГБ DDR5 4800 МГц DIMM M323R2GA3BB0-CQK", "brand": "Samsung", "category": "Оперативная память", "price": 4290.0, "rating": 4.6, "reviews_count": 198, "url": "https://www.regard.ru/product/samsung-16gb-ddr5-4800"},

        # Видеокарты
        {"name": "Видеокарта NVIDIA GeForce RTX 4070 Ti SUPER 16 ГБ ASUS ROG STRIX RTX 4070 Ti SUPER OC GAMING 16G", "brand": "ASUS", "category": "Видеокарты", "price": 89990.0, "rating": 4.9, "reviews_count": 38, "url": "https://www.regard.ru/product/asus-rog-strix-rtx4070tis-oc"},
        {"name": "Видеокарта AMD Radeon RX 7600 XT 16 ГБ Gigabyte Gaming OC RX 7600 XT GAMING OC-16GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 35990.0, "rating": 4.5, "reviews_count": 61, "url": "https://www.regard.ru/product/gigabyte-rx7600xt-gaming-oc-16g"},
        {"name": "Видеокарта NVIDIA GeForce RTX 3070 8 ГБ MSI Gaming X Trio GeForce RTX 3070 8G LHR", "brand": "MSI", "category": "Видеокарты", "price": 34990.0, "rating": 4.6, "reviews_count": 178, "url": "https://www.regard.ru/product/msi-rtx3070-gaming-x-trio-lhr"},
        {"name": "Видеокарта NVIDIA GeForce RTX 4060 8 ГБ Palit Dual RTX 4060 8G", "brand": "Palit", "category": "Видеокарты", "price": 30990.0, "rating": 4.5, "reviews_count": 112, "url": "https://www.regard.ru/product/palit-dual-rtx4060-8g"},
        {"name": "Видеокарта AMD Radeon RX 7900 XT 20 ГБ Sapphire NITRO+ RX 7900 XT Vapor-X 20GB", "brand": "Sapphire", "category": "Видеокарты", "price": 79990.0, "rating": 4.8, "reviews_count": 29, "url": "https://www.regard.ru/product/sapphire-nitro-rx7900xt-20g"},
        {"name": "Видеокарта NVIDIA GeForce RTX 4070 12 ГБ Gigabyte AERO OC GV-N4070AERO OC-12GD", "brand": "Gigabyte", "category": "Видеокарты", "price": 53490.0, "rating": 4.7, "reviews_count": 84, "url": "https://www.regard.ru/product/gigabyte-rtx4070-aero-oc-12g"},
        {"name": "Видеокарта NVIDIA GeForce RTX 4090 24 ГБ MSI SUPRIM LIQUID X GeForce RTX 4090 24G", "brand": "MSI", "category": "Видеокарты", "price": 229990.0, "rating": 5.0, "reviews_count": 18, "url": "https://www.regard.ru/product/msi-rtx4090-suprim-liquid-x"},
        {"name": "Видеокарта AMD Radeon RX 6700 XT 12 ГБ XFX SPEEDSTER QICK319 RX 6700 XT Black Gaming", "brand": "XFX", "category": "Видеокарты", "price": 29990.0, "rating": 4.5, "reviews_count": 143, "url": "https://www.regard.ru/product/xfx-speedster-qick319-rx6700xt"},

        # Смартфоны
        {"name": "Смартфон Apple iPhone 15 Pro Max 256 ГБ натуральный титан", "brand": "Apple", "category": "Смартфоны", "price": 134990.0, "rating": 4.9, "reviews_count": 432, "url": "https://www.regard.ru/product/apple-iphone-15-pro-max-256gb"},
        {"name": "Смартфон Samsung Galaxy S24+ 256 ГБ мраморный серый", "brand": "Samsung", "category": "Смартфоны", "price": 94990.0, "rating": 4.8, "reviews_count": 287, "url": "https://www.regard.ru/product/samsung-galaxy-s24-plus-256gb"},
        {"name": "Смартфон Apple iPhone 14 128 ГБ полуночный", "brand": "Apple", "category": "Смартфоны", "price": 62990.0, "rating": 4.7, "reviews_count": 876, "url": "https://www.regard.ru/product/apple-iphone-14-128gb"},
        {"name": "Смартфон Xiaomi Poco X6 Pro 256 ГБ черный", "brand": "Xiaomi", "category": "Смартфоны", "price": 27990.0, "rating": 4.6, "reviews_count": 345, "url": "https://www.regard.ru/product/xiaomi-poco-x6-pro-256gb"},
        {"name": "Смартфон Samsung Galaxy A35 256 ГБ темно-синий", "brand": "Samsung", "category": "Смартфоны", "price": 28990.0, "rating": 4.4, "reviews_count": 213, "url": "https://www.regard.ru/product/samsung-galaxy-a35-256gb"},
        {"name": "Смартфон HONOR Magic6 Pro 512 ГБ черный", "brand": "HONOR", "category": "Смартфоны", "price": 79990.0, "rating": 4.7, "reviews_count": 94, "url": "https://www.regard.ru/product/honor-magic6-pro-512gb"},
        {"name": "Смартфон Xiaomi Redmi Note 13 128 ГБ полночный черный", "brand": "Xiaomi", "category": "Смартфоны", "price": 16990.0, "rating": 4.3, "reviews_count": 534, "url": "https://www.regard.ru/product/xiaomi-redmi-note-13-128gb"},
        {"name": "Смартфон realme GT 6 256 ГБ серебристый", "brand": "realme", "category": "Смартфоны", "price": 44990.0, "rating": 4.5, "reviews_count": 67, "url": "https://www.regard.ru/product/realme-gt6-256gb"},

        # Процессоры
        {"name": "Процессор Intel Core i5-14600KF, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 21490.0, "rating": 4.8, "reviews_count": 389, "url": "https://www.regard.ru/product/intel-core-i5-14600kf"},
        {"name": "Процессор Intel Core i7-14700KF, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 33490.0, "rating": 4.9, "reviews_count": 234, "url": "https://www.regard.ru/product/intel-core-i7-14700kf"},
        {"name": "Процессор AMD Ryzen 7 7700, AM5, OEM", "brand": "AMD", "category": "Процессоры", "price": 22990.0, "rating": 4.7, "reviews_count": 178, "url": "https://www.regard.ru/product/amd-ryzen-7-7700"},
        {"name": "Процессор AMD Ryzen 9 7900, AM5, OEM", "brand": "AMD", "category": "Процессоры", "price": 31990.0, "rating": 4.8, "reviews_count": 112, "url": "https://www.regard.ru/product/amd-ryzen-9-7900"},
        {"name": "Процессор AMD Ryzen 5 7500F, AM5, OEM", "brand": "AMD", "category": "Процессоры", "price": 14990.0, "rating": 4.7, "reviews_count": 345, "url": "https://www.regard.ru/product/amd-ryzen-5-7500f"},
        {"name": "Процессор Intel Core i9-14900KF, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 52990.0, "rating": 4.9, "reviews_count": 87, "url": "https://www.regard.ru/product/intel-core-i9-14900kf"},
        {"name": "Процессор Intel Core i5-12400F, LGA1700, OEM", "brand": "Intel", "category": "Процессоры", "price": 10990.0, "rating": 4.7, "reviews_count": 567, "url": "https://www.regard.ru/product/intel-core-i5-12400f"},
        {"name": "Процессор AMD Ryzen 5 5600X, AM4, OEM", "brand": "AMD", "category": "Процессоры", "price": 11490.0, "rating": 4.8, "reviews_count": 456, "url": "https://www.regard.ru/product/amd-ryzen-5-5600x"},

        # Ноутбуки
        {"name": "Ноутбук ASUS ROG Zephyrus G14 GA403UV-QS013W 14\" AMD Ryzen 9 8945HS/16GB/1TB SSD/RTX 4060 8GB", "brand": "ASUS", "category": "Ноутбуки", "price": 139990.0, "rating": 4.8, "reviews_count": 67, "url": "https://www.regard.ru/product/asus-rog-zephyrus-g14-ga403uv"},
        {"name": "Ноутбук Lenovo Legion Pro 5 16IRX8 16\" Intel Core i7-13700HX/16GB/512GB SSD/RTX 4060 8GB", "brand": "Lenovo", "category": "Ноутбуки", "price": 109990.0, "rating": 4.7, "reviews_count": 89, "url": "https://www.regard.ru/product/lenovo-legion-pro-5-16irx8"},
        {"name": "Ноутбук MSI Katana 15 B13VGK-1472RU 15.6\" Intel Core i7-13620H/16GB/512GB SSD/RTX 4070 8GB", "brand": "MSI", "category": "Ноутбуки", "price": 89990.0, "rating": 4.6, "reviews_count": 112, "url": "https://www.regard.ru/product/msi-katana-15-b13vgk"},
        {"name": "Ноутбук HP Omen 16-xf0074ci 16.1\" AMD Ryzen 7 7745HX/16GB/512GB SSD/RTX 4060 8GB", "brand": "HP", "category": "Ноутбуки", "price": 94990.0, "rating": 4.6, "reviews_count": 78, "url": "https://www.regard.ru/product/hp-omen-16-xf0074ci"},
        {"name": "Ноутбук Acer Predator Helios 16 PH16-71 16\" Intel Core i9-13900HX/32GB/1TB SSD/RTX 4080 12GB", "brand": "Acer", "category": "Ноутбуки", "price": 179990.0, "rating": 4.7, "reviews_count": 45, "url": "https://www.regard.ru/product/acer-predator-helios-16-ph16-71"},
        {"name": "Ноутбук Xiaomi RedmiBook 14 2024 14\" Intel Core i5-13500H/16GB/512GB SSD", "brand": "Xiaomi", "category": "Ноутбуки", "price": 47990.0, "rating": 4.4, "reviews_count": 234, "url": "https://www.regard.ru/product/xiaomi-redmibook-14-2024"},
        {"name": "Ноутбук Huawei MateBook D 14 53013XFQ 14\" Intel Core i5-1240P/8GB/512GB SSD", "brand": "Huawei", "category": "Ноутбуки", "price": 52990.0, "rating": 4.5, "reviews_count": 189, "url": "https://www.regard.ru/product/huawei-matebook-d14-53013xfq"},
        {"name": "Ноутбук Samsung Galaxy Book4 Pro NP960XGK 16\" Intel Core Ultra 7 155H/16GB/512GB SSD", "brand": "Samsung", "category": "Ноутбуки", "price": 114990.0, "rating": 4.7, "reviews_count": 56, "url": "https://www.regard.ru/product/samsung-galaxy-book4-pro"},

        # SSD-накопители
        {"name": "SSD Samsung 990 Pro 1 ТБ M.2 2280 MZ-V9P1T0BW", "brand": "Samsung", "category": "SSD-накопители", "price": 9990.0, "rating": 4.9, "reviews_count": 654, "url": "https://www.regard.ru/product/samsung-990-pro-1tb"},
        {"name": "SSD WD Black SN770 1 ТБ M.2 2280 WDS100T3X0E", "brand": "WD", "category": "SSD-накопители", "price": 6490.0, "rating": 4.8, "reviews_count": 432, "url": "https://www.regard.ru/product/wd-black-sn770-1tb"},
        {"name": "SSD Crucial T700 2 ТБ M.2 2280 CT2000T700SSD3", "brand": "Crucial", "category": "SSD-накопители", "price": 19990.0, "rating": 4.9, "reviews_count": 178, "url": "https://www.regard.ru/product/crucial-t700-2tb"},
        {"name": "SSD Kingston Fury Renegade 1 ТБ M.2 2280 SFYRD/1000G", "brand": "Kingston", "category": "SSD-накопители", "price": 9490.0, "rating": 4.8, "reviews_count": 312, "url": "https://www.regard.ru/product/kingston-fury-renegade-1tb"},
        {"name": "SSD Corsair MP600 Pro LPX 2 ТБ M.2 2280 CSSD-F2000GBMP600PLP", "brand": "Corsair", "category": "SSD-накопители", "price": 17990.0, "rating": 4.8, "reviews_count": 134, "url": "https://www.regard.ru/product/corsair-mp600-pro-lpx-2tb"},
        {"name": "SSD ADATA Legend 800 1 ТБ M.2 2280 ALEG-800-1000GCS", "brand": "ADATA", "category": "SSD-накопители", "price": 4990.0, "rating": 4.5, "reviews_count": 456, "url": "https://www.regard.ru/product/adata-legend-800-1tb"},
        {"name": "SSD Seagate FireCuda 530 1 ТБ M.2 2280 ZP1000GM3A013", "brand": "Seagate", "category": "SSD-накопители", "price": 8990.0, "rating": 4.7, "reviews_count": 234, "url": "https://www.regard.ru/product/seagate-firecuda-530-1tb"},
        {"name": "SSD Transcend ESD310C 1 ТБ USB Type-C TS1TESD310C", "brand": "Transcend", "category": "SSD-накопители", "price": 6990.0, "rating": 4.6, "reviews_count": 167, "url": "https://www.regard.ru/product/transcend-esd310c-1tb"},

        # Наушники
        {"name": "Наушники Sony WH-1000XM5, накладные, активное шумоподавление, серебристые", "brand": "Sony", "category": "Наушники", "price": 30990.0, "rating": 4.9, "reviews_count": 543, "url": "https://www.regard.ru/product/sony-wh-1000xm5-silver"},
        {"name": "Наушники Bose QuietComfort Ultra, накладные, активное шумоподавление, черные", "brand": "Bose", "category": "Наушники", "price": 39990.0, "rating": 4.9, "reviews_count": 234, "url": "https://www.regard.ru/product/bose-quietcomfort-ultra-black"},
        {"name": "Наушники Apple AirPods Max, накладные, космический серый", "brand": "Apple", "category": "Наушники", "price": 49990.0, "rating": 4.7, "reviews_count": 312, "url": "https://www.regard.ru/product/apple-airpods-max-space-gray"},
        {"name": "Наушники Sennheiser HD 660S2, накладные, открытые, черные", "brand": "Sennheiser", "category": "Наушники", "price": 44990.0, "rating": 4.8, "reviews_count": 89, "url": "https://www.regard.ru/product/sennheiser-hd-660s2"},
        {"name": "Наушники HiFiMAN SUNDARA, накладные, открытые, черно-серебристые", "brand": "HiFiMAN", "category": "Наушники", "price": 29990.0, "rating": 4.8, "reviews_count": 67, "url": "https://www.regard.ru/product/hifiman-sundara"},
        {"name": "Наушники Nothing Ear (2), вставные, TWS, активное шумоподавление, белые", "brand": "Nothing", "category": "Наушники", "price": 8990.0, "rating": 4.6, "reviews_count": 213, "url": "https://www.regard.ru/product/nothing-ear-2-white"},
        {"name": "Наушники HONOR Choice Earbuds X5 Pro, вставные, TWS, активное шумоподавление", "brand": "HONOR", "category": "Наушники", "price": 3490.0, "rating": 4.3, "reviews_count": 456, "url": "https://www.regard.ru/product/honor-choice-earbuds-x5-pro"},
        {"name": "Наушники Technics EAH-A800, накладные, активное шумоподавление, черные", "brand": "Technics", "category": "Наушники", "price": 24990.0, "rating": 4.7, "reviews_count": 123, "url": "https://www.regard.ru/product/technics-eah-a800-black"},
    ],
}
