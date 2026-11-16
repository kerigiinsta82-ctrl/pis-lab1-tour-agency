"""Демонстрация работы класса Client."""

from client import Client


def try_create(*args):
    try:
        client = Client(*args)
        print("Создан:", client.last_name, client.phone)
    except (TypeError, ValueError) as error:
        print("Ошибка:", error)


def main():
    client = Client(1, "Иванов", "Иван", "Иванович", "8 (916) 123-45-67", "г. Москва, ул. Ленина, д. 1")
    print(client.client_id, client.last_name, client.first_name,
          client.patronymic, client.phone, client.address)

    print("\nНекорректные данные:")
    try_create(0, "Петров", "Пётр", None, "+79160000000", "г. Тула")
    try_create(2, "петров", "Пётр", None, "+79160000000", "г. Тула")
    try_create(3, "Петров", "Пётр", None, "12345", "г. Тула")
    try_create(4, "Петров", "Пётр", None, "+79160000000", "   ")

    print("\nНекорректное присваивание:")
    try:
        client.phone = "abc"
    except ValueError as error:
        print("Ошибка:", error, "| телефон остался", client.phone)


if __name__ == "__main__":
    main()
