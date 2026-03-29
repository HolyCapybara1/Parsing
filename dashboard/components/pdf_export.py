"""
Утилита экспорта графиков в PDF.
Требует: pip install kaleido fpdf2
"""
import io
from typing import List, Tuple
import plotly.graph_objects as go


def export_to_pdf(charts: List[Tuple[str, go.Figure]]) -> bytes | None:
    """
    Конвертирует список графиков в PDF.

    :param charts: список кортежей (заголовок, Figure)
    :return: байты PDF или None если не удалось
    """
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    try:
        pdf = FPDF(orientation="L", format="A4")
        pdf.set_auto_page_break(auto=False)

        for title, fig in charts:
            if fig is None:
                continue

            # Рендерим график как PNG
            try:
                img_bytes = fig.to_image(format="png", width=1100, height=560, scale=1.5)
            except Exception:
                continue

            pdf.add_page()

            # Заголовок раздела (латиница — fpdf без доп. шрифта не поддерживает кириллицу)
            pdf.set_font("Helvetica", "B", 12)
            safe_title = _to_ascii(title)
            pdf.set_xy(10, 5)
            pdf.cell(0, 8, safe_title, align="C")

            # Вставляем изображение
            pdf.image(io.BytesIO(img_bytes), x=5, y=14, w=285, h=178)

        return bytes(pdf.output())

    except Exception:
        return None


def _to_ascii(text: str) -> str:
    """Транслитерация для PDF-заголовков (fpdf без встроенного шрифта не рендерит кириллицу)."""
    mapping = {
        "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Е": "E", "Ё": "Yo",
        "Ж": "Zh", "З": "Z", "И": "I", "Й": "Y", "К": "K", "Л": "L", "М": "M",
        "Н": "N", "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T", "У": "U",
        "Ф": "F", "Х": "Kh", "Ц": "Ts", "Ч": "Ch", "Ш": "Sh", "Щ": "Sch",
        "Ъ": "", "Ы": "Y", "Ь": "", "Э": "E", "Ю": "Yu", "Я": "Ya",
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
    return "".join(mapping.get(c, c) for c in text)
