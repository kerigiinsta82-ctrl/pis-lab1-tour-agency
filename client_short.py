"""Базовый класс иерархии: краткие данные клиента (ФИО и один контакт, без адреса)."""

import json
import re

NAME_PATTERN = re.compile(r"[А-ЯЁA-Z][а-яёa-z]+(?:-[А-ЯЁA-Z][а-яёa-z]+)?")
PHONE_PATTERN = re.compile(r"(?:\+7|8)\d{10}")
NAME_MAX_LENGTH = 50


class ClientShort:
    """Краткие данные клиента: id, ФИО, телефон.

    Содержит всю общую логику иерархии:
    перегруженный конструктор, валидацию, вывод и сравнение.
    Наследники только расширяют кортеж FIELDS и добавляют свои свойства.
    """

    # Порядок полей: используется в позиционном конструкторе и в строковом формате.
    FIELDS = ("client_id", "last_name", "first_name", "patronymic", "phone")
    OPTIONAL_FIELDS = ("patronymic",)
    STRING_SEPARATOR = ";"

    def __init__(self, *args, **kwargs):
        """Перегруженный конструктор.

        Варианты вызова (для наследника Client добавляется поле address):
            ClientShort(1, "Иванов", "Иван", "Иванович", "+79161234567")
            ClientShort(client_id=1, last_name="Иванов", ...)
            ClientShort("1;Иванов;Иван;Иванович;+79161234567")
            ClientShort('{"client_id": 1, "last_name": "Иванов", ...}')
            ClientShort({"client_id": 1, "last_name": "Иванов", ...})
        """
        if len(args) == 1 and not kwargs and isinstance(args[0], (str, dict)):
            args, kwargs = (), self._parse(args[0])
        values = self._bind_arguments(args, kwargs)
        for field in self.FIELDS:
            setattr(self, field, values[field])

    @classmethod
    def _bind_arguments(cls, args, kwargs):
        """Сопоставляет позиционные и именованные аргументы с полями."""
        if len(args) > len(cls.FIELDS):
            raise TypeError(f"Ожидается не более {len(cls.FIELDS)} аргументов, "
                            f"передано {len(args)}")
        values = dict(zip(cls.FIELDS, args))
        for name, value in kwargs.items():
            if name not in cls.FIELDS:
                raise TypeError(f"Неизвестное поле: {name!r}")
            if name in values:
                raise TypeError(f"Поле {name!r} передано дважды")
            values[name] = value
        for field in cls.OPTIONAL_FIELDS:
            values.setdefault(field, None)
        missing = [field for field in cls.FIELDS if field not in values]
        if missing:
            raise TypeError(f"Не заданы поля: {', '.join(missing)}")
        return values

    @classmethod
    def _parse(cls, data):
        """Разбирает словарь, JSON-строку или строку с разделителем в словарь полей."""
        if isinstance(data, dict):
            return dict(data)
        text = data.strip()
        if text.startswith("{"):
            return cls._parse_json(text)
        return cls._parse_separated(text)

    @staticmethod
    def _parse_json(text):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as error:
            raise ValueError(f"Некорректный JSON: {error}") from error
        if not isinstance(data, dict):
            raise ValueError("JSON должен описывать объект")
        return data

    @classmethod
    def _parse_separated(cls, text):
        # Последнее поле может само содержать разделитель — ограничиваем split.
        parts = text.split(cls.STRING_SEPARATOR, len(cls.FIELDS) - 1)
        if len(parts) != len(cls.FIELDS):
            raise ValueError(f"Строка должна содержать {len(cls.FIELDS)} полей, "
                             f"разделённых {cls.STRING_SEPARATOR!r}")
        return dict(zip(cls.FIELDS, (part.strip() for part in parts)))

    @classmethod
    def from_client(cls, client):
        """Создаёт объект класса cls из любого объекта иерархии (берёт только нужные поля)."""
        return cls(**{field: getattr(client, field) for field in cls.FIELDS})

    # ---------- вывод и сравнение ----------

    @property
    def full_name(self):
        """Фамилия Имя Отчество."""
        parts = (self.last_name, self.first_name, self.patronymic)
        return " ".join(part for part in parts if part)

    @property
    def short_name(self):
        """Фамилия И. О."""
        initials = " ".join(f"{part[0]}." for part in (self.first_name, self.patronymic) if part)
        return f"{self.last_name} {initials}"

    def to_dict(self):
        return {field: getattr(self, field) for field in self.FIELDS}

    def short_str(self):
        """Краткая версия объекта."""
        return f"{self.short_name}, тел.: {self.phone}"

    def __str__(self):
        return self.short_str()

    def __repr__(self):
        args = ", ".join(f"{field}={value!r}" for field, value in self.to_dict().items())
        return f"{type(self).__name__}({args})"

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    # Объект изменяемый, поэтому хешировать его нельзя (иначе сломаются множества/словари).
    __hash__ = None

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
        if isinstance(value, str) and value.strip().isdigit():
            value = int(value)
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("ID клиента должен быть целым числом")
        if value <= 0:
            raise ValueError("ID клиента должен быть положительным")
        return value

    @staticmethod
    def validate_last_name(value):
        return ClientShort._validate_string(value, "Фамилия", NAME_MAX_LENGTH, NAME_PATTERN)

    @staticmethod
    def validate_first_name(value):
        return ClientShort._validate_string(value, "Имя", NAME_MAX_LENGTH, NAME_PATTERN)

    @staticmethod
    def validate_patronymic(value):
        return ClientShort._validate_string(value, "Отчество", NAME_MAX_LENGTH, NAME_PATTERN,
                                            required=False)

    @staticmethod
    def validate_phone(value):
        if isinstance(value, str):
            value = re.sub(r"[\s()\-]", "", value)
        value = ClientShort._validate_string(value, "Телефон", 12, PHONE_PATTERN)
        return "+7" + value[-10:]

    # ---------- свойства ----------

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        self.__client_id = ClientShort.validate_client_id(value)

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = ClientShort.validate_last_name(value)

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = ClientShort.validate_first_name(value)

    @property
    def patronymic(self):
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, value):
        self.__patronymic = ClientShort.validate_patronymic(value)

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = ClientShort.validate_phone(value)
