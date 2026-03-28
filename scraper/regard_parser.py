from .base import BaseParser

CATEGORIES = {
    "Оперативная память": "/catalog/18/",
    "Видеокарты": "/catalog/14/",
    "Смартфоны": "/catalog/33/",
}


class RegardParser(BaseParser):
    def __init__(self):
        super().__init__("Regard", "https://www.regard.ru")

    def parse_category(self, category: str) -> list[dict]:
        path = CATEGORIES.get(category, "")
        if not path:
            return []

        products, page = [], 1
        while True:
            url = f"{self.base_url}{path}?page={page}"
            soup = self.get_page(url)
            if not soup:
                break

            items = soup.select(".product-card") or soup.select(".b-product-card")
            if not items:
                items = soup.select("[class*='product']")
            if not items:
                break

            for item in items:
                try:
                    name_tag = (
                        item.select_one(".product-card__name") or
                        item.select_one(".b-product-card__name") or
                        item.select_one("[class*='name']")
                    )
                    price_tag = (
                        item.select_one(".product-card__price") or
                        item.select_one(".b-product-card__price") or
                        item.select_one("[class*='price']")
                    )
                    rating_tag = item.select_one("[class*='rating']")
                    link_tag = item.select_one("a[href]")

                    name = name_tag.text.strip() if name_tag else ""
                    price_str = price_tag.text.strip() if price_tag else "0"
                    price = float("".join(filter(str.isdigit, price_str)) or 0)
                    rating_text = rating_tag.text.strip() if rating_tag else "0"
                    rating = float("".join(c for c in rating_text if c.isdigit() or c == ".") or 0)
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
                            "reviews_count": 0,
                            "url": item_url,
                            "source": "Regard",
                        })
                except Exception as e:
                    self.logger.error(f"Ошибка парсинга товара Regard: {e}")

            page += 1
            if page > 5:
                break

        self.logger.info(f"Regard {category}: собрано {len(products)} товаров")
        return products
