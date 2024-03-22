import os

from app.schemas import InStock
from app.services.utils import get_date_difference, days_declension
from app.settings import BASE_DIR

STRING_HEADER = 'Позиции, отсутствующие на складе'
STRING_NOT_IN_STOCK = 'отсутствует на складе'

EMAIL_TEMPLATE = os.path.join(BASE_DIR, 'files', 'email_template.txt')


def generate_text_report(data: dict) -> str:
    """
    :param data: структура типа: {'category': {'in stock' [Stock]}, {'not in stock': [Stock]}}
    :return: сгенерированный текст
    """
    text = f'{STRING_HEADER}\n'
    for category, categories in data.items():
        text += f'{category}: \n'
        for is_in_stock, items in categories.items():
            if is_in_stock == InStock.IN_STOCK:
                # Если есть в наличии - продолжаем
                continue
            for item in items:
                days = get_date_difference(item.date_ordered)
                days = f'{days} {days_declension(days)}'
                text += f'{item.name} {STRING_NOT_IN_STOCK} {days}\n'
    return text
