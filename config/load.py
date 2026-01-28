import re


# def load_stylesheet(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return f.read()


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
            # If it's safe to read, then split the key, values by a colon
            if root_block == 2:
                split = line.split(':')

                # Expect exactly two elements: key and value
                if len(split) == 2:
                    key, value = split
                    variables[key.strip()] = value.strip()
                else:
                    raise invalid_syntax

    # This pattern uses a logical OR to capture the words in the brackets
    # The dictionary keys are sorted in reversed since the regex engine only captures the first occurrence
    # If p.e. "primary" is set before "primary-dark" then it will only capture "primary"
    pattern = re.compile('@(' + '|'.join(sorted(variables, key=len, reverse=True)).strip('|') + ')')
    # Replace each match with the value of the variables dictionary (group 0 is a match that contains the @)
    stylesheet = pattern.sub(lambda match: variables[match.group(1)], stylesheet)

    return stylesheet
