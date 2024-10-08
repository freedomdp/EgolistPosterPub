from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import (
    LOGIN_URL, TARGET_URL, LOGIN_SELECTOR, PASSWORD_SELECTOR,
    SUBMIT_BUTTON_SELECTOR, DASHBOARD_TEXT, USERNAME, PASSWORD,
    CHROME_OPTIONS, SLEEP_AFTER_ACTION
)

def login():
    try:
        print("Установка и инициализация WebDriver...")
        chrome_options = webdriver.ChromeOptions()
        for option in CHROME_OPTIONS:
            chrome_options.add_argument(option)
        chrome_options.add_argument("--remote-debugging-port=9222")  # Добавляем эту опцию

        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver успешно установлен и инициализирован.")

        driver.get(LOGIN_URL)

        try:
            WebDriverWait(driver, SLEEP_AFTER_ACTION * 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, LOGIN_SELECTOR))).send_keys(USERNAME)
            WebDriverWait(driver, SLEEP_AFTER_ACTION * 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, PASSWORD_SELECTOR))).send_keys(PASSWORD)
            WebDriverWait(driver, SLEEP_AFTER_ACTION * 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR))).click()

            time.sleep(SLEEP_AFTER_ACTION)
            dashboard_element = WebDriverWait(driver, SLEEP_AFTER_ACTION * 5).until(EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{DASHBOARD_TEXT}')]")))
            if dashboard_element:
                print("Авторизация успешно выполнена.")
                driver.get(TARGET_URL)
            else:
                print("Авторизация не удалась.")

        except Exception as e:
            print(f"Произошла ошибка при авторизации: {e}")

        return driver

    except Exception as e:
        print(f"Ошибка инициализации WebDriver: {e}")
        return None
