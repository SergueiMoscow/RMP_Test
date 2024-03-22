import os
import tempfile

import pytest

from app.RMP_Test import RMP_Test
from app.services.utils import change_extension
from tests.conftest import XLS_FILE, COUNT_ROWS, GROUPED_JSON


def test_group_stock(temp_file):
    # Сначала получаем негруппированный json
    json_file_not_grouped = tempfile.NamedTemporaryFile(delete_on_close=False)
    RMP_Test.excel_to_json(XLS_FILE, json_file_not_grouped.name, overwrite=True)
    json_file_not_grouped.close()

    result = RMP_Test.group_stock_from_json(json_file_not_grouped.name, temp_file.name)
    # для получения GROUPED_JSON:
    # result = RMP_Test.group_stock_from_json(json_file_not_grouped.name, GROUPED_JSON)
    # Удаляем временный файл
    os.remove(json_file_not_grouped.name)
    assert os.path.exists(temp_file.name)
    count_items = 0
    for key, categories in result.items():
        for is_in_stock, items in categories.items():
            count_items += len(items)
            for i in range(1, len(items)):
                # Проверяем is_in_stock внутри каждой категории
                if is_in_stock == 0 and i == 1:
                    count_items += 1
                    continue  # Пропускаем, если первый is_in_stock = 0
                assert items[i - 1].is_in_stock >= items[i].is_in_stock
                # Проверяем date_ordered внутри каждой категории
                assert items[i - 1].date_ordered >= items[i].date_ordered
    assert count_items == COUNT_ROWS
