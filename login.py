from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login():
    # URL-адрес для авторизации и целевой страницы
    login_url = "https://admin.egolist.ua/"
    target_url = "https://admin.egolist.ua/events/list"  # URL-адрес после авторизации

    # Селекторы и данные для входа
    login_selector = "input[type='text'].el-input__inner"
    password_selector = "input[type='password'].el-input__inner"
    submit_button_selector = "button.el-button.el-button--primary"
    dashboard_text = "Dashboard"
    username = "admin@admin.com"
    password = "12345678"

    # Инициализация WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(login_url)

    try:
        # Авторизация на сайте
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, login_selector))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, password_selector))).send_keys(password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector))).click()

        # Ожидание и проверка успешности авторизации
        time.sleep(1)
        dashboard_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{dashboard_text}')]")))
        if dashboard_element:
            print("Авторизация успешно выполнена.")
            driver.get(target_url)  # Переход на целевую страницу
        else:
            print("Авторизация не удалась.")

    except Exception as e:
        print(f"Произошла ошибка при авторизации: {e}")

    return driver
