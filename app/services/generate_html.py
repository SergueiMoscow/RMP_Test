import os
from yattag import Doc, indent
from app.services.utils import get_date_difference, convert_date
from app.settings import BASE_DIR

CSS_FILE = os.path.join(BASE_DIR, 'files', 'styles.css')

FIELDS = {
    'name': {'text': 'Название', 'class': 'left'},
    'date_added': {'text': 'Дата создания', 'class': 'left', 'func': convert_date},
    'date_ordered': {'text': 'Дата посл. заказа', 'class': 'left', 'func': convert_date},
    'price': {'text': 'Стоимость', 'class': 'right'},
    'stock': {'text': 'В наличии на складе', 'class': 'right'},
}


def get_doc_tag_text():
    doc, tag, text = Doc().tagtext()
    return doc, tag, text


def read_css_file(css_file_path):
    with open(css_file_path, 'r') as file:
        return file.read()


def create_table(data, tag, text):
    """
    Создает HTML-таблицу с данными.
    """
    with tag('table'):
        with tag('tr'):
            for field in FIELDS:
                with tag('th', klass=FIELDS[field].get('class', '')):
                    text(FIELDS[field]['text'])
        for category, categories in data.items():
            with tag('tr'):
                with tag('td', colspan=len(FIELDS), klass='category'):
                    text(category)
            for is_in_stock, items in categories.items():
                with tag('tr'):
                    with tag('td', colspan=len(FIELDS), klass='in-stock'):
                        text(is_in_stock)
                for item in items:
                    with tag('tr'):
                        month_diff = get_date_difference(item.date_ordered, 'm')
                        for field in FIELDS:
                            klass = 'old-order' if month_diff > 3 else 'td'
                            additional_class = FIELDS[field].get('class', '')
                            if additional_class:
                                klass += f" {additional_class}"
                            with tag('td', klass=klass):
                                value = FIELDS[field]['func'](getattr(item, field)) if FIELDS[field].get('func') else getattr(item, field)
                                text(value)


def generate_stock_report(data: dict, css_file: str = CSS_FILE, block_after_table: str = '') -> str:
    """
    Генерирует HTML отчет о состоянии склада товаров.
    """
    doc, tag, text = get_doc_tag_text()
    with tag('html'):
        with tag('head'):
            with tag('style'):
                css_content = read_css_file(css_file)
                text(css_content)
        with tag('body'):
            with tag('div', klass='container'):
                create_table(data=data, tag=tag, text=text)
                if block_after_table:
                    with tag('p'):
                        doc.asis(block_after_table)
    html = indent(doc.getvalue())
    return html

