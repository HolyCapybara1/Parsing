import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)


def setup_logger(name: str) -> logging.Logger:
    """Настроить логгер с выводом в файл и консоль."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    today = datetime.now().strftime("%Y-%m-%d")
    fh = logging.FileHandler(f"logs/scraper_{today}.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def setup_all_loggers():
    """Настроить логгеры для всех модулей."""
    for name in ["runner", "DNS", "Ситилинк", "Regard", "analytics", "ml"]:
        setup_logger(name)
