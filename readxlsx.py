import openpyxl
from model import Event

def read_excel(filename, sheet_name):
    try:
        workbook = openpyxl.load_workbook(filename, data_only=True)
        sheet = workbook[sheet_name]

        events = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if all([cell is None for cell in row]):
                break

            if row[0] is None:
                continue

            # Измените следующую строку, чтобы передавать только нужное количество аргументов
            event_data = row[:14]  # предполагая, что вам нужны первые 14 столбцов
            event = Event(*event_data)
            events.append(event)

        return events

    except Exception as e:
        print(f"Произошла ошибка при чтении файла {filename}: {e}")
        return []
