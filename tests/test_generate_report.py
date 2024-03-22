from app.RMP_Test import RMP_Test
from app.schemas import InStock
from app.services.utils import read_grouped_json, change_extension
from tests.conftest import GROUPED_JSON


def test_generate_report(temp_file):
    RMP_Test.generate_report(GROUPED_JSON, temp_file.name)
    # для получения текстового файла в /files
    # RMP_Test.generate_report(GROUPED_JSON, change_extension(GROUPED_JSON, 'txt'))
    with open(temp_file.name, 'r') as file:
        content = file.read()
    data = read_grouped_json(GROUPED_JSON)
    for category, categories in data.items():
        for is_in_stock, items in categories.items():
            if is_in_stock == InStock.IN_STOCK:
                continue
            for item in items:
                assert item.name in content
