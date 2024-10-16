import os

# Существующие параметры
URL_CREATE_EVENT = "https://admin.egolist.ua/events/create"
SLEEP_AFTER_ACTION = 2
CREATE_BUTTON_SELECTOR = "button.el-button.el-button--success"
MAX_PUBLICATION_ATTEMPTS = 1

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

# Параметры для Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'afisha-pub-438209-a7f91828f60d.json')
GOOGLE_SHEETS_SPREADSHEET_ID = '1GKQZ7wvJk44LWkJzaO4-d7wnkw6XNTgA5OPyrkrQBeU'
GOOGLE_SHEETS_RANGE_NAME = 'Data!A:N'

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

#Парсинг поиска в афишах
EVENTS_LIST_URL = "https://admin.egolist.ua/events/list"
SEARCH_INPUT_SELECTOR = "input.el-input__inner[placeholder='Поиск']"
PAGINATION_SELECTOR = ".el-pagination"
EVENT_TITLE_SELECTOR = ".cell"
EVENT_DATE_SELECTOR = ".el-table_1_column_4 .cell"
EVENT_TIME_SELECTOR = ".el-table_1_column_5 .cell"
