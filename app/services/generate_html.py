import os

from yattag import Doc, indent

from app.services.utils import get_date_difference, convert_date
from app.settings import BASE_DIR

CSS_FILE = os.path.join(BASE_DIR, 'files', 'styles.css')


def generate_stock_report(
    data: dict,
    css_file: str = CSS_FILE,
) -> str:
    """
    :param data: структура типа: {'category': {'in stock' [Stock]}, {'not in stock': [Stock]}}
    Эту структуру можно получить из уже сгруппированного json, используя функцию read_grouped_json()
    :param css_file: вставляемые внутрь html стили
    :return: - str html content
    """
    fields = {
        'name': {'text': 'Название', 'class': 'left'},
        'date_added': {'text': 'Дата создания', 'class': 'left', 'func': convert_date},
        'date_ordered': {'text': 'Дата посл. заказа', 'class': 'left', 'func': convert_date},
        'price': {'text': 'Стоимость', 'class': 'right'},
        'stock': {'text': 'В наличии на складе', 'class': 'right'},
    }
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('style'):
                with open(css_file, 'r') as file:
                    styles = file.read()
                text(styles)
        with tag('body'):
            with tag('div', klass='container'):
                with tag('table'):
                    with tag('tr'):
                        for field in fields:
                            with tag('th'):
                                text(fields[field]['text'])
                    for category, categories in data.items():
                        with tag('tr'):
                            with tag('td', colspan=len(fields), klass='category'):
                                text(category)
                        for is_in_stock, items in categories.items():
                            with tag('tr'):
                                with tag('td', colspan=len(fields), klass='in-stock'):
                                    text(is_in_stock)
                            for item in items:
                                with tag('tr'):
                                    month_diff = get_date_difference(item.date_ordered, 'm')
                                    for field in fields:
                                        if month_diff > 3:
                                            klass = 'old-order'
                                        else:
                                            klass = 'td'
                                        if fields[field].get('class', ''):
                                            klass += ' ' + fields[field].get('class')
                                        with tag('td', klass=klass):
                                            if fields[field].get('func'):
                                                value = fields[field]['func'](getattr(item, field))
                                            else:
                                                value = getattr(item, field)
                                            text(value)

    html = indent(doc.getvalue())
    return html
