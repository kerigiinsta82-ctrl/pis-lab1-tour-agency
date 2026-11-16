"""Сущность «Клиент» туристической фирмы."""

import re


class Client:
    """Клиент туристической фирмы.

    Все поля приватные (name mangling через двойное подчёркивание),
    доступ к ним — только через свойства (property).
    Каждое присваивание проходит через статический метод валидации,
    а конструктор заполняет поля через свойства — поэтому объект
    с недопустимыми значениями полей создать невозможно.
    """

    def __init__(self, client_id, last_name, first_name, patronymic, phone, address):
        self.client_id = client_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.phone = phone
        self.address = address

    # ---------- статические методы валидации ----------

    @staticmethod
    def validate_client_id(value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("ID клиента должен быть целым числом")
        if value <= 0:
            raise ValueError("ID клиента должен быть положительным")
        return value

    @staticmethod
    def validate_last_name(value):
        if not isinstance(value, str):
            raise TypeError("Фамилия должна быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Фамилия не может быть пустой")
        if len(value) > 50:
            raise ValueError("Фамилия длиннее 50 символов")
        if not re.fullmatch(r"[А-ЯЁA-Z][а-яёa-z]+(?:-[А-ЯЁA-Z][а-яёa-z]+)?", value):
            raise ValueError(f"Фамилия имеет неверный формат: {value!r}")
        return value

    @staticmethod
    def validate_first_name(value):
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Имя не может быть пустым")
        if len(value) > 50:
            raise ValueError("Имя длиннее 50 символов")
        if not re.fullmatch(r"[А-ЯЁA-Z][а-яёa-z]+(?:-[А-ЯЁA-Z][а-яёa-z]+)?", value):
            raise ValueError(f"Имя имеет неверный формат: {value!r}")
        return value

    @staticmethod
    def validate_patronymic(value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("Отчество должно быть строкой")
        value = value.strip()
        if not value:
            return None
        if len(value) > 50:
            raise ValueError("Отчество длиннее 50 символов")
        if not re.fullmatch(r"[А-ЯЁA-Z][а-яёa-z]+(?:-[А-ЯЁA-Z][а-яёa-z]+)?", value):
            raise ValueError(f"Отчество имеет неверный формат: {value!r}")
        return value

    @staticmethod
    def validate_phone(value):
        if not isinstance(value, str):
            raise TypeError("Телефон должен быть строкой")
        value = re.sub(r"[\s()\-]", "", value)
        if not value:
            raise ValueError("Телефон не может быть пустым")
        if not re.fullmatch(r"(?:\+7|8)\d{10}", value):
            raise ValueError(f"Телефон имеет неверный формат: {value!r}")
        return "+7" + value[-10:]

    @staticmethod
    def validate_address(value):
        if not isinstance(value, str):
            raise TypeError("Адрес должен быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Адрес не может быть пустым")
        if len(value) > 200:
            raise ValueError("Адрес длиннее 200 символов")
        return value

    # ---------- свойства ----------

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        self.__client_id = Client.validate_client_id(value)

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = Client.validate_last_name(value)

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = Client.validate_first_name(value)

    @property
    def patronymic(self):
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, value):
        self.__patronymic = Client.validate_patronymic(value)

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = Client.validate_phone(value)

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = Client.validate_address(value)
