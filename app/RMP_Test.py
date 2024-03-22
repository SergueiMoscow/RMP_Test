from typing import List

from app.schemas import Stock
from app.services.excel_to_json import ExcelToJson
from app.services.generate_html import generate_stock_report
from app.services.generate_text_report import generate_text_report
from app.services.group_json import GroupStock
from app.services.utils import exception, change_extension, save_file, read_grouped_json


class RMP_Test:

    @classmethod
    def excel_to_json(
        cls,
        excel_filename: str,
        json_filename: str | None = None,
        overwrite: bool = False,
    ) -> List[Stock] | dict:
        """
        # dict возвращаем в случае ошибки.
        # Не совсем верно, но обработчик ошибок - отдельная тема,
        # выходящая за рамки тестового задания
        :param excel_filename: required
        :param json_filename: если None - меняем расширение excel_filename на json
        :param overwrite: default False
        :return: List[Stock]
        """
        # Читаем из файла (п.1 ТЗ)
        parser = ExcelToJson(excel_filename)
        if not json_filename:
            json_filename = change_extension(excel_filename, 'json')
        try:
            # Не валидированный не сохраняем
            parser.parse()  # .save_not_validated(json_filename, overwrite)
            # Сохраняем валидированный json
            parser.validate_stock().save_validated(json_filename, overwrite=overwrite)
        # except ValidationError as e:

        # Это было сделано для валидации с Pydantic, от которого отказался по причине
        # сомнения, можно ли его использовать.

        #     error_summary = e.errors()[0]['msg']
        #     field_with_error = list(e.errors()[0]['loc'])[0]
        #     return exception(e, f'Validation error {error_summary}, field required {field_with_error}')
        except ValueError as e:
            return exception(e, f'Could not parse file: {excel_filename}')
        except FileNotFoundError as e:
            return exception(e, e.args[0])
        except FileExistsError as e:
            return exception(e, e.args[0])
        except TypeError as e:
            return exception(e, e.args[0])
        # Возвращаем структуру (п.1 ТЗ)
        # Структура - List[Stock]
        return parser.validated_stock

    @classmethod
    def group_stock_from_json(
        cls,
        input_json_file: str,
        output_json_file: str,
    ):
        # Здесь немножко запутанно, т.к. по условию п.2 нужно считать данные из файла,
        # а по условию п.5 получить из п.1, поэтому чтение json и запись результата используются только в этом методе.
        # Читаем из файла (п.2 ТЗ)
        group_stock = GroupStock().read_from_json(json_file=input_json_file)
        # группируем
        result = group_stock.group_stock()
        # пишем в файл
        group_stock.save_grouped_data(output_json_file)
        # возвращаем структуру
        return result

    @classmethod
    def generate_html(cls, input_json_file: str, output_html_file: str) -> str:
        """
        :param input_json_file: сгруппированный json
        :param output_html_file:
        :return: сгенерированная страница
        """
        # читаем json
        stocks = read_grouped_json(input_json_file)
        # генерируем html
        result = generate_stock_report(stocks)
        # сохраняем html, п.3
        save_file(result, output_html_file)
        # возвращаем html content
        return result

    @classmethod
    def generate_report(cls, input_json_file: str, output_text_file: str):
        # читаем json
        stocks = read_grouped_json(input_json_file)
        # генерируем текст
        result = generate_text_report(stocks)
        # сохраняем html, п.3
        save_file(result, output_text_file)

    @classmethod
    def sequencing(cls, excel_filename: str, output_html_file: str) -> str:
        """
        Генерация html с группировкой по товарам и наличию на складе на основе данных excel файла
        :param excel_filename:
        :param output_html_file: имя файла для сохранения html
        :return: html content
        """
        # последовательность
        # чтение с парсингом
        json_items = ExcelToJson(excel_filename).parse().validate_stock()
        # группировка
        group_stock = GroupStock(stocks=json_items.validated_stock).group_stock()
        # генерация html с сохранением
        html_content = generate_stock_report(group_stock)
        save_file(html_content, output_html_file)
        return html_content
