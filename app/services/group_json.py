import json
from itertools import groupby
from operator import itemgetter
from typing import List

from app.schemas import Stock, InStock
from app.services.utils import dataclass_to_dict


class GroupStock:

    stocks: List[Stock]

    def __init__(self, stocks: List[Stock] | None = None):
        self.grouped_data = None
        if stocks:
            self.stocks = stocks

    def read_from_json(self, json_file: str) -> 'GroupStock':
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return self.load_json_data(data)

    def load_json_data(self, json_data: list) -> 'GroupStock':
        result = [Stock(**row) for row in json_data]
        self.stocks = result
        return self

    def group_stock(self) -> dict:
        data = sorted(self.stocks, key=lambda x: x.category)

        grouped_data = {}
        for key, group in groupby(data, key=lambda x: x.category):
            inner_group = list(group)
            grouped_data[key] = {}
            for key_is_in_stock in [InStock.IN_STOCK.value, InStock.NOT_IN_STOCK.value]:
                group_is_in_stock = [item for item in inner_group if item.is_in_stock == key_is_in_stock]
                sorted_group_is_in_stock = sorted(group_is_in_stock, key=lambda x: x.date_ordered, reverse=True)
                grouped_data[key][key_is_in_stock] = sorted_group_is_in_stock
        self.grouped_data = grouped_data
        return grouped_data

    def save_grouped_data(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(dataclass_to_dict(self.grouped_data), file, ensure_ascii=False, indent=4)
