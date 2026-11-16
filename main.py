"""Демонстрация работы класса Client."""

from client import Client


def main():
    client = Client(1, "Иванов", "Иван", "Иванович", "+79161234567", "г. Москва, ул. Ленина, д. 1")
    print(client.client_id, client.last_name, client.first_name,
          client.patronymic, client.phone, client.address)

    client.phone = "+79990001122"
    print("Новый телефон:", client.phone)


if __name__ == "__main__":
    main()
