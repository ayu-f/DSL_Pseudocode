import copy
import re
from macros import Macros
from typing import List

MACROS_DEFINE = "\\newcommand"
macroses: List[Macros] = list()


def print_macro(body: [], count_tab=0):
    for b in body:
        if isinstance(b, list):
            print_macro(b, count_tab + 1)
        elif isinstance(b, str):
            print('\t' * count_tab, b)


def parse(src_file_path: str):
    lines = []
    final_text = []
    with open(src_file_path, "r") as file:
        for line in file:
            lines.append(line)

    """ main loop """
    for line in lines:
        # remove comments
        line = remove_comment(line)
        line = re.sub("\n", "", line)
        # add macro defines
        if line.startswith(MACROS_DEFINE):
            macroses.append(parse_macros(line))
            continue

        # processing the calling macro
        if any(macros.name in line for macros in macroses):
            parsed_macro = handle_macros(line)
            line = parsed_macro.body_str
            # print_macro(parsed_macro.get_body())

        if line not in ['\n', '\r\n', '']:
            final_text.append(line)

    for t in final_text:
        print(t)


def remove_comment(text: str):
    pattern = r"%.*(\n|$)"
    text = re.sub(pattern, "", text)
    return text


def parse_macros(line) -> Macros:
    macros = Macros()
    start_len = 2
    name = re.search('\w+{(.+?)}', line).group(1)
    try:
        args = re.search('\[(.+?)]', line).group(1)
        start_len += 2
    except Exception:
        args = ""

    body = line[len(MACROS_DEFINE) + len(name) + len(args) + start_len:]

    macros.body_str = body
    macros.name = name
    try:
        macros.args_count = int(args)
    except Exception:
        macros.args_count = 0

    return macros


def handle_macros(line: str) -> Macros:
    new_macro = None
    for macro in macroses:
        if macro.name in line:
            new_macro = copy.deepcopy(macro)
            new_macro.body_str = emplace_macro_body(line, macro)

    # макросы в макросах
    new_line = new_macro.body_str
    for macro in macroses:
        if macro.name in new_line:
            new_macro.body_str = emplace_macro_body(new_line, macro)

    return new_macro


def emplace_macro_body(line: str, macro: Macros):
    start = line.index(macro.name)
    length = len(macro.name) + 3 * macro.args_count
    macro_str = line[start: start + length]
    arguments = re.findall('\{(\w+)}', macro_str)

    new_body_build = macro.body_str
    for i, arg in enumerate(arguments):
        find_arg = "#" + str(i + 1)
        new_body_build = new_body_build.replace(find_arg, arg)

    return line[0:start] + new_body_build[1:-1] + line[start + length:]
