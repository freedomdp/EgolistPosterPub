from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import logging
from config import URL_CREATE_EVENT, SLEEP_AFTER_ACTION, CREATE_BUTTON_SELECTOR, FORM_FIELDS, MAX_PUBLICATION_ATTEMPTS
from utils import clean_text, select_dropdown_option, close_calendar_with_js, get_browser_logs, check_publication_status

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def publish_event(driver, event):
    if event.publication_mark != 0:
        logging.info(f"Событие '{event.title}' уже опубликовано. Пропуск.")
        return

    for attempt in range(1, MAX_PUBLICATION_ATTEMPTS + 1):
        logging.info(f"Попытка публикации {attempt} из {MAX_PUBLICATION_ATTEMPTS} для события '{event.title}'")

        driver.get(URL_CREATE_EVENT)

        try:
            WebDriverWait(driver, SLEEP_AFTER_ACTION * 5).until(
                EC.presence_of_element_located((By.ID, FORM_FIELDS["title"]))
            )

            # Заполнение формы
            fill_event_form(driver, event)

            # Нажатие на кнопку "Создать" для сохранения публикации
            logging.info("Нажатие кнопки 'Создать'")
            create_button = WebDriverWait(driver, SLEEP_AFTER_ACTION * 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, CREATE_BUTTON_SELECTOR))
            )
            driver.execute_script("arguments[0].click();", create_button)

            # Ожидание завершения публикации
            try:
                WebDriverWait(driver, SLEEP_AFTER_ACTION * 10).until(
                    EC.url_changes(URL_CREATE_EVENT)
                )
                logging.info("URL изменился после нажатия кнопки 'Создать'")

                # Дополнительное ожидание для загрузки новой страницы
                time.sleep(SLEEP_AFTER_ACTION * 2)

                # Проверка наличия сообщения об успешной публикации
                success_message = driver.find_elements(By.CSS_SELECTOR, ".el-message--success")
                if success_message:
                    logging.info("Публикация успешно завершена")
                    return True
                else:
                    logging.warning("Сообщение об успешной публикации не найдено")
            except TimeoutException:
                logging.warning("Тайм-аут при ожидании изменения URL")

            # Получение логов консоли браузера
            get_browser_logs(driver)

            # Проверка статуса публикации
            if check_publication_status(driver, event, SLEEP_AFTER_ACTION):
                logging.info(f"Событие '{event.title}' успешно опубликовано")
                return True

            logging.warning(f"Попытка {attempt} не удалась. Повтор через {SLEEP_AFTER_ACTION * 2} секунд.")
            time.sleep(SLEEP_AFTER_ACTION * 2)

        except Exception as e:
            logging.error(f"Ошибка при публикации события {event.title}: {e}")
            time.sleep(SLEEP_AFTER_ACTION * 2)

    logging.error(f"Не удалось опубликовать событие '{event.title}' после {MAX_PUBLICATION_ATTEMPTS} попыток")
    return False

def fill_event_form(driver, event):
    # Заголовок мероприятия
    title = clean_text(str(event.title))
    if len(title) > 255:
        title = title[:252] + "..."
    logging.info(f"Заполнение заголовка: '{title}'")
    driver.find_element(By.ID, FORM_FIELDS["title"]).send_keys(title)

    # Описание мероприятия
    if event.description:
        description = clean_text(str(event.description))
        logging.info(f"Заполнение описания: '{description[:100]}...'")
        driver.find_element(By.ID, FORM_FIELDS["description"]).send_keys(description)

    # Тип мероприятия
    event_type = clean_text(str(event.type))
    logging.info(f"Выбор типа мероприятия: '{event_type}'")
    select_dropdown_option(driver, driver.find_element(By.ID, FORM_FIELDS["type"]), event_type, SLEEP_AFTER_ACTION)

    # Город
    city = clean_text(str(event.city))
    logging.info(f"Выбор города: '{city}'")
    select_dropdown_option(driver, driver.find_element(By.ID, FORM_FIELDS["city"]), city, SLEEP_AFTER_ACTION)

    # Цена
    if event.price:
        logging.info(f"Заполнение цены: '{event.price}'")
        driver.find_element(By.ID, FORM_FIELDS["price"]).send_keys(str(event.price))

    # Дата проведения мероприятий
    if event.date:
        date_str = event.date.strftime("%Y-%m-%d") if hasattr(event.date, 'strftime') else str(event.date)
        logging.info(f"Заполнение даты: '{date_str}'")
        driver.find_element(By.ID, FORM_FIELDS["date"]).send_keys(date_str)
        close_calendar_with_js(driver)

    # Время проведения
    if event.time:
        time_str = event.time.strftime("%H:%M") if hasattr(event.time, 'strftime') else str(event.time)
        logging.info(f"Заполнение времени: '{time_str}'")
        driver.find_element(By.ID, FORM_FIELDS["time"]).send_keys(time_str)

    # Название заведения
    if event.venue_name:
        logging.info(f"Заполнение названия заведения: '{event.venue_name}'")
        driver.find_element(By.ID, FORM_FIELDS["venue_name"]).send_keys(str(event.venue_name))

    # Адрес
    if event.address:
        address = clean_text(str(event.address))
        logging.info(f"Заполнение адреса: '{address}'")
        driver.find_element(By.ID, FORM_FIELDS["address"]).send_keys(address)

    # Источник
    if event.source:
        logging.info(f"Заполнение источника: '{event.source}'")
        driver.find_element(By.ID, FORM_FIELDS["source"]).send_keys(str(event.source))

    # Контакты
    if event.contacts:
        contacts = clean_text(str(event.contacts))
        logging.info(f"Заполнение контактов: '{contacts}'")
        driver.find_element(By.ID, FORM_FIELDS["contacts"]).send_keys(contacts)

    # Фото
    if event.photo_url:
        logging.info(f"Заполнение URL фото: '{event.photo_url}'")
        driver.find_element(By.ID, FORM_FIELDS["photo"]).send_keys(str(event.photo_url))

    # Видео
    if event.video_url:
        logging.info(f"Заполнение URL видео: '{event.video_url}'")
        driver.find_element(By.ID, FORM_FIELDS["video"]).send_keys(str(event.video_url))

    logging.info("Заполнение формы завершено")
