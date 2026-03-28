from .base import BaseParser

# Реальные URL категорий DNS
CATEGORIES = {
    "Оперативная память": "/catalog/operativnaya-pamyat/",
    "Видеокарты": "/catalog/videokarty/",
    "Смартфоны": "/catalog/smartfony/",
    "Процессоры": "/catalog/processory/",
    "Ноутбуки": "/catalog/noutbuki/",
    "SSD-накопители": "/catalog/ssd-nakopiteli/",
    "Наушники": "/catalog/naushniki-vkladyshi/",
}


class DnsParser(BaseParser):
    def __init__(self):
        super().__init__("DNS", "https://www.dns-shop.ru")

    def parse_category(self, category: str) -> list[dict]:
        path = CATEGORIES.get(category)
        if not path:
            self.logger.warning(f"DNS: категория '{category}' не найдена")
            return []

        products = []
        for page_num in range(1, 6):  # первые 5 страниц
            url = f"{self.base_url}{path}?p={page_num}"
            self.logger.info(f"DNS {category}: страница {page_num} — {url}")

            soup = self.get_page(url, wait_selector=".catalog-product")
            if not soup:
                break

            items = soup.select(".catalog-product")
            if not items:
                self.logger.info(f"DNS {category}: страница {page_num} пустая, стоп")
                break

            for item in items:
                try:
                    # Название
                    name_tag = (
                        item.select_one("a.catalog-product__name") or
                        item.select_one(".catalog-product__name")
                    )
                    if not name_tag:
                        continue
                    name = name_tag.get_text(strip=True)
                    if not name:
                        continue

                    # Ссылка
                    href = name_tag.get("href", "")
                    item_url = self.base_url + href if href.startswith("/") else href

                    # Цена
                    price_tag = (
                        item.select_one(".product-buy__price") or
                        item.select_one("[class*='price_current']") or
                        item.select_one("[class*='price-current']")
                    )
                    price = self.clean_price(price_tag.get_text() if price_tag else "")
                    if price <= 0:
                        continue

                    # Рейтинг
                    rating_tag = (
                        item.select_one(".product-item__rating-count") or
                        item.select_one("[class*='rating']")
                    )
                    rating = self.clean_rating(rating_tag.get_text() if rating_tag else "")

                    # Отзывы
                    reviews_tag = (
                        item.select_one(".product-item__reviews-count") or
                        item.select_one("[class*='reviews']")
                    )
                    reviews = self.clean_reviews(reviews_tag.get_text() if reviews_tag else "")

                    # Бренд — первое слово названия
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

            self.logger.info(f"DNS {category}: страница {page_num} — {len(items)} карточек")

            # Проверяем есть ли следующая страница
            next_btn = soup.select_one("a.pagination-widget__page-link[rel='next']")
            if not next_btn:
                break

        self.logger.info(f"DNS {category}: итого {len(products)} товаров")
        return products
