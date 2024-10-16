import traceback
from google_sheets_reader import read_google_sheet, update_google_sheet
from utils import print_events_to_publish
from publish import publish_event
from login import login

def main():
    print("Запуск программы...")

    try:
        print("Попытка входа...")
        driver = login()
        if driver is None:
            print("Ошибка инициализации WebDriver. Завершение программы.")
            return

        print("Чтение данных из Google Sheets...")

        try:
            events = read_google_sheet()
            print(f"Данные из Google Sheets прочитаны. Количество событий: {len(events)}")

            if not events:
                print("Нет данных для обработки. Завершение программы.")
                return

            events_to_publish = [event for event in events if event.get('Отметка о публикации') == '0']
            for event in events_to_publish:
                if publish_event(driver, event):
                    print(f"Событие '{event['Заголовок']}' успешно опубликовано")
                else:
                    print(f"Не удалось опубликовать событие '{event['Заголовок']}'")

            if not events_to_publish:
                print("Нет новых событий для публикации. Завершение программы.")
                return

            print("\nПримеры первых 5 событий для публикации:")
            for i, event in enumerate(events_to_publish[:5]):
                print(f"Событие {i+1}:")
                for key, value in event.items():
                    print(f"  {key}: {value}")
                print()

            total_events = len(events_to_publish)
            published_count = 0

            for index, event in enumerate(events_to_publish, 1):
                print(f"\n\n\nОбработка события {index}/{total_events}: '{event['Заголовок']}' (Дата: {event['Дата']}, Время: {event.get('Время', 'Не указано')})\n\n\n")
                try:
                    if publish_event(driver, event):
                        published_count += 1
                        print(f"Событие успешно опубликовано. Обновление статуса в Google Sheets...")
                        update_google_sheet(GOOGLE_SHEETS_SPREADSHEET_ID, event['row'], '1')
                    else:
                        print(f"Не удалось опубликовать событие.")
                except Exception as e:
                    print(f"Ошибка при публикации события: {e}")

                print(f"Прогресс: {published_count}/{total_events} опубликовано")

            print(f"Итого опубликовано событий: {published_count}/{total_events}")

        except Exception as e:
            print(f"Ошибка при работе с Google Sheets: {e}")
            traceback.print_exc()

    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")
        traceback.print_exc()

    finally:
        if 'driver' in locals() and driver:
            print("Закрытие WebDriver...")
            driver.quit()

    print("Программа завершена.")

if __name__ == "__main__":
    main()
