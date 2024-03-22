from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import logging
from selenium.webdriver.common.action_chains import ActionChains

def select_dropdown_option(driver, input_element, option_text):
    input_element.click()
    time.sleep(1)

    dropdown_selector = "div.el-select-dropdown li.el-select-dropdown__item"
    dropdown_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, dropdown_selector))
    )

    for item in dropdown_elements:
        if item.text == option_text:
            scroll_to_element(driver, item)
            time.sleep(1)
            item.click()
            break

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)

def clean_text(text):
    if not text:
        return text

    # Удаление пробелов, апострофов и кавычек в начале и в конце строки
    text = text.strip()

    # Удаление всех типов кавычек в начале и в конце строки
    quotes = ["'", '"', '“', '”', '‘', '’']
    while len(text) > 0 and text[0] in quotes:
        text = text[1:].strip()
    while len(text) > 0 and text[-1] in quotes:
        text = text[:-1].strip()

    return text

#Вам нужно убедиться, что весь текст, отправляемый в браузер, не содержит символов за пределами BMP. Можно добавить функцию, которая будет очищать текст от таких символов:
def clean_non_bmp(text):
    return ''.join(char for char in text if char.isprintable() and ord(char) <= 0xFFFF)


def print_events(events):
    for event in events:
        if event.publication_mark == 0:
            print("Отметка о публикации:", event.publication_mark)
            print("Заголовок:", event.title)
            print("Описание:", event.description)
            print("Тип:", event.type)
            print("Цена:", event.price)
            print("Дата:", event.date)
            print("Время:", event.time)
            print("Город:", event.city)
            print("Название заведения:", event.venue_name)
            print("Адрес:", event.address)
            print("Источник:", event.source)
            print("Контакты:", event.contacts)
            print("Фото URL:", event.photo_url)
            print("Видео URL:", event.video_url)
            print("---------------")


def format_time(time_value):
    """
    Преобразует значение времени в формат 'ЧЧ:ММ'.
    Если значение уже в правильном формате или не является строкой, возвращает исходное значение.
    """
    # Проверяем, является ли time_value строкой и содержит ли она только часы
    if isinstance(time_value, str) and len(time_value) <= 2 and time_value.isdigit():
        # Добавляем ":00" к значению времени
        return f"{time_value}:00"
    else:
        # Если time_value не соответствует ожидаемому формату, используем его как есть
        return time_value


def print_events_to_publish(events):
    # Заголовки для таблицы
    headers = ["Отметка о публикации", "Название публикации", "Дата публикации"]
    print(f"{headers[0]:<25} | {headers[1]:<50} | {headers[2]:<20}")

    # Фильтрация событий, готовых к публикации
    events_to_publish = [event for event in events if event.publication_mark == 0]

    for event in events_to_publish:
        publication_mark = event.publication_mark
        title = event.title
        date = event.date.strftime("%Y-%m-%d") if hasattr(event, 'date') and event.date else "Нет даты"
        print(f"{publication_mark:<25} | {title:<50} | {date:<20}")

    print(f"\nВсего событий, готовых к публикации: {len(events_to_publish)}")

def close_calendar_with_js(driver):
    script = """
    var calendar = document.querySelector('.el-picker-panel__body');
    if (calendar) {
        calendar.style.display = 'none';
    }
    """
    driver.execute_script(script)

def scroll_to_element(driver, element):
    # Функция для прокрутки до элемента
    driver.execute_script("arguments[0].scrollIntoView();", element)

# Функция для очистки текста от пробелов и кавычек в начале и конце

def clean_text(text):
    original_text = text  # Сохраняем исходный текст для логирования
    if not text:
        return text

    pattern = r"[^a-zA-Zа-яА-Я0-9\n.,!?() \-іїєґІЇЄҐ'’]"
    cleaned_text = re.sub(pattern, " ", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    if original_text != cleaned_text:
        logging.warning(f"Text modified during cleaning: Original '{original_text}', Cleaned '{cleaned_text}'")

    return cleaned_text if cleaned_text else text
