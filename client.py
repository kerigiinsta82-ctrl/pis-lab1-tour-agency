"""Сущность «Клиент» туристической фирмы — полная версия данных."""

from client_short import ClientShort

ADDRESS_MAX_LENGTH = 200


class Client(ClientShort):
    """Клиент туристической фирмы (полные данные).

    Наследует от ClientShort конструктор, валидацию, вывод и сравнение,
    добавляет только поле «адрес» и полный вывод.
    Объект с недопустимыми значениями полей создать невозможно:
    конструктор заполняет поля через свойства с валидацией.
    """

    FIELDS = ClientShort.FIELDS + ("address",)

    def to_short(self):
        """Краткая версия клиента."""
        return ClientShort.from_client(self)

    def __str__(self):
        """Полная версия объекта (переопределяет краткий вывод базового класса)."""
        return f"Клиент #{self.client_id}: {self.full_name}, тел.: {self.phone}, адрес: {self.address}"

    @staticmethod
    def validate_address(value):
        return ClientShort._validate_string(value, "Адрес", ADDRESS_MAX_LENGTH)

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = Client.validate_address(value)
