from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, time as datetime_time
from selenium.webdriver.common.action_chains import ActionChains
import time
from utils import format_time
from utils import close_calendar_with_js, clean_text, scroll_to_element
from selenium.common.exceptions import TimeoutException



# Конфигурационные параметры
url_create_event = "https://admin.egolist.ua/events/create"
sleep_after_publish = 2  # время задержки для визуальной проверки
create_button_selector = "button.el-button.el-button--success"

fields_mapping = {
    "title": 1,
    "description": 2,
    "type": 3,
    "price": 4,
    "date": 5,
    "time": 6,
    "city": 7,
    "venue_name": 8,
    "address": 9,
    "source": 10,
    "contacts": 11,
    "photo_url": 12,
    "video_url": 20
}

def publish_event(driver, event):
    if event.publication_mark != 0:
        # Пропускаем публикацию, если publication_mark не равен 0
        return

    driver.get(url_create_event)

    try:
        # Ожидание загрузки страницы
        time.sleep(1)

        # Получение всех элементов input и textarea
        inputs = driver.find_elements(By.CSS_SELECTOR, "input, textarea")

        # Обязательные поля
        print(f"Tite ... 'event.title'")
        inputs[fields_mapping["title"] - 1].send_keys(clean_text(event.title))
        print(f"Type ... 'event.type'")
        select_dropdown_option(driver, inputs[fields_mapping["type"] - 1], event.type)
        # Форматирование и заполнение поля даты
        print(f"Date ... 'event.date'")
        date_input = inputs[fields_mapping["date"] - 1]
        date_str = event.date.strftime("%Y-%m-%d") if isinstance(event.date, datetime) else ""
        date_input.send_keys(date_str)

        # Закрытие календаря с помощью JavaScript
        close_calendar_with_js(driver)
        # Пауза, чтобы убедиться, что календарь закрыт
        print("City ...")
        select_dropdown_option(driver, inputs[fields_mapping["city"] - 1], event.city)
        time.sleep(1)
        print(f"Sorce ... 'event.source'")
        inputs[fields_mapping["source"] - 1].send_keys(event.source)
        try:
            # Попытка заполнить поле "venue_name"
            time.sleep(1)
            close_calendar_with_js(driver)
            print(f"Venue_name ... '{event.venue_name}'")
            venue_name_input = inputs[fields_mapping["venue_name"] - 1]
            cleaned_venue_name = clean_text(event.venue_name)
            venue_name_input.send_keys(cleaned_venue_name)
        except Exception as e:
            # Вывод деталей ошибки и значения, которое вызвало ошибку
            print(f"Ошибка при заполнении поля 'venue_name' значением '{event.venue_name}': {e}")
            raise  # Повторно вызываем исключение для остановки выполнения


        # Необязательные поля
        if event.description:
            print(f"Description ... '{event.description[:100]}' ...")
            inputs[fields_mapping["description"] - 1].send_keys(clean_text(event.description))
        if event.price:
            print("Price ... 'event.price'")
            inputs[fields_mapping["price"] - 1].send_keys(event.price)
        # Форматирование и заполнение поля времени
        if event.time:
            # Для объектов datetime.time или непустых строк выполняем форматирование и заполнение
            if isinstance(event.time, datetime_time):
                # Если event.time - это объект datetime.time, форматируем его в строку
                time_formatted = event.time.strftime("%H:%M")
            elif isinstance(event.time, str) and len(event.time.strip()) > 0:
                # Если event.time - это непустая строка, используем её напрямую после удаления возможных пробелов в начале и конце
                time_formatted = event.time.strip()
            else:
                # Если event.time - это пустая строка или строка из пробелов, пропускаем заполнение поля времени
                return
            
            # Если мы здесь, значит есть значение для заполнения поля времени
            inputs[fields_mapping["time"] - 1].send_keys(time_formatted)
        if event.contacts:
            print("Contacts ... 'event.contacts' ")
            inputs[fields_mapping["contacts"] - 1].send_keys(event.contacts)
        if event.photo_url:
            print("Photo url ... 'event.photo_url'")
            inputs[fields_mapping["photo_url"] - 1].send_keys(event.photo_url)
        if event.video_url:
            print("Video url ... 'event.video_url'")
            inputs[fields_mapping["video_url"] - 1].send_keys(event.video_url)

        # Нажатие на кнопку "Создать" для сохранения публикации
        print("Button ...")
        create_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, create_button_selector))
        )
        create_button.click()

        print(f"---------- ПУБЛИКАЦИЯ МЕРОПРИЯТИЯ '{event.title}' ВЫПОЛНЕНА ----------")
        time.sleep(sleep_after_publish)

    except Exception as e:
        print(f"Ошибка при публикации события {event.title}: {e}")
        time.sleep(sleep_after_publish * 10)


def select_dropdown_option(driver, input_element, option_text):
    print("Dropdown ...")
    input_element.click()
    time.sleep(1)

    dropdown_selector = "div.el-select-dropdown li.el-select-dropdown__item"
    dropdown_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, dropdown_selector))
    )

    #print(f"Найдено {len(dropdown_elements)} элементов в выпадающем списке.")

    for item in dropdown_elements:
        print(f"Элемент списка: {item.text}")
        if item.text == option_text:
            scroll_to_element(driver, item)
            time.sleep(1)
            item.click()
            break
