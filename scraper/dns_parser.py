from .base import BaseParser

# Актуальные URL категорий DNS (с числовыми ID)
CATEGORIES = {
    "Оперативная память": "/catalog/17a89a3916404e77/operativnaa-pamat-dimm/",
    "Видеокарты": "/catalog/17a8a01d16404e77/videokarty/",
    "Смартфоны": "/catalog/17a89adb16404e77/smartfony/",
    "Процессоры": "/catalog/17a8936716404e77/processory/",
    "Ноутбуки": "/catalog/17a892c816404e77/noutbuki/",
    "SSD-накопители": "/catalog/17a8993c16404e77/ssd-nakopiteli/",
    "Наушники": "/catalog/17a89a3316404e77/naushniki-vkladyshi/",
}

# Возможные селекторы карточек товара на DNS (пробуем по очереди)
PRODUCT_SELECTORS = [
    ".catalog-product",
    "[data-id]",
    ".catalog-product-list__product",
    ".ui-2-card",
    "article",
]


class DnsParser(BaseParser):
    def __init__(self):
        super().__init__("DNS", "https://www.dns-shop.ru")

    def parse_category(self, category: str) -> list[dict]:
        path = CATEGORIES.get(category)
        if not path:
            self.logger.warning(f"DNS: категория '{category}' не найдена")
            return []

        products = []
        for page_num in range(1, 6):
            url = f"{self.base_url}{path}?p={page_num}"
            self.logger.info(f"DNS {category}: страница {page_num} — {url}")

            soup = self.get_page(url, wait_selector=None)
            if not soup:
                break

            # Диагностика: показываем какие классы есть на странице
            if page_num == 1:
                all_classes = set()
                for tag in soup.find_all(True, limit=200):
                    for cls in tag.get("class", []):
                        if "product" in cls.lower() or "catalog" in cls.lower() or "card" in cls.lower():
                            all_classes.add(cls)
                self.logger.info(f"DNS классы на странице: {sorted(all_classes)[:30]}")

            # Пробуем все возможные селекторы
            items = []
            used_selector = None
            for sel in PRODUCT_SELECTORS:
                items = soup.select(sel)
                if items:
                    used_selector = sel
                    self.logger.info(f"DNS: найдено {len(items)} элементов по селектору '{sel}'")
                    break

            if not items:
                self.logger.warning(f"DNS {category}: стр.{page_num} — карточки не найдены ни по одному селектору")
                break

            for item in items:
                try:
                    # Название
                    name_tag = (
                        item.select_one("a.catalog-product__name") or
                        item.select_one(".catalog-product__name") or
                        item.select_one("a[class*='name']") or
                        item.select_one("a[href*='/product/']") or
                        item.select_one("h3 a") or item.select_one("h2 a")
                    )
                    if not name_tag:
                        continue
                    name = name_tag.get_text(strip=True)
                    if not name or len(name) < 5:
                        continue

                    href = name_tag.get("href", "")
                    item_url = self.base_url + href if href.startswith("/") else href

                    # Цена
                    price_tag = (
                        item.select_one(".product-buy__price") or
                        item.select_one("[class*='price_current']") or
                        item.select_one("[class*='price-current']") or
                        item.select_one("[class*='price']")
                    )
                    price = self.clean_price(price_tag.get_text() if price_tag else "")
                    if price <= 0:
                        continue

                    # Рейтинг
                    rating_tag = (
                        item.select_one(".product-item__rating-count") or
                        item.select_one("[class*='rating-count']") or
                        item.select_one("[class*='rating']")
                    )
                    rating = self.clean_rating(rating_tag.get_text() if rating_tag else "")

                    # Отзывы — "16.2k отзывов"
                    reviews_tag = (
                        item.select_one(".product-item__reviews-count") or
                        item.select_one("[class*='reviews']") or
                        item.select_one("[class*='otzyv']")
                    )
                    reviews_text = reviews_tag.get_text() if reviews_tag else ""
                    # Обрабатываем формат "16.2k"
                    if "k" in reviews_text.lower():
                        try:
                            num = float("".join(c for c in reviews_text if c.isdigit() or c == "."))
                            reviews = int(num * 1000)
                        except Exception:
                            reviews = 0
                    else:
                        reviews = self.clean_reviews(reviews_text)

                    brand = name.split()[0] if name else ""

                    products.append({
                        "name": name,
                        "brand": brand,
                        "category": category,
                        "price": price,
                        "rating": rating,
                        "reviews_count": reviews,
                        "url": item_url,
                        "source": "DNS",
                    })
                except Exception as e:
                    self.logger.error(f"DNS: ошибка обработки товара: {e}")

            self.logger.info(f"DNS {category}: страница {page_num} — {len(products)} товаров всего")

            next_btn = (
                soup.select_one("a.pagination-widget__page-link[rel='next']") or
                soup.select_one("[class*='pagination'] a[rel='next']")
            )
            if not next_btn:
                break

        self.logger.info(f"DNS {category}: итого {len(products)} товаров")
        return products
