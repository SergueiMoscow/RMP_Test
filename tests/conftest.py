import os
import shutil
import tempfile

import pandas as pd
import pytest
import xlrd
import xlutils

from app.settings import BASE_DIR

XLS_FILE = os.path.join(BASE_DIR, 'files', 'dataset.xls')
COUNT_ROWS = 9
GROUPED_JSON = os.path.join(BASE_DIR, 'files', 'grouped.json')


@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile() as temp_file:
        yield temp_file


@pytest.fixture
def excel_wrong_structure(faker):
    with tempfile.NamedTemporaryFile(suffix='.xlsx') as temp_file:
        shutil.copy(XLS_FILE, temp_file.name)
        df = pd.read_excel(XLS_FILE)
        df.rename(columns={df.columns[0]: faker.word()}, inplace=True)
        df.to_excel(temp_file.name, index=False)
        yield temp_file.name
