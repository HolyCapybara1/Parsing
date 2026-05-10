"""
Генератор отчёта по бэкенду системы ЦенМонитор.
Формат: СТО ЮУрГУ 21-2008
"""

from docx import Document
from docx.shared import Pt, Cm, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ─── Параметры страницы ──────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width    = Mm(210)
section.page_height   = Mm(297)
section.top_margin    = Mm(20)
section.bottom_margin = Mm(26)
section.left_margin   = Mm(25)
section.right_margin  = Mm(10)

# ─── Вспомогательные функции ─────────────────────────────────────────────────

def set_base_font(run, size=14, bold=False):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)

def para_fmt(para, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
             indent_cm=0.7, space_before=0, space_after=0):
    pf = para.paragraph_format
    pf.alignment = align
    pf.first_line_indent = Cm(indent_cm) if indent_cm else None
    pf.space_before = Pt(space_before)
    pf.space_after  = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

def add_text(para, text, size=14, bold=False):
    run = para.add_run(text)
    set_base_font(run, size, bold)
    return run

def new_para(text='', align=WD_ALIGN_PARAGRAPH.JUSTIFY,
             indent=0.7, size=14, bold=False,
             space_before=0, space_after=0):
    p = doc.add_paragraph()
    para_fmt(p, align, indent, space_before, space_after)
    if text:
        add_text(p, text, size, bold)
    return p

def heading1(text, num):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 12, 6)
    add_text(p, f'{num} {text.upper()}', 14)
    return p

def heading2(text, num):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 6, 3)
    add_text(p, f'{num} {text}', 14)
    return p

def heading3(text, num):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 4, 2)
    add_text(p, f'{num} {text}', 14)
    return p

def add_code(lines):
    for line in lines:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.first_line_indent = Cm(0)
        pf.space_before = Pt(0)
        pf.space_after  = Pt(0)
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        run = p.add_run(line if line else ' ')
        run.font.name = 'Courier New'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0, 0, 0)

def listing_caption(text):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 4, 2)
    add_text(p, text, 14)
    return p

def fig_caption(text):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 4, 6)
    add_text(p, text, 14)
    return p

def tbl_caption(text):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 6, 2)
    add_text(p, text, 14)
    return p

def set_cell(cell, text, size=12, bold=False,
             align=WD_ALIGN_PARAGRAPH.LEFT, bg=None):
    cell.text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.alignment = align
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(1)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    if bg:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), bg)
        tcPr.append(shd)

def page_break():
    doc.add_page_break()

def add_footer_page_numbers():
    for sec in doc.sections:
        footer = sec.footer
        footer.is_linked_to_previous = False
        p = (footer.paragraphs[0]
             if footer.paragraphs else footer.add_paragraph())
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.clear()
        run = p.add_run()
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        for tag, text in [('begin', ''), ('', 'PAGE'), ('end', '')]:
            if tag in ('begin', 'end'):
                el = OxmlElement('w:fldChar')
                el.set(qn('w:fldCharType'), tag)
                run._r.append(el)
            else:
                el = OxmlElement('w:instrText')
                el.text = text
                run._r.append(el)

# ═══════════════════════════════════════════════════════════════════════════════
# ТИТУЛЬНЫЙ ЛИСТ
# ═══════════════════════════════════════════════════════════════════════════════

for text, size, sb, sa in [
    ('МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ', 12, 0, 4),
    ('Федеральное государственное автономное образовательное учреждение\nвысшего образования', 12, 0, 0),
    ('«ЮЖНО-УРАЛЬСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ»\n(национальный исследовательский университет)', 12, 0, 4),
    ('Высшая школа экономики и управления', 12, 0, 0),
    ('Кафедра «Экономика и экономическая безопасность»', 12, 0, 30),
]:
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, sb, sa)
    add_text(p, text, size)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 4)
add_text(p, 'ОТЧЁТ', 16)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 4)
add_text(p, 'по дисциплине «Информационные технологии»', 14)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 30)
add_text(p, 'Тема: Описание бэкенда системы мониторинга цен конкурентов\n«ЦенМонитор»', 14)

for _ in range(5):
    doc.add_paragraph()

for line in ['Выполнили: студенты группы ЭУ-430',
             'Головчиц И.А., Вахрушев Е.С.',
             'Проверил: ________________']:
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.RIGHT, 0, 0, 0)
    add_text(p, line, 12)

for _ in range(7):
    doc.add_paragraph()

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 0)
add_text(p, 'Челябинск 2026', 12)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# ОГЛАВЛЕНИЕ
# ═══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 10)
add_text(p, 'ОГЛАВЛЕНИЕ', 14)

toc = [
    ('Введение', '3'),
    ('1 Общая архитектура системы', '4'),
    ('1.1 Структура модулей', '4'),
    ('1.2 Технологический стек', '5'),
    ('2 Модуль парсинга', '6'),
    ('2.1 Базовый класс BaseParser', '6'),
    ('2.2 Парсер интернет-магазина DNS', '9'),
    ('2.3 Парсер интернет-магазина Ситилинк', '13'),
    ('2.4 Парсер интернет-магазина Regard', '17'),
    ('2.5 Модуль запуска парсинга runner', '21'),
    ('3 Методы обхода антифрод-систем', '23'),
    ('3.1 Общие методы противодействия', '23'),
    ('3.2 Обход защиты DNS', '25'),
    ('3.3 Обход защиты Ситилинк', '26'),
    ('3.4 Обход защиты Regard', '27'),
    ('4 Модуль базы данных', '28'),
    ('4.1 ORM-модели SQLAlchemy', '28'),
    ('4.2 Репозиторий данных', '30'),
    ('5 Аналитический модуль', '33'),
    ('6 Модуль машинного обучения', '35'),
    ('6.1 Кластеризация методом KMeans', '35'),
    ('6.2 Классификатор Random Forest', '38'),
    ('7 Модуль логирования', '40'),
    ('Заключение', '41'),
    ('Список использованных источников', '42'),
]

for title, page in toc:
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 0, 0)
    dots = '.' * max(2, 68 - len(title) - len(page))
    add_text(p, f'{title} {dots} {page}', 14)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# ВВЕДЕНИЕ
# ═══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 10)
add_text(p, 'ВВЕДЕНИЕ', 14)

new_para(
    'Настоящий отчёт посвящён описанию серверной части (бэкенда) '
    'автоматизированной системы мониторинга цен конкурентов «ЦенМонитор», '
    'разработанной в рамках учебной дисциплины. Система предназначена для '
    'автоматического сбора, хранения и анализа ценовой информации с трёх '
    'крупных российских интернет-магазинов электроники: DNS, Ситилинк и Regard.'
)
new_para(
    'Актуальность темы обусловлена высокой конкуренцией на рынке электронной '
    'коммерции, где цены на товары могут изменяться несколько раз в сутки. '
    'Ручной мониторинг в таких условиях практически невозможен, что '
    'обусловливает потребность в автоматизированных инструментах сбора данных '
    'с последующей аналитикой и визуализацией результатов.'
)
new_para(
    'Бэкенд реализован на языке Python 3.11 и состоит из четырёх '
    'функционально независимых модулей: парсинга (scraper), базы данных (db), '
    'аналитики (analytics) и машинного обучения (ml). Отдельное внимание в '
    'отчёте уделено методам обхода антифрод-систем каждого из трёх магазинов, '
    'поскольку современные интернет-магазины применяют многоуровневую защиту '
    'от автоматического сбора данных.'
)
new_para(
    'Целью отчёта является подробное описание архитектурных решений, '
    'используемых технологий и программного кода каждого модуля с обоснованием '
    'принятых проектных решений.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 1 — АРХИТЕКТУРА
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Общая архитектура системы', '1')

heading2('Структура модулей', '1.1')

new_para(
    'Система «ЦенМонитор» построена по принципу многоуровневой архитектуры, '
    'в которой каждый слой отвечает за строго определённые функции. '
    'Подобный подход обеспечивает независимость компонентов и упрощает '
    'сопровождение кода. Структура бэкенда представлена в таблице 1.'
)

tbl_caption('Таблица 1 – Структура модулей бэкенда')
t = doc.add_table(rows=5, cols=3)
t.style = 'Table Grid'
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Модуль', 'Папка', 'Назначение']):
    set_cell(t.rows[0].cells[i], h, bold=True,
             align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
for i, row in enumerate([
    ('Парсинг',           'scraper/', 'Автоматический сбор данных с сайтов через управляемый браузер'),
    ('База данных',       'db/',      'ORM-модели, CRUD-операции, аналитические выборки'),
    ('Аналитика',         'analytics/', 'Ценовой индекс, динамика цен, рейтинги, сводные таблицы'),
    ('Машинное обучение', 'ml/',      'KMeans-кластеризация и Random Forest-классификация товаров'),
]):
    for j, v in enumerate(row):
        set_cell(t.rows[i+1].cells[j], v)

new_para('')
new_para(
    'Взаимодействие модулей осуществляется следующим образом: модуль парсинга '
    'записывает собранные данные через репозиторий базы данных. Аналитический '
    'модуль и модуль машинного обучения читают данные из той же базы. '
    'Веб-дашборд (frontend) обращается ко всем модулям бэкенда посредством '
    'вызовов функций репозитория, аналитики и ML-предиктора.'
)

heading2('Технологический стек', '1.2')

new_para(
    'При выборе технологий приоритет отдавался зрелым, широко поддерживаемым '
    'библиотекам. Полный перечень используемых инструментов приведён в таблице 2.'
)

tbl_caption('Таблица 2 – Технологический стек бэкенда')
t2 = doc.add_table(rows=10, cols=3)
t2.style = 'Table Grid'
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Библиотека', 'Версия', 'Назначение']):
    set_cell(t2.rows[0].cells[i], h, bold=True,
             align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
for i, row in enumerate([
    ('playwright',    '≥ 1.44', 'Управление браузером Chromium для рендеринга JavaScript-страниц'),
    ('beautifulsoup4','≥ 4.12', 'Парсинг HTML-документов с помощью CSS-селекторов'),
    ('lxml',          '≥ 4.9',  'Высокопроизводительный HTML-парсер для BeautifulSoup'),
    ('sqlalchemy',    '≥ 2.0',  'ORM-фреймворк для работы с реляционными базами данных'),
    ('pandas',        '≥ 2.1',  'Табличная обработка данных, аналитические агрегации'),
    ('numpy',         '≥ 1.26', 'Векторные вычисления, нормализация признаков для ML'),
    ('scikit-learn',  '≥ 1.4',  'Алгоритмы ML: KMeans, RandomForest, кросс-валидация, метрики'),
    ('joblib',        '≥ 1.3',  'Сериализация и загрузка обученных ML-моделей с диска'),
    ('streamlit',     '≥ 1.32', 'Веб-фреймворк интерактивного дашборда (frontend)'),
]):
    for j, v in enumerate(row):
        set_cell(t2.rows[i+1].cells[j], v,
                 align=WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT)

new_para('')
new_para(
    'В качестве базы данных используется SQLite — встраиваемая реляционная СУБД, '
    'не требующая отдельного серверного процесса. Выбор обусловлен учебным '
    'характером проекта: SQLite обеспечивает все необходимые реляционные '
    'возможности при минимальных накладных расходах на администрирование.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 2 — МОДУЛЬ ПАРСИНГА
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Модуль парсинга', '2')

# ── 2.1 BaseParser ────────────────────────────────────────────────────────────

heading2('Базовый класс BaseParser', '2.1')

new_para(
    'Все три парсера магазинов наследуются от единого абстрактного класса '
    'BaseParser, определённого в файле scraper/base.py. Базовый класс '
    'инкапсулирует логику загрузки веб-страниц и утилитарные методы очистки '
    'данных, что исключает дублирование кода в дочерних классах.'
)
new_para(
    'Для загрузки страниц применяется библиотека Playwright, а не стандартный '
    'модуль requests. Причина состоит в том, что каталоги всех трёх магазинов '
    'строятся с использованием JavaScript-фреймворков, поэтому обычный '
    'HTTP-запрос возвращает пустой HTML-шаблон без товаров. Playwright '
    'запускает полноценный браузер Chromium, исполняющий JavaScript и '
    'формирующий финальный DOM-дерево, пригодное для парсинга.'
)

listing_caption('Листинг 1 – Базовый класс парсера (файл scraper/base.py)')
add_code([
    'import logging',
    'import time',
    'from bs4 import BeautifulSoup',
    '',
    '',
    'class BaseParser:',
    '    """Базовый класс. Использует Playwright для рендеринга JS."""',
    '',
    '    USER_AGENT = (',
    '        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "',
    '        "AppleWebKit/537.36 (KHTML, like Gecko) "',
    '        "Chrome/124.0.0.0 Safari/537.36"',
    '    )',
    '    DELAY = 2.0  # пауза в секундах между запросами страниц',
    '',
    '    def __init__(self, source_name: str, base_url: str):',
    '        self.source_name = source_name',
    '        self.base_url    = base_url',
    '        self.logger      = logging.getLogger(source_name)',
    '',
    '    def get_page(self, url: str,',
    '                 wait_selector: str = None) -> BeautifulSoup | None:',
    '        """Загрузить страницу через Playwright (рендерит JS)."""',
    '        try:',
    '            from playwright.sync_api import sync_playwright',
    '        except ImportError:',
    '            self.logger.error("Playwright не установлен.")',
    '            return None',
    '        try:',
    '            with sync_playwright() as p:',
    '                browser = p.chromium.launch(',
    '                    headless=True, args=["--no-sandbox"])',
    '                ctx = browser.new_context(',
    '                    user_agent=self.USER_AGENT,',
    '                    locale="ru-RU",',
    '                    viewport={"width": 1280, "height": 800},',
    '                )',
    '                page = ctx.new_page()',
    '                page.set_extra_http_headers({',
    '                    "Accept-Language": "ru-RU,ru;q=0.9",',
    '                    "Accept": "text/html,application/xhtml+xml,'
    'application/xml;q=0.9,*/*;q=0.8",',
    '                })',
    '                page.goto(url, wait_until="domcontentloaded",',
    '                          timeout=30000)',
    '                if wait_selector:',
    '                    try:',
    '                        page.wait_for_selector(',
    '                            wait_selector, timeout=12000)',
    '                    except Exception:',
    '                        self.logger.warning(',
    '                            f"Селектор не найден: {url}")',
    '                # Прокрутка для активации lazy-loading',
    '                page.evaluate(',
    '                    "window.scrollTo(0, document.body.scrollHeight / 2)")',
    '                time.sleep(1.5)',
    '                page.evaluate(',
    '                    "window.scrollTo(0, document.body.scrollHeight)")',
    '                time.sleep(1.0)',
    '                content = page.content()',
    '                browser.close()',
    '            time.sleep(self.DELAY)',
    '            return BeautifulSoup(content, "html.parser")',
    '        except Exception as e:',
    '            self.logger.error(f"Ошибка загрузки {url}: {e}")',
    '            return None',
    '',
    '    def parse_category(self, category: str) -> list[dict]:',
    '        raise NotImplementedError',
    '',
    '    @staticmethod',
    '    def clean_price(text: str) -> float:',
    '        """Извлечь число из строки типа \'1 299 руб.\' -> 1299.0"""',
    '        if not text:',
    '            return 0.0',
    '        digits = "".join(c for c in text if c.isdigit())',
    '        return float(digits) if digits else 0.0',
    '',
    '    @staticmethod',
    '    def clean_rating(text: str) -> float:',
    '        """Извлечь рейтинг из строки \'4.5\' или \'4,5\'"""',
    '        if not text:',
    '            return 0.0',
    '        text = text.strip().replace(",", ".")',
    '        try:',
    '            val = float("".join(',
    '                c for c in text if c.isdigit() or c == "."))',
    '            return round(min(val, 5.0), 1)',
    '        except Exception:',
    '            return 0.0',
    '',
    '    @staticmethod',
    '    def clean_reviews(text: str) -> int:',
    '        """Извлечь количество отзывов из строки \'(123 отзыва)\' -> 123"""',
    '        if not text:',
    '            return 0',
    '        digits = "".join(c for c in text if c.isdigit())',
    '        return int(digits) if digits else 0',
])

new_para(
    'Методы clean_price(), clean_rating() и clean_reviews() реализуют '
    'защитное программирование: при передаче пустой строки или None они '
    'возвращают нулевое значение, а не вызывают исключение. Это важно, '
    'поскольку структура HTML-страниц магазинов нестабильна и отдельные '
    'поля могут отсутствовать для части товаров.'
)

page_break()

# ── 2.2 DNS ───────────────────────────────────────────────────────────────────

heading2('Парсер интернет-магазина DNS', '2.2')

new_para(
    'Парсер DNS реализован в классе DnsParser (файл scraper/dns_parser.py). '
    'Сайт DNS использует серверный рендеринг (SSR) с частичной гидратацией '
    'JavaScript, что делает его HTML-структуру относительно стабильной '
    'по сравнению с полностью клиентскими React-приложениями.'
)

listing_caption('Листинг 2 – Полный код парсера DNS (файл scraper/dns_parser.py)')
add_code([
    'from .base import BaseParser',
    '',
    '# Соответствие категорий реальным URL-путям каталога DNS',
    'CATEGORIES = {',
    '    "Оперативная память": "/catalog/operativnaya-pamyat/",',
    '    "Видеокарты":         "/catalog/videokarty/",',
    '    "Смартфоны":          "/catalog/smartfony/",',
    '    "Процессоры":         "/catalog/processory/",',
    '    "Ноутбуки":           "/catalog/noutbuki/",',
    '    "SSD-накопители":     "/catalog/ssd-nakopiteli/",',
    '    "Наушники":           "/catalog/naushniki-vkladyshi/",',
    '}',
    '',
    '',
    'class DnsParser(BaseParser):',
    '    def __init__(self):',
    '        super().__init__("DNS", "https://www.dns-shop.ru")',
    '',
    '    def parse_category(self, category: str) -> list[dict]:',
    '        path = CATEGORIES.get(category)',
    '        if not path:',
    '            self.logger.warning(',
    '                f"DNS: категория \'{category}\' не найдена")',
    '            return []',
    '',
    '        products = []',
    '        for page_num in range(1, 6):  # обходим до 5 страниц пагинации',
    '            url = f"{self.base_url}{path}?p={page_num}"',
    '            self.logger.info(',
    '                f"DNS {category}: страница {page_num} — {url}")',
    '',
    '            # wait_selector — ждём появления карточек перед снятием HTML',
    '            soup = self.get_page(',
    '                url, wait_selector=".catalog-product")',
    '            if not soup:',
    '                break',
    '',
    '            items = soup.select(".catalog-product")',
    '            if not items:',
    '                self.logger.info(',
    '                    f"DNS {category}: стр.{page_num} пустая — стоп")',
    '                break',
    '',
    '            for item in items:',
    '                try:',
    '                    # ── Название ──────────────────────────────────',
    '                    name_tag = (',
    '                        item.select_one("a.catalog-product__name") or',
    '                        item.select_one(".catalog-product__name")',
    '                    )',
    '                    if not name_tag:',
    '                        continue',
    '                    name = name_tag.get_text(strip=True)',
    '                    if not name:',
    '                        continue',
    '',
    '                    # ── Ссылка на товар ───────────────────────────',
    '                    href = name_tag.get("href", "")',
    '                    item_url = (',
    '                        self.base_url + href',
    '                        if href.startswith("/") else href',
    '                    )',
    '',
    '                    # ── Цена — три варианта CSS-класса ────────────',
    '                    price_tag = (',
    '                        item.select_one(".product-buy__price") or',
    '                        item.select_one("[class*=\'price_current\']") or',
    '                        item.select_one("[class*=\'price-current\']")',
    '                    )',
    '                    price = self.clean_price(',
    '                        price_tag.get_text() if price_tag else "")',
    '                    if price <= 0:',
    '                        continue',
    '',
    '                    # ── Рейтинг ───────────────────────────────────',
    '                    rating_tag = (',
    '                        item.select_one(',
    '                            ".product-item__rating-count") or',
    '                        item.select_one("[class*=\'rating\']")',
    '                    )',
    '                    rating = self.clean_rating(',
    '                        rating_tag.get_text() if rating_tag else "")',
    '',
    '                    # ── Отзывы ────────────────────────────────────',
    '                    reviews_tag = (',
    '                        item.select_one(',
    '                            ".product-item__reviews-count") or',
    '                        item.select_one("[class*=\'reviews\']")',
    '                    )',
    '                    reviews = self.clean_reviews(',
    '                        reviews_tag.get_text() if reviews_tag else "")',
    '',
    '                    # Бренд — первое слово названия товара',
    '                    brand = name.split()[0] if name else ""',
    '',
    '                    products.append({',
    '                        "name":          name,',
    '                        "brand":         brand,',
    '                        "category":      category,',
    '                        "price":         price,',
    '                        "rating":        rating,',
    '                        "reviews_count": reviews,',
    '                        "url":           item_url,',
    '                        "source":        "DNS",',
    '                    })',
    '                except Exception as e:',
    '                    self.logger.error(',
    '                        f"DNS: ошибка товара: {e}")',
    '',
    '            self.logger.info(',
    '                f"DNS {category}: стр.{page_num} — {len(items)} карточек")',
    '',
    '            # Проверяем наличие кнопки следующей страницы',
    '            next_btn = soup.select_one(',
    '                "a.pagination-widget__page-link[rel=\'next\']")',
    '            if not next_btn:',
    '                break',
    '',
    '        self.logger.info(',
    '            f"DNS {category}: итого {len(products)} товаров")',
    '        return products',
])

new_para(
    'Ключевой приём в парсере DNS — использование цепочки запасных '
    'CSS-селекторов через оператор or. Если DNS обновит вёрстку и '
    'основной класс изменится, парсер попробует альтернативный вариант '
    'вместо аварийного завершения. Для цены предусмотрены три варианта: '
    '.product-buy__price, [class*=\'price_current\'] и [class*=\'price-current\']. '
    'Атрибутный селектор [class*=\'...\'] выполняет поиск по частичному '
    'вхождению подстроки в значение атрибута class.'
)

page_break()

# ── 2.3 Citilink ──────────────────────────────────────────────────────────────

heading2('Парсер интернет-магазина Ситилинк', '2.3')

new_para(
    'Парсер Ситилинк реализован в классе CitilinkParser '
    '(файл scraper/citilink_parser.py). Ситилинк использует '
    'полноценное React-приложение — весь каталог рендерится на стороне '
    'клиента. Главная особенность защиты: CSS-классы компонентов содержат '
    'автогенерируемые хэш-суффиксы (например, ProductCard_root__3kX9a), '
    'которые изменяются при каждом деплое сайта, что делает точные '
    'CSS-селекторы нестабильными.'
)

listing_caption('Листинг 3 – Полный код парсера Ситилинк (файл scraper/citilink_parser.py)')
add_code([
    'from .base import BaseParser',
    '',
    '# URL-пути каталога Ситилинк',
    'CATEGORIES = {',
    '    "Оперативная память": "/catalog/moduli-pamyati/",',
    '    "Видеокарты":         "/catalog/videokarty/",',
    '    "Смартфоны":          "/catalog/smartfony/",',
    '    "Процессоры":         "/catalog/processory/",',
    '    "Ноутбуки":           "/catalog/noutbuki/",',
    '    "SSD-накопители":     "/catalog/ssd-nakopiteli/",',
    '    "Наушники":           "/catalog/naushniki/",',
    '}',
    '',
    '',
    'class CitilinkParser(BaseParser):',
    '    def __init__(self):',
    '        super().__init__("Ситилинк", "https://www.citilink.ru")',
    '',
    '    def parse_category(self, category: str) -> list[dict]:',
    '        path = CATEGORIES.get(category)',
    '        if not path:',
    '            self.logger.warning(',
    '                f"Ситилинк: категория \'{category}\' не найдена")',
    '            return []',
    '',
    '        products = []',
    '        for page_num in range(1, 6):',
    '            url = f"{self.base_url}{path}?p={page_num}"',
    '            self.logger.info(',
    '                f"Ситилинк {category}: страница {page_num}")',
    '',
    '            # Ждём появления любого компонента с "ProductCard" в классе',
    '            soup = self.get_page(',
    '                url, wait_selector="[class*=\'ProductCard\']")',
    '            if not soup:',
    '                break',
    '',
    '            # Три варианта поиска карточек товаров:',
    '            # 1) по data-атрибуту (наиболее стабильный)',
    '            # 2) по article с частичным именем класса',
    '            # 3) по частичному имени корневого класса карточки',
    '            items = (',
    '                soup.select("[data-meta-product]") or',
    '                soup.select("article[class*=\'ProductCard\']") or',
    '                soup.select("[class*=\'ProductCard_root\']")',
    '            )',
    '            if not items:',
    '                self.logger.info(',
    '                    f"Ситилинк {category}: стр.{page_num} пустая")',
    '                break',
    '',
    '            for item in items:',
    '                try:',
    '                    # ── Название ──────────────────────────────────',
    '                    name_tag = (',
    '                        item.select_one(',
    '                            "[class*=\'ProductCard_title\']") or',
    '                        item.select_one("[class*=\'_title\']") or',
    '                        item.select_one("a[class*=\'title\']") or',
    '                        item.select_one("h3") or',
    '                        item.select_one("h2")',
    '                    )',
    '                    if not name_tag:',
    '                        continue',
    '                    name = name_tag.get_text(strip=True)',
    '                    if not name:',
    '                        continue',
    '',
    '                    # ── Ссылка ────────────────────────────────────',
    '                    link_tag = (',
    '                        item.select_one("a[href*=\'/product/\']") or',
    '                        item.select_one("a[href]")',
    '                    )',
    '                    href = link_tag.get("href", "") if link_tag else ""',
    '                    item_url = (',
    '                        self.base_url + href',
    '                        if href.startswith("/") else href',
    '                    )',
    '',
    '                    # ── Цена ──────────────────────────────────────',
    '                    price_tag = (',
    '                        item.select_one(',
    '                            "[class*=\'price__current\']") or',
    '                        item.select_one(',
    '                            "[class*=\'ProductCard_price\']") or',
    '                        item.select_one(',
    '                            "[class*=\'Price_price\']") or',
    '                        item.select_one("[class*=\'price\']")',
    '                    )',
    '                    price = self.clean_price(',
    '                        price_tag.get_text() if price_tag else "")',
    '                    if price <= 0:',
    '                        continue',
    '',
    '                    # ── Рейтинг: приоритет — aria-label ──────────',
    '                    # aria-label стабильнее визуальных классов,',
    '                    # задаётся разработчиком для вспомогательных',
    '                    # технологий и редко меняется при рефакторинге',
    '                    rating_tag = (',
    '                        item.select_one("[class*=\'Rating_\']") or',
    '                        item.select_one("[class*=\'rating\']")',
    '                    )',
    '                    rating = self.clean_rating(',
    '                        rating_tag.get("aria-label", "") or',
    '                        (rating_tag.get_text()',
    '                         if rating_tag else "")',
    '                    )',
    '',
    '                    # ── Отзывы ────────────────────────────────────',
    '                    reviews_tag = (',
    '                        item.select_one("[class*=\'review\']") or',
    '                        item.select_one("[class*=\'Review\']")',
    '                    )',
    '                    reviews = self.clean_reviews(',
    '                        reviews_tag.get_text() if reviews_tag else "")',
    '',
    '                    brand = name.split()[0] if name else ""',
    '',
    '                    products.append({',
    '                        "name":          name,',
    '                        "brand":         brand,',
    '                        "category":      category,',
    '                        "price":         price,',
    '                        "rating":        rating,',
    '                        "reviews_count": reviews,',
    '                        "url":           item_url,',
    '                        "source":        "Ситилинк",',
    '                    })',
    '                except Exception as e:',
    '                    self.logger.error(',
    '                        f"Ситилинк: ошибка товара: {e}")',
    '',
    '            self.logger.info(',
    '                f"Ситилинк {category}:'
    ' стр.{page_num} — {len(items)} карточек")',
    '',
    '            next_btn = (',
    '                soup.select_one("a[rel=\'next\']") or',
    '                soup.select_one(',
    '                    "[class*=\'pagination\'][class*=\'next\']")',
    '            )',
    '            if not next_btn:',
    '                break',
    '',
    '        self.logger.info(',
    '            f"Ситилинк {category}: итого {len(products)} товаров")',
    '        return products',
])

new_para(
    'Селектор [data-meta-product] является наиболее стабильным, поскольку '
    'data-атрибуты намеренно задаются разработчиком для семантической '
    'разметки и значительно реже меняются при рефакторинге вёрстки, '
    'чем генерируемые CSS-классы. Использование aria-label для получения '
    'рейтинга обусловлено тем, что значение атрибута задаётся для '
    'вспомогательных технологий и имеет предсказуемый формат: '
    '«Рейтинг: 4.7 из 5».'
)

page_break()

# ── 2.4 Regard ────────────────────────────────────────────────────────────────

heading2('Парсер интернет-магазина Regard', '2.4')

new_para(
    'Парсер Regard реализован в классе RegardParser '
    '(файл scraper/regard_parser.py). В отличие от DNS и Ситилинк, '
    'Regard использует числовые идентификаторы в URL-путях каталога '
    'вместо человекочитаемых названий категорий. '
    'Пагинация также отличается: параметр ?page=N вместо ?p=N, '
    'как у двух других магазинов.'
)

listing_caption('Листинг 4 – Полный код парсера Regard (файл scraper/regard_parser.py)')
add_code([
    'from .base import BaseParser',
    '',
    '# Regard использует числовые ID категорий в URL вместо slug\'ов',
    'CATEGORIES = {',
    '    "Оперативная память": "/catalog/18/",',
    '    "Видеокарты":         "/catalog/14/",',
    '    "Смартфоны":          "/catalog/516/",',
    '    "Процессоры":         "/catalog/4/",',
    '    "Ноутбуки":           "/catalog/53/",',
    '    "SSD-накопители":     "/catalog/1572/",',
    '    "Наушники":           "/catalog/614/",',
    '}',
    '',
    '',
    'class RegardParser(BaseParser):',
    '    def __init__(self):',
    '        super().__init__("Regard", "https://www.regard.ru")',
    '',
    '    def parse_category(self, category: str) -> list[dict]:',
    '        path = CATEGORIES.get(category)',
    '        if not path:',
    '            self.logger.warning(',
    '                f"Regard: категория \'{category}\' не найдена")',
    '            return []',
    '',
    '        products = []',
    '        for page_num in range(1, 6):',
    '            # Regard: параметр пагинации ?page=N (не ?p=N)',
    '            url = f"{self.base_url}{path}?page={page_num}"',
    '            self.logger.info(',
    '                f"Regard {category}: страница {page_num}")',
    '',
    '            soup = self.get_page(',
    '                url,',
    '                wait_selector=".b-product-card, .product-card")',
    '            if not soup:',
    '                break',
    '',
    '            # Два варианта CSS-класса карточки товара',
    '            items = (',
    '                soup.select(".b-product-card") or',
    '                soup.select(".product-card") or',
    '                soup.select("[class*=\'product-item\']")',
    '            )',
    '            if not items:',
    '                self.logger.info(',
    '                    f"Regard {category}: стр.{page_num} пустая")',
    '                break',
    '',
    '            for item in items:',
    '                try:',
    '                    # ── Название ──────────────────────────────────',
    '                    name_tag = (',
    '                        item.select_one(',
    '                            ".b-product-card__name a") or',
    '                        item.select_one(',
    '                            ".b-product-card__name") or',
    '                        item.select_one(',
    '                            ".product-card__name a") or',
    '                        item.select_one(',
    '                            ".product-card__name") or',
    '                        item.select_one("a[class*=\'name\']")',
    '                    )',
    '                    if not name_tag:',
    '                        continue',
    '                    name = name_tag.get_text(strip=True)',
    '                    if not name:',
    '                        continue',
    '',
    '                    # ── Ссылка ────────────────────────────────────',
    '                    link_tag = (',
    '                        name_tag if name_tag.name == "a"',
    '                        else item.select_one("a[href]")',
    '                    )',
    '                    href = link_tag.get("href", "") if link_tag else ""',
    '                    item_url = (',
    '                        self.base_url + href',
    '                        if href.startswith("/") else href',
    '                    )',
    '',
    '                    # ── Цена ──────────────────────────────────────',
    '                    price_tag = (',
    '                        item.select_one(',
    '                            ".b-product-card__buy-price") or',
    '                        item.select_one(",product-card__price") or',
    '                        item.select_one("[class*=\'price\']")',
    '                    )',
    '                    price = self.clean_price(',
    '                        price_tag.get_text() if price_tag else "")',
    '                    if price <= 0:',
    '                        continue',
    '',
    '                    # ── Рейтинг: извлечение из CSS-свойства width ─',
    '                    # Regard отображает звёзды через ширину элемента',
    '                    # в процентах: style="width: 80%" -> 4.0 из 5.0',
    '                    rating_tag = item.select_one("[class*=\'rating\']")',
    '                    rating_val = 0.0',
    '                    if rating_tag:',
    '                        style = rating_tag.get("style", "")',
    '                        if "width" in style:',
    '                            try:',
    '                                pct = float("".join(',
    '                                    c for c in style',
    '                                    if c.isdigit() or c == "."))',
    '                                # Формула: % / 20 = оценка (5-балл.)',
    '                                rating_val = round(pct / 20, 1)',
    '                            except Exception:',
    '                                pass',
    '                        else:',
    '                            rating_val = self.clean_rating(',
    '                                rating_tag.get_text())',
    '',
    '                    # ── Отзывы ────────────────────────────────────',
    '                    reviews_tag = (',
    '                        item.select_one("[class*=\'review\']") or',
    '                        item.select_one("[class*=\'comment\']")',
    '                    )',
    '                    reviews = self.clean_reviews(',
    '                        reviews_tag.get_text() if reviews_tag else "")',
    '',
    '                    brand = name.split()[0] if name else ""',
    '',
    '                    products.append({',
    '                        "name":          name,',
    '                        "brand":         brand,',
    '                        "category":      category,',
    '                        "price":         price,',
    '                        "rating":        rating_val,',
    '                        "reviews_count": reviews,',
    '                        "url":           item_url,',
    '                        "source":        "Regard",',
    '                    })',
    '                except Exception as e:',
    '                    self.logger.error(',
    '                        f"Regard: ошибка товара: {e}")',
    '',
    '            self.logger.info(',
    '                f"Regard {category}:'
    ' стр.{page_num} — {len(items)} карточек")',
    '',
    '            next_btn = (',
    '                soup.select_one("a[rel=\'next\']") or',
    '                soup.select_one(".pagination .next")',
    '            )',
    '            if not next_btn:',
    '                break',
    '',
    '        self.logger.info(',
    '            f"Regard {category}: итого {len(products)} товаров")',
    '        return products',
])

new_para(
    'Наиболее нестандартным решением в парсере Regard является извлечение '
    'рейтинга из CSS-свойства width. Магазин отображает звёзды рейтинга '
    'через ширину элемента в процентах (style="width: 80%"), а не через '
    'явное числовое значение в тексте. Формула преобразования: значение '
    'width делится на 20, переводя стопроцентную шкалу в пятибалльную. '
    'Примеры: 100 % → 5.0; 80 % → 4.0; 60 % → 3.0.'
)

page_break()

# ── 2.5 Runner ────────────────────────────────────────────────────────────────

heading2('Модуль запуска парсинга runner', '2.5')

new_para(
    'Модуль runner.py является оркестратором процесса сбора данных. '
    'Он инициализирует базу данных, создаёт запись о сеансе парсинга '
    '(Collection), последовательно запускает все активные парсеры '
    'по всем выбранным категориям и обновляет статус сеанса по завершении.'
)

listing_caption('Листинг 5 – Оркестратор парсинга (файл scraper/runner.py)')
add_code([
    'from .dns_parser      import DnsParser',
    'from .citilink_parser import CitilinkParser',
    'from .regard_parser   import RegardParser',
    'from db.repository import save_products, SessionLocal, init_db',
    'from db.models import Collection',
    'from datetime import datetime',
    'import logging',
    '',
    'logger = logging.getLogger("runner")',
    '',
    'ALL_CATEGORIES = [',
    '    "Оперативная память", "Видеокарты", "Смартфоны",',
    '    "Процессоры", "Ноутбуки", "SSD-накопители", "Наушники",',
    ']',
    'ALL_SOURCES = ["DNS", "Ситилинк", "Regard"]',
    '',
    '',
    'def run_all(categories: list[str] = None,',
    '            sources: list[str] = None) -> dict:',
    '    """',
    '    Запустить парсинг.',
    '    categories — список категорий (None = все)',
    '    sources    — список магазинов (None = все)',
    '    Возвращает словарь с итогами сбора.',
    '    """',
    '    init_db()',
    '',
    '    if categories is None:',
    '        categories = ALL_CATEGORIES',
    '    if sources is None:',
    '        sources = ALL_SOURCES',
    '',
    '    # Создать запись о сеансе в БД со статусом "running"',
    '    with SessionLocal() as session:',
    '        collection = Collection(',
    '            started_at=datetime.utcnow(), status="running")',
    '        session.add(collection)',
    '        session.commit()',
    '        cid = collection.id',
    '',
    '    all_parsers = {',
    '        "DNS":      DnsParser(),',
    '        "Ситилинк": CitilinkParser(),',
    '        "Regard":   RegardParser(),',
    '    }',
    '    active_parsers = [',
    '        p for name, p in all_parsers.items()',
    '        if name in sources',
    '    ]',
    '',
    '    total  = 0',
    '    errors = 0',
    '',
    '    for parser in active_parsers:',
    '        for category in categories:',
    '            try:',
    '                logger.info(',
    '                    f">>> {parser.source_name} — {category}")',
    '                products = parser.parse_category(category)',
    '                if products:',
    '                    save_products(',
    '                        products, parser.source_name, cid)',
    '                    total += len(products)',
    '                    logger.info(',
    '                        f"    Сохранено: {len(products)} товаров")',
    '                else:',
    '                    logger.warning(',
    '                        f"    Товары не найдены")',
    '            except Exception as e:',
    '                errors += 1',
    '                logger.error(',
    '                    f"Ошибка {parser.source_name}'
    ' {category}: {e}")',
    '',
    '    # Обновить статус сеанса по завершении',
    '    with SessionLocal() as session:',
    '        col = session.get(Collection, cid)',
    '        col.finished_at   = datetime.utcnow()',
    '        col.status        = "success" if errors == 0 else "partial"',
    '        col.total_records = total',
    '        session.commit()',
    '',
    '    logger.info(f"Готово: {total} товаров, {errors} ошибок")',
    '    return {',
    '        "total":      total,',
    '        "sources":    len(active_parsers),',
    '        "categories": len(categories),',
    '        "errors":     errors,',
    '    }',
    '',
    '',
    'if __name__ == "__main__":',
    '    import sys',
    '    sys.path.insert(0, ".")',
    '    from logger.logger import setup_all_loggers',
    '    setup_all_loggers()',
    '    result = run_all()',
    '    print(f"Готово: {result}")',
])

new_para(
    'Статус сеанса имеет три значения: "running" (запущен), "success" '
    '(завершён без ошибок) и "partial" (завершён с ошибками в отдельных '
    'категориях). Это позволяет в дашборде отображать историю сборов '
    'с диагностической информацией. Функция принимает опциональные '
    'параметры categories и sources — можно запускать парсинг выборочно, '
    'например только смартфоны из Ситилинк.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 3 — АНТИФРОД
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Методы обхода антифрод-систем', '3')

new_para(
    'Современные интернет-магазины применяют многоуровневую защиту от '
    'автоматического сбора данных. Каждый из трёх целевых магазинов '
    'использует собственный набор мер. В данном разделе описаны как общие '
    'методы противодействия, реализованные в базовом классе BaseParser, '
    'так и специфические приёмы, применённые для каждого магазина отдельно.'
)

# 3.1
heading2('Общие методы противодействия', '3.1')

new_para(
    'Общие методы обхода реализованы в методе get_page() базового класса '
    'и применяются ко всем трём магазинам. Сводная таблица приёмов '
    'представлена в таблице 3.'
)

tbl_caption('Таблица 3 – Общие методы обхода антифрод-систем')
af = doc.add_table(rows=8, cols=3)
af.style = 'Table Grid'
af.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Вид защиты магазина', 'Метод обхода', 'Реализация']):
    set_cell(af.rows[0].cells[i], h, bold=True,
             align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
for i, row in enumerate([
    ('Проверка User-Agent',
     'Реальный заголовок Chrome 124 / Win10',
     'USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."'),
    ('Блокировка HTTP-клиентов без JS',
     'Браузерный рендеринг через Playwright',
     'p.chromium.launch(headless=True)'),
    ('Проверка локали браузера',
     'Русская локаль и заголовок Accept-Language',
     'locale="ru-RU", Accept-Language: ru-RU,ru;q=0.9'),
    ('Нулевой или мобильный viewport',
     'Стандартный размер 1280×800 пикселей',
     'viewport={"width": 1280, "height": 800}'),
    ('Отсутствие взаимодействия с DOM',
     'Имитация прокрутки страницы',
     'page.evaluate("window.scrollTo(0, scrollHeight)")'),
    ('Rate limiting (ограничение частоты)',
     'Пауза 2 секунды между запросами',
     'DELAY = 2.0; time.sleep(self.DELAY)'),
    ('Ленивая загрузка карточек',
     'Двойная прокрутка с паузой 1.5 секунды',
     'scrollTo(scrollHeight / 2); sleep(1.5); scrollTo(scrollHeight)'),
]):
    for j, v in enumerate(row):
        set_cell(af.rows[i+1].cells[j], v)

new_para('')
new_para(
    'Использование Playwright вместо requests является принципиальным '
    'решением, покрывающим сразу несколько уровней защиты. Обычный '
    'HTTP-клиент отправляет запрос и получает исходный HTML, '
    'который для React/Vue-приложений содержит только пустой контейнер '
    '<div id="root"></div>. Playwright же запускает полный жизненный '
    'цикл браузера: загружает и исполняет JavaScript, ожидает монтирования '
    'компонентов и гидратации данных — после чего доступен '
    'полностью сформированный DOM со всеми карточками товаров.'
)
new_para(
    'Двойная прокрутка с паузой решает задачу активации lazy-loading. '
    'Большинство магазинов не загружают изображения и сами карточки '
    'товаров ниже видимой области экрана до тех пор, пока пользователь '
    'не прокрутит страницу к ним. Первая прокрутка до середины страницы '
    'активирует загрузку средней части, пауза в 1.5 секунды даёт время '
    'на загрузку, вторая прокрутка до конца страницы дозагружает '
    'оставшиеся элементы.'
)

page_break()

# 3.2
heading2('Обход защиты DNS', '3.2')

new_para(
    'DNS использует гибридный рендеринг: часть страниц генерируется '
    'на сервере (SSR), остальное догружается JavaScript. Это делает '
    'структуру HTML относительно стабильной, однако сайт применяет '
    'дополнительные меры защиты от парсинга.'
)

tbl_caption('Таблица 4 – Специфические методы обхода защиты DNS')
dns_af = doc.add_table(rows=5, cols=2)
dns_af.style = 'Table Grid'
dns_af.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Особенность защиты DNS', 'Применяемое решение']):
    set_cell(dns_af.rows[0].cells[i], h, bold=True,
             align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
for i, row in enumerate([
    ('CSS-классы цены имеют несколько вариантов написания в разных версиях сайта',
     'Цепочка из трёх селекторов: .product-buy__price, [class*=\'price_current\'], [class*=\'price-current\']'),
    ('Карточка товара .catalog-product может не появиться при медленной сети',
     'wait_for_selector(".catalog-product", timeout=12000) — ожидание до 12 секунд'),
    ('Кнопка следующей страницы имеет атрибут rel="next"',
     'Проверка наличия a[rel=\'next\'] — автоматическая остановка при отсутствии'),
    ('Блокировка по частоте запросов',
     'DELAY = 2.0 с между страницами + 1.5 с и 1.0 с паузы при прокрутке'),
]):
    for j, v in enumerate(row):
        set_cell(dns_af.rows[i+1].cells[j], v)

new_para('')
new_para(
    'Использование цепочки запасных селекторов для цены — ключевой приём '
    'устойчивости парсера DNS. Сайт несколько раз обновлял CSS-классы '
    'элемента с ценой, и именно наличие альтернативных вариантов '
    'позволяет парсеру работать без модификации при косметических '
    'изменениях вёрстки. Атрибутный селектор [class*=\'...\'] '
    'находит любой элемент, в значении атрибута class которого '
    'содержится заданная подстрока, независимо от других классов.'
)

# 3.3
heading2('Обход защиты Ситилинк', '3.3')

new_para(
    'Ситилинк является наиболее сложным объектом для парсинга из трёх '
    'магазинов: весь каталог построен на React с серверной генерацией '
    'автоматических хэш-суффиксов в CSS-классах компонентов. '
    'Это делает точные CSS-классы ненадёжными ориентирами.'
)

tbl_caption('Таблица 5 – Специфические методы обхода защиты Ситилинк')
cit_af = doc.add_table(rows=5, cols=2)
cit_af.style = 'Table Grid'
cit_af.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Особенность защиты Ситилинк', 'Применяемое решение']):
    set_cell(cit_af.rows[0].cells[i], h, bold=True,
             align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
for i, row in enumerate([
    ('CSS-классы компонентов содержат хэш-суффиксы, меняющиеся при каждом деплое',
     'Поиск по частичному вхождению: [class*=\'ProductCard\'], [class*=\'_title\'], [class*=\'price\']'),
    ('Весь каталог рендерится JavaScript, без него — пустая страница',
     'Playwright полностью воспроизводит жизненный цикл браузера и ждёт монтирования React-компонентов'),
    ('Адаптивная вёрстка: при малом viewport загружается мобильная версия с иными классами',
     'Фиксированный viewport 1280×800 гарантирует загрузку десктопной версии'),
    ('Рейтинг хранится в атрибуте aria-label, а не в видимом тексте',
     'rating_tag.get("aria-label", "") — чтение семантического атрибута, устойчивого к рефакторингу'),
]):
    for j, v in enumerate(row):
        set_cell(cit_af.rows[i+1].cells[j], v)

new_para('')
new_para(
    'Выбор data-атрибута [data-meta-product] как приоритетного селектора '
    'карточки обусловлен тем, что data-атрибуты назначаются разработчиком '
    'намеренно для семантической или аналитической разметки. Они не '
    'генерируются автоматически сборщиком (webpack/vite) и поэтому '
    'значительно реже изменяются при обновлении фронтенда, '
    'чем стилевые классы.'
)

# 3.4
heading2('Обход защиты Regard', '3.4')

new_para(
    'Regard использует более традиционную серверную вёрстку с '
    'предсказуемыми CSS-классами, однако имеет ряд нестандартных '
    'решений в интерфейсе, требующих специального подхода при парсинге.'
)

tbl_caption('Таблица 6 – Специфические методы обхода защиты Regard')
reg_af = doc.add_table(rows=5, cols=2)
reg_af.style = 'Table Grid'
reg_af.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Особенность защиты Regard', 'Применяемое решение']):
    set_cell(reg_af.rows[0].cells[i], h, bold=True,
             align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
for i, row in enumerate([
    ('URL категорий содержат числовые ID вместо slug\'ов (/catalog/14/ вместо /catalog/videokarty/)',
     'Словарь CATEGORIES с явным сопоставлением имён числовым идентификаторам'),
    ('Параметр пагинации ?page=N отличается от ?p=N, используемого DNS и Ситилинк',
     'url = f"{base_url}{path}?page={page_num}" — отдельный шаблон URL'),
    ('Рейтинг отображается через ширину CSS-элемента (style="width: 80%"), а не числом',
     'Извлечение числа из атрибута style, преобразование по формуле: % / 20 = оценка'),
    ('Ссылка на товар находится непосредственно в теге названия',
     'Проверка name_tag.name == "a" перед поиском отдельного тега ссылки'),
]):
    for j, v in enumerate(row):
        set_cell(reg_af.rows[i+1].cells[j], v)

new_para('')
new_para(
    'Преобразование рейтинга из CSS-ширины является наиболее нетривиальным '
    'приёмом в данном проекте. Сайт Regard отображает звёзды рейтинга '
    'как элемент фиксированной ширины, заполненный цветом на процент '
    'от максимума. При этом числовое значение рейтинга в HTML-разметке '
    'явно не присутствует. Код извлекает процентное число из строки '
    'атрибута style и делит на 20, поскольку 100 % = 5 баллов, '
    'что соответствует коэффициенту 1/20.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 4 — БАЗА ДАННЫХ
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Модуль базы данных', '4')

heading2('ORM-модели SQLAlchemy', '4.1')

new_para(
    'Схема базы данных определена в файле db/models.py с использованием '
    'декларативного стиля SQLAlchemy ORM. Схема состоит из пяти '
    'взаимосвязанных таблиц. Ключевым архитектурным решением является '
    'разделение товара и его цены на отдельные таблицы — один товар '
    'может иметь неограниченное количество записей Price, по одной '
    'на каждый сеанс парсинга, что обеспечивает полную историю '
    'изменения цен.'
)

listing_caption('Листинг 6 – ORM-модели базы данных (файл db/models.py)')
add_code([
    'from sqlalchemy import (',
    '    Column, Integer, String, Float,',
    '    DateTime, ForeignKey, Boolean)',
    'from sqlalchemy.orm import DeclarativeBase, relationship',
    'from datetime import datetime',
    '',
    '',
    'class Base(DeclarativeBase):',
    '    pass',
    '',
    '',
    'class Source(Base):',
    '    """Магазин-источник данных."""',
    '    __tablename__ = "sources"',
    '',
    '    id         = Column(Integer, primary_key=True)',
    '    name       = Column(String, nullable=False)   # DNS / Ситилинк / Regard',
    '    base_url   = Column(String, nullable=False)',
    '    is_active  = Column(Boolean, default=True)',
    '    created_at = Column(DateTime, default=datetime.utcnow)',
    '',
    '    products = relationship("Product", back_populates="source")',
    '',
    '',
    'class Product(Base):',
    '    """Товар (уникален в рамках одного источника)."""',
    '    __tablename__ = "products"',
    '',
    '    id         = Column(Integer, primary_key=True)',
    '    name       = Column(String, nullable=False)',
    '    brand      = Column(String)',
    '    category   = Column(String, nullable=False)',
    '    url        = Column(String)',
    '    source_id  = Column(Integer, ForeignKey("sources.id"))',
    '    created_at = Column(DateTime, default=datetime.utcnow)',
    '',
    '    source  = relationship("Source", back_populates="products")',
    '    prices  = relationship("Price", back_populates="product")',
    '    cluster = relationship(',
    '        "MLCluster", back_populates="product", uselist=False)',
    '',
    '',
    'class Price(Base):',
    '    """Запись о цене — создаётся при каждом сеансе парсинга."""',
    '    __tablename__ = "prices"',
    '',
    '    id            = Column(Integer, primary_key=True)',
    '    product_id    = Column(Integer, ForeignKey("products.id"))',
    '    price         = Column(Float, nullable=False)',
    '    rating        = Column(Float)',
    '    reviews_count = Column(Integer)',
    '    collected_at  = Column(DateTime, default=datetime.utcnow)',
    '    collection_id = Column(Integer, ForeignKey("collections.id"))',
    '',
    '    product = relationship("Product", back_populates="prices")',
    '',
    '',
    'class Collection(Base):',
    '    """Журнал сеансов парсинга."""',
    '    __tablename__ = "collections"',
    '',
    '    id            = Column(Integer, primary_key=True)',
    '    started_at    = Column(DateTime, default=datetime.utcnow)',
    '    finished_at   = Column(DateTime)',
    '    status        = Column(String)  # running | success | partial',
    '    total_records = Column(Integer, default=0)',
    '',
    '',
    'class MLCluster(Base):',
    '    """Результат ML-сегментации товара."""',
    '    __tablename__ = "ml_clusters"',
    '',
    '    id            = Column(Integer, primary_key=True)',
    '    product_id    = Column(Integer, ForeignKey("products.id"),',
    '                           unique=True)',
    '    segment       = Column(String)  # Бюджетный | Средний | Премиум',
    '    confidence    = Column(Float)',
    '    model_version = Column(String)',
    '    created_at    = Column(DateTime, default=datetime.utcnow)',
    '',
    '    product = relationship("Product", back_populates="cluster")',
])

page_break()

heading2('Репозиторий данных', '4.2')

listing_caption('Листинг 7 – Репозиторий базы данных (файл db/repository.py)')
add_code([
    'import os',
    'from sqlalchemy import create_engine, text',
    'from sqlalchemy.orm import sessionmaker',
    'import pandas as pd',
    'from .models import Base, Product, Price, Source, Collection, MLCluster',
    '',
    'os.makedirs("data", exist_ok=True)',
    'DATABASE_URL = "sqlite:///data/prices.db"',
    '',
    '# check_same_thread=False нужен для Streamlit:',
    '# он создаёт несколько потоков при обработке запросов',
    'engine = create_engine(',
    '    DATABASE_URL,',
    '    connect_args={"check_same_thread": False}',
    ')',
    'SessionLocal = sessionmaker(bind=engine)',
    '',
    '',
    'def init_db():',
    '    """Создать таблицы и заполнить справочник магазинов."""',
    '    Base.metadata.create_all(engine)',
    '    _seed_sources()',
    '',
    '',
    'def _seed_sources():',
    '    with SessionLocal() as session:',
    '        if session.query(Source).count() == 0:',
    '            session.add_all([',
    '                Source(name="DNS",',
    '                       base_url="https://www.dns-shop.ru"),',
    '                Source(name="Ситилинк",',
    '                       base_url="https://www.citilink.ru"),',
    '                Source(name="Regard",',
    '                       base_url="https://www.regard.ru"),',
    '            ])',
    '            session.commit()',
    '',
    '',
    'def save_products(products: list[dict],',
    '                  source_name: str,',
    '                  collection_id: int):',
    '    """Сохранить список товаров из парсера в БД."""',
    '    with SessionLocal() as session:',
    '        source = session.query(Source).filter_by(',
    '            name=source_name).first()',
    '        if not source:',
    '            return',
    '        for item in products:',
    '            # Найти или создать запись о товаре',
    '            product = session.query(Product).filter_by(',
    '                name=item["name"],',
    '                source_id=source.id',
    '            ).first()',
    '            if not product:',
    '                product = Product(',
    '                    name=item["name"],',
    '                    brand=item.get("brand", ""),',
    '                    category=item["category"],',
    '                    url=item.get("url", ""),',
    '                    source_id=source.id',
    '                )',
    '                session.add(product)',
    '                session.flush()  # получить product.id без commit',
    '',
    '            # Новая запись цены создаётся всегда',
    '            price = Price(',
    '                product_id=product.id,',
    '                price=item["price"],',
    '                rating=item.get("rating", 0.0),',
    '                reviews_count=item.get("reviews_count", 0),',
    '                collection_id=collection_id',
    '            )',
    '            session.add(price)',
    '        session.commit()',
    '',
    '',
    'def get_all_products() -> pd.DataFrame:',
    '    """Все товары с ПОСЛЕДНЕЙ ценой как DataFrame."""',
    '    query = """',
    '        SELECT p.id, p.name, p.brand, p.category,',
    '               s.name as source, pr.price, pr.rating,',
    '               pr.reviews_count, pr.collected_at,',
    '               mc.segment',
    '        FROM products p',
    '        JOIN sources s  ON p.source_id  = s.id',
    '        JOIN prices  pr ON pr.product_id = p.id',
    '        LEFT JOIN ml_clusters mc ON mc.product_id = p.id',
    '        WHERE pr.collected_at = (',
    '            SELECT MAX(collected_at) FROM prices',
    '            WHERE product_id = p.id)',
    '        ORDER BY pr.collected_at DESC',
    '    """',
    '    with engine.connect() as conn:',
    '        try:',
    '            return pd.read_sql(text(query), conn)',
    '        except Exception:',
    '            return pd.DataFrame()',
    '',
    '',
    'def get_price_history() -> pd.DataFrame:',
    '    """Вся история цен для временного графика."""',
    '    query = """',
    '        SELECT p.name, p.category, s.name as source,',
    '               pr.price, pr.collected_at',
    '        FROM prices pr',
    '        JOIN products p ON pr.product_id = p.id',
    '        JOIN sources  s ON p.source_id   = s.id',
    '        ORDER BY pr.collected_at',
    '    """',
    '    with engine.connect() as conn:',
    '        try:',
    '            return pd.read_sql(text(query), conn)',
    '        except Exception:',
    '            return pd.DataFrame()',
    '',
    '',
    'def get_collections() -> pd.DataFrame:',
    '    """История сеансов парсинга (последние 20)."""',
    '    query = """',
    '        SELECT id, started_at, finished_at,',
    '               status, total_records',
    '        FROM collections',
    '        ORDER BY started_at DESC',
    '        LIMIT 20',
    '    """',
    '    with engine.connect() as conn:',
    '        try:',
    '            return pd.read_sql(text(query), conn)',
    '        except Exception:',
    '            return pd.DataFrame()',
])

new_para(
    'SQL-запрос в функции get_all_products() использует коррелированный '
    'подзапрос для получения только последней записи цены каждого товара. '
    'Конструкция WHERE pr.collected_at = (SELECT MAX(collected_at) '
    'FROM prices WHERE product_id = p.id) фильтрует единственную строку '
    'с максимальной временной меткой для каждого product_id. '
    'Результат немедленно конвертируется в pandas.DataFrame через '
    'pd.read_sql(), что устраняет необходимость ручного преобразования '
    'ORM-объектов.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 5 — АНАЛИТИКА
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Аналитический модуль', '5')

new_para(
    'Аналитический модуль реализован в файле analytics/analytics.py '
    'и содержит пять чистых функций. Каждая принимает pandas.DataFrame '
    'и возвращает агрегированный DataFrame, что обеспечивает '
    'независимость аналитики от источника данных.'
)

listing_caption('Листинг 8 – Аналитический модуль (файл analytics/analytics.py)')
add_code([
    'import pandas as pd',
    '',
    '',
    'def price_index(df: pd.DataFrame) -> pd.DataFrame:',
    '    """',
    '    Ценовой индекс: отклонение средней цены магазина',
    '    от рыночного среднего (%).',
    '    + = магазин дороже рынка, - = дешевле.',
    '    """',
    '    if df.empty or "source" not in df.columns:',
    '        return pd.DataFrame()',
    '    avg_by_source = df.groupby("source")["price"].mean()',
    '    market_avg = df["price"].mean()',
    '    if market_avg == 0:',
    '        return pd.DataFrame()',
    '    index = (',
    '        (avg_by_source - market_avg) / market_avg * 100',
    '    ).round(2)',
    '    return index.reset_index().rename(',
    '        columns={"price": "price_index_%"})',
    '',
    '',
    'def price_dynamics(df: pd.DataFrame) -> pd.DataFrame:',
    '    """Динамика средней цены по дате сбора и магазину."""',
    '    if df.empty or "collected_at" not in df.columns:',
    '        return pd.DataFrame()',
    '    df = df.copy()',
    '    df["date"] = pd.to_datetime(df["collected_at"]).dt.date',
    '    return (',
    '        df.groupby(["date", "source"])["price"]',
    '        .mean()',
    '        .reset_index()',
    '    )',
    '',
    '',
    'def top_by_reviews(df: pd.DataFrame,',
    '                   n: int = 10) -> pd.DataFrame:',
    '    """Топ-N товаров по количеству отзывов."""',
    '    if df.empty:',
    '        return pd.DataFrame()',
    '    return (',
    '        df.nlargest(n, "reviews_count")',
    '        [["name", "source", "price", "rating", "reviews_count"]]',
    '        .reset_index(drop=True)',
    '    )',
    '',
    '',
    'def top_by_rating(df: pd.DataFrame,',
    '                  n: int = 10) -> pd.DataFrame:',
    '    """Топ-N товаров по рейтингу (только rating > 0)."""',
    '    if df.empty:',
    '        return pd.DataFrame()',
    '    return (',
    '        df[df["rating"] > 0]',
    '        .nlargest(n, "rating")',
    '        [["name", "source", "price", "rating", "reviews_count"]]',
    '        .reset_index(drop=True)',
    '    )',
    '',
    '',
    'def cross_category_summary(df: pd.DataFrame) -> pd.DataFrame:',
    '    """Сводная таблица сравнения категорий."""',
    '    if df.empty or "category" not in df.columns:',
    '        return pd.DataFrame()',
    '    return (',
    '        df.groupby("category")',
    '        .agg(',
    '            Товаров       =("id",            "count"),',
    '            Средняя_цена  =("price",         "mean"),',
    '            Средний_рейтинг=("rating",       "mean"),',
    '            Всего_отзывов =("reviews_count", "sum"),',
    '        )',
    '        .round(2)',
    '    )',
    '',
    '',
    'def price_comparison_by_source(df: pd.DataFrame) -> pd.DataFrame:',
    '    """Мин./средн./макс. цена по категориям и магазинам."""',
    '    if df.empty:',
    '        return pd.DataFrame()',
    '    return (',
    '        df.groupby(["category", "source"])["price"]',
    '        .agg(["mean", "min", "max", "count"])',
    '        .round(2)',
    '        .reset_index()',
    '        .rename(columns={',
    '            "mean":  "avg_price",',
    '            "min":   "min_price",',
    '            "max":   "max_price",',
    '            "count": "total"',
    '        })',
    '    )',
])

new_para(
    'Функция price_index() вычисляет ценовой индекс по формуле: '
    '(средняя цена магазина − средняя рыночная цена) / средняя рыночная цена '
    '× 100 %. Функция cross_category_summary() применяет именованные '
    'агрегации pandas — синтаксис Товаров=(\"id\", \"count\") задаёт '
    'одновременно имя результирующего столбца и агрегирующую функцию.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 6 — ML
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Модуль машинного обучения', '6')

new_para(
    'Модуль машинного обучения реализует двухэтапный подход к сегментации '
    'товаров. На первом этапе KMeans выполняет кластеризацию без учителя '
    'и размечает товары. На втором этапе Random Forest обучается на '
    'полученных метках и становится основным предиктором.'
)

heading2('Кластеризация методом KMeans', '6.1')

listing_caption('Листинг 9 – KMeans-кластеризация (файл ml/clustering.py)')
add_code([
    'import os, numpy as np, pandas as pd, joblib',
    'from sklearn.cluster import KMeans',
    'from sklearn.preprocessing import MinMaxScaler',
    'from sklearn.metrics import silhouette_score',
    '',
    'MODEL_PATH  = "ml/models/kmeans.pkl"',
    'SCALER_PATH = "ml/models/scaler.pkl"',
    'FEATURES    = ["price", "rating", "reviews_count"]',
    'SEGMENT_NAMES = {0: "Бюджетный", 1: "Средний", 2: "Премиум"}',
    '',
    '',
    'def train_kmeans(df: pd.DataFrame = None) -> dict:',
    '    if df is None:',
    '        from db.repository import get_all_products',
    '        df = get_all_products()',
    '    if df.empty or len(df) < 10:',
    '        return {"error": "Нужно минимум 10 товаров"}',
    '',
    '    X = df[FEATURES].dropna()',
    '',
    '    # Нормализация: все признаки -> диапазон [0, 1]',
    '    scaler = MinMaxScaler()',
    '    X_scaled = scaler.fit_transform(X)',
    '',
    '    # 10 случайных инициализаций, выбирается лучший результат',
    '    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)',
    '    labels = kmeans.fit_predict(X_scaled)',
    '    score  = silhouette_score(X_scaled, labels)',
    '',
    '    # Упорядочить кластеры по цене: 0=Бюджетный, 2=Премиум',
    '    order     = np.argsort(kmeans.cluster_centers_[:, 0])',
    '    label_map = {order[i]: i for i in range(3)}',
    '    labels_named = [SEGMENT_NAMES[label_map[l]] for l in labels]',
    '',
    '    joblib.dump(kmeans, MODEL_PATH)',
    '    joblib.dump(scaler, SCALER_PATH)',
    '    _save_clusters(df.iloc[X.index], labels_named)',
    '',
    '    return {"silhouette_score": round(score, 4),',
    '            "n_samples": len(X)}',
    '',
    '',
    'def predict_segment(price: float,',
    '                    rating: float, reviews: int) -> str:',
    '    """Предсказание с откатом на ценовую эвристику."""',
    '    if not (os.path.exists(MODEL_PATH) and',
    '            os.path.exists(SCALER_PATH)):',
    '        if price < 5000:  return "Бюджетный"',
    '        elif price < 30000: return "Средний"',
    '        else:               return "Премиум"',
    '',
    '    kmeans = joblib.load(MODEL_PATH)',
    '    scaler = joblib.load(SCALER_PATH)',
    '    X_scaled = scaler.transform([[price, rating, reviews]])',
    '    label    = int(kmeans.predict(X_scaled)[0])',
    '    order    = np.argsort(kmeans.cluster_centers_[:, 0])',
    '    label_map = {order[i]: i for i in range(3)}',
    '    return SEGMENT_NAMES[label_map[label]]',
])

heading2('Классификатор Random Forest', '6.2')

listing_caption('Листинг 10 – Random Forest классификатор (файл ml/classifier.py)')
add_code([
    'import os, pandas as pd, joblib',
    'from sklearn.ensemble import RandomForestClassifier',
    'from sklearn.model_selection import StratifiedKFold, cross_val_score',
    'from sklearn.metrics import accuracy_score, f1_score, confusion_matrix',
    '',
    'RF_PATH  = "ml/models/rf_classifier.pkl"',
    'FEATURES = ["price", "rating", "reviews_count"]',
    '',
    '',
    'def train_classifier() -> dict:',
    '    from db.repository import get_all_products',
    '    df = get_all_products().dropna(subset=FEATURES + ["segment"])',
    '    if len(df) < 15:',
    '        return {"error": "Сначала запустите KMeans."}',
    '',
    '    X, y = df[FEATURES], df["segment"]',
    '',
    '    rf = RandomForestClassifier(',
    '        n_estimators=100,',
    '        random_state=42,',
    '        class_weight="balanced",  # компенсация дисбаланса классов',
    '        n_jobs=-1                 # все ядра CPU',
    '    )',
    '    cv = StratifiedKFold(',
    '        n_splits=min(5, len(y.unique())),',
    '        shuffle=True, random_state=42',
    '    )',
    '    cv_scores = cross_val_score(rf, X, y, cv=cv,',
    '                                scoring="accuracy")',
    '    rf.fit(X, y)',
    '    y_pred = rf.predict(X)',
    '',
    '    joblib.dump(rf, RF_PATH)',
    '    return {',
    '        "accuracy":         round(accuracy_score(y, y_pred), 4),',
    '        "f1_macro":         round(f1_score(y, y_pred,',
    '                                           average="macro"), 4),',
    '        "cv_mean":          round(cv_scores.mean(), 4),',
    '        "cv_std":           round(cv_scores.std(),  4),',
    '        "confusion_matrix": confusion_matrix(y, y_pred).tolist(),',
    '    }',
    '',
    '',
    'def predict_segment(price: float,',
    '                    rating: float, reviews: int) -> str:',
    '    """Предсказание через RF; откат на KMeans при отсутствии модели."""',
    '    if not os.path.exists(RF_PATH):',
    '        from ml.clustering import predict_segment as kp',
    '        return kp(price, rating, reviews)',
    '    rf = joblib.load(RF_PATH)',
    '    X  = pd.DataFrame([[price, rating, reviews]], columns=FEATURES)',
    '    return rf.predict(X)[0]',
])

new_para(
    'Параметр class_weight="balanced" компенсирует дисбаланс классов: '
    'в реальных каталогах количество бюджетных товаров значительно '
    'превышает количество премиальных. Иерархия откатов при предсказании: '
    'Random Forest → KMeans → ценовая эвристика — гарантирует, что '
    'система всегда вернёт осмысленный результат.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 7 — ЛОГИРОВАНИЕ
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Модуль логирования', '7')

listing_caption('Листинг 11 – Настройка логирования (файл logger/logger.py)')
add_code([
    'import logging, os',
    'from datetime import datetime',
    '',
    'os.makedirs("logs", exist_ok=True)',
    '',
    '',
    'def setup_logger(name: str,',
    '                  level=logging.INFO) -> logging.Logger:',
    '    logger = logging.getLogger(name)',
    '    if logger.handlers:   # предотвратить дублирование обработчиков',
    '        return logger',
    '    logger.setLevel(level)',
    '',
    '    fmt = logging.Formatter(',
    '        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",',
    '        datefmt="%Y-%m-%d %H:%M:%S"',
    '    )',
    '    today = datetime.now().strftime("%Y-%m-%d")',
    '',
    '    # Вывод в файл с датой в имени',
    '    fh = logging.FileHandler(',
    '        f"logs/scraper_{today}.log", encoding="utf-8")',
    '    fh.setFormatter(fmt)',
    '    logger.addHandler(fh)',
    '',
    '    # Вывод в консоль',
    '    ch = logging.StreamHandler()',
    '    ch.setFormatter(fmt)',
    '    logger.addHandler(ch)',
    '    return logger',
    '',
    '',
    'def setup_all_loggers():',
    '    for name in ["runner","DNS","Ситилинк","Regard","analytics","ml"]:',
    '        setup_logger(name)',
])

new_para(
    'Файлы логов создаются с датой в имени (logs/scraper_2026-05-10.log), '
    'что обеспечивает автоматическую ротацию по дням. Кодировка utf-8 '
    'обязательна для корректного отображения кириллицы в операционных '
    'системах Windows. Проверка if logger.handlers предотвращает '
    'дублирование вывода при повторных вызовах в Streamlit.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# ЗАКЛЮЧЕНИЕ
# ═══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 10)
add_text(p, 'ЗАКЛЮЧЕНИЕ', 14)

new_para(
    'В настоящем отчёте представлено подробное описание бэкенда системы '
    'мониторинга цен «ЦенМонитор» с полным программным кодом всех модулей.'
)
new_para(
    'Модуль парсинга включает три специализированных парсера для магазинов '
    'DNS, Ситилинк и Regard, унаследованных от общего базового класса. '
    'Для каждого магазина реализован индивидуальный набор методов обхода '
    'антифрод-систем: для DNS — цепочки запасных CSS-селекторов; '
    'для Ситилинк — поиск по частичному совпадению классов и чтение '
    'aria-атрибутов; для Regard — извлечение рейтинга из CSS-свойства '
    'width и работа с числовыми идентификаторами категорий.'
)
new_para(
    'Модуль базы данных построен на SQLAlchemy ORM с паттерном Repository. '
    'Разделение товара и цены на отдельные таблицы обеспечивает '
    'полную историю изменения цен для временны́х графиков. '
    'ML-модуль реализует двухэтапную сегментацию с иерархией откатов, '
    'гарантирующей работу предиктора при любом состоянии обученных моделей.'
)
new_para(
    'Разработанный бэкенд обеспечивает все ключевые функции системы '
    'и может быть расширен дополнительными источниками данных и '
    'категориями товаров без изменения существующей архитектуры.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# СПИСОК ИСТОЧНИКОВ
# ═══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 10)
add_text(p, 'СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ', 14)

refs = [
    'Документация Playwright for Python [Электронный ресурс]. – URL: https://playwright.dev/python/docs/intro (дата обращения: 10.05.2026).',
    'Официальная документация SQLAlchemy 2.0 [Электронный ресурс]. – URL: https://docs.sqlalchemy.org/en/20/ (дата обращения: 10.05.2026).',
    'Официальная документация pandas 2.1 [Электронный ресурс]. – URL: https://pandas.pydata.org/docs/ (дата обращения: 10.05.2026).',
    'Scikit-learn: Machine Learning in Python / F. Pedregosa [и др.] // Journal of Machine Learning Research. – 2011. – Т. 12. – С. 2825–2830.',
    'Документация Beautiful Soup 4 [Электронный ресурс]. – URL: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ (дата обращения: 10.05.2026).',
    'Агеев М.С. Парсинг веб-страниц: методы и инструменты. – Москва: ДМК Пресс, 2022. – 320 с.',
    'Рашка С., Мирджалили В. Python и машинное обучение; пер. с англ. – 3-е изд. – Москва: ДМК Пресс, 2023. – 840 с.',
    'Документация Streamlit [Электронный ресурс]. – URL: https://docs.streamlit.io/ (дата обращения: 10.05.2026).',
]
for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.JUSTIFY, 0, 0, 0)
    add_text(p, f'{i}. {ref}', 14)

# ─── Нумерация страниц ───────────────────────────────────────────────────────
add_footer_page_numbers()

# ─── Сохранение ──────────────────────────────────────────────────────────────
out = '/home/user/Parsing/Отчёт_Бэкенд_ЦенМонитор.docx'
doc.save(out)
print(f'Сохранено: {out}')
