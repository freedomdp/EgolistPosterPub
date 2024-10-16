import warnings
warnings.filterwarnings("ignore", message="file_cache is only supported with oauth2client<4.0.0")

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import GOOGLE_SHEETS_CREDENTIALS_FILE, GOOGLE_SHEETS_SPREADSHEET_ID, GOOGLE_SHEETS_RANGE_NAME

def read_google_sheet():
    """
    Читает данные из Google Sheets.
    """
    print(f"Попытка чтения данных из таблицы {GOOGLE_SHEETS_SPREADSHEET_ID}")
    print(f"Используется файл учетных данных: {GOOGLE_SHEETS_CREDENTIALS_FILE}")

    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_SHEETS_CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
    except Exception as e:
        print(f"Ошибка при чтении файла учетных данных: {e}")
        raise

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=GOOGLE_SHEETS_SPREADSHEET_ID, range=GOOGLE_SHEETS_RANGE_NAME).execute()
        values = result.get('values', [])
    except Exception as e:
        print(f"Ошибка при получении данных из Google Sheets: {e}")
        raise

    if not values:
        print('Данные не найдены в таблице.')
        return []

    print(f"Получено {len(values)} строк данных.")

    # Предполагаем, что первая строка содержит заголовки
    headers = values[0]
    print("Заголовки столбцов:", headers)
    data = []
    for row in values[1:]:
        if any(row):  # Проверяем, что строка не пустая
            event = {}
            for i, value in enumerate(row):
                if i < len(headers):
                    event[headers[i]] = value.strip() if isinstance(value, str) else value
            if event:  # Добавляем событие, только если оно не пустое
                data.append(event)

    print(f"Обработано {len(data)} непустых событий.")
    return data

def update_google_sheet(row_index, column_index, value):
    """
    Обновляет конкретную ячейку в Google Sheets.
    """
    creds = Credentials.from_service_account_file(
        GOOGLE_SHEETS_CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    range_name = f'Data!{chr(64 + column_index)}{row_index}'
    body = {
        'values': [[value]]
    }

    result = sheet.values().update(
        spreadsheetId=GOOGLE_SHEETS_SPREADSHEET_ID,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f'{result.get("updatedCells")} ячеек обновлено.')
