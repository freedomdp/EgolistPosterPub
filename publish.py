from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import datetime
import logging
from config import URL_CREATE_EVENT, SLEEP_AFTER_ACTION, CREATE_BUTTON_SELECTOR, FORM_FIELDS, MAX_PUBLICATION_ATTEMPTS
from utils import clean_text, select_dropdown_option, close_calendar_with_js, get_browser_logs
from publication_checker import check_publication_success, update_google_sheet


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def publish_event(driver, event):

    for attempt in range(1, MAX_PUBLICATION_ATTEMPTS + 1):
        try:
            driver.get(URL_CREATE_EVENT)
            WebDriverWait(driver, SLEEP_AFTER_ACTION * 5).until(
                EC.presence_of_element_located((By.ID, FORM_FIELDS["title"]))
            )

            fill_event_form(driver, event)

            if not validate_form(driver):
                logging.error("Форма содержит ошибки валидации. Пропуск публикации.")
                return False

            create_button = WebDriverWait(driver, SLEEP_AFTER_ACTION * 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, CREATE_BUTTON_SELECTOR))
            )
            driver.execute_script("arguments[0].click();", create_button)

            if check_publication_success(driver, event):
                logging.info(f"Событие '{event.get('Заголовок', 'Без названия')}' успешно опубликовано")
                update_google_sheet(GOOGLE_SHEETS_SPREADSHEET_ID, event['row'], '1')
                return True

            logging.warning(f"Попытка {attempt} завершена неудачно.")
            if attempt < MAX_PUBLICATION_ATTEMPTS:
                time.sleep(SLEEP_AFTER_ACTION * 2)

        except Exception as e:
            logging.error(f"Ошибка при публикации события {event.get('Заголовок', 'Без названия')}: {e}")

    logging.error(f"Не удалось опубликовать событие '{event.get('Заголовок', 'Без названия')}' после {MAX_PUBLICATION_ATTEMPTS} попыток")
    return False

def validate_form(driver):
    fields_to_check = ['title', 'type', 'city', 'date']
    for field in fields_to_check:
        element = driver.find_element(By.ID, FORM_FIELDS[field])
        if 'is-error' in element.get_attribute('class'):
            logging.error(f"Поле {field} содержит ошибку валидации")
            return False
    return True

def fill_event_form(driver, event):
    logging.info(f"Заполнение формы для события: '{event['Заголовок']}' (Дата: {event['Дата']}, Время: {event.get('Время', 'Не указано')})")

    # Заголовок мероприятия
    title = clean_text(str(event.get('Заголовок', '')))
    if title:
        #logging.info(f"Заполнение заголовка: '{title}'")
        driver.find_element(By.ID, FORM_FIELDS["title"]).send_keys(title)
    else:
        logging.warning("Заголовок отсутствует")

    # Описание мероприятия
    description = clean_text(str(event.get('Описание', '')))
    if description:
        #logging.info(f"Заполнение описания: '{description[:100]}...'")
        driver.find_element(By.ID, FORM_FIELDS["description"]).send_keys(description)
    else:
        logging.warning("Описание отсутствует")

    # Тип мероприятия
    event_type = clean_text(str(event.get('Тип', '')))
    if event_type:
        #logging.info(f"Выбор типа мероприятия: '{event_type}'")
        select_dropdown_option(driver, driver.find_element(By.ID, FORM_FIELDS["type"]), event_type, SLEEP_AFTER_ACTION)
    else:
        logging.warning("Тип мероприятия отсутствует")

    # Город
    city = clean_text(str(event.get('Город', '')))
    if city:
        #logging.info(f"Выбор города: '{city}'")
        select_dropdown_option(driver, driver.find_element(By.ID, FORM_FIELDS["city"]), city, SLEEP_AFTER_ACTION)
    else:
        logging.warning("Город отсутствует")

    # Цена
    price = event.get('Цена', '')
    if price:
        #logging.info(f"Заполнение цены: '{price}'")
        driver.find_element(By.ID, FORM_FIELDS["price"]).send_keys(str(price))
    else:
        logging.warning("Цена отсутствует")

    # Дата проведения мероприятий
    date = event.get('Дата', '')
    if date:
        try:
            # Преобразуем дату в правильный формат
            date_obj = datetime.datetime.strptime(date, '%d.%m.%Y')
            formatted_date = date_obj.strftime('%Y-%m-%d')
            #logging.info(f"Заполнение даты: '{formatted_date}'")
            driver.find_element(By.ID, FORM_FIELDS["date"]).send_keys(formatted_date)
            close_calendar_with_js(driver)
        except ValueError:
            logging.warning(f"Неверный формат даты: '{date}'. Пропуск заполнения даты.")
    else:
        logging.warning("Дата отсутствует")

    # Время проведения
    time = event.get('Время', '')
    if time:
        #logging.info(f"Заполнение времени: '{time}'")
        driver.find_element(By.ID, FORM_FIELDS["time"]).send_keys(time)
    else:
        logging.warning("Время отсутствует")

    # Название заведения
    venue_name = event.get('Название заведения', '')
    if venue_name:
        #logging.info(f"Заполнение названия заведения: '{venue_name}'")
        driver.find_element(By.ID, FORM_FIELDS["venue_name"]).send_keys(str(venue_name))
    else:
        logging.warning("Название заведения отсутствует")

    # Адрес
    address = clean_text(str(event.get('Адрес', '')))
    if address:
        #logging.info(f"Заполнение адреса: '{address}'")
        driver.find_element(By.ID, FORM_FIELDS["address"]).send_keys(address)
    else:
        logging.warning("Адрес отсутствует")

    # Источник
    source = event.get('Источник', '')
    if source:
        #logging.info(f"Заполнение источника: '{source}'")
        driver.find_element(By.ID, FORM_FIELDS["source"]).send_keys(str(source))
    else:
        logging.warning("Источник отсутствует")

    # Контакты
    contacts = clean_text(str(event.get('Контакты', '')))
    if contacts:
        #logging.info(f"Заполнение контактов: '{contacts}'")
        driver.find_element(By.ID, FORM_FIELDS["contacts"]).send_keys(contacts)
    else:
        logging.warning("Контакты отсутствуют")

    # Фото
    photo_url = event.get('Фото URL 1', '')
    if photo_url:
        #logging.info(f"Заполнение URL фото: '{photo_url}'")
        driver.find_element(By.ID, FORM_FIELDS["photo"]).send_keys(str(photo_url))
    else:
        logging.warning("URL фото отсутствует")

    # Видео
    video_url = event.get('Видео URL 1', '')
    if video_url:
        #logging.info(f"Заполнение URL видео: '{video_url}'")
        driver.find_element(By.ID, FORM_FIELDS["video"]).send_keys(str(video_url))
    else:
        logging.warning("URL видео отсутствует")

    logging.info("Заполнение формы завершено")
