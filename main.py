from readxlsx import read_excel
from utils import print_events_to_publish
from publish import publish_event
from login import login
import os


def main():
    print("Запуск программы...")

    # Проверка подключения модулей
    try:
        from readxlsx import read_excel
        print("Модуль read_excel успешно подключен.")
    except Exception as e:
        print(f"Ошибка подключения модуля read_excel: {e}")
        return

    try:
        from utils import print_events_to_publish
        print("Модуль print_events_to_publish успешно подключен.")
    except Exception as e:
        print(f"Ошибка подключения модуля print_events_to_publish: {e}")
        return

    try:
        from publish import publish_event
        print("Модуль publish_event успешно подключен.")
    except Exception as e:
        print(f"Ошибка подключения модуля publish_event: {e}")
        return

    try:
        from login import login
        print("Модуль login успешно подключен.")
    except Exception as e:
        print(f"Ошибка подключения модуля login: {e}")
        return

    try:
        print("Попытка входа...")
        driver = login()
        if driver is None:
            print("Ошибка инициализации WebDriver. Завершение программы.")
            return

        path_to_file = os.path.join(os.path.dirname(__file__), "afisha.xlsx")
        print(f"Чтение данных из файла Excel: {path_to_file}")

        try:
            events = read_excel(path_to_file, 'data')
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
