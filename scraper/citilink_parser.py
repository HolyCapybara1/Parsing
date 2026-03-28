from .base import BaseParser

# Реальные URL категорий Ситилинк
CATEGORIES = {
    "Оперативная память": "/catalog/moduli-pamyati/",
    "Видеокарты": "/catalog/videokarty/",
    "Смартфоны": "/catalog/smartfony/",
    "Процессоры": "/catalog/processory/",
    "Ноутбуки": "/catalog/noutbuki/",
    "SSD-накопители": "/catalog/ssd-nakopiteli/",
    "Наушники": "/catalog/naushniki/",
}


class CitilinkParser(BaseParser):
    def __init__(self):
        super().__init__("Ситилинк", "https://www.citilink.ru")

    def parse_category(self, category: str) -> list[dict]:
        path = CATEGORIES.get(category)
        if not path:
            self.logger.warning(f"Ситилинк: категория '{category}' не найдена")
            return []

        products = []
        for page_num in range(1, 6):
            url = f"{self.base_url}{path}?p={page_num}"
            self.logger.info(f"Ситилинк {category}: страница {page_num}")

            soup = self.get_page(url, wait_selector="[class*='ProductCard']")
            if not soup:
                break

            # Ситилинк использует React — ищем по data-атрибутам и стабильным структурам
            items = (
                soup.select("[data-meta-product]") or
                soup.select("article[class*='ProductCard']") or
                soup.select("[class*='ProductCard_root']")
            )
            if not items:
                self.logger.info(f"Ситилинк {category}: стр.{page_num} пустая, стоп")
                break

            for item in items:
                try:
                    # Название
                    name_tag = (
                        item.select_one("[class*='ProductCard_title']") or
                        item.select_one("[class*='_title']") or
                        item.select_one("a[class*='title']") or
                        item.select_one("h3") or
                        item.select_one("h2")
                    )
                    if not name_tag:
                        continue
                    name = name_tag.get_text(strip=True)
                    if not name:
                        continue

                    # Ссылка
                    link_tag = item.select_one("a[href*='/product/']") or item.select_one("a[href]")
                    href = link_tag.get("href", "") if link_tag else ""
                    item_url = self.base_url + href if href.startswith("/") else href

                    # Цена — ищем числа в элементах с price в классе
                    price_tag = (
                        item.select_one("[class*='price__current']") or
                        item.select_one("[class*='ProductCard_price']") or
                        item.select_one("[class*='Price_price']") or
                        item.select_one("[class*='price']")
                    )
                    price = self.clean_price(price_tag.get_text() if price_tag else "")
                    if price <= 0:
                        continue

                    # Рейтинг
                    rating_tag = (
                        item.select_one("[class*='Rating_']") or
                        item.select_one("[class*='rating']")
                    )
                    rating = self.clean_rating(rating_tag.get("aria-label", "") or
                                               (rating_tag.get_text() if rating_tag else ""))

                    # Отзывы
                    reviews_tag = item.select_one("[class*='review']") or item.select_one("[class*='Review']")
                    reviews = self.clean_reviews(reviews_tag.get_text() if reviews_tag else "")

                    brand = name.split()[0] if name else ""

                    products.append({
                        "name": name,
                        "brand": brand,
                        "category": category,
                        "price": price,
                        "rating": rating,
                        "reviews_count": reviews,
                        "url": item_url,
                        "source": "Ситилинк",
                    })
                except Exception as e:
                    self.logger.error(f"Ситилинк: ошибка обработки товара: {e}")

            self.logger.info(f"Ситилинк {category}: стр.{page_num} — {len(items)} карточек")

            next_btn = soup.select_one("a[rel='next']") or soup.select_one("[class*='pagination'][class*='next']")
            if not next_btn:
                break

        self.logger.info(f"Ситилинк {category}: итого {len(products)} товаров")
        return products
