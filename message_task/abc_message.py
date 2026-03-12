import enum

from abc import ABC, abstractmethod

from exceptions import MessageValueError, ParserValueError


class TypeMessage(enum.Enum):
    """Класс Enum для перечисления источников
    TELEGRAM = enum.auto()
    """
    TELEGRAM = enum.auto()


class MainMessage(ABC):
    def __init__(self, message_type: TypeMessage, payload: dict):
        """Обязательные атрибуты
        :param message_type: TypeMessage (тип сообщения)
        :param payload: dict (тело сообщения)"""
        if not message_type or not isinstance(message_type, TypeMessage):
            raise MessageValueError('Тип сообщения должен быть не пустым либо иметь тип TypeMessage')

        if not payload or not isinstance(payload, dict):
            raise MessageValueError('Тело сообщения должен быть не пустым либо принадлежать типа dict')

        self.message_type = message_type
        self.payload = payload

    @abstractmethod
    def to_dict(self) -> dict:
        """Создаёт унифицированное представление сообщений"""


class Parser(ABC):
    def __init__(self, type_message: TypeMessage):
        if not type_message or not isinstance(type_message, TypeMessage):
            raise ParserValueError('Тип сообщения должен быть не пустым либо иметь тип TypeMessage')

        self.type_message = type_message

    @abstractmethod
    def parser(self) -> dict:
        """Реализация парсера"""


class TelegramParser(Parser):
    def __init__(self):
        super().__init__(TypeMessage.TELEGRAM)

    def parser(self):
        """Реализация парсера telegram"""


class FactoryParser:
    def create_parser(self, message_type: TypeMessage) -> Parser:
        """Создание фабрики парсера"""
        parsers = {
            TypeMessage.TELEGRAM: TelegramParser
        }
        parser = parsers.get(message_type)

        if not parser:
            raise ParserValueError('Данное парсера не существует')

        return parser()
