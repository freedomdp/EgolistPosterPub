from readxlsx import read_excel
from utils import print_events_to_publish
from publish import publish_event
from login import login
from config import EXCEL_FILE_PATH, EXCEL_SHEET_NAME

def main():
    print("Запуск программы...")

    # Проверка подключения модулей
    modules_to_check = [
        ('readxlsx', 'read_excel'),
        ('utils', 'print_events_to_publish'),
        ('publish', 'publish_event'),
        ('login', 'login')
    ]

    for module_name, function_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"Модуль {function_name} успешно подключен.")
        except Exception as e:
            print(f"Ошибка подключения модуля {function_name}: {e}")
            return

    try:
        print("Попытка входа...")
        driver = login()
        if driver is None:
            print("Ошибка инициализации WebDriver. Завершение программы.")
            return

        print(f"Чтение данных из файла Excel: {EXCEL_FILE_PATH}")

        try:
            events = read_excel(EXCEL_FILE_PATH, EXCEL_SHEET_NAME)
            print(f"Данные из Excel файла успешно прочитаны. Количество событий: {len(events)}")

            # Вывод событий, готовых к публикации
            print_events_to_publish(events)

            published_count = 0
            for event in events:
                if event.publication_mark == 0:
                    publish_event(driver, event)
                    published_count += 1

            if published_count > 0:
                print(f"Все события опубликованы. Опубликовано событий: {published_count}")
            else:
                print("Нет данных для публикации.")

        except Exception as e:
            print(f"Ошибка при чтении данных из Excel файла: {e}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    print("Программа завершена.")

if __name__ == "__main__":
    main()
