from requests import RequestException


class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ParserNoneResponseException(Exception):
    """Вызывается, когда парсер не может получить отклик."""
    pass


class ParserFindVersionException(Exception):
    """
    Вызывается, когда парсер не может найти 'All versions' в latest_versions.
    """
    pass


class ParserRequestException(RequestException):
    """Вызывается, когда парсер получает ошибку вместо ответа."""
    pass
