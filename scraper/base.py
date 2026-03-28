import logging
import time
from bs4 import BeautifulSoup


class BaseParser:
    """Базовый класс парсеров. Использует Playwright для рендеринга JavaScript."""

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    DELAY = 2.0  # секунд между страницами

    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.logger = logging.getLogger(source_name)

    def get_page(self, url: str, wait_selector: str = None) -> BeautifulSoup | None:
        """Загрузить страницу через Playwright в отдельном потоке (обход проблем asyncio на Windows)."""
        try:
            import playwright  # noqa: F401
        except ImportError:
            self.logger.error("Playwright не установлен. Выполните: python -m pip install playwright && python -m playwright install chromium")
            return None

        result = [None]
        exc = [None]
        user_agent = self.USER_AGENT
        delay = self.DELAY
        logger = self.logger

        def _run():
            import asyncio
            import sys
            import random
            if sys.platform == "win32":
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

            try:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        args=[
                            "--no-sandbox",
                            "--disable-blink-features=AutomationControlled",
                            "--disable-infobars",
                            "--disable-dev-shm-usage",
                        ],
                    )
                    ctx = browser.new_context(
                        user_agent=user_agent,
                        locale="ru-RU",
                        timezone_id="Europe/Moscow",
                        viewport={"width": 1280, "height": 800},
                        java_script_enabled=True,
                        # Передаём реальные параметры браузера
                        extra_http_headers={
                            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Upgrade-Insecure-Requests": "1",
                            "Sec-Fetch-Dest": "document",
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-Site": "none",
                            "Sec-Fetch-User": "?1",
                        },
                    )
                    page = ctx.new_page()

                    # Скрываем признаки автоматизации через JS
                    page.add_init_script("""
                        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
                        Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU','ru','en-US','en']});
                        window.chrome = {runtime: {}};
                    """)

                    # Применяем playwright-stealth если установлен
                    try:
                        from playwright_stealth import stealth_sync
                        stealth_sync(page)
                        logger.info("Stealth-режим активирован")
                    except ImportError:
                        logger.warning("playwright-stealth не установлен, работаем без него")

                    page.goto(url, wait_until="networkidle", timeout=40000)

                    # Имитируем поведение человека
                    time.sleep(random.uniform(1.5, 3.0))
                    page.mouse.move(random.randint(200, 800), random.randint(200, 500))
                    time.sleep(random.uniform(0.5, 1.5))

                    if wait_selector:
                        try:
                            page.wait_for_selector(wait_selector, timeout=12000)
                        except Exception:
                            logger.warning(f"Селектор '{wait_selector}' не найден на {url}")

                    page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
                    time.sleep(random.uniform(1.0, 2.0))
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight * 2 / 3)")
                    time.sleep(random.uniform(0.8, 1.5))
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(1.0)

                    result[0] = page.content()
                    browser.close()
            except Exception as e:
                exc[0] = e

        import threading
        t = threading.Thread(target=_run, daemon=True)
        t.start()
        t.join(timeout=60)

        if exc[0]:
            self.logger.error(f"Ошибка загрузки {url}: {exc[0]}")
            return None
        if not result[0]:
            self.logger.error(f"Пустой ответ от {url}")
            return None

        time.sleep(delay)
        return BeautifulSoup(result[0], "html.parser")

    def parse_category(self, category: str) -> list[dict]:
        raise NotImplementedError

    @staticmethod
    def clean_price(text: str) -> float:
        """Извлечь число из строки цены '1 299 ₽' → 1299.0"""
        if not text:
            return 0.0
        digits = "".join(c for c in text if c.isdigit())
        return float(digits) if digits else 0.0

    @staticmethod
    def clean_rating(text: str) -> float:
        """Извлечь рейтинг из строки '4.5' или '4,5'"""
        if not text:
            return 0.0
        text = text.strip().replace(",", ".")
        try:
            val = float("".join(c for c in text if c.isdigit() or c == "."))
            return round(min(val, 5.0), 1)
        except Exception:
            return 0.0

    @staticmethod
    def clean_reviews(text: str) -> int:
        """Извлечь количество отзывов из строки '(123 отзыва)' → 123"""
        if not text:
            return 0
        digits = "".join(c for c in text if c.isdigit())
        return int(digits) if digits else 0
