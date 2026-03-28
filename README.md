# ЦенМонитор — Система мониторинга цен конкурентов

Автоматизированная система парсинга и анализа цен на электронику с интернет-магазинов **DNS**, **Ситилинк** и **Regard** с интерактивным дашбордом и ML-сегментацией товаров.

**Авторы:** Илья Головчиц, Егор Вахрушев (ЭУ-430)

---

## Возможности

- Автоматический сбор цен с 3 магазинов по 3 категориям (оперативная память, видеокарты, смартфоны)
- История цен и отслеживание динамики
- ML-кластеризация товаров по ценовым сегментам (Бюджетный / Средний / Премиум)
- Классификация нового товара по сегменту (Random Forest)
- Интерактивный веб-дашборд на Streamlit с фильтрами и графиками
- Экспорт данных в CSV
- Логирование всех операций

---

## Структура проекта

```
Parsing/
├── dashboard/               # Веб-дашборд (Streamlit)
│   ├── app.py               # Точка входа
│   ├── pages/               # Страницы дашборда
│   │   ├── 1_Главный_дашборд.py
│   │   ├── 2_Аналитика.py
│   │   ├── 3_Сравнение_категорий.py
│   │   ├── 4_ML_сегментация.py
│   │   └── 5_Все_товары.py
│   └── components/          # Переиспользуемые компоненты
│       ├── filters.py
│       ├── charts.py
│       └── stat_cards.py
├── scraper/                 # Модуль парсинга
│   ├── base.py              # Базовый класс парсера
│   ├── dns_parser.py        # Парсер DNS
│   ├── citilink_parser.py   # Парсер Ситилинк
│   ├── regard_parser.py     # Парсер Regard
│   └── runner.py            # Запуск всех парсеров
├── db/                      # База данных
│   ├── models.py            # SQLAlchemy ORM-модели
│   └── repository.py        # Репозиторий (CRUD)
├── ml/                      # ML-модуль
│   ├── clustering.py        # KMeans кластеризация
│   ├── classifier.py        # Random Forest классификатор
│   └── models/              # Сохранённые модели (.pkl)
├── analytics/               # Аналитические функции
│   └── analytics.py
├── logger/                  # Логирование
│   └── logger.py
├── data/                    # SQLite база данных (prices.db)
├── logs/                    # Файлы логов
├── backups/                 # Резервные копии БД
└── requirements.txt
```

---

## Установка

### Требования

- Python **3.11** или выше
- pip (входит в стандартную поставку Python)

### Шаг 1 — Клонирование репозитория

```bash
git clone https://github.com/HolyCapybara1/Parsing.git
cd Parsing
```

### Шаг 2 — Создание виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Шаг 3 — Установка зависимостей

```bash
pip install -r requirements.txt
```

> Установка может занять 2–5 минут, так как включает scikit-learn, plotly и streamlit.

---

## Запуск

### Запуск веб-дашборда

Из корневой папки проекта выполните:

```bash
streamlit run dashboard/app.py
```

После этого браузер автоматически откроется по адресу:
```
http://localhost:8501
```

### Запуск парсинга из командной строки

Если нужно запустить сбор данных без дашборда:

```bash
python -m scraper.runner
```

или:

```bash
python scraper/runner.py
```

> Парсинг 3 магазинов × 3 категории занимает **5–15 минут** из-за задержек между запросами (защита от блокировки).

---

## Использование дашборда

1. **Откройте** `http://localhost:8501` в браузере
2. Перейдите на страницу **Главный дашборд**
3. Нажмите кнопку **Собрать данные** — запустится парсинг
4. После завершения сбора страница обновится автоматически
5. Используйте фильтры в левой панели для выбора категории, магазина, бренда и ценового диапазона

### Страницы дашборда

| Страница | Описание |
|---|---|
| Главный дашборд | Ключевые метрики, гистограмма цен, сравнение магазинов |
| Аналитика | Динамика цен, ценовой индекс, топ товаров |
| Сравнение категорий | Сводная таблица и боксплот по категориям |
| ML-сегментация | Кластеры KMeans, форма классификации нового товара |
| Все товары | Полная таблица с поиском и экспортом в CSV |

### ML-сегментация

1. Перейдите на страницу **ML-сегментация**
2. Нажмите **Обучить KMeans** — система кластеризует все товары на 3 сегмента
3. (Опционально) Нажмите **Обучить Random Forest** — для более точной классификации
4. Используйте форму внизу страницы для определения сегмента нового товара

---

## Технологии

| Компонент | Технология |
|---|---|
| Парсинг | requests, BeautifulSoup4, lxml |
| База данных | SQLite + SQLAlchemy ORM |
| Обработка данных | pandas, numpy |
| ML | scikit-learn (KMeans, RandomForest), joblib |
| Дашборд | Streamlit |
| Графики | Plotly Express |

---

## Возможные ошибки

**`ModuleNotFoundError`** — убедитесь, что виртуальное окружение активировано и зависимости установлены:
```bash
pip install -r requirements.txt
```

**Парсинг вернул 0 товаров** — магазины могут блокировать автоматические запросы. Попробуйте позже или используйте демо-данные (см. ниже).

**Ошибка при обучении ML** — сначала нужно собрать данные через парсинг (минимум 10 товаров).

### Загрузка демо-данных (без парсинга)

Если сайты недоступны, можно сгенерировать тестовые данные:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from db.repository import init_db, save_products, SessionLocal
from db.models import Collection
from datetime import datetime
import random

init_db()
with SessionLocal() as s:
    col = Collection(started_at=datetime.utcnow(), status='running')
    s.add(col); s.commit(); cid = col.id

categories = ['Оперативная память', 'Видеокарты', 'Смартфоны']
sources = ['DNS', 'Ситилинк', 'Regard']
brands = ['Samsung', 'Kingston', 'Crucial', 'NVIDIA', 'AMD', 'Apple', 'Xiaomi']

for src in sources:
    products = []
    for i in range(30):
        cat = random.choice(categories)
        price = random.randint(2000, 80000)
        products.append({
            'name': f'{random.choice(brands)} {cat} {i+1}',
            'brand': random.choice(brands),
            'category': cat,
            'price': float(price),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'reviews_count': random.randint(10, 500),
            'url': '',
        })
    save_products(products, src, cid)

with SessionLocal() as s:
    col = s.get(Collection, cid)
    col.status = 'success'; col.total_records = 90
    col.finished_at = datetime.utcnow(); s.commit()

print('Демо-данные загружены: 90 товаров из 3 магазинов')
"
```

---

## Лицензия

Учебный проект. Использование только в образовательных целях.
