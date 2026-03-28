from .base import BaseParser

# Реальные URL категорий Regard
CATEGORIES = {
    "Оперативная память": "/catalog/18/",
    "Видеокарты": "/catalog/14/",
    "Смартфоны": "/catalog/516/",
    "Процессоры": "/catalog/4/",
    "Ноутбуки": "/catalog/53/",
    "SSD-накопители": "/catalog/1572/",
    "Наушники": "/catalog/614/",
}


class RegardParser(BaseParser):
    def __init__(self):
        super().__init__("Regard", "https://www.regard.ru")

    def parse_category(self, category: str) -> list[dict]:
        path = CATEGORIES.get(category)
        if not path:
            self.logger.warning(f"Regard: категория '{category}' не найдена")
            return []

        products = []
        for page_num in range(1, 6):
            url = f"{self.base_url}{path}?page={page_num}"
            self.logger.info(f"Regard {category}: страница {page_num}")

            soup = self.get_page(url, wait_selector=".b-product-card, .product-card")
            if not soup:
                break

            items = (
                soup.select(".b-product-card") or
                soup.select(".product-card") or
                soup.select("[class*='product-item']")
            )
            if not items:
                self.logger.info(f"Regard {category}: стр.{page_num} пустая, стоп")
                break

            for item in items:
                try:
                    # Название
                    name_tag = (
                        item.select_one(".b-product-card__name a") or
                        item.select_one(".b-product-card__name") or
                        item.select_one(".product-card__name a") or
                        item.select_one(".product-card__name") or
                        item.select_one("a[class*='name']")
                    )
                    if not name_tag:
                        continue
                    name = name_tag.get_text(strip=True)
                    if not name:
                        continue

                    # Ссылка
                    link_tag = name_tag if name_tag.name == "a" else item.select_one("a[href]")
                    href = link_tag.get("href", "") if link_tag else ""
                    item_url = self.base_url + href if href.startswith("/") else href

                    # Цена
                    price_tag = (
                        item.select_one(".b-product-card__buy-price") or
                        item.select_one(".product-card__price") or
                        item.select_one("[class*='price']")
                    )
                    price = self.clean_price(price_tag.get_text() if price_tag else "")
                    if price <= 0:
                        continue

                    # Рейтинг
                    rating_tag = item.select_one("[class*='rating']")
                    rating_val = 0.0
                    if rating_tag:
                        # Regard показывает рейтинг звёздами — ищем числовое значение
                        style = rating_tag.get("style", "")
                        if "width" in style:
                            # width: 80% → 4.0 из 5
                            try:
                                pct = float("".join(c for c in style if c.isdigit() or c == "."))
                                rating_val = round(pct / 20, 1)
                            except Exception:
                                pass
                        else:
                            rating_val = self.clean_rating(rating_tag.get_text())

                    # Отзывы
                    reviews_tag = item.select_one("[class*='review']") or item.select_one("[class*='comment']")
                    reviews = self.clean_reviews(reviews_tag.get_text() if reviews_tag else "")

                    brand = name.split()[0] if name else ""

                    products.append({
                        "name": name,
                        "brand": brand,
                        "category": category,
                        "price": price,
                        "rating": rating_val,
                        "reviews_count": reviews,
                        "url": item_url,
                        "source": "Regard",
                    })
                except Exception as e:
                    self.logger.error(f"Regard: ошибка обработки товара: {e}")

            self.logger.info(f"Regard {category}: стр.{page_num} — {len(items)} карточек")

            next_btn = soup.select_one("a[rel='next']") or soup.select_one(".pagination .next")
            if not next_btn:
                break

        self.logger.info(f"Regard {category}: итого {len(products)} товаров")
        return products
