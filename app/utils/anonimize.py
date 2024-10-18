def delete_comments(code: str):
    flag = False
    processed_code = ""

    for line in code.split('\n'):
        if flag and line.strip().startswith('"""'):
            flag = False
        elif line.strip().endswith('"""'):
            flag = True
        elif not(line.strip().startswith('#') or flag):
            processed_code += line+'\n'
    return processed_code[:-1]

import re

def anonymize_code(code):
    keywords = {
        "def", "return", "class", "if", "else", "elif", "for", "while", "import",
        "from", "as", "with", "print", "input", "and", "or", "not", "in", "is",
        "True", "False", "None", "break", "continue", "pass", "lambda"
    }

    var_pattern = r'\b([a-zA-Z_][a-zA-Z_0-9]*)\b'
    func_pattern = r'\bdef\s+([a-zA-Z_][a-zA-Z_0-9]*)\b'
    class_pattern = r'\bclass\s+([a-zA-Z_][a-zA-Z_0-9]*)\b'

    var_counter = 1
    func_counter = 1
    class_counter = 1

    var_replacements = {}
    func_replacements = {}
    class_replacements = {}

    def replace_class(match):
        nonlocal class_counter
        class_name = match.group(1)
        if class_name not in class_replacements:
            class_replacements[class_name] = f'class{class_counter}'
            class_counter += 1
        return f'class {class_replacements[class_name]}'

    def replace_func(match):
        nonlocal func_counter
        func_name = match.group(1)
        if func_name not in func_replacements:
            func_replacements[func_name] = f'func{func_counter}'
            func_counter += 1
        return f'def {func_replacements[func_name]}'

    def replace_var(match):
        nonlocal var_counter
        var_name = match.group(1)
        if var_name not in keywords and var_name not in var_replacements:
            var_replacements[var_name] = f'var{var_counter}'
            var_counter += 1
        return var_replacements.get(var_name, var_name)

    anonymized_code = re.sub(class_pattern, replace_class, code)
    anonymized_code = re.sub(func_pattern, replace_func, anonymized_code)
    anonymized_code = re.sub(var_pattern, replace_var, anonymized_code)

    return anonymized_code
