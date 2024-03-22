import json
import os
from dataclasses import is_dataclass, asdict
from datetime import datetime

from dateutil.relativedelta import relativedelta

from app.schemas import Stock


def change_extension(filename, new_extension):
    base, _ = os.path.splitext(filename)
    return f'{base}.{new_extension}'


def exception(error: Exception, message: str | None = None):
    if message is None:
        message = 'error'
    return {'error': error, 'message': message}


def dataclass_to_dict(obj):
    if is_dataclass(obj):
        return asdict(obj)
    elif isinstance(obj, (list, tuple)):
        return [dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    else:
        return obj


def get_date_difference(date: str | datetime, interval='d') -> int:
    if isinstance(date, str):
        start_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    elif isinstance(date, datetime):
        start_date = date
    else:
        raise ValueError(f'{__name__}: Invalid date format')
    end_date = datetime.now()

    if interval == 'd':
        diff = (end_date - start_date).days
        return abs(diff)
    elif interval == 'm':
        diff = relativedelta(end_date, start_date)
        return abs(diff.years * 12 + diff.months)


def days_declension(days: int) -> str:
    """
    Склоняет слово 'день' в зависимости от количества дней.
    :param days: Количество дней
    :return:
    """
    if days % 10 == 1:
        return 'день'
    if days % 10 in [2, 3, 4]:
        return 'дня'
    return 'дней'


def save_file(
    content: str,
    filename: str,
):
    with open(filename, 'w') as file:
        file.write(content)


def read_grouped_json(
    json_filename: str,
) -> dict:
    """
    items сразу конвертируем в Stock
    :param json_filename:
    :return: {'category': {'in stock' [items]}, {'not in stock': [items]}}
    """
    with open(json_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return convert_grouped_to_stock(data)


def convert_grouped_to_stock(data: dict) -> dict:
    stock_dict = {}
    for category, stock_status in data.items():
        for status, stock_list in stock_status.items():
            for item in stock_list:
                stock = Stock(**item)
                stock_dict.setdefault(category, {}).setdefault(status, []).append(stock)

    return stock_dict


def convert_date(date_time: str | datetime) -> str:
    """
    :param date_time: дата или строка в формате 'YYYY-MM-DD HH:MM:SS'
    :return: дата в формате 'DD.mmm.YYYY'
    """
    months = ['янв.', 'фев.', 'мар.', 'апр.', 'май', 'июн.', 'июл.', 'авг.', 'сен.', 'окт.', 'ноя.', 'дек.']
    if isinstance(date_time, datetime):
        date_time_str = date_time.strftime('%Y-%m-%d H:%M:%S')
    elif isinstance(date_time, str):
        date_time_str = date_time
    else:
        raise ValueError(f'{__name__} convert_date: datetime must be str or datetime')
    date_str = date_time_str.split(' ')
    parts = date_str[0].split('-')
    return f"{int(parts[2]):02d} {months[int(parts[1])-1]} {parts[0]}"
