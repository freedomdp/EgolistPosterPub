from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, time as datetime_time
import re
import logging
from selenium.webdriver.common.action_chains import ActionChains
import json

def select_dropdown_option(driver, input_element, option_text, sleep_after_action):
    input_element.click()
    time.sleep(sleep_after_action)

    dropdown_selector = "div.el-select-dropdown li.el-select-dropdown__item"
    dropdown_elements = WebDriverWait(driver, sleep_after_action * 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, dropdown_selector))
    )

    for item in dropdown_elements:
        if item.text == option_text:
            scroll_to_element(driver, item)
            time.sleep(sleep_after_action)
            item.click()
            break

    # Ожидание исчезновения выпадающего списка
    WebDriverWait(driver, sleep_after_action * 5).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, dropdown_selector))
    )

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)

def clean_text(text):
    original_text = text
    if not text:
        return text

    pattern = r"[^a-zA-Zа-яА-Я0-9\n.,!?+:() \-іїєґІЇЄҐ'']"
    cleaned_text = re.sub(pattern, " ", text)

    lines = cleaned_text.split('\n')
    cleaned_lines = [re.sub(r"\s+", " ", line).strip() for line in lines]
    cleaned_text = '\n'.join(cleaned_lines).strip()

    if original_text != cleaned_text:
        logging.warning(f"Text modified during cleaning: Original '{original_text}', Cleaned '{cleaned_text}'")

    return cleaned_text if cleaned_text else text

def print_events_to_publish(events):
    print("Отметка о публикации | Название публикации                                | Дата публикации      | Время публикации")
    for event in events:
        publication_mark = event.get('publication_mark', '0')
        title = event.get('title', '')[:50].ljust(50)
        date = event.get('date', '')
        time = event.get('time', '')
        print(f"{publication_mark:<20} | {title} | {date:<20} | {time}")

def close_calendar_with_js(driver):
    script = """
    var calendar = document.querySelector('.el-picker-panel__body');
    if (calendar) {
        calendar.style.display = 'none';
    }
    """
    driver.execute_script(script)

def get_browser_logs(driver):
    browser_logs = driver.get_log('browser')
    print("Логи консоли браузера:")
    for log in browser_logs:
        print(json.dumps(log, indent=2))

def check_publication_status(driver, event, sleep_after_action):
    try:
        success_message = driver.find_elements(By.CSS_SELECTOR, ".el-message--success")
        error_message = driver.find_elements(By.CSS_SELECTOR, ".el-message--error")

        if success_message:
            print("Сообщение об успешной публикации найдено")
        elif error_message:
            print("Найдено сообщение об ошибке:")
            print(error_message[0].text)
        else:
            print("Не найдено сообщений об успешной публикации или ошибках")

        current_url = driver.current_url
        print(f"Текущий URL после попытки публикации: {current_url}")

        # Проверка наличия события в списке опубликованных
        driver.get("https://admin.egolist.ua/events/list")
        time.sleep(sleep_after_action * 2)

        event_titles = driver.find_elements(By.CSS_SELECTOR, "tbody tr td:nth-child(2)")
        found = any(event.title in title.text for title in event_titles)
        if found:
            print(f"Событие '{event.title}' найдено в списке опубликованных")
        else:
            print(f"Событие '{event.title}' НЕ найдено в списке опубликованных")
    except Exception as e:
        print(f"Ошибка при проверке публикации: {e}")
