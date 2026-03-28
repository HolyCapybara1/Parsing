from .base import BaseParser

# URL категорий Regard (уточните остальные по аналогии с RAM)
CATEGORIES = {
    "Оперативная память": "/catalog/1010/operativnaya-pamyat/",
    "Видеокарты": "/catalog/1070/videokarty/",
    "Смартфоны": "/catalog/1130/smartfony/",
    "Процессоры": "/catalog/1020/processory/",
    "Ноутбуки": "/catalog/1040/noutbuki/",
    "SSD-накопители": "/catalog/1572/ssd-nakopiteli/",
    "Наушники": "/catalog/614/naushniki/",
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
            url = f"{self.base_url}{path}?sort=price&page={page_num}"
            self.logger.info(f"Regard {category}: страница {page_num}")

            soup = self.get_page(url, wait_selector="[class*='ListingRenderer_listingCard']")
            if not soup:
                break

            cards = soup.select("[class*='ListingRenderer_listingCard']")
            if not cards:
                self.logger.info(f"Regard {category}: стр.{page_num} пустая, стоп")
                break

            for card in cards:
                try:
                    # Название
                    name_tag = (
                        card.select_one("[class*='CardText_title']") or
                        card.select_one("a[class*='CardText_link']")
                    )
                    if not name_tag:
                        continue
                    name = name_tag.get_text(strip=True)
                    if not name or len(name) < 5:
                        continue

                    # Ссылка
                    link_tag = card.select_one("a[class*='CardText_link']")
                    href = link_tag.get("href", "") if link_tag else ""
                    item_url = self.base_url + href if href.startswith("/") else href

                    # Цена — берём из основного блока цены (не SimilarGood)
                    price_tag = card.select_one(
                        "[class*='CardPrice_price'], span[class*='Price_price']"
                    )
                    # Избегаем цен из блока "похожие товары"
                    if not price_tag:
                        price_tag = card.select_one("[class*='Card_price']")
                    price = self.clean_price(price_tag.get_text() if price_tag else "")
                    if price <= 0:
                        continue

                    # Рейтинг — считаем звёзды
                    full = len(card.select("[class*='ReviewStars_full']"))
                    half = len(card.select("[class*='ReviewStars_half']"))
                    rating = round(full + 0.5 * half, 1)

                    # Количество отзывов
                    reviews_tag = card.select_one(
                        "p[class*='ReviewStars_text'], a[class*='ReviewStars_link']"
                    )
                    reviews = self.clean_reviews(reviews_tag.get_text() if reviews_tag else "")

                    # Бренд — второе слово (первое обычно "Оперативная", "Видеокарта" и т.д.)
                    words = name.split()
                    brand = words[2] if len(words) > 2 else (words[0] if words else "")

                    products.append({
                        "name": name,
                        "brand": brand,
                        "category": category,
                        "price": price,
                        "rating": rating,
                        "reviews_count": reviews,
                        "url": item_url,
                        "source": "Regard",
                    })
                except Exception as e:
                    self.logger.error(f"Regard: ошибка обработки товара: {e}")

            self.logger.info(f"Regard {category}: стр.{page_num} — {len(products)} товаров всего")

            # Проверяем пагинацию
            next_btn = (
                soup.select_one("a[rel='next']") or
                soup.select_one("[class*='pagination'] [class*='next']") or
                soup.select_one("[class*='Pagination'] [class*='next']")
            )
            if not next_btn:
                break

        self.logger.info(f"Regard {category}: итого {len(products)} товаров")
        return products
