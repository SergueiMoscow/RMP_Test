import json
import os


def save_uploaded_file(post_data: bytes, filename: str):

    file_start = post_data.find(b'\r\n\r\n')+4
    file_content = post_data[file_start:]

    with open(filename, 'wb') as f:
        f.write(file_content)
        message = 'File uploaded successfully'

    return len(file_content)


def get_form_value(fields, key):
    first_key = list(fields.keys())[0]
    json_data = fields[first_key][0]
    prefix = '"json_string"\r\n\r\n'
    suffix = '\r\n------'
    clean_json_data = json_data[json_data.find(prefix) + len(prefix):json_data.rfind(suffix)]
    clean_fields = json.loads(clean_json_data)

    if key in clean_fields:
        return clean_fields[key]
    return None
