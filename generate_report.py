"""
Генератор отчёта по бэкенду системы ЦенМонитор.
Формат: СТО ЮУрГУ 21-2008
"""

from docx import Document
from docx.shared import Pt, Cm, Mm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ─── Параметры страницы ──────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width  = Mm(210)
section.page_height = Mm(297)
section.top_margin    = Mm(20)
section.bottom_margin = Mm(26)
section.left_margin   = Mm(25)
section.right_margin  = Mm(10)

# ─── Стили ──────────────────────────────────────────────────────────────────
styles = doc.styles

def set_base_font(run, size=14, bold=False):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)

def para_fmt(para, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent_cm=0.7, space_before=0, space_after=0):
    pf = para.paragraph_format
    pf.alignment = align
    if indent_cm:
        pf.first_line_indent = Cm(indent_cm)
    pf.space_before = Pt(space_before)
    pf.space_after  = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

def add_text(para, text, size=14, bold=False):
    run = para.add_run(text)
    set_base_font(run, size, bold)
    return run

def new_para(text='', align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.7, size=14, bold=False, space_before=0, space_after=0):
    p = doc.add_paragraph()
    para_fmt(p, align, indent, space_before, space_after)
    if text:
        add_text(p, text, size, bold)
    return p

def heading1(text, num):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 12, 6)
    add_text(p, f'{num} {text.upper()}', 14, False)
    return p

def heading2(text, num):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 6, 3)
    add_text(p, f'{num} {text}', 14, False)
    return p

def heading3(text, num):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 3, 3)
    add_text(p, f'{num} {text}', 14, False)
    return p

def add_code(lines):
    """Блок кода — Courier New 11pt, без отступа, без выравнивания по ширине."""
    for line in lines:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.first_line_indent = Cm(0)
        pf.space_before = Pt(0)
        pf.space_after  = Pt(0)
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        run = p.add_run(line)
        run.font.name = 'Courier New'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0, 0, 0)

def fig_caption(text):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 6, 6)
    add_text(p, text, 14)
    return p

def tbl_caption(text):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 6, 3)
    add_text(p, text, 14)
    return p

def set_cell(cell, text, size=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, bg=None):
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
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.clear()
        run = p.add_run()
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        instrText = OxmlElement('w:instrText')
        instrText.text = 'PAGE'
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)

# ═══════════════════════════════════════════════════════════════════════════════
# ТИТУЛЬНЫЙ ЛИСТ
# ═══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 6)
add_text(p, 'МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ', 12)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 0)
add_text(p, 'Федеральное государственное автономное образовательное учреждение\nвысшего образования', 12)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 6)
add_text(p, '«ЮЖНО-УРАЛЬСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ»\n(национальный исследовательский университет)', 12)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 0)
add_text(p, 'Высшая школа экономики и управления', 12)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 30)
add_text(p, 'Кафедра «Экономика и экономическая безопасность»', 12)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 6)
add_text(p, 'ОТЧЁТ', 16)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 6)
add_text(p, 'по дисциплине «Информационные технологии»', 14)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 30)
add_text(p, 'Тема: Описание бэкенда системы мониторинга цен конкурентов «ЦенМонитор»', 14)

# Подпись
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.RIGHT, 0, 0, 0)
add_text(p, 'Выполнили: студенты группы ЭУ-430', 12)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.RIGHT, 0, 0, 0)
add_text(p, 'Головчиц И.А., Вахрушев Е.С.', 12)

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.RIGHT, 0, 0, 0)
add_text(p, 'Проверил: ________________', 12)

for _ in range(6):
    doc.add_paragraph()

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 0)
add_text(p, 'Челябинск 2026', 12)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# ОГЛАВЛЕНИЕ
# ═══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 0, 12)
add_text(p, 'ОГЛАВЛЕНИЕ', 14)

contents = [
    ('Введение', '3'),
    ('1 Общая архитектура системы', '4'),
    ('1.1 Структура модулей', '4'),
    ('1.2 Технологический стек', '5'),
    ('2 Модуль парсинга (scraper)', '6'),
    ('2.1 Базовый класс BaseParser', '6'),
    ('2.2 Методы обхода антифрод-систем', '8'),
    ('2.3 Парсер интернет-магазина DNS', '10'),
    ('2.4 Парсер интернет-магазина Ситилинк', '12'),
    ('2.5 Парсер интернет-магазина Regard', '14'),
    ('2.6 Модуль запуска парсинга (runner)', '16'),
    ('3 Модуль базы данных (db)', '17'),
    ('3.1 ORM-модели SQLAlchemy', '17'),
    ('3.2 Репозиторий данных', '19'),
    ('4 Аналитический модуль (analytics)', '21'),
    ('5 Модуль машинного обучения (ml)', '23'),
    ('5.1 Кластеризация методом KMeans', '23'),
    ('5.2 Классификатор Random Forest', '26'),
    ('6 Модуль логирования', '28'),
    ('Заключение', '29'),
    ('Список использованных источников', '30'),
]

for title, page in contents:
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.LEFT, 0, 0, 0)
    tab_stop = p.paragraph_format
    dots = '.' * max(1, 70 - len(title) - len(page))
    add_text(p, f'{title} {dots} {page}', 14)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# ВВЕДЕНИЕ
# ═══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 12, 6)
add_text(p, 'ВВЕДЕНИЕ', 14)

new_para(
    'Настоящий отчёт посвящён описанию серверной части (бэкенда) автоматизированной '
    'системы мониторинга цен конкурентов «ЦенМонитор», разработанной в рамках '
    'учебной дисциплины. Система предназначена для автоматического сбора, хранения '
    'и анализа ценовой информации с трёх крупных российских интернет-магазинов '
    'электроники: DNS, Ситилинк и Regard.'
)

new_para(
    'Актуальность темы обусловлена высокой конкуренцией на рынке электронной '
    'коммерции, где цены на товары могут изменяться несколько раз в сутки. '
    'Ручной мониторинг цен в таких условиях практически невозможен, что '
    'обусловливает потребность в автоматизированных инструментах сбора данных '
    'с последующей аналитикой и визуализацией.'
)

new_para(
    'Бэкенд системы реализован на языке Python 3.11 и состоит из четырёх '
    'функционально независимых модулей: модуля парсинга (scraper), модуля '
    'базы данных (db), аналитического модуля (analytics) и модуля машинного '
    'обучения (ml). Взаимодействие между модулями осуществляется через '
    'единый интерфейс репозитория базы данных на основе объектов '
    'pandas.DataFrame.'
)

new_para(
    'Целью отчёта является подробное описание архитектурных решений, '
    'используемых технологий и программного кода каждого модуля с '
    'обоснованием принятых решений.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 1
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Общая архитектура системы', '1')

# 1.1
heading2('Структура модулей', '1.1')

new_para(
    'Система «ЦенМонитор» построена по принципу многоуровневой архитектуры, '
    'в которой каждый слой отвечает за строго определённые функции. '
    'Подобный подход обеспечивает независимость компонентов и упрощает '
    'сопровождение кода. Структура бэкенда представлена в таблице 1.'
)

tbl_caption('Таблица 1 – Структура модулей бэкенда')
table = doc.add_table(rows=5, cols=3)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['Модуль', 'Папка', 'Назначение']
for i, h in enumerate(headers):
    set_cell(table.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
rows_data = [
    ('Парсинг', 'scraper/', 'Автоматический сбор данных с сайтов магазинов через управляемый браузер'),
    ('База данных', 'db/', 'Определение ORM-моделей, CRUD-операции, получение аналитических выборок'),
    ('Аналитика', 'analytics/', 'Статистические расчёты: ценовой индекс, динамика, рейтинги'),
    ('Машинное обучение', 'ml/', 'Кластеризация товаров по ценовым сегментам, классификация новых товаров'),
]
for i, (col1, col2, col3) in enumerate(rows_data):
    set_cell(table.rows[i+1].cells[0], col1)
    set_cell(table.rows[i+1].cells[1], col2)
    set_cell(table.rows[i+1].cells[2], col3)

new_para('')
new_para(
    'Взаимодействие модулей осуществляется следующим образом: модуль парсинга '
    'записывает собранные данные через репозиторий базы данных. Аналитический '
    'модуль и модуль машинного обучения читают данные из той же базы. '
    'Веб-дашборд (frontend) обращается ко всем модулям бэкенда посредством '
    'вызовов функций репозитория, аналитики и ML-предиктора, представленных '
    'на рисунке 1.1.'
)

# Схема взаимодействия как таблица
tbl_caption('Рисунок 1.1 – Схема взаимодействия модулей системы')
arch = doc.add_table(rows=3, cols=5)
arch.style = 'Table Grid'
arch.alignment = WD_TABLE_ALIGNMENT.CENTER

arch_data = [
    ['DNS\nСайт', '→', 'Модуль\nпарсинга\n(scraper/)', '→', 'База данных\nSQLite\n(db/)'],
    ['Ситилинк\nСайт', '', '', '←', 'Аналитика\n(analytics/)'],
    ['Regard\nСайт', '', 'Дашборд\n(frontend)', '←', 'ML-модуль\n(ml/)'],
]
for i, row_data in enumerate(arch_data):
    for j, cell_text in enumerate(row_data):
        c = arch.rows[i].cells[j]
        set_cell(c, cell_text, align=WD_ALIGN_PARAGRAPH.CENTER)
        if j in [0, 2, 4] and cell_text:
            tc = c._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), 'EBF3FB')
            tcPr.append(shd)

new_para('')

# 1.2
heading2('Технологический стек', '1.2')

new_para(
    'При выборе технологий приоритет отдавался зрелым, широко поддерживаемым '
    'библиотекам с активным сообществом. Полный перечень используемых '
    'библиотек приведён в таблице 2.'
)

tbl_caption('Таблица 2 – Технологический стек бэкенда')
tech_table = doc.add_table(rows=10, cols=3)
tech_table.style = 'Table Grid'
tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Библиотека', 'Версия', 'Назначение']):
    set_cell(tech_table.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
tech_data = [
    ('playwright', '≥ 1.44', 'Управление браузером Chromium для рендеринга JavaScript-страниц'),
    ('beautifulsoup4', '≥ 4.12', 'Парсинг HTML-документов с помощью CSS-селекторов'),
    ('lxml', '≥ 4.9', 'Высокопроизводительный XML/HTML-парсер, используемый BeautifulSoup'),
    ('sqlalchemy', '≥ 2.0', 'ORM-фреймворк для работы с реляционными базами данных'),
    ('pandas', '≥ 2.1', 'Табличная обработка данных, аналитические агрегации'),
    ('numpy', '≥ 1.26', 'Векторные вычисления, нормализация признаков'),
    ('scikit-learn', '≥ 1.4', 'Алгоритмы ML: KMeans, RandomForest, кросс-валидация, метрики'),
    ('joblib', '≥ 1.3', 'Сериализация и десериализация обученных ML-моделей на диск'),
    ('streamlit', '≥ 1.32', 'Веб-фреймворк для интерактивного дашборда (frontend)'),
]
for i, (lib, ver, desc) in enumerate(tech_data):
    set_cell(tech_table.rows[i+1].cells[0], lib)
    set_cell(tech_table.rows[i+1].cells[1], ver, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell(tech_table.rows[i+1].cells[2], desc)

new_para('')
new_para(
    'В качестве базы данных используется SQLite — встраиваемая реляционная '
    'СУБД, не требующая отдельного серверного процесса. Выбор обусловлен '
    'учебным характером проекта: SQLite обеспечивает все необходимые '
    'реляционные возможности при минимальных накладных расходах на '
    'администрирование.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 2
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Модуль парсинга (scraper)', '2')

# 2.1
heading2('Базовый класс BaseParser', '2.1')

new_para(
    'Все три парсера магазинов наследуются от единого абстрактного класса '
    'BaseParser, определённого в файле scraper/base.py. Базовый класс '
    'инкапсулирует логику загрузки веб-страниц и утилитарные методы '
    'очистки данных, что исключает дублирование кода в дочерних классах.'
)

new_para(
    'Для загрузки страниц применяется библиотека Playwright, а не '
    'стандартный модуль requests. Причина состоит в том, что каталоги '
    'всех трёх магазинов строятся с использованием JavaScript-фреймворков '
    '(React, Vue), поэтому обычный HTTP-запрос возвращает пустой HTML-шаблон '
    'без товаров. Playwright запускает полноценный браузер Chromium, '
    'который исполняет JavaScript и формирует финальный DOM-дерево, '
    'доступное для последующего парсинга.'
)

new_para('Листинг 1 – Определение класса BaseParser (файл scraper/base.py)')
add_code([
    'import logging',
    'import time',
    'from bs4 import BeautifulSoup',
    '',
    '',
    'class BaseParser:',
    '    """Базовый класс парсеров. Использует Playwright для рендеринга JavaScript."""',
    '',
    '    USER_AGENT = (',
    '        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "',
    '        "AppleWebKit/537.36 (KHTML, like Gecko) "',
    '        "Chrome/124.0.0.0 Safari/537.36"',
    '    )',
    '    DELAY = 2.0  # секунд между страницами',
    '',
    '    def __init__(self, source_name: str, base_url: str):',
    '        self.source_name = source_name',
    '        self.base_url = base_url',
    '        self.logger = logging.getLogger(source_name)',
])

new_para(
    'Константа USER_AGENT содержит строку идентификации браузера Chrome 124 '
    'под операционной системой Windows 10. Большинство антифрод-систем '
    'интернет-магазинов проверяют данный заголовок в первую очередь: '
    'нехарактерный User-Agent (например, python-requests/2.31) является '
    'немедленным сигналом для блокировки IP-адреса. Значение DELAY '
    'определяет паузу между запросами страниц.'
)

new_para('Листинг 2 – Метод загрузки страницы get_page() (файл scraper/base.py)')
add_code([
    '    def get_page(self, url: str,',
    '                 wait_selector: str = None) -> BeautifulSoup | None:',
    '        """Загрузить страницу через Playwright (рендерит JS)."""',
    '        try:',
    '            from playwright.sync_api import sync_playwright',
    '        except ImportError:',
    '            self.logger.error("Playwright не установлен.")',
    '            return None',
    '',
    '        try:',
    '            with sync_playwright() as p:',
    '                browser = p.chromium.launch(',
    '                    headless=True,',
    '                    args=["--no-sandbox"]',
    '                )',
    '                ctx = browser.new_context(',
    '                    user_agent=self.USER_AGENT,',
    '                    locale="ru-RU",',
    '                    viewport={"width": 1280, "height": 800},',
    '                )',
    '                page = ctx.new_page()',
    '                page.set_extra_http_headers({',
    '                    "Accept-Language": "ru-RU,ru;q=0.9",',
    '                    "Accept": "text/html,application/xhtml+xml,...",',
    '                })',
    '',
    '                page.goto(url, wait_until="domcontentloaded",',
    '                           timeout=30000)',
    '',
    '                if wait_selector:',
    '                    try:',
    '                        page.wait_for_selector(',
    '                            wait_selector, timeout=12000)',
    '                    except Exception:',
    '                        self.logger.warning(',
    '                            f"Селектор не найден на {url}")',
    '',
    '                # Прокрутка для активации ленивой загрузки',
    '                page.evaluate(',
    '                    "window.scrollTo(0, document.body.scrollHeight / 2)")',
    '                time.sleep(1.5)',
    '                page.evaluate(',
    '                    "window.scrollTo(0, document.body.scrollHeight)")',
    '                time.sleep(1.0)',
    '',
    '                content = page.content()',
    '                browser.close()',
    '',
    '            time.sleep(self.DELAY)',
    '            return BeautifulSoup(content, "html.parser")',
    '',
    '        except Exception as e:',
    '            self.logger.error(f"Ошибка загрузки {url}: {e}")',
    '            return None',
])

new_para('Листинг 3 – Утилитарные методы очистки данных (файл scraper/base.py)')
add_code([
    '    @staticmethod',
    '    def clean_price(text: str) -> float:',
    '        """Извлечь число из строки цены \'1 299 руб.\' -> 1299.0"""',
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
    'Все три метода реализуют защитное программирование: при передаче '
    'пустой строки или None они возвращают нулевое значение, а не '
    'вызывают исключение. Это важно, поскольку структура HTML-страниц '
    'магазинов нестабильна — отдельные поля могут отсутствовать для '
    'части товаров.'
)

page_break()

# 2.2
heading2('Методы обхода антифрод-систем', '2.2')

new_para(
    'Современные интернет-магазины применяют многоуровневую защиту от '
    'автоматического сбора данных. В системе «ЦенМонитор» реализован '
    'комплекс мер противодействия, описанных в таблице 3.'
)

tbl_caption('Таблица 3 – Применяемые меры обхода антифрод-систем')
af_table = doc.add_table(rows=8, cols=3)
af_table.style = 'Table Grid'
af_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Метод защиты магазина', 'Применяемое противодействие', 'Реализация в коде']):
    set_cell(af_table.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
af_data = [
    ('Проверка User-Agent', 'Реальный заголовок Chrome 124 / Win10', 'USER_AGENT = "Mozilla/5.0..."'),
    ('Отсутствие выполнения JS', 'Браузерный рендеринг через Playwright', 'p.chromium.launch(headless=True)'),
    ('Проверка локали и языка', 'Русская локаль и заголовок Accept-Language', 'locale="ru-RU"'),
    ('Нулевой или нестандартный viewport', 'Реалистичный размер 1280×800 пикселей', 'viewport={"width":1280,"height":800}'),
    ('Отсутствие взаимодействия с DOM', 'Имитация прокрутки страницы', 'page.evaluate("window.scrollTo(...)")'),
    ('Rate limiting (ограничение частоты)', 'Пауза 2 секунды между запросами', 'DELAY = 2.0; time.sleep(self.DELAY)'),
    ('Ленивая загрузка карточек', 'Двойная прокрутка с задержкой 1.5 с', 'time.sleep(1.5) между scrollTo'),
]
for i, row in enumerate(af_data):
    for j, val in enumerate(row):
        set_cell(af_table.rows[i+1].cells[j], val)

new_para('')
new_para(
    'Первым и наиболее важным барьером является проверка заголовка '
    'User-Agent. Библиотека requests по умолчанию отправляет '
    'идентификатор «python-requests/2.31», который немедленно '
    'распознаётся системой защиты. В противовес этому используется '
    'актуальный User-Agent браузера Chrome версии 124.'
)

new_para(
    'Вторым барьером служит проверка выполнения JavaScript. '
    'Если сервер возвращает страницу, предполагающую рендеринг '
    'на стороне клиента, обычный HTTP-клиент получит пустой '
    'контейнер. Playwright полностью воспроизводит жизненный цикл '
    'браузера: загружает скрипты, выполняет React-гидратацию '
    'и ожидает отрисовки компонентов.'
)

new_para(
    'Проверка viewport особенно актуальна для Ситилинк: сайт '
    'использует адаптивную вёрстку и при нулевых или минимальных '
    'размерах окна переключается в мобильный режим с иными '
    'CSS-классами, что нарушает работу селекторов. Установка '
    'viewport 1280×800 гарантирует загрузку десктопной версии сайта.'
)

new_para(
    'Имитация прокрутки страницы решает две задачи одновременно. '
    'Во-первых, большинство магазинов применяют технику ленивой '
    'загрузки (lazy loading): карточки товаров ниже видимой '
    'области экрана загружаются только при прокрутке к ним. '
    'Во-вторых, fingerprint-системы фиксируют полное отсутствие '
    'взаимодействия с DOM как признак бота — прокрутка страницы '
    'снижает вероятность блокировки, представленную в виде схемы '
    'на рисунке 2.1.'
)

tbl_caption('Рисунок 2.1 – Схема обхода антифрод-системы')
schema = doc.add_table(rows=6, cols=1)
schema.style = 'Table Grid'
schema.alignment = WD_TABLE_ALIGNMENT.CENTER
steps = [
    '1. Запуск браузера Chromium (headless=True, --no-sandbox)',
    '2. Создание контекста: User-Agent Chrome 124, locale=ru-RU, viewport 1280×800',
    '3. Установка HTTP-заголовков: Accept-Language: ru-RU, Accept: text/html...',
    '4. Переход на страницу: wait_until="domcontentloaded" (ожидание JS)',
    '5. Ожидание целевого CSS-селектора (карточки товаров): timeout 12 сек',
    '6. Прокрутка страницы → пауза 1.5 с → прокрутка до конца → пауза 1.0 с → снятие HTML',
]
for i, step in enumerate(steps):
    set_cell(schema.rows[i].cells[0], step, bg='F2F9FF' if i % 2 == 0 else 'FFFFFF')

new_para('')
page_break()

# 2.3 DNS
heading2('Парсер интернет-магазина DNS', '2.3')

new_para(
    'Парсер DNS реализован в классе DnsParser (файл scraper/dns_parser.py). '
    'Сайт DNS строится с применением серверного рендеринга (SSR) с частичной '
    'гидратацией JavaScript, что делает его структуру относительно стабильной '
    'по сравнению с полностью клиентскими React-приложениями.'
)

new_para('Листинг 4 – Определение категорий и класса DnsParser (файл scraper/dns_parser.py)')
add_code([
    'from .base import BaseParser',
    '',
    '# Реальные URL категорий DNS',
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
])

new_para(
    'Словарь CATEGORIES отображает человекочитаемые названия категорий '
    'на реальные URL-пути каталога DNS. Это позволяет вызывать метод '
    'parse_category() с понятными именами вместо URL, а также легко '
    'добавлять новые категории в одном месте без изменения логики парсинга.'
)

new_para('Листинг 5 – Метод parse_category() класса DnsParser')
add_code([
    '    def parse_category(self, category: str) -> list[dict]:',
    '        path = CATEGORIES.get(category)',
    '        if not path:',
    '            self.logger.warning(f"DNS: категория \'{category}\' не найдена")',
    '            return []',
    '',
    '        products = []',
    '        for page_num in range(1, 6):  # первые 5 страниц',
    '            url = f"{self.base_url}{path}?p={page_num}"',
    '            self.logger.info(',
    '                f"DNS {category}: страница {page_num} — {url}")',
    '',
    '            soup = self.get_page(url,',
    '                                  wait_selector=".catalog-product")',
    '            if not soup:',
    '                break',
    '',
    '            items = soup.select(".catalog-product")',
    '            if not items:',
    '                self.logger.info(',
    '                    f"DNS {category}: стр.{page_num} пустая, стоп")',
    '                break',
    '',
    '            for item in items:',
    '                try:',
    '                    # Название — несколько запасных селекторов',
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
    '                    # Ссылка на товар',
    '                    href = name_tag.get("href", "")',
    '                    item_url = (',
    '                        self.base_url + href',
    '                        if href.startswith("/") else href',
    '                    )',
    '',
    '                    # Цена — три варианта CSS-класса',
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
    '                    # Рейтинг и отзывы',
    '                    rating_tag = (',
    '                        item.select_one(".product-item__rating-count") or',
    '                        item.select_one("[class*=\'rating\']")',
    '                    )',
    '                    rating = self.clean_rating(',
    '                        rating_tag.get_text() if rating_tag else "")',
    '',
    '                    reviews_tag = (',
    '                        item.select_one(".product-item__reviews-count") or',
    '                        item.select_one("[class*=\'reviews\']")',
    '                    )',
    '                    reviews = self.clean_reviews(',
    '                        reviews_tag.get_text() if reviews_tag else "")',
    '',
    '                    # Бренд — первое слово названия',
    '                    brand = name.split()[0] if name else ""',
    '',
    '                    products.append({',
    '                        "name": name,',
    '                        "brand": brand,',
    '                        "category": category,',
    '                        "price": price,',
    '                        "rating": rating,',
    '                        "reviews_count": reviews,',
    '                        "url": item_url,',
    '                        "source": "DNS",',
    '                    })',
    '                except Exception as e:',
    '                    self.logger.error(',
    '                        f"DNS: ошибка обработки товара: {e}")',
    '',
    '            # Проверяем наличие следующей страницы пагинации',
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
    'вместо аварийного завершения. Например, для цены предусмотрены '
    'три варианта: .product-buy__price, [class*=\'price_current\'] '
    'и [class*=\'price-current\']. Атрибутный селектор [class*=\'...\'] '
    'выполняет поиск по частичному вхождению подстроки в значение '
    'атрибута class, что устойчивее к незначительным изменениям '
    'наименований классов.'
)

new_para(
    'Бренд извлекается как первое слово полного названия товара. '
    'Этот эвристический подход работает корректно для подавляющего '
    'большинства карточек электроники, где название традиционно '
    'начинается с имени производителя (например, «Kingston FURY '
    'Beast 16 ГБ DDR5» → бренд «Kingston»).'
)

page_break()

# 2.4 Citilink
heading2('Парсер интернет-магазина Ситилинк', '2.4')

new_para(
    'Парсер Ситилинк реализован в классе CitilinkParser '
    '(файл scraper/citilink_parser.py). Ситилинк использует '
    'React-приложение — весь каталог полностью рендерится на '
    'стороне клиента. Главная особенность защиты: CSS-классы '
    'компонентов содержат автогенерируемые хэш-суффиксы '
    '(например, ProductCard_root__3kX9a), которые изменяются '
    'при каждом деплое сайта.'
)

new_para('Листинг 6 – Поиск карточек товаров Ситилинк (файл scraper/citilink_parser.py)')
add_code([
    'from .base import BaseParser',
    '',
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
    '        ...',
    '        soup = self.get_page(url,',
    '            wait_selector="[class*=\'ProductCard\']")',
    '',
    '        # Три варианта поиска карточек с частичным совпадением класса',
    '        items = (',
    '            soup.select("[data-meta-product]") or',
    '            soup.select("article[class*=\'ProductCard\']") or',
    '            soup.select("[class*=\'ProductCard_root\']")',
    '        )',
])

new_para(
    'Селектор [data-meta-product] является наиболее стабильным, '
    'поскольку data-атрибуты намеренно задаются разработчиком '
    'для семантической разметки и реже меняются при рефакторинге '
    'вёрстки. Если он недоступен, используется поиск по частичному '
    'совпадению class — это обеспечивает устойчивость к '
    'автогенерируемым хэш-суффиксам.'
)

new_para('Листинг 7 – Извлечение рейтинга из aria-атрибута (файл scraper/citilink_parser.py)')
add_code([
    '                    # Рейтинг: приоритет отдаётся aria-label',
    '                    # (семантически стабильнее визуальных классов)',
    '                    rating_tag = (',
    '                        item.select_one("[class*=\'Rating_\']") or',
    '                        item.select_one("[class*=\'rating\']")',
    '                    )',
    '                    rating = self.clean_rating(',
    '                        rating_tag.get("aria-label", "") or',
    '                        (rating_tag.get_text()',
    '                         if rating_tag else "")',
    '                    )',
])

new_para(
    'Для рейтинга используется атрибут aria-label вместо текстового '
    'содержимого элемента. Значение aria-label задаётся разработчиком '
    'специально для вспомогательных технологий (screen reader), '
    'поэтому его формат более предсказуем и редко изменяется при '
    'косметических обновлениях вёрстки. Типичное значение: '
    '«Рейтинг: 4.7 из 5» — из него метод clean_rating() извлекает '
    'число 4.7.'
)

page_break()

# 2.5 Regard
heading2('Парсер интернет-магазина Regard', '2.5')

new_para(
    'Парсер Regard реализован в классе RegardParser '
    '(файл scraper/regard_parser.py). В отличие от DNS и Ситилинк, '
    'Regard использует числовые идентификаторы в URL-путях каталога '
    'вместо человекочитаемых названий категорий.'
)

new_para('Листинг 8 – Категории и пагинация Regard (файл scraper/regard_parser.py)')
add_code([
    'from .base import BaseParser',
    '',
    '# Regard использует числовые ID категорий в URL',
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
    '        ...',
    '        for page_num in range(1, 6):',
    '            # Regard использует ?page=N, а не ?p=N как DNS',
    '            url = f"{self.base_url}{path}?page={page_num}"',
])

new_para(
    'Наиболее нестандартным является способ извлечения рейтинга '
    'на Regard. Магазин отображает звёзды рейтинга через CSS-свойство '
    'width элемента в процентах (например, style="width: 80%"), '
    'а не через явное числовое значение в тексте.'
)

new_para('Листинг 9 – Извлечение рейтинга из CSS-свойства width (файл scraper/regard_parser.py)')
add_code([
    '                    # Regard отображает звёзды через width в процентах',
    '                    rating_tag = item.select_one("[class*=\'rating\']")',
    '                    rating_val = 0.0',
    '                    if rating_tag:',
    '                        style = rating_tag.get("style", "")',
    '                        if "width" in style:',
    '                            # width: 80% -> 4.0 из 5.0',
    '                            # Формула: процент / 20 = оценка',
    '                            try:',
    '                                pct = float("".join(',
    '                                    c for c in style',
    '                                    if c.isdigit() or c == "."))',
    '                                rating_val = round(pct / 20, 1)',
    '                            except Exception:',
    '                                pass',
    '                        else:',
    '                            rating_val = self.clean_rating(',
    '                                rating_tag.get_text())',
])

new_para(
    'Формула преобразования: значение width в процентах делится на 20, '
    'что переводит стопроцентную шкалу в пятибалльную. Примеры '
    'преобразования: 100 % → 5.0 (максимальный рейтинг); '
    '80 % → 4.0; 60 % → 3.0. '
    'Если элемент рейтинга не содержит атрибут style с width, '
    'применяется стандартный метод clean_rating(), '
    'извлекающий числовое значение из текстового содержимого.'
)

page_break()

# 2.6 Runner
heading2('Модуль запуска парсинга (runner)', '2.6')

new_para(
    'Модуль runner.py является оркестратором всего процесса сбора данных. '
    'Он инициализирует базу данных, создаёт запись о сеансе парсинга '
    '(Collection), последовательно запускает все активные парсеры по '
    'всем выбранным категориям и обновляет статус сеанса по завершении.'
)

new_para('Листинг 10 – Основная функция run_all() (файл scraper/runner.py)')
add_code([
    'from .dns_parser import DnsParser',
    'from .citilink_parser import CitilinkParser',
    'from .regard_parser import RegardParser',
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
    '    init_db()',
    '',
    '    if categories is None:',
    '        categories = ALL_CATEGORIES',
    '    if sources is None:',
    '        sources = ALL_SOURCES',
    '',
    '    # Создать запись о сеансе сбора в БД',
    '    with SessionLocal() as session:',
    '        collection = Collection(',
    '            started_at=datetime.utcnow(), status="running")',
    '        session.add(collection)',
    '        session.commit()',
    '        cid = collection.id',
    '',
    '    all_parsers = {',
    '        "DNS": DnsParser(),',
    '        "Ситилинк": CitilinkParser(),',
    '        "Regard": RegardParser(),',
    '    }',
    '    active_parsers = [p for name, p in all_parsers.items()',
    '                      if name in sources]',
    '',
    '    total = 0',
    '    errors = 0',
    '',
    '    for parser in active_parsers:',
    '        for category in categories:',
    '            try:',
    '                logger.info(',
    '                    f">>> Парсинг: {parser.source_name} — {category}")',
    '                products = parser.parse_category(category)',
    '                if products:',
    '                    save_products(products, parser.source_name, cid)',
    '                    total += len(products)',
    '            except Exception as e:',
    '                errors += 1',
    '                logger.error(',
    '                    f"Ошибка {parser.source_name} {category}: {e}")',
    '',
    '    # Обновить статус сеанса',
    '    with SessionLocal() as session:',
    '        col = session.get(Collection, cid)',
    '        col.finished_at = datetime.utcnow()',
    '        col.status = "success" if errors == 0 else "partial"',
    '        col.total_records = total',
    '        session.commit()',
    '',
    '    return {"total": total, "sources": len(active_parsers),',
    '            "categories": len(categories), "errors": errors}',
])

new_para(
    'Функция принимает опциональные параметры categories и sources, '
    'что позволяет запускать парсинг выборочно — например, только '
    'смартфоны из DNS. Статус сеанса имеет три значения: "running" '
    '(запущен), "success" (завершён без ошибок) и "partial" '
    '(завершён с ошибками в отдельных категориях). '
    'Это позволяет в дашборде отображать историю сборов с '
    'диагностической информацией.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 3
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Модуль базы данных (db)', '3')

# 3.1
heading2('ORM-модели SQLAlchemy', '3.1')

new_para(
    'Схема базы данных определена в файле db/models.py с использованием '
    'декларативного стиля SQLAlchemy ORM. Схема состоит из пяти взаимосвязанных '
    'таблиц, описанных в таблице 4 и на рисунке 3.1.'
)

tbl_caption('Таблица 4 – Описание таблиц базы данных')
db_table = doc.add_table(rows=6, cols=3)
db_table.style = 'Table Grid'
db_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Таблица', 'Класс модели', 'Назначение']):
    set_cell(db_table.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
db_data = [
    ('sources', 'Source', 'Список магазинов-источников: DNS, Ситилинк, Regard'),
    ('products', 'Product', 'Каталог уникальных товаров с названием, брендом, категорией и URL'),
    ('prices', 'Price', 'История цен: каждый сеанс парсинга добавляет новую запись'),
    ('collections', 'Collection', 'Журнал сеансов сбора данных с временными метками и статусом'),
    ('ml_clusters', 'MLCluster', 'Результаты ML-сегментации: сегмент и версия модели для каждого товара'),
]
for i, (tname, cls, desc) in enumerate(db_data):
    set_cell(db_table.rows[i+1].cells[0], tname)
    set_cell(db_table.rows[i+1].cells[1], cls)
    set_cell(db_table.rows[i+1].cells[2], desc)

new_para('')

tbl_caption('Рисунок 3.1 – Схема базы данных (ER-диаграмма)')
er = doc.add_table(rows=5, cols=5)
er.style = 'Table Grid'
er.alignment = WD_TABLE_ALIGNMENT.CENTER
er_data = [
    ['sources\n─────\nid (PK)\nname\nbase_url\nis_active', '1\n→\nN', 'products\n─────\nid (PK)\nname\nbrand\ncategory\nurl\nsource_id (FK)', '1\n→\nN', 'prices\n─────\nid (PK)\nproduct_id (FK)\nprice\nrating\nreviews_count\ncollected_at\ncollection_id (FK)'],
    ['', '', '1\n↓\nN', '', ''],
    ['', '', 'ml_clusters\n─────\nid (PK)\nproduct_id (FK)\nsegment\nconfidence\nmodel_version', '', 'collections\n─────\nid (PK)\nstarted_at\nfinished_at\nstatus\ntotal_records'],
    ['', '', '', '', ''],
    ['', '', '', '↑\n1\n←\nN', ''],
]
for i, row in enumerate(er_data):
    for j, val in enumerate(row):
        c = er.rows[i].cells[j]
        set_cell(c, val, align=WD_ALIGN_PARAGRAPH.CENTER,
                 bg='EBF3FB' if (j in [0,2,4] and val.strip()) else 'FFFFFF')

new_para('')
new_para('Листинг 11 – ORM-модели базы данных (файл db/models.py)')
add_code([
    'from sqlalchemy import (',
    '    Column, Integer, String, Float, DateTime, ForeignKey, Boolean)',
    'from sqlalchemy.orm import DeclarativeBase, relationship',
    'from datetime import datetime',
    '',
    '',
    'class Base(DeclarativeBase):',
    '    pass',
    '',
    '',
    'class Source(Base):',
    '    __tablename__ = "sources"',
    '',
    '    id         = Column(Integer, primary_key=True)',
    '    name       = Column(String, nullable=False)',
    '    base_url   = Column(String, nullable=False)',
    '    is_active  = Column(Boolean, default=True)',
    '    created_at = Column(DateTime, default=datetime.utcnow)',
    '',
    '    products = relationship("Product", back_populates="source")',
    '',
    '',
    'class Product(Base):',
    '    __tablename__ = "products"',
    '',
    '    id        = Column(Integer, primary_key=True)',
    '    name      = Column(String, nullable=False)',
    '    brand     = Column(String)',
    '    category  = Column(String, nullable=False)',
    '    url       = Column(String)',
    '    source_id = Column(Integer, ForeignKey("sources.id"))',
    '    created_at = Column(DateTime, default=datetime.utcnow)',
    '',
    '    source = relationship("Source", back_populates="products")',
    '    prices = relationship("Price", back_populates="product")',
    '    cluster = relationship(',
    '        "MLCluster", back_populates="product", uselist=False)',
    '',
    '',
    'class Price(Base):',
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
    '    __tablename__ = "ml_clusters"',
    '',
    '    id            = Column(Integer, primary_key=True)',
    '    product_id    = Column(Integer, ForeignKey("products.id"),',
    '                           unique=True)',
    '    segment       = Column(String)  # Бюджетный|Средний|Премиум',
    '    confidence    = Column(Float)',
    '    model_version = Column(String)',
    '    created_at    = Column(DateTime, default=datetime.utcnow)',
    '',
    '    product = relationship("Product", back_populates="cluster")',
])

new_para(
    'Ключевым архитектурным решением является разделение товара (Product) '
    'и его цены (Price) на отдельные таблицы. Один товар может иметь '
    'неограниченное количество записей Price — по одной на каждый сеанс '
    'парсинга. Это обеспечивает полную историю изменения цен, которая '
    'используется для построения временных графиков в дашборде. '
    'Если бы цена хранилась непосредственно в таблице products, '
    'история была бы утеряна при каждом обновлении.'
)

page_break()

# 3.2
heading2('Репозиторий данных', '3.2')

new_para(
    'Файл db/repository.py реализует паттерн Repository — слой '
    'абстракции между бизнес-логикой и базой данных. Все обращения '
    'к SQLite проходят через функции репозитория, что позволяет '
    'при необходимости заменить СУБД без изменения остального кода.'
)

new_para('Листинг 12 – Инициализация и заполнение источников (файл db/repository.py)')
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
    'engine = create_engine(',
    '    DATABASE_URL,',
    '    connect_args={"check_same_thread": False}',
    ')',
    'SessionLocal = sessionmaker(bind=engine)',
    '',
    '',
    'def init_db():',
    '    """Создать все таблицы если не существуют."""',
    '    Base.metadata.create_all(engine)',
    '    _seed_sources()',
    '',
    '',
    'def _seed_sources():',
    '    """Добавить магазины в БД при первом запуске."""',
    '    with SessionLocal() as session:',
    '        if session.query(Source).count() == 0:',
    '            sources = [',
    '                Source(name="DNS",',
    '                       base_url="https://www.dns-shop.ru"),',
    '                Source(name="Ситилинк",',
    '                       base_url="https://www.citilink.ru"),',
    '                Source(name="Regard",',
    '                       base_url="https://www.regard.ru"),',
    '            ]',
    '            session.add_all(sources)',
    '            session.commit()',
])

new_para(
    'Параметр check_same_thread=False в строке подключения к SQLite '
    'необходим, поскольку Streamlit создаёт несколько потоков при '
    'обработке пользовательских запросов. По умолчанию SQLite '
    'запрещает использование соединения из нескольких потоков, '
    'что вызывало бы ошибку при работе дашборда.'
)

new_para('Листинг 13 – Сохранение товаров и запрос последних цен (файл db/repository.py)')
add_code([
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
    '                session.flush()',
    '',
    '            # Всегда создаётся новая запись цены',
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
    '    """Вернуть все товары с ПОСЛЕДНЕЙ ценой как DataFrame."""',
    '    query = """',
    '        SELECT p.id, p.name, p.brand, p.category,',
    '               s.name as source, pr.price, pr.rating,',
    '               pr.reviews_count, pr.collected_at,',
    '               mc.segment',
    '        FROM products p',
    '        JOIN sources s ON p.source_id = s.id',
    '        JOIN prices pr ON pr.product_id = p.id',
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
])

new_para(
    'SQL-запрос в функции get_all_products() использует коррелированный '
    'подзапрос для получения только последней записи цены каждого товара. '
    'Конструкция WHERE pr.collected_at = (SELECT MAX(collected_at) FROM prices '
    'WHERE product_id = p.id) фильтрует из таблицы prices единственную '
    'строку — с максимальной временной меткой — для каждого product_id. '
    'Результат немедленно конвертируется в pandas.DataFrame через '
    'pd.read_sql(), что устраняет необходимость ручного преобразования '
    'объектов ORM в структуры данных Python.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 4
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Аналитический модуль (analytics)', '4')

new_para(
    'Аналитический модуль реализован в файле analytics/analytics.py '
    'и содержит пять чистых функций, каждая из которых принимает '
    'pandas.DataFrame и возвращает агрегированный pandas.DataFrame. '
    'Такой интерфейс обеспечивает независимость аналитики от '
    'источника данных и упрощает тестирование.'
)

new_para('Листинг 14 – Функции аналитического модуля (файл analytics/analytics.py)')
add_code([
    'import pandas as pd',
    '',
    '',
    'def price_index(df: pd.DataFrame) -> pd.DataFrame:',
    '    """',
    '    Ценовой индекс: отклонение средней цены магазина',
    '    от рыночной (%).',
    '    Положительное значение = магазин дороже рынка.',
    '    """',
    '    if df.empty or "source" not in df.columns:',
    '        return pd.DataFrame()',
    '    avg_by_source = df.groupby("source")["price"].mean()',
    '    market_avg = df["price"].mean()',
    '    if market_avg == 0:',
    '        return pd.DataFrame()',
    '    index = ((avg_by_source - market_avg) / market_avg * 100).round(2)',
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
    '    return df.groupby(["date", "source"])["price"].mean().reset_index()',
    '',
    '',
    'def top_by_reviews(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:',
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
    'def top_by_rating(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:',
    '    """Топ-N товаров по рейтингу (только с рейтингом > 0)."""',
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
    '            Товаров=("id", "count"),',
    '            Средняя_цена=("price", "mean"),',
    '            Средний_рейтинг=("rating", "mean"),',
    '            Всего_отзывов=("reviews_count", "sum"),',
    '        )',
    '        .round(2)',
    '    )',
    '',
    '',
    'def price_comparison_by_source(df: pd.DataFrame) -> pd.DataFrame:',
    '    """Сравнение цен по магазинам для каждой категории."""',
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
    'Функция price_index() вычисляет ценовой индекс по формуле '
    'отклонения от рыночного среднего: (средняя цена магазина — '
    'средняя цена рынка) / средняя цена рынка × 100 %. '
    'Положительное значение индекса означает, что магазин '
    'в среднем дороже рынка. Например, если индекс DNS равен '
    '+3.7 %, цены DNS в среднем на 3.7 % выше среднерыночных '
    'в выбранной категории.'
)

new_para(
    'Функция price_dynamics() использует метод pandas dt.date '
    'для группировки временных меток по дате, что позволяет '
    'строить дневные графики динамики цен. Данные истории цен '
    'поступают из функции get_price_history() репозитория, '
    'возвращающей все записи таблицы prices без фильтрации '
    'по последнему сеансу.'
)

new_para(
    'Функция cross_category_summary() применяет именованные '
    'агрегации (Named Aggregations), введённые в pandas 0.25: '
    'синтаксис Товаров=("id", "count") задаёт одновременно '
    'имя результирующего столбца и применяемую агрегирующую '
    'функцию, что делает код компактным и самодокументируемым.'
)

tbl_caption('Таблица 5 – Описание аналитических функций модуля')
an_table = doc.add_table(rows=6, cols=3)
an_table.style = 'Table Grid'
an_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Функция', 'Входные данные', 'Результат']):
    set_cell(an_table.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
an_data = [
    ('price_index(df)', 'Текущие цены всех товаров', 'Отклонение (%) средней цены каждого магазина от рыночной'),
    ('price_dynamics(df)', 'Полная история цен', 'Средняя цена по дням и магазинам для временного графика'),
    ('top_by_reviews(df, n)', 'Текущие цены с отзывами', 'Топ-N товаров с наибольшим количеством отзывов'),
    ('cross_category_summary(df)', 'Текущие цены всех категорий', 'Агрегация по категориям: кол-во товаров, средняя цена, рейтинг'),
    ('price_comparison_by_source(df)', 'Текущие цены', 'Мин./средн./макс. цена по категориям и магазинам'),
]
for i, row in enumerate(an_data):
    for j, val in enumerate(row):
        set_cell(an_table.rows[i+1].cells[j], val)

new_para('')
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 5
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Модуль машинного обучения (ml)', '5')

new_para(
    'Модуль машинного обучения реализует двухэтапный подход к '
    'сегментации товаров. На первом этапе алгоритм KMeans выполняет '
    'кластеризацию без учителя и размечает товары на три '
    'ценовых сегмента. На втором этапе классификатор '
    'Random Forest обучается на полученных метках и становится '
    'основным предиктором для новых товаров, показывая более '
    'точные и устойчивые результаты.'
)

# 5.1
heading2('Кластеризация методом KMeans', '5.1')

new_para(
    'Кластеризация реализована в файле ml/clustering.py. '
    'В качестве признаков используются три числовых характеристики '
    'товара: цена (price), рейтинг (rating) и количество '
    'отзывов (reviews_count). Перед обучением данные '
    'нормализуются MinMaxScaler, чтобы цена в десятках тысяч '
    'рублей не доминировала над рейтингом в диапазоне 0–5.'
)

new_para('Листинг 15 – Обучение KMeans-модели (файл ml/clustering.py)')
add_code([
    'import os',
    'import pandas as pd',
    'import numpy as np',
    'import joblib',
    'from sklearn.cluster import KMeans',
    'from sklearn.preprocessing import MinMaxScaler',
    'from sklearn.metrics import silhouette_score',
    '',
    'os.makedirs("ml/models", exist_ok=True)',
    '',
    'MODEL_PATH  = "ml/models/kmeans.pkl"',
    'SCALER_PATH = "ml/models/scaler.pkl"',
    'FEATURES    = ["price", "rating", "reviews_count"]',
    'SEGMENT_NAMES = {0: "Бюджетный", 1: "Средний", 2: "Премиум"}',
    '',
    '',
    'def train_kmeans(df: pd.DataFrame = None) -> dict:',
    '    """Обучить KMeans на текущих данных из БД."""',
    '    if df is None:',
    '        from db.repository import get_all_products',
    '        df = get_all_products()',
    '',
    '    if df.empty or len(df) < 10:',
    '        return {"error": "Недостаточно данных (минимум 10 товаров)"}',
    '',
    '    X = df[FEATURES].dropna()',
    '',
    '    # Нормализация: приводим все признаки к диапазону [0, 1]',
    '    scaler = MinMaxScaler()',
    '    X_scaled = scaler.fit_transform(X)',
    '',
    '    # Обучение: 3 кластера, 10 случайных инициализаций',
    '    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)',
    '    labels = kmeans.fit_predict(X_scaled)',
    '',
    '    # Оценка качества кластеризации',
    '    score = silhouette_score(X_scaled, labels)',
    '',
    '    # Упорядочить кластеры по цене:',
    '    # 0 = Бюджетный, 1 = Средний, 2 = Премиум',
    '    centers = kmeans.cluster_centers_',
    '    order = np.argsort(centers[:, 0])  # сортировка по признаку price',
    '    label_map = {order[i]: i for i in range(3)}',
    '    labels_named = [SEGMENT_NAMES[label_map[l]] for l in labels]',
    '',
    '    # Сохранение модели и масштабировщика на диск',
    '    joblib.dump(kmeans, MODEL_PATH)',
    '    joblib.dump(scaler, SCALER_PATH)',
    '',
    '    _save_clusters(df.iloc[X.index], labels_named)',
    '',
    '    return {',
    '        "silhouette_score": round(score, 4),',
    '        "n_samples": len(X)',
    '    }',
])

new_para(
    'Параметр n_init=10 означает, что алгоритм KMeans запускается '
    'десять раз с различными начальными центроидами, после чего '
    'выбирается лучший результат по критерию инерции (суммарное '
    'квадратичное расстояние объектов до своих центроидов). '
    'Это снижает вероятность попасть в локальный минимум при '
    'случайной инициализации.'
)

new_para(
    'Силуэтный коэффициент (silhouette_score) является основной '
    'метрикой качества кластеризации. Значение варьируется от '
    '−1 до +1: значения близкие к +1 указывают на чёткое разделение '
    'кластеров, значения около 0 — на перекрывающиеся кластеры, '
    'отрицательные значения свидетельствуют об ошибочной '
    'кластеризации. Для ценовых данных электроники '
    'типичное значение составляет 0.55–0.75.'
)

new_para('Листинг 16 – Предсказание сегмента с резервной эвристикой (файл ml/clustering.py)')
add_code([
    'def predict_segment(price: float,',
    '                    rating: float,',
    '                    reviews: int) -> str:',
    '    """Предсказать ценовой сегмент для нового товара."""',
    '    if not os.path.exists(MODEL_PATH) or \\',
    '       not os.path.exists(SCALER_PATH):',
    '        # Ценовая эвристика при отсутствии обученной модели',
    '        if price < 5000:',
    '            return "Бюджетный"',
    '        elif price < 30000:',
    '            return "Средний"',
    '        else:',
    '            return "Премиум"',
    '',
    '    kmeans = joblib.load(MODEL_PATH)',
    '    scaler = joblib.load(SCALER_PATH)',
    '    X = np.array([[price, rating, reviews]])',
    '    X_scaled = scaler.transform(X)',
    '    label = int(kmeans.predict(X_scaled)[0])',
    '',
    '    # Восстановить маппинг кластер -> сегмент',
    '    centers = kmeans.cluster_centers_',
    '    order = np.argsort(centers[:, 0])',
    '    label_map = {order[i]: i for i in range(3)}',
    '    return SEGMENT_NAMES[label_map[label]]',
])

new_para(
    'Функция predict_segment() реализует принцип graceful degradation: '
    'при отсутствии обученной модели на диске она применяет простую '
    'ценовую эвристику (до 5 000 рублей — «Бюджетный», до '
    '30 000 рублей — «Средний», выше — «Премиум»), а не возвращает '
    'ошибку. Это позволяет дашборду корректно работать с формой '
    'классификации даже до первого обучения модели.'
)

page_break()

# 5.2
heading2('Классификатор Random Forest', '5.2')

new_para(
    'Классификатор реализован в файле ml/classifier.py. '
    'Алгоритм Random Forest обучается на метках сегментов, '
    'полученных от KMeans, и затем используется как основной '
    'предиктор. Преимущество перед прямым применением KMeans '
    'состоит в том, что Random Forest работает быстрее при '
    'инференсе и показывает более стабильные результаты '
    'на новых данных.'
)

new_para('Листинг 17 – Обучение Random Forest с кросс-валидацией (файл ml/classifier.py)')
add_code([
    'import os',
    'import pandas as pd',
    'import joblib',
    'from sklearn.ensemble import RandomForestClassifier',
    'from sklearn.model_selection import StratifiedKFold, cross_val_score',
    'from sklearn.metrics import accuracy_score, f1_score, confusion_matrix',
    '',
    'os.makedirs("ml/models", exist_ok=True)',
    'RF_PATH  = "ml/models/rf_classifier.pkl"',
    'FEATURES = ["price", "rating", "reviews_count"]',
    '',
    '',
    'def train_classifier() -> dict:',
    '    """Обучить Random Forest на метках KMeans из БД."""',
    '    from db.repository import get_all_products',
    '    df = get_all_products()',
    '    df = df.dropna(subset=FEATURES + ["segment"])',
    '',
    '    if len(df) < 15:',
    '        return {"error": "Сначала запустите KMeans-кластеризацию."}',
    '',
    '    X = df[FEATURES]',
    '    y = df["segment"]',
    '',
    '    rf = RandomForestClassifier(',
    '        n_estimators=100,   # 100 деревьев решений',
    '        random_state=42,',
    '        class_weight="balanced",  # компенсация дисбаланса классов',
    '        n_jobs=-1           # использовать все ядра CPU',
    '    )',
    '',
    '    # Стратифицированная кросс-валидация',
    '    cv = StratifiedKFold(',
    '        n_splits=min(5, len(y.unique())),',
    '        shuffle=True,',
    '        random_state=42',
    '    )',
    '    cv_scores = cross_val_score(rf, X, y, cv=cv, scoring="accuracy")',
    '',
    '    # Финальное обучение на всех данных',
    '    rf.fit(X, y)',
    '    y_pred = rf.predict(X)',
    '',
    '    acc = accuracy_score(y, y_pred)',
    '    f1  = f1_score(y, y_pred, average="macro")',
    '    cm  = confusion_matrix(y, y_pred)',
    '',
    '    joblib.dump(rf, RF_PATH)',
    '',
    '    return {',
    '        "accuracy":         round(acc, 4),',
    '        "f1_macro":         round(f1, 4),',
    '        "cv_mean":          round(cv_scores.mean(), 4),',
    '        "cv_std":           round(cv_scores.std(), 4),',
    '        "confusion_matrix": cm.tolist(),',
    '    }',
])

new_para(
    'Параметр class_weight="balanced" критически важен для корректного '
    'обучения на несбалансированных данных. В реальных каталогах '
    'магазинов количество бюджетных товаров значительно превышает '
    'количество премиальных. Без балансировки модель оптимизировалась '
    'бы под большинство и игнорировала редкие классы. '
    'При balanced каждый класс получает вес, обратно пропорциональный '
    'его частоте в обучающей выборке.'
)

new_para(
    'Стратифицированная кросс-валидация (StratifiedKFold) сохраняет '
    'пропорции классов в каждом разбиении, что даёт объективную '
    'оценку качества модели. Параметр n_splits=min(5, len(y.unique())) '
    'автоматически уменьшает число блоков до количества уникальных '
    'классов, если классов меньше пяти, что предотвращает ошибку '
    'при малых наборах данных.'
)

new_para('Листинг 18 – Предсказание сегмента с откатом на KMeans (файл ml/classifier.py)')
add_code([
    'def predict_segment(price: float,',
    '                    rating: float,',
    '                    reviews: int) -> str:',
    '    """Предсказать сегмент через Random Forest.',
    '    При отсутствии модели — откат на KMeans.',
    '    """',
    '    if not os.path.exists(RF_PATH):',
    '        from ml.clustering import predict_segment as kmeans_predict',
    '        return kmeans_predict(price, rating, reviews)',
    '',
    '    rf = joblib.load(RF_PATH)',
    '    X = pd.DataFrame(',
    '        [[price, rating, reviews]],',
    '        columns=FEATURES',
    '    )',
    '    return rf.predict(X)[0]',
])

new_para(
    'Иерархия откатов при предсказании реализована по цепочке: '
    'Random Forest → KMeans → ценовая эвристика. Это гарантирует, '
    'что система всегда вернёт осмысленный результат вне зависимости '
    'от того, какие модели обучены. Пользователь дашборда видит '
    'предсказание сразу после загрузки данных, ещё до обучения '
    'каких-либо ML-моделей.'
)

tbl_caption('Таблица 6 – Метрики качества ML-моделей')
ml_table = doc.add_table(rows=4, cols=4)
ml_table.style = 'Table Grid'
ml_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(['Модель', 'Метрика', 'Типичное значение', 'Интерпретация']):
    set_cell(ml_table.rows[0].cells[i], h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, bg='D9D9D9')
ml_data = [
    ('KMeans', 'Silhouette Score', '0.55–0.75', 'Чёткость разделения кластеров'),
    ('Random Forest', 'Accuracy', '0.90–0.98', 'Доля верных предсказаний'),
    ('Random Forest', 'F1-macro', '0.88–0.96', 'Среднее F1 по всем классам (с учётом дисбаланса)'),
]
for i, row in enumerate(ml_data):
    for j, val in enumerate(row):
        set_cell(ml_table.rows[i+1].cells[j], val, align=WD_ALIGN_PARAGRAPH.CENTER if j in [1,2] else WD_ALIGN_PARAGRAPH.LEFT)

new_para('')
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# РАЗДЕЛ 6
# ═══════════════════════════════════════════════════════════════════════════════

heading1('Модуль логирования', '6')

new_para(
    'Модуль логирования реализован в файле logger/logger.py. '
    'Он обеспечивает единую точку конфигурации логгеров для '
    'всех компонентов системы с дублированием вывода в файл '
    'и в консоль.'
)

new_para('Листинг 19 – Настройка логирования (файл logger/logger.py)')
add_code([
    'import logging',
    'import os',
    'from datetime import datetime',
    '',
    'os.makedirs("logs", exist_ok=True)',
    '',
    '',
    'def setup_logger(name: str,',
    '                  level=logging.INFO) -> logging.Logger:',
    '    """Создать логгер с выводом в файл и консоль."""',
    '    logger = logging.getLogger(name)',
    '    if logger.handlers:',
    '        return logger',
    '',
    '    logger.setLevel(level)',
    '',
    '    # Формат: 2026-05-10 14:32:01 [INFO] runner: сообщение',
    '    fmt = logging.Formatter(',
    '        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",',
    '        datefmt="%Y-%m-%d %H:%M:%S"',
    '    )',
    '',
    '    # Вывод в файл с датой в имени',
    '    today = datetime.now().strftime("%Y-%m-%d")',
    '    fh = logging.FileHandler(',
    '        f"logs/scraper_{today}.log",',
    '        encoding="utf-8"',
    '    )',
    '    fh.setFormatter(fmt)',
    '    logger.addHandler(fh)',
    '',
    '    # Вывод в консоль',
    '    ch = logging.StreamHandler()',
    '    ch.setFormatter(fmt)',
    '    logger.addHandler(ch)',
    '',
    '    return logger',
    '',
    '',
    'def setup_all_loggers():',
    '    """Инициализировать логгеры для всех модулей."""',
    '    names = [',
    '        "runner", "DNS", "Ситилинк", "Regard",',
    '        "analytics", "ml"',
    '    ]',
    '    for name in names:',
    '        setup_logger(name)',
])

new_para(
    'Проверка if logger.handlers предотвращает дублирование обработчиков '
    'при повторных вызовах setup_logger() с одним именем. Это важно '
    'в Streamlit, где функции могут вызываться многократно при '
    'каждом взаимодействии пользователя со страницей. Без этой '
    'проверки каждое нажатие кнопки в дашборде добавляло бы '
    'новый обработчик, и одно сообщение выводилось бы '
    'несколько раз.'
)

new_para(
    'Файлы логов создаются с датой в имени '
    '(logs/scraper_2026-05-10.log), что обеспечивает автоматическую '
    'ротацию по дням. Кодировка utf-8 обязательна для корректного '
    'отображения кириллических символов в именах категорий и '
    'товаров в операционных системах Windows, где кодировка '
    'файловой системы по умолчанию отличается от UTF-8.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# ЗАКЛЮЧЕНИЕ
# ═══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 12, 6)
add_text(p, 'ЗАКЛЮЧЕНИЕ', 14)

new_para(
    'В настоящем отчёте представлено подробное описание бэкенда '
    'системы мониторинга цен «ЦенМонитор». Система реализована '
    'на языке Python 3.11 и состоит из четырёх взаимодействующих '
    'модулей: парсинга, базы данных, аналитики и машинного обучения.'
)

new_para(
    'В рамках модуля парсинга разработан базовый класс BaseParser '
    'с использованием библиотеки Playwright для рендеринга '
    'JavaScript-страниц. Реализован комплекс мер обхода '
    'антифрод-систем: имитация реального браузера через '
    'корректный User-Agent, настройку локали, размера viewport, '
    'прокрутку страниц и временны́е задержки между запросами. '
    'На основе базового класса созданы три специализированных '
    'парсера для магазинов DNS, Ситилинк и Regard с учётом '
    'особенностей HTML-структуры каждого сайта.'
)

new_para(
    'Модуль базы данных построен на SQLAlchemy ORM с применением '
    'паттерна Repository. Схема базы данных из пяти таблиц '
    'обеспечивает хранение полной истории цен, что является '
    'ключевым требованием для аналитики динамики рынка.'
)

new_para(
    'Аналитический модуль предоставляет пять чистых функций '
    'для расчёта ценового индекса, динамики цен, рейтингов '
    'и сводных таблиц по категориям. Все функции работают '
    'с pandas.DataFrame, что обеспечивает простую интеграцию '
    'с визуализациями Plotly в дашборде.'
)

new_para(
    'Модуль машинного обучения реализует двухэтапную сегментацию: '
    'кластеризацию KMeans для первичной разметки данных и '
    'классификатор Random Forest для последующего предсказания. '
    'Реализована иерархия откатов, гарантирующая работу '
    'предиктора даже при отсутствии обученных моделей.'
)

new_para(
    'Разработанный бэкенд обеспечивает все ключевые функции '
    'системы мониторинга цен и может быть расширен '
    'дополнительными источниками данных, категориями товаров '
    'и аналитическими метриками без изменения существующей '
    'архитектуры.'
)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# СПИСОК ИСТОЧНИКОВ
# ═══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
para_fmt(p, WD_ALIGN_PARAGRAPH.CENTER, 0, 12, 6)
add_text(p, 'СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ', 14)

refs = [
    'Документация Playwright for Python [Электронный ресурс]. – URL: https://playwright.dev/python/docs/intro (дата обращения: 10.05.2026).',
    'Официальная документация SQLAlchemy 2.0 [Электронный ресурс]. – URL: https://docs.sqlalchemy.org/en/20/ (дата обращения: 10.05.2026).',
    'Официальная документация pandas 2.1 [Электронный ресурс]. – URL: https://pandas.pydata.org/docs/ (дата обращения: 10.05.2026).',
    'Scikit-learn: Machine Learning in Python / F. Pedregosa [и др.] // Journal of Machine Learning Research. – 2011. – Vol. 12. – С. 2825–2830.',
    'Документация Beautiful Soup 4 [Электронный ресурс]. – URL: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ (дата обращения: 10.05.2026).',
    'Агеев, М. С. Парсинг веб-страниц: методы и инструменты / М. С. Агеев. – Москва: ДМК Пресс, 2022. – 320 с.',
    'Рашка, С. Python и машинное обучение / С. Рашка, В. Мирджалили; пер. с англ. А. В. Логунова. – 3-е изд. – Москва: ДМК Пресс, 2023. – 840 с.',
    'Документация Streamlit [Электронный ресурс]. – URL: https://docs.streamlit.io/ (дата обращения: 10.05.2026).',
]

for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph()
    para_fmt(p, WD_ALIGN_PARAGRAPH.JUSTIFY, 0, 0, 0)
    add_text(p, f'{i}. {ref}', 14)

# ─── Нумерация страниц ────────────────────────────────────────────────────────
add_footer_page_numbers()

# ─── Сохранение ───────────────────────────────────────────────────────────────
output_path = '/home/user/Parsing/Отчёт_Бэкенд_ЦенМонитор.docx'
doc.save(output_path)
print(f'Документ сохранён: {output_path}')
