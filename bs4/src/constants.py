from pathlib import Path


MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
RESULTS_DIR = 'results'
DOWNLOAD_DIR = 'downloads'
CHOICE_PRETTY = 'pretty'
CHOICE_FILE = 'file'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted', ),
    'D': ('Deferred', ),
    'F': ('Final', ),
    'P': ('Provisional', ),
    'R': ('Rejected', ),
    'S': ('Superseded', ),
    'W': ('Withdrawn', ),
    '': ('Draft', 'Active', ),
}
