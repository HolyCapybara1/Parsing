"""
Диагностика парсинга — проверяет страницу товаров на Regard.
Запуск: python debug_dns.py
"""
import sys
import os
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.makedirs("debug_output", exist_ok=True)

# URL страницы с реальными товарами (не категории, а листинг)
TEST_URL = "https://www.nix.ru/price/ozu-pamyat-ddr5/"


def _playwright_thread(result: dict):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            locale="ru-RU",
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.new_page()
        page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )

        try:
            stealth_applied = False
            try:
                from playwright_stealth import stealth_sync
                stealth_sync(page)
                stealth_applied = True
            except ImportError:
                pass

            print(f"Stealth: {'да' if stealth_applied else 'нет'}")
            print(f"Загружаю: {TEST_URL}")

            page.goto(TEST_URL, wait_until="networkidle", timeout=40000)
            time.sleep(3)

            # Скролл вниз чтобы загрузить lazy-контент
            page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            time.sleep(1.5)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)

            html = page.content()
            result["title"] = page.title()
            result["html"] = html

            with open("debug_output/nix_page.html", "w", encoding="utf-8") as f:
                f.write(html)

            page.screenshot(path="debug_output/nix_screenshot.png", full_page=False)

        except Exception as e:
            result["error"] = str(e)
        finally:
            browser.close()


def run():
    result = {}
    t = threading.Thread(target=_playwright_thread, args=(result,), daemon=True)
    t.start()
    t.join(timeout=60)

    if "error" in result:
        print(f"Ошибка: {result['error']}")
        return

    html = result.get("html", "")
    print(f"Заголовок: {result.get('title', 'N/A')}")
    print(f"Размер HTML: {len(html)} символов")
    print(f"Скриншот сохранён: debug_output/nix_screenshot.png")

    if not html:
        print("HTML пустой!")
        return

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Ищем классы связанные с товарами
    classes = set()
    for tag in soup.find_all(True, limit=2000):
        for cls in tag.get("class", []):
            for kw in ["product", "catalog", "card", "item", "price", "name",
                       "good", "товар", "Product", "Card", "Good", "Item"]:
                if kw.lower() in cls.lower():
                    classes.add(cls)

    if classes:
        print(f"\nНайденные CSS-классы ({len(classes)} шт.):")
        for c in sorted(classes):
            print(f"  .{c}")
    else:
        body = soup.find("body")
        text = body.get_text()[:800] if body else ""
        print(f"\nКлассы не найдены. Текст страницы:\n{text}")

    # Показываем структуру карточки товара
    product_links = soup.select("a[href*='/product/'], a[href*='/good/'], a[href*='/tovar/']")
    if product_links:
        print(f"\nНайдено ссылок на товары: {len(product_links)}")
        link = product_links[0]
        print(f"Пример ссылки: {link.get('href', '')}")
        print(f"Текст ссылки: {link.get_text(strip=True)[:80]}")

        # Поднимаемся вверх по дереву и показываем классы родителей
        print("\nЦепочка родительских классов (снизу вверх):")
        node = link
        for i in range(8):
            node = node.parent
            if node is None or node.name in ["html", "body", "[document]"]:
                break
            classes = node.get("class", [])
            print(f"  {i+1}. <{node.name}> классы: {classes}")

        # Показываем всё содержимое карточки
        card = soup.select_one("[class*='ListingRenderer_listingCard']")
        if card:
            print("\n--- Все классы внутри карточки ---")
            for tag in card.find_all(True):
                cls = tag.get("class", [])
                text = tag.get_text(strip=True)[:60]
                if cls:
                    print(f"  <{tag.name}> {cls} → '{text}'")


if __name__ == "__main__":
    run()
