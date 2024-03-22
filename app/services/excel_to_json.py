import dataclasses
import os
from typing import List

import pandas as pd
import json

from app.schemas import Stock
from app.services.utils import change_extension


class ExcelToJson:

    def __init__(self, excel_filename: str):
        self.excel_filename: str = excel_filename
        # Инициализируем всё здесь
        self.pd_data = None
        self.json_filename: str | None = None
        self.overwrite: bool = False
        self.validated_stock: List[Stock] | None = None

    def parse(
        self,
    ) -> 'ExcelToJson':
        if not os.path.exists(self.excel_filename):
            raise FileNotFoundError(f'File {self.excel_filename} not found')
        self.pd_data = pd.read_excel(self.excel_filename)
        return self

    def _check_out_file_name(self) -> str:
        # Если бы это не было тестовым заданием, то нужно было бы добавить проверку наличия директории
        # и её создание в случае отсутствия.
        if not os.path.exists(self.json_filename) or self.overwrite:
            return self.json_filename
        raise FileExistsError(f'File {self.json_filename} already exists')

    def save_not_validated(
        self,
        json_file_name: str | None = None,
        overwrite: bool = False,
    ) -> 'ExcelToJson':
        if not json_file_name:
            json_file_name = change_extension(self.excel_filename, 'json')
        self.overwrite = overwrite
        self.json_filename = json_file_name
        out_file = self._check_out_file_name()
        json_data = self.pd_data.to_json(orient='records', force_ascii=False)
        with open(out_file, 'w', encoding='utf-8') as file:
            file.write(json_data)
        return self

    def validate_stock(self) -> 'ExcelToJson':
        """
        Для валидации структуры входного файла используем схему Pydantic
        Если структура не валидная, рейзится ValidationError, который отлавливается на уровне выше.
        На это есть тест text_excel_to_json.test_read_excel_validate_error
        """
        self.validated_stock = [Stock(**row) for row in self.pd_data.to_dict(orient='records')]
        for item in self.validated_stock:
            # Даты переводим в валидный для сериализации формат
            if isinstance(item.date_added, pd.Timestamp):
                item.date_added = item.date_added.to_pydatetime()
            if isinstance(item.date_ordered, pd.Timestamp):
                item.date_ordered = item.date_ordered.to_pydatetime()

        return self

    def get_validated_json(self):
        if not self.validated_stock:
            self.validate_stock()
        result = []
        for item in self.validated_stock:
            result.append(dataclasses.asdict(item))
        return result

    def save_validated(
        self,
        json_file_name: str,
        overwrite: bool = False,
    ) -> 'ExcelToJson':
        self.json_filename = json_file_name
        self.overwrite = overwrite
        self._check_out_file_name()
        result = self.get_validated_json()
        with open(self.json_filename, 'w', encoding='utf-8') as file:
            json.dump(result, file, default=str, ensure_ascii=False, indent=4)
        return self
