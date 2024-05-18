import re
import logging
import requests_cache
from urllib.parse import urljoin
from tqdm import tqdm

from utils import get_soup, find_tag
from outputs import control_output
from configs import configure_argument_parser, configure_logging
from constants import MAIN_DOC_URL, PEP_DOC_URL, DOWNLOAD_DIR, BASE_DIR
from exceptions import (
    ParserFindVersionException,
)


def whats_new(session):
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    sections_by_python = soup.select(
        'section#what-s-new-in-python div.toctree-wrapper li.toctree-l1')
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = get_soup(session, version_link)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    soup = get_soup(session, MAIN_DOC_URL)
    ul_tags = soup.select('div.sphinxsidebarwrapper ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindVersionException(
            f'В {MAIN_DOC_URL} не нашлось блока с версиями')
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    pdf_a4_tag = soup.select(
        'div[role="main"] table.docutils td a[href*="pdf-a4.zip"]'
    )
    pdf_a4_link = pdf_a4_tag[0]['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOAD_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    results = [('Status', 'Amount')]
    counter = {'Total': 0, }
    soup = get_soup(session, PEP_DOC_URL)
    row_tags = soup.select('section#numerical-index tbody tr')
    for tr in tqdm(row_tags, desc='Пересчитываем статусы'):
        pep_url = urljoin(PEP_DOC_URL, find_tag(tr, 'a')['href'])
        soup = get_soup(session, pep_url)
        dl_tag = find_tag(soup, 'dl', {'class': 'rfc2822 field-list simple'})
        table_status = tr.abbr['title'].split(', ')[1]
        for tag_dt in dl_tag:
            if tag_dt.name == 'dt' and tag_dt.text == 'Status:':
                page_status = tag_dt.next_sibling.next_sibling.string
                if page_status != table_status:
                    logging.info(
                        f'Несовпадающие статусы: {pep_url} '
                        f'Статус в карточке: {page_status} '
                        f'Ожидаемые статусы: {table_status}'
                    )
                counter.setdefault(page_status, 0)
                counter[page_status] += 1
                counter['Total'] += 1
    [results.append((key, counter[key])
                    ) for key in counter.keys() if key != 'Total']
    results.append(('Total', counter['Total']))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    try:
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(f'Аргументы командной строки: {args}')

        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()

        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.error(error, stack_info=True)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
