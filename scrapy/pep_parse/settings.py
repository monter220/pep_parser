from pathlib import Path


BOT_NAME: str = 'pep_parse'

BASE_DIR = Path(__file__).parent.parent
PATTERN: str = 'PEP (\\w+) . (\\w.*)'

SPIDER_MODULES = ['pep_parse.spiders']


ROBOTSTXT_OBEY: bool = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    'results/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    },
}
