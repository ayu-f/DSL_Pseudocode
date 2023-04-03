from print_node import print_node, print_default, print_new_line


def print_code_block(root:dict, depth, nonterm_handler_map:dict):
    depth += 1
    for node in root["content"]:
        print_node(node, depth, nonterm_handler_map)


unformated_nonterm_print_map = {
    'ЗАГОЛОВОК_АЛГОРИТМА': print_new_line,
    'КОМАНДА': print_new_line,
    'БЛОК_КОДА': print_code_block,
}