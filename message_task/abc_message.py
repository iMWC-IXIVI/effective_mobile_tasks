import enum

from abc import ABC, abstractmethod

from exceptions import MessageValueError, ParserValueError


class TypeMessage(enum.Enum):
    """
    Класс Enum для перечисления источников
    """
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


class JSONMessage(ABC):
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
        """Возвращение сообщения"""
        pass


class TelegramMessage(JSONMessage):
    def to_dict(self) -> dict:
        return self.payload


class MattermostMessage(JSONMessage):
    def __init__(self, payload: dict):
        super().__init__(TypeMessage.MATTERMOST, payload)

    def to_dict(self) -> dict:
        return self.payload


class SlackMessage(JSONMessage):
    def __init__(self, payload: dict):
        super().__init__(TypeMessage.SLACK, payload)

    def to_dict(self) -> dict:
        return self.payload


class ParsedMessage:
    def __init__(self, type_message: TypeMessage, payload: dict):
        self.type_message = type_message
        self.payload = payload

    def to_dict(self):
        return {
            'type': self.type_message.name,
            'payload': self.payload
        }


class Parser(ABC):
    @abstractmethod
    def parse(self, message: JSONMessage) -> ParsedMessage:
        """Преобразование сообщения в нужный тип сообщения"""
        pass


class TelegramParser(Parser):
    def parse(self, message: JSONMessage):
        return ParsedMessage(TypeMessage.TELEGRAM, message.payload)


class MattermostParser(Parser):
    def parse(self, message: JSONMessage):
        return ParsedMessage(TypeMessage.MATTERMOST, message.payload)


class SlackParser(Parser):
    def parse(self, message: JSONMessage):
        return ParsedMessage(TypeMessage.SLACK, message.payload)


class FactoryParser:
    def create_parser(self, message_type: TypeMessage) -> Parser:
        """Создание фабрики парсера"""
        parsers = {
            TypeMessage.TELEGRAM: TelegramParser,
            TypeMessage.MATTERMOST: MattermostParser,
            TypeMessage.SLACK: SlackParser
        }
        parser = parsers.get(message_type)

        if not parser:
            raise ParserValueError('Данное парсера не существует')

        return parser()
