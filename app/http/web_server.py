import json
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

from app import settings
from app.http.templates import get_template, merge_template
from app.http.web_utils import save_uploaded_file, get_form_value
from app.services.excel_to_json import ExcelToJson
from app.services.generate_html import generate_stock_report
from app.services.generate_text_report import generate_text_report
from app.services.group_json import GroupStock
from app.services.utils import dataclass_to_dict, convert_grouped_to_stock


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def response(self, content, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8', )
        self.end_headers()
        if isinstance(content, str):
            content = content.encode()
        self.wfile.write(content)

    def get_form_field(self, field_name: str):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        return form[field_name].file.read()

    def step1_get(self):
        content = get_template('step1.html')
        return self.response(content)

    def step1_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        with tempfile.NamedTemporaryFile(suffix='xls') as temp_file:
            save_uploaded_file(post_data, temp_file.name)
            message = 'File uploaded successfully'
            json_list = ExcelToJson(temp_file.name).parse().get_validated_json()
        json_string = json.dumps(json_list, default=str, indent=4, ensure_ascii=False)
        template = get_template('step2.html')
        content = merge_template(template, {'message': message, 'json': json_string, 'action': '/step2'})
        self.response(content)

    def step2_post(self):
        json_string = self.get_form_field('json_string')
        group_stock = GroupStock().load_json_data(json.loads(json_string)).group_stock()
        formatted_json = json.dumps(dataclass_to_dict(group_stock), indent=4, ensure_ascii=False)

        template = get_template('step2.html')
        content = merge_template(
            template=template,
            values={'message': 'Сгруппированные данные', 'json': formatted_json, 'action': '/step3'},
        )
        self.response(content)

    def step3_post(self):
        json_string = self.get_form_field('json_string')
        prepared_data = convert_grouped_to_stock(json.loads(json_string))
        content = generate_stock_report(prepared_data)
        email_text = generate_text_report(prepared_data).replace('\n', '<br/>')
        content = content.replace('</table>', f'</table><p>{email_text}</p>')
        self.response(content)

    def do_GET(self):
        routes = {
            '/': self.step1_get,
        }
        print(f'route "{self.path}"')
        handler = routes.get(self.path, None)
        if handler:
            print(f'handler "{handler}"')
            handler()
            print(f'handler "{handler} отработал"')
        else:
            print(f'route "{self.path} не найден"')
            self.send_response(404)
            self.end_headers()
            content = f'Not found "{self.path}"'
            self.wfile.write(content.encode())

    def do_POST(self):
        routes = {
            '/step1': self.step1_post,
            '/step2': self.step2_post,
            '/step3': self.step3_post,
        }
        handler = routes.get(self.path, None)
        if handler:
            handler()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {settings.SERVER_PORT}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
