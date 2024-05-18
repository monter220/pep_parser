import csv
from datetime import datetime

from pep_parse.settings import BASE_DIR


class PepParsePipeline:

    def open_spider(self, spider):
        self.counter = {}

    def process_item(self, item, spider):
        self.counter[item['status']] = self.counter.setdefault(
            item['status'], 0) + 1
        return item

    def close_spider(self, spider):
        time = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        path = BASE_DIR / f'results/status_summary_{time}.csv'
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Status', 'Amount'])
            writer.writerows(self.counter.items())
            writer.writerow(['Total', sum(self.counter.values())])
