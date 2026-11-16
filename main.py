"""Демонстрация работы класса Client."""

from client import Client
from client_short import ClientShort


def try_create(*args, **kwargs):
    try:
        client = Client(*args, **kwargs)
        print("Создан:", client.client_id, client.last_name, client.phone, client.address)
    except (TypeError, ValueError) as error:
        print("Ошибка:", error)


def main():
    print("Перегрузка конструктора:")
    try_create(1, "Иванов", "Иван", "Иванович", "8 (916) 123-45-67", "г. Москва, ул. Ленина, д. 1")
    try_create(client_id=2, last_name="Петрова", first_name="Анна",
               phone="+79035556677", address="г. Казань")
    try_create("3; Сидоров; Олег; ; +79261112233; г. Тверь; ул. Мира, 5")
    try_create('{"client_id": 4, "last_name": "Смирнов", "first_name": "Павел", '
               '"patronymic": "Олегович", "phone": "+79991234567", "address": "г. Сочи"}')
    try_create({"client_id": "5", "last_name": "Кузнецова", "first_name": "Мария",
                "patronymic": None, "phone": "89005554433", "address": "г. Омск"})

    print("\nНекорректные данные:")
    try_create(0, "Петров", "Пётр", None, "+79160000000", "г. Тула")
    try_create(2, "петров", "Пётр", None, "+79160000000", "г. Тула")
    try_create(3, "Петров", "Пётр", None, "12345", "г. Тула")
    try_create("6;Орлов;Илья")
    try_create('{"client_id": 7, ')
    try_create(8, "Орлов", "Илья", None, "+79160000000")

    print("\nПолный и краткий вывод:")
    ivanov = Client(1, "Иванов", "Иван", "Иванович", "+79161234567", "г. Москва, ул. Ленина, д. 1")
    print(ivanov)
    print(ivanov.short_str())
    print(repr(ivanov))

    print("\nСравнение:")
    same = Client("1;Иванов;Иван;Иванович;8 916 123 45 67;г. Москва, ул. Ленина, д. 1")
    other = Client(2, "Иванов", "Иван", None, "+79161234567", "г. Москва")
    print("ivanov == same: ", ivanov == same)
    print("ivanov == other:", ivanov == other)
    print("ivanov is same: ", ivanov is same)

    print("\nКраткая версия (ClientShort):")
    short = ivanov.to_short()
    print(short)
    print(repr(short))
    print("short == ClientShort(строка):",
          short == ClientShort("1;Иванов;Иван;Иванович;+79161234567"))
    print("short == ivanov:", short == ivanov)

    print("\nИерархия наследования:")
    print("Client.__mro__:", [cls.__name__ for cls in Client.__mro__])
    print("isinstance(ivanov, ClientShort):", isinstance(ivanov, ClientShort))
    print("Краткий вывод полного объекта:", ivanov.short_str())

    print("\nНекорректное присваивание:")
    client = Client(1, "Иванов", "Иван", "Иванович", "+79161234567", "г. Москва")
    try:
        client.phone = "abc"
    except ValueError as error:
        print("Ошибка:", error, "| телефон остался", client.phone)


if __name__ == "__main__":
    main()
