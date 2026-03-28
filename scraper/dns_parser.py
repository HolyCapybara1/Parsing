from .base import BaseParser

CATEGORIES = {
    "Оперативная память": "/catalog/operativnaya-pamyat/",
    "Видеокарты": "/catalog/videokarty/",
    "Смартфоны": "/catalog/smartfony/",
}


class DnsParser(BaseParser):
    def __init__(self):
        super().__init__("DNS", "https://www.dns-shop.ru")

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

            items = soup.select(".catalog-product")
            if not items:
                break

            for item in items:
                try:
                    name_tag = item.select_one(".catalog-product__name")
                    price_tag = item.select_one(".product-buy__price")
                    rating_tag = item.select_one(".product-item__rating-count")
                    reviews_tag = item.select_one(".product-item__reviews-count")
                    link_tag = item.select_one("a[href]")

                    name = name_tag.text.strip() if name_tag else ""
                    price_str = (
                        price_tag.text.strip().replace(" ", "").replace("₽", "")
                        if price_tag else "0"
                    )
                    price = float("".join(filter(str.isdigit, price_str)) or 0)
                    rating = float(rating_tag.text.strip()) if rating_tag else 0.0
                    reviews = int(
                        "".join(filter(str.isdigit, reviews_tag.text))
                        if reviews_tag else 0
                    )
                    brand = name.split()[0] if name else ""
                    item_url = (
                        self.base_url + link_tag["href"]
                        if link_tag else ""
                    )

                    if name and price > 0:
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
                    self.logger.error(f"Ошибка парсинга товара DNS: {e}")

            page += 1
            if page > 5:
                break

        self.logger.info(f"DNS {category}: собрано {len(products)} товаров")
        return products
