from print_node import print_node

def print_new_line(root:dict, depth, nonterm_handler_map:dict, term_map:dict):
    print(depth * "\\tab ", end="")
    for i, node in enumerate(root["content"]):
        print_node(node, depth, nonterm_handler_map, term_map)
        if i != len(root["content"]) - 1:
            print(" ", end="")

def print_code_block(root:dict, depth, nonterm_handler_map:dict, term_map:dict):
    depth += 1
    for i, node in enumerate(root["content"]):
        print_node(node, depth, nonterm_handler_map, term_map)
        if i != len(root["content"]) - 1:
            print("\\\\")

def print_set(root:dict, depth, nonterm_handler_map:dict, term_map:dict):
    print('$\\{$', end='')
    print_node(root["content"][2], depth, nonterm_handler_map, term_map)
    print('$\\}$', end='')
    
def print_alg(root:dict, depth, nonterm_handler_map:dict, term_map:dict):
    print_node(root["content"][0], depth, nonterm_handler_map, term_map)
    print(" ", end="")
    print_node(root["content"][1], depth, nonterm_handler_map, term_map)
    print("\\\\")
    print_node(root["content"][2], depth, nonterm_handler_map, term_map)
    print("\\\\")
    print_node(root["content"][3], depth, nonterm_handler_map, term_map)

def print_params_list(root:dict, depth, nonterm_handler_map:dict, term_map:dict):
    for i, node in enumerate(root["content"]):
        if "term" in node.keys() and node["term"] == ',':
            print_node(node, depth, nonterm_handler_map, term_map)
            if i != len(root["content"]) - 1:
                print(" ", end="")
        elif "term" in node.keys() and node["term"] == '...':
            print(" ", end="")
            print_node(node, depth, nonterm_handler_map, term_map)
            if i != len(root["content"]) - 1:
                print(" ", end="")
        else:
            print_node(node, depth, nonterm_handler_map, term_map)

def tex_textbf(term: str):
    return f'\\textbf{{{{{term}}}}}'

nonterm_map = {
    'ALG': print_alg,
    'КОМАНДА': print_new_line,
    'БЛОК_КОДА': print_code_block,
    'НЕУПОРЯДОЧЕННАЯ_ПОСЛЕДОВАТЕЛЬНОСТЬ': print_set,
    'СПИСОК_ПАРАМЕТРОВ': print_params_list,
}
term_map = {
    'algorithm': tex_textbf('algorithm'),
    'end algorithm': tex_textbf('end algorithm'),
    'return': tex_textbf('return'),
    'ИМЯ': '${value}$',
    '(': '$($',
    ')': '$)$',
    '...': '$...$',
    ':=': '$:=$',
    'ЧИСЛЕННАЯ_КОНСТАНТА': '${value}$',
    'for': tex_textbf('for'),
    'do': tex_textbf('do'),
    'end for': tex_textbf('end for'),
    'if': tex_textbf('if'),
    'then': tex_textbf('then'),
    'elseif': tex_textbf('elseif'),
    'else': tex_textbf('else'),
    'end if': tex_textbf('end if'),
    'while': tex_textbf('while'),
    'end while': tex_textbf('end while'),
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