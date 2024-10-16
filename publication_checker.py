# publication_checker.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

# Импортируем необходимые константы из config.py
from config import SLEEP_AFTER_ACTION, EVENTS_LIST_URL, SEARCH_INPUT_SELECTOR, PAGINATION_SELECTOR, EVENT_TITLE_SELECTOR, EVENT_DATE_SELECTOR, EVENT_TIME_SELECTOR

def check_publication_success(driver, event):
    """Основная функция проверки успешности публикации"""
    start_time = time.time()
    timeout = 300  # 5 минут

    if not navigate_to_events_list(driver):
        return False

    if not search_for_event(driver, event['Заголовок']):
        return False

    result = check_event_in_list(driver, event)

    if result:
        logging.info(f"Событие '{event['Заголовок']}' успешно найдено в списке опубликованных")
    else:
        logging.warning(f"Событие '{event['Заголовок']}' не найдено в списке опубликованных")

    return result

def navigate_to_events_list(driver):
    """Переход на страницу со списком опубликованных афиш"""
    try:
        driver.get(EVENTS_LIST_URL)
        WebDriverWait(driver, SLEEP_AFTER_ACTION * 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_INPUT_SELECTOR))
        )
        return True
    except TimeoutException:
        logging.error("Не удалось загрузить страницу со списком событий")
        return False

def search_for_event(driver, event_title):
    """Поиск события по заголовку"""
    try:
        search_input = driver.find_element(By.CSS_SELECTOR, SEARCH_INPUT_SELECTOR)
        search_input.clear()
        search_input.send_keys(event_title)
        time.sleep(SLEEP_AFTER_ACTION)  # Ждем обновления результатов поиска
        return True
    except NoSuchElementException:
        logging.error("Не удалось найти поле поиска")
        return False

def check_event_in_list(driver, event):
    """Проверка наличия события в списке"""
    page_number = 1
    max_pages = 10

    while page_number <= max_pages:
        logging.info(f"Проверка страницы {page_number}")
        events_on_page = get_events_from_current_page(driver)

        for page_event in events_on_page:
            if event_matches(page_event, event):
                logging.info(f"Событие найдено: '{page_event['Заголовок']}' (Дата: {page_event['Дата']}, Время: {page_event.get('Время', 'Не указано')})")
                logging.info(f"Совпадает с: '{event['Заголовок']}' (Дата: {event['Дата']}, Время: {event.get('Время', 'Не указано')})")
                return True

        if not go_to_next_page(driver):
            break

        page_number += 1

    logging.warning(f"Событие не найдено: '{event['Заголовок']}' (Дата: {event['Дата']}, Время: {event.get('Время', 'Не указано')})")
    return False

def event_matches(page_event, target_event):
    """Проверка совпадения события с целевым"""
    title_match = page_event["Заголовок"].lower() == target_event["Заголовок"].lower()
    date_match = page_event["Дата"] == target_event["Дата"]
    time_match = page_event.get("Время", "") == target_event.get("Время", "")

    logging.info(f"Сравнение: '{page_event['Заголовок']}' с '{target_event['Заголовок']}'")
    logging.info(f"Совпадение заголовка: {title_match}")
    logging.info(f"Совпадение даты: {date_match}")
    logging.info(f"Совпадение времени: {time_match}")

    return title_match and date_match and time_match

def go_to_next_page(driver):
    """Переход на следующую страницу, если она есть"""
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "button.btn-next")
        if next_button.is_enabled():
            next_button.click()
            WebDriverWait(driver, SLEEP_AFTER_ACTION * 2).until(
                EC.staleness_of(next_button)
            )
            return True
        else:
            logging.info("Достигнута последняя страница")
            return False
    except NoSuchElementException:
        logging.info("Кнопка 'Следующая страница' не найдена.")
        return False
    except Exception as e:
        logging.error(f"Ошибка при переходе на следующую страницу: {e}")
        return False

def get_events_from_current_page(driver):
    """Получение всех событий с текущей страницы"""
    events = []
    try:
        WebDriverWait(driver, SLEEP_AFTER_ACTION * 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
        )
        event_rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in event_rows:
            try:
                title = row.find_element(By.CSS_SELECTOR, EVENT_TITLE_SELECTOR).text
                date = row.find_element(By.CSS_SELECTOR, EVENT_DATE_SELECTOR).text
                time = row.find_element(By.CSS_SELECTOR, EVENT_TIME_SELECTOR).text
                events.append({"Заголовок": title, "Дата": date, "Время": time})
            except NoSuchElementException:
                logging.warning(f"Не удалось извлечь данные из строки таблицы")
        logging.info(f"Найдено {len(events)} событий на текущей странице")
    except TimeoutException:
        logging.error("Тайм-аут при ожидании загрузки таблицы событий")
    except Exception as e:
        logging.error(f"Ошибка при получении событий с текущей страницы: {e}")
    return events

def event_matches(events, target_event):
    """Проверка совпадения события с целевым"""
    for event in events:
        if (event["Заголовок"] == target_event["Заголовок"] and
            event["Дата"] == target_event["Дата"] and
            event["Время"] == target_event["Время"]):
            return True
    return False

def update_google_sheet(sheet_id, event_row, new_value):
    """Обновление статуса публикации в Google Sheets"""
    # Здесь нужно реализовать логику обновления Google Sheets
    # Используйте Google Sheets API для обновления ячейки
    pass
