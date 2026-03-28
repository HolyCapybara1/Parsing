import requests
from bs4 import BeautifulSoup
import time
import logging


class BaseParser:
    """Базовый класс для всех парсеров магазинов."""

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    DELAY = 1.5   # секунд между запросами

    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.logger = logging.getLogger(source_name)

    def get_page(self, url: str) -> BeautifulSoup | None:
        """Загрузить страницу с повторными попытками (3 раза)."""
        for attempt in range(3):
            try:
                response = requests.get(url, headers=self.HEADERS, timeout=15)
                response.raise_for_status()
                time.sleep(self.DELAY)
                return BeautifulSoup(response.text, "html.parser")
            except Exception as e:
                self.logger.warning(f"Попытка {attempt + 1} не удалась для {url}: {e}")
                time.sleep(3 * (attempt + 1))
        self.logger.error(f"Не удалось загрузить страницу: {url}")
        return None

    def parse_category(self, category: str) -> list[dict]:
        """Переопределить в каждом парсере."""
        raise NotImplementedError
