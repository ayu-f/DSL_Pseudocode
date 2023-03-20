import pyparsing
import re
from macros import Macros
from pyparsing import nestedExpr
from typing import List

MACROS_DEFINE = "\\newcommand"
macroses:List[Macros] = list()


def parse(src_file_path: str):
    lines = []
    with open(src_file_path, "r") as file:
        for line in file:
            lines.append(line)

    for line in lines:
        line = remove_comment(line)
        if line.startswith(MACROS_DEFINE):
            macroses.append(parse_macros(line))
        elif line.startswith(tuple([macros.name for macros in macroses])):
            handle_macros(line)
        else:
            print(line)


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
        print(f"No args in line:{line}")

    body = line[len(MACROS_DEFINE) + len(name) + len(args) + start_len:]
    blocks = nestedExpr('{', '}').parseString(body).asList()
    for b in blocks:
        print(b)

    macros.name = name
    try:
        macros.args_count = int(args)
    except Exception:
        macros.args_count = 0

    macros.body = blocks
    return macros


def handle_macros(line: str):
    for macro in macroses:
        if line.startswith(macro.name):
            argument = re.search('\w+{(.+?)}', line).group(1)
            for i in range(macro.args_count):
                find_arg = "#" + str(i + 1)
                # TODO заменить в структуре макроса  на аргумент argument
                #line.replace(find_arg, argument)
                #print(line)

