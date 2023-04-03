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

nonterm_map = {
    'ЗАГОЛОВОК_АЛГОРИТМА': print_new_line,
    'КОМАНДА': print_new_line,
    'БЛОК_КОДА': print_code_block,
    'НЕУПОРЯДОЧЕННАЯ_ПОСЛЕДОВАТЕЛЬНОСТЬ': print_set,
}
term_map = {
    'algorithm': '\\textbf{{algorithm}} ',
    'end algorithm': '\\textbf{{end algorithm}} ',
    'return': '\\textbf{{return}} ',
    'ИМЯ': '${value}$ ',
    '(': '$($ ',
    ')': '$)$ ',
    '...': '$...$ ',
    ':=': '$:=$ ',
    'ЧИСЛЕННАЯ_КОНСТАНТА': '${value}$ ',
}