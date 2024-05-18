from requests import RequestException
from bs4 import BeautifulSoup

from exceptions import (
    ParserFindTagException,
    ParserNoneResponseException,
    ParserRequestException,
)


def get_response(session, url, encode='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encode
        if response is not None:
            return response
        raise ParserNoneResponseException(
            f'Страница {url} не ответила'
        )
    except RequestException:
        raise ParserRequestException(
            f'Возникла ошибка при загрузке страницы {url}'
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(f'Не найден тег {tag} {attrs}')
    return searched_tag


def get_soup(session, url, encode='utf-8', feature='lxml'):
    return BeautifulSoup(
        get_response(session, url, encode).text, features=feature)
