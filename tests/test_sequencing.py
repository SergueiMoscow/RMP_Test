import json

from app.RMP_Test import RMP_Test
from app.services.utils import change_extension
from tests.conftest import XLS_FILE


def test_sequencing(temp_file):
    html_content = RMP_Test.sequencing(XLS_FILE, temp_file.name)
    # файл dataset.json должен иметь импортированные данные из excel
    with open(change_extension(XLS_FILE, 'json'), 'r') as file:
        items = json.load(file)
    for item in items:
        assert item['name'] in html_content
