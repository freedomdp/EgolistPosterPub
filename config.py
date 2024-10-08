import os

# Существующие параметры
URL_CREATE_EVENT = "https://admin.egolist.ua/events/create"
SLEEP_AFTER_ACTION = 2
CREATE_BUTTON_SELECTOR = "button.el-button.el-button--success"
MAX_PUBLICATION_ATTEMPTS = 2

# Параметры для логина
LOGIN_URL = "https://admin.egolist.ua/"
TARGET_URL = "https://admin.egolist.ua/events/list"
LOGIN_SELECTOR = "input[type='text'].el-input__inner"
PASSWORD_SELECTOR = "input[type='password'].el-input__inner"
SUBMIT_BUTTON_SELECTOR = "button.el-button.el-button--primary"
DASHBOARD_TEXT = "Dashboard"
USERNAME = "admin@admin.com"
PASSWORD = "12345678"

# Параметры WebDriver
CHROME_OPTIONS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--remote-debugging-port=9222'
]

# Параметры для main()
EXCEL_FILE_NAME = "afisha.xlsx"
EXCEL_SHEET_NAME = 'data'
EXCEL_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), EXCEL_FILE_NAME)

# ID элементов формы
FORM_FIELDS = {
    "title": "name",
    "description": "descr",
    "type": "type_event",
    "city": "town",
    "price": "price",
    "date": "date_event",
    "time": "time_event",
    "venue_name": "name_estab",
    "address": "addr_estab",
    "source": "link_estab",
    "contacts": "contact_estab",
    "photo": "photo_0",
    "video": "video_0"
}
