from .base import BaseParser

CATEGORIES = {
    "Оперативная память": "/category/moduli-pamyati/",
    "Видеокарты": "/category/videokarty/",
    "Смартфоны": "/category/smartfony/",
}


class CitilinkParser(BaseParser):
    def __init__(self):
        super().__init__("Ситилинк", "https://www.citilink.ru")

    def parse_category(self, category: str) -> list[dict]:
        path = CATEGORIES.get(category, "")
        if not path:
            return []

        products, page = [], 1
        while True:
            url = f"{self.base_url}{path}?p={page}"
            soup = self.get_page(url)
            if not soup:
                break

            items = soup.select(".product-card")
            if not items:
                items = soup.select("[data-meta-product]")
            if not items:
                break

            for item in items:
                try:
                    name_tag = item.select_one(".product-card__title") or \
                               item.select_one("[class*='title']")
                    price_tag = item.select_one(".product-card__price_current") or \
                                item.select_one("[class*='price']")
                    rating_tag = item.select_one(".rating__value") or \
                                 item.select_one("[class*='rating']")
                    reviews_tag = item.select_one(".product-card__reviews-count") or \
                                  item.select_one("[class*='reviews']")
                    link_tag = item.select_one("a[href]")

                    name = name_tag.text.strip() if name_tag else ""
                    price_str = price_tag.text.strip() if price_tag else "0"
                    price = float("".join(filter(str.isdigit, price_str)) or 0)
                    rating_text = rating_tag.text.strip() if rating_tag else "0"
                    rating = float("".join(c for c in rating_text if c.isdigit() or c == ".") or 0)
                    reviews_text = reviews_tag.text.strip() if reviews_tag else "0"
                    reviews = int("".join(filter(str.isdigit, reviews_text)) or 0)
                    brand = name.split()[0] if name else ""
                    item_url = link_tag["href"] if link_tag else ""
                    if item_url and not item_url.startswith("http"):
                        item_url = self.base_url + item_url

                    if name and price > 0:
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
                    self.logger.error(f"Ошибка парсинга товара Ситилинк: {e}")

            page += 1
            if page > 5:
                break

        self.logger.info(f"Ситилинк {category}: собрано {len(products)} товаров")
        return products
