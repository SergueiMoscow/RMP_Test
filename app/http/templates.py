import os

from app.settings import BASE_DIR

TEMPLATE_DIR = os.path.join(BASE_DIR, 'app', 'http', 'templates')


def get_template(html_file: str) -> str:
    full_name = os.path.join(TEMPLATE_DIR, html_file)
    with open(full_name, 'r') as file:
        content = file.read()
    return content


def merge_template(template: str, values: dict) -> str:
    for key, value in values.items():
        template = template.replace('{{' + key + '}}', value)
    return template
