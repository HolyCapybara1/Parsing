"""
Диагностический скрипт — проверяет что возвращает сайт.
Запуск: python debug_dns.py
"""
import sys, os, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.makedirs("debug_output", exist_ok=True)

TEST_URL = "https://www.regard.ru/catalog/1010/operativnaya-pamyat"

def run():
    if sys.platform == "win32":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    result = {}

    def _thread():
        import asyncio as _asyncio
        if sys.platform == "win32":
            _asyncio.set_event_loop_policy(_asyncio.WindowsProactorEventLoopPolicy())
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
                ctx = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    locale="ru-RU", viewport={"width": 1280, "height": 800},
                )
                page = ctx.new_page()
                page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                page.goto(TEST_URL, wait_until="networkidle", timeout=40000)
                time.sleep(3)
                html = page.content()
                with open("debug_output/regard_page.html", "w", encoding="utf-8") as f:
                    f.write(html)
                page.screenshot(path="debug_output/regard_screenshot.png")
                result["title"] = page.title()
                result["size"] = len(html)
                browser.close()
        except Exception as e:
            result["error"] = str(e)

    t = threading.Thread(target=_thread)
    t.start()
    t.join(timeout=60)

    if "error" in result:
        print(f"Ошибка: {result['error']}")
        return

    print(f"Заголовок: {result.get('title')}")
    print(f"Размер HTML: {result.get('size', 0)} символов")
    print(f"Скриншот: debug_output/regard_screenshot.png")

    from bs4 import BeautifulSoup
    with open("debug_output/regard_page.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    classes = set()
    for tag in soup.find_all(True, limit=500):
        for cls in tag.get("class", []):
            for kw in ["product", "catalog", "card", "item", "price", "name", "good"]:
                if kw in cls.lower():
                    classes.add(cls)

    if classes:
        print("\nКлассы на странице:")
        for c in sorted(classes):
            print(f"  .{c}")
    else:
        body = soup.find("body")
        print("\nКлассы не найдены. Содержимое страницы:")
        print(body.get_text()[:600] if body else "(пусто)")

if __name__ == "__main__":
    run()

import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.makedirs("debug_output", exist_ok=True)

def run():
    import asyncio
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    from playwright.sync_api import sync_playwright
    import threading

    result = {}

    def _thread():
        import asyncio as _asyncio
        if sys.platform == "win32":
            _asyncio.set_event_loop_policy(_asyncio.WindowsProactorEventLoopPolicy())

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            ctx = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                locale="ru-RU",
                viewport={"width": 1280, "height": 800},
            )
            page = ctx.new_page()
            page.set_extra_http_headers({
                "Accept-Language": "ru-RU,ru;q=0.9",
            })

            url = "https://www.dns-shop.ru/catalog/17a89a3916404e77/operativnaa-pamat-dimm/"
            print(f"Загружаю: {url}")
            page.goto(url, wait_until="networkidle", timeout=40000)

            import time
            time.sleep(3)

            # Сохраняем HTML
            html = page.content()
            with open("debug_output/dns_page.html", "w", encoding="utf-8") as f:
                f.write(html)

            # Сохраняем скриншот
            page.screenshot(path="debug_output/dns_screenshot.png", full_page=False)

            result["html_size"] = len(html)
            result["title"] = page.title()
            browser.close()

    t = threading.Thread(target=_thread)
    t.start()
    t.join(timeout=60)

    print(f"Заголовок страницы: {result.get('title', 'N/A')}")
    print(f"Размер HTML: {result.get('html_size', 0)} символов")
    print(f"HTML сохранён в: debug_output/dns_page.html")
    print(f"Скриншот сохранён в: debug_output/dns_screenshot.png")

    # Анализируем HTML
    if result.get("html_size", 0) > 0:
        from bs4 import BeautifulSoup
        with open("debug_output/dns_page.html", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        # Ищем классы с нужными словами
        interesting = set()
        for tag in soup.find_all(True):
            for cls in tag.get("class", []):
                for kw in ["product", "catalog", "card", "item", "price", "name"]:
                    if kw in cls.lower():
                        interesting.add(cls)

        print(f"\nНайденные классы (product/catalog/card/item/price/name):")
        for cls in sorted(interesting):
            print(f"  .{cls}")

        if not interesting:
            # Смотрим первые 500 символов body
            body = soup.find("body")
            if body:
                text = body.get_text()[:500]
                print(f"\nСодержимое страницы (первые 500 символов):")
                print(text)

if __name__ == "__main__":
    run()
