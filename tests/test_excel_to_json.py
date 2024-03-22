import os

import pytest

from app.RMP_Test import RMP_Test
from app.services.excel_to_json import ExcelToJson
from app.services.utils import change_extension
from tests.conftest import XLS_FILE, COUNT_ROWS


def test_read_excel_file_ok(temp_file):
    assert os.path.exists(XLS_FILE)
    result = RMP_Test.excel_to_json(XLS_FILE, temp_file.name, overwrite=True)
    # для получения dataset.json:
    # result = RMP_Test.excel_to_json(XLS_FILE, change_extension(XLS_FILE, 'json'), overwrite=True)
    assert os.path.exists(temp_file.name)
    assert len(result) == COUNT_ROWS


def test_excel_to_json_wrong_file_content(temp_file):
    with pytest.raises(ValueError):
        ExcelToJson(change_extension(XLS_FILE, 'json')).parse()


def test_rmp_read_excel_file_wrong_file_content(temp_file):
    result = RMP_Test.excel_to_json(temp_file.name)
    assert 'Could not parse file' in result['message']


def test_read_excel_file_error_file_exists(temp_file):
    with open(temp_file.name, 'w') as file:
        file.write('Error')
    result = RMP_Test.excel_to_json(XLS_FILE, temp_file.name, overwrite=False)
    assert result['message'] == f'File {temp_file.name} already exists'


def test_read_excel_file_error_file_not_exists(faker):
    wrong_file = f'{faker.word()}.{faker.word()}'
    result = RMP_Test.excel_to_json(wrong_file)
    assert result['message'] == f'File {wrong_file} not found'


def test_read_excel_validate_error(excel_wrong_structure):
    result = RMP_Test.excel_to_json(excel_wrong_structure)
    assert 'unexpected keyword' in result['message']


def test_validated(temp_file):
    result = RMP_Test().excel_to_json(XLS_FILE, temp_file.name, overwrite=True)
    assert isinstance(result, list)
    assert os.path.exists(temp_file.name)
    assert os.path.getsize(temp_file.name) > 0

