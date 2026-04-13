import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from db.repository import get_all_products, init_db
from scraper.runner import ALL_CATEGORIES, ALL_SOURCES

st.set_page_config(page_title="Парсинг — ЦенМонитор", layout="wide")
init_db()

st.header("Сбор данных")


def _cat_word(n):
    if n % 10 == 1 and n % 100 != 11:
        return "категория"
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return "категории"
    return "категорий"


def _src_word(n):
    if n % 10 == 1 and n % 100 != 11:
        return "магазин"
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return "магазина"
    return "магазинов"


# ── Инициализация session state ────────────────────────────────────────────
if "selected_categories" not in st.session_state:
    st.session_state["selected_categories"] = ["Оперативная память", "Видеокарты", "Смартфоны"]
if "show_cat_picker" not in st.session_state:
    st.session_state["show_cat_picker"] = False

# ── Настройки сбора данных ─────────────────────────────────────────────────
with st.expander("Настройки сбора данных", expanded=True):
    col_cat, col_src = st.columns([3, 2])

    with col_cat:
        st.subheader("Категории товаров")

        # Показываем выбранные категории как теги с кнопкой удаления
        cats = list(st.session_state["selected_categories"])
        if cats:
            rows = [cats[i:i + 4] for i in range(0, len(cats), 4)]
            for row in rows:
                tag_cols = st.columns(len(row))
                for i, cat in enumerate(row):
                    if tag_cols[i].button(
                        f"✕  {cat}",
                        key=f"del_{cat}",
                        use_container_width=True,
                        help="Нажмите, чтобы убрать категорию",
                    ):
                        st.session_state["selected_categories"].remove(cat)
                        st.rerun()
        else:
            st.warning("Не выбрана ни одна категория. Нажмите «Добавить».")

        # Кнопка «Добавить»
        btn_col, _ = st.columns([1, 3])
        if btn_col.button("➕ Добавить категории", use_container_width=True):
            st.session_state["show_cat_picker"] = not st.session_state["show_cat_picker"]

        # Выпадающий пикер категорий
        if st.session_state["show_cat_picker"]:
            remaining = [c for c in ALL_CATEGORIES if c not in st.session_state["selected_categories"]]
            if remaining:
                with st.container(border=True):
                    to_add = st.multiselect(
                        "Категории для добавления:",
                        options=remaining,
                        key="cats_to_add_picker",
                        placeholder="Выберите одну или несколько...",
                    )
                    ok_col, cancel_col, _ = st.columns([1, 1, 4])
                    if ok_col.button("Добавить", type="primary", key="confirm_add_cats"):
                        for cat in to_add:
                            if cat not in st.session_state["selected_categories"]:
                                st.session_state["selected_categories"].append(cat)
                        st.session_state["show_cat_picker"] = False
                        st.rerun()
                    if cancel_col.button("Отмена", key="cancel_add_cats"):
                        st.session_state["show_cat_picker"] = False
                        st.rerun()
            else:
                st.info("Все доступные категории уже добавлены.")
                if st.button("Закрыть", key="close_cat_picker"):
                    st.session_state["show_cat_picker"] = False
                    st.rerun()

    with col_src:
        st.subheader("Магазины")
        selected_sources = st.multiselect(
            "Выберите магазины",
            options=ALL_SOURCES,
            default=ALL_SOURCES,
        )

    # Итоги и кнопка запуска
    selected_categories = st.session_state["selected_categories"]

    if not selected_categories:
        st.warning("Выберите хотя бы одну категорию.")
    elif not selected_sources:
        st.warning("Выберите хотя бы один магазин.")
    else:
        n_pages = len(selected_categories) * len(selected_sources)
        st.info(
            f"Будет собрано: **{len(selected_categories)}** {_cat_word(len(selected_categories))} "
            f"× **{len(selected_sources)}** {_src_word(len(selected_sources))} "
            f"≈ {n_pages * 5} страниц. "
            f"Примерное время: **{n_pages * 2}–{n_pages * 5} мин.**"
        )

        if st.button("▶ Собрать данные", type="primary", use_container_width=True):
            with st.spinner("Идёт парсинг... Не закрывайте страницу."):
                from scraper.runner import run_all
                from logger.logger import setup_all_loggers
                setup_all_loggers()
                result = run_all(
                    categories=selected_categories,
                    sources=selected_sources,
                )
            if result["total"] > 0:
                st.success(
                    f"Готово! Собрано **{result['total']}** товаров "
                    f"из **{result['sources']}** магазинов по **{result['categories']}** категориям."
                )
            else:
                st.error(
                    "Товары не найдены. Возможные причины:\n"
                    "- Сайты заблокировали запросы (попробуйте позже)\n"
                    "- Playwright не установлен (см. инструкцию ниже)\n"
                    "- Проблемы с интернетом"
                )
            st.rerun()

# ── Статус данных ─────────────────────────────────────────────────────────
st.divider()
df = get_all_products()

if df.empty:
    st.warning("Данных пока нет. Настройте параметры выше и нажмите **Собрать данные**.")
    st.markdown("""
    #### Если парсинг не работает — установите Playwright:
    В терминале VS Code выполните:
    ```
    pip install playwright
    playwright install chromium
    ```
    """)
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Товаров в базе", f"{len(df):,}")
    col2.metric("Магазинов", f"{df['source'].nunique()}")
    col3.metric("Категорий", f"{df['category'].nunique()}")
    col4.metric("Последнее обновление", str(df["collected_at"].max())[:16])
    st.info("Перейдите в раздел **Аналитика** для просмотра графиков и статистики.")
