from readxlsx import read_excel
from utils import print_events_to_publish
from publish import publish_event
from login import login



def main():
    print("Запуск программы...")

    try:
        driver = login()
        path_to_file = "/Users/sergej/Desktop/Afisha/afisha.xlsx"
        print("Чтение данных из Excel...")
        events = read_excel(path_to_file, 'data')

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
        print(f"Произошла ошибка: {e}")

    print("Программа завершена.")

if __name__ == "__main__":
    main()
