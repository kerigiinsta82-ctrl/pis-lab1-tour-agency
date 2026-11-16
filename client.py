"""Сущность «Клиент» туристической фирмы."""

import re

NAME_PATTERN = re.compile(r"[А-ЯЁA-Z][а-яёa-z]+(?:-[А-ЯЁA-Z][а-яёa-z]+)?")
PHONE_PATTERN = re.compile(r"(?:\+7|8)\d{10}")
NAME_MAX_LENGTH = 50
ADDRESS_MAX_LENGTH = 200


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
    def _validate_string(value, field_name, max_length, pattern=None, required=True):
        """Общая проверка строкового поля.

        Возвращает очищенное значение; для необязательного пустого поля — None.
        """
        if value is None and not required:
            return None
        if not isinstance(value, str):
            raise TypeError(f"Поле «{field_name}» должно быть строкой")
        value = value.strip()
        if not value:
            if required:
                raise ValueError(f"Поле «{field_name}» не может быть пустым")
            return None
        if len(value) > max_length:
            raise ValueError(f"Поле «{field_name}» длиннее {max_length} символов")
        if pattern is not None and not pattern.fullmatch(value):
            raise ValueError(f"Поле «{field_name}» имеет неверный формат: {value!r}")
        return value

    @staticmethod
    def validate_client_id(value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("ID клиента должен быть целым числом")
        if value <= 0:
            raise ValueError("ID клиента должен быть положительным")
        return value

    @staticmethod
    def validate_last_name(value):
        return Client._validate_string(value, "Фамилия", NAME_MAX_LENGTH, NAME_PATTERN)

    @staticmethod
    def validate_first_name(value):
        return Client._validate_string(value, "Имя", NAME_MAX_LENGTH, NAME_PATTERN)

    @staticmethod
    def validate_patronymic(value):
        return Client._validate_string(value, "Отчество", NAME_MAX_LENGTH, NAME_PATTERN,
                                       required=False)

    @staticmethod
    def validate_phone(value):
        if isinstance(value, str):
            value = re.sub(r"[\s()\-]", "", value)
        value = Client._validate_string(value, "Телефон", 12, PHONE_PATTERN)
        return "+7" + value[-10:]

    @staticmethod
    def validate_address(value):
        return Client._validate_string(value, "Адрес", ADDRESS_MAX_LENGTH)

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
