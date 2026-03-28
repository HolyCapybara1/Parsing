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
        """Загрузить страницу через Playwright (рендерит JS)."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.logger.error("Playwright не установлен. Выполните: pip install playwright && playwright install chromium")
            return None

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
                ctx = browser.new_context(
                    user_agent=self.USER_AGENT,
                    locale="ru-RU",
                    viewport={"width": 1280, "height": 800},
                )
                page = ctx.new_page()
                page.set_extra_http_headers({
                    "Accept-Language": "ru-RU,ru;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                })

                page.goto(url, wait_until="domcontentloaded", timeout=30000)

                if wait_selector:
                    try:
                        page.wait_for_selector(wait_selector, timeout=12000)
                    except Exception:
                        self.logger.warning(f"Селектор '{wait_selector}' не найден на {url}")

                # Прокрутка для ленивой загрузки
                page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                time.sleep(1.5)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1.0)

                content = page.content()
                browser.close()

            time.sleep(self.DELAY)
            return BeautifulSoup(content, "html.parser")

        except Exception as e:
            self.logger.error(f"Ошибка загрузки {url}: {e}")
            return None

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
