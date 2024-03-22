class Event:
    def __init__(self, publication_mark, title, description, type, price, date, time, city, venue_name, address, source, contacts, photo_url, video_url):
        self.publication_mark = publication_mark
        self.title = title
        self.description = description
        self.type = type
        self.price = price
        self.date = date
        self.time = time
        self.city = city
        self.venue_name = venue_name
        self.address = address
        self.source = source
        self.contacts = contacts
        self.photo_url = photo_url
        self.video_url = video_url

    def __str__(self):
        return f"Event({self.title}, {self.date}, {self.city})"
# Отметка о публикации, Заголовок,	Описание, Тип,	Цена,	Дата, 	Время,	Город,	Название заведения,	Адрес,	Источник ,	Контакты,	Фото URL 1,	Видео URL 1
