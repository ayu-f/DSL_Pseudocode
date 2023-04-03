from print_node import print_node

def print_new_line(root:dict, depth, nonterm_handler_map:dict, term_map:dict):
    print(depth * "\\tab ", end="")
    for node in root["content"]:
        print_node(node, depth, nonterm_handler_map, term_map)
    print("\\\\")

def print_code_block(root:dict, depth, nonterm_handler_map:dict, term_map:dict):
    depth += 1
    for node in root["content"]:
        print_node(node, depth, nonterm_handler_map, term_map)

def print_set(root:dict, depth, nonterm_handler_map:dict, term_map:dict):
    print('$\\{$ ', end='')
    for node in root["content"][2:-1]:
        print_node(node, depth, nonterm_handler_map, term_map)
    print('$\\}$ ', end='')


def tex_textbf(str: str):
    return f'\\textbf{{{str}}} '

nonterm_map = {
    'ЗАГОЛОВОК_АЛГОРИТМА': print_new_line,
    'КОМАНДА': print_new_line,
    'БЛОК_КОДА': print_code_block,
    'НЕУПОРЯДОЧЕННАЯ_ПОСЛЕДОВАТЕЛЬНОСТЬ': print_set,
}
term_map = {
    'algorithm': tex_textbf('algorithm'),
    'end algorithm': tex_textbf('end algorithm'),
    'return': tex_textbf('return'),
    'ИМЯ': '${value}$ ',
    '(': '$($ ',
    ')': '$)$ ',
    '...': '$...$ ',
    ':=': '$:=$ ',
    'ЧИСЛЕННАЯ_КОНСТАНТА': '${value}$ ',
    'then': tex_textbf('then'),
    'for': tex_textbf('for'),
    'if': tex_textbf('if'),
    'while': tex_textbf('while'),
    'do': tex_textbf('do'),
    'next for': tex_textbf('next for'),
    'repeat': tex_textbf('repeat'),
    'until': tex_textbf('until'),
    'yield': tex_textbf('yield'),
    'select': tex_textbf('select'),
    'goto': tex_textbf('goto'),
    'proc': tex_textbf('proc'),
    'func': tex_textbf('func'),
    'iter': tex_textbf('iter'),
}