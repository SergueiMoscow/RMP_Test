import json
import os

from app.RMP_Test import RMP_Test
from app.settings import BASE_DIR
from tests.conftest import GROUPED_JSON


def test_generate_html(temp_file):
    output_file_name = os.path.join(BASE_DIR, 'files', 'result.html')
    html_content = RMP_Test.generate_html(GROUPED_JSON, output_file_name)
    html_content = RMP_Test.generate_html(GROUPED_JSON, temp_file.name)
    with open(GROUPED_JSON, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for category in data:
        for in_stock in data[category]:
            for item in data[category][in_stock]:
                assert item['name'] in html_content
    assert html_content is not None
