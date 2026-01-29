import re
import os
import json


def open_json(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as jsonfile:
            jsondata = ''.join(line for line in jsonfile if not line.startswith('//'))
            data = json.loads(jsondata)
            return data
    return {}


def save_json(file_path, content):
    with open(file_path, 'w') as f:
        json.dump(content, f, indent=4)


def load_stylesheet(path: str):
    """
    Parses through the stylesheet to create similar variable abilities as in css files.\n
    Example :
        :root{
            primary: #1a1f1f
            primary-dark: #101010
            primary-light: #353535
            secondary: #2a82da
            secondary-dark: #163f68
        }
        QWidget{
            border: 0px;
            background-color: @primary;
            color: white;
        }
    """
    invalid_syntax = Exception('Invalid syntax')
    stylesheet = ''

    with open(path, 'r') as file:
        root_block = 0
        variables = dict[str, str]()

        for line in file:
            if ':root' in line:
                root_block = 1
            if '{' in line:
                if root_block == 1:
                    root_block = 2
                    continue
                else:
                    raise invalid_syntax
            if '}' in line:
                if root_block != 2:
                    raise invalid_syntax
                else:
                    stylesheet = file.read()
                    break

            if root_block == 2:
                split = line.split(':')

                if len(split) == 2:
                    key, value = split
                    variables[key.strip()] = value.strip()
                else:
                    raise invalid_syntax

    pattern = re.compile('@(' + '|'.join(sorted(variables, key=len, reverse=True)).strip('|') + ')')
    stylesheet = pattern.sub(lambda match: variables[match.group(1)], stylesheet)

    return stylesheet


def load_qss_with_fixed_urls(qss_path):
    base_dir = os.path.dirname(qss_path)

    qss = load_stylesheet(qss_path)

    def replace_url(match):
        relative_path = match.group(1).strip('\'"')
        absolute_path = os.path.abspath(os.path.join(base_dir, relative_path))

        qt_path = absolute_path.replace("\\", "/")
        return f"url({qt_path})"

    fixed_qss = re.sub(r'url\(([^)]+)\)', replace_url, qss)
    return fixed_qss
