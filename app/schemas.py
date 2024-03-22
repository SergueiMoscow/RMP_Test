from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class InStock(Enum):
    IN_STOCK = 'В наличии'
    NOT_IN_STOCK = 'Нет в наличии'


@dataclass
class Stock:
    name: str
    category: str
    date_added: datetime
    date_ordered: datetime
    price: int
    height: int
    width: int
    length: int
    stock: int
    is_in_stock: str | None = None  # Поле для группировки. Заполняется в group_json

    def __post_init__(self):
        if self.stock > 0:
            self.is_in_stock = InStock.IN_STOCK.value
        else:
            self.is_in_stock = InStock.NOT_IN_STOCK.value
        for field in self.__dataclass_fields__.values():
            if not hasattr(self, field.name):
                raise ValueError(f"Field '{field.name}' must be provided")
