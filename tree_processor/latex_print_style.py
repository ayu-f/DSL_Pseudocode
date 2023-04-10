from tree_processor import TreeProcessor

class PragmaCommand:
    
    def __init__(self, root:dict):
        self.name = root["content"][1]["content"][0]["value"]
        self.args = []
        for child in root["content"]:
            if "term" in child.keys() and child["term"] == "СТРОКА":
                self.args.append(child["value"][1:-1])

def print_pragma(root:dict, depth, processor: TreeProcessor):
    pragma_command = PragmaCommand(root)
    if pragma_command.name == "comment":
        print("//", *pragma_command.args, end="")
    elif pragma_command.name == "set_name_formatted":
        if not hasattr(processor, "names_formated"):
            processor.names_formated = {}
        processor.names_formated[pragma_command.args[0]] = pragma_command.args[1]

def print_lines(root:dict, depth, processor: TreeProcessor):
    for i, node in enumerate(root["content"]):
        processor.print_node(node, depth)
        if i != len(root["content"]) - 1:
            print("\\\\")
            print(depth * "\\tb ", end="")

def print_code_block(root:dict, depth, processor: TreeProcessor):
    print_lines(root, depth, processor)

def print_set(root:dict, depth, processor: TreeProcessor):
    print('$\\{$', end='')
    processor.print_node(root["content"][2], depth)
    print('$\\}$', end='')

def print_comma_list(root:dict, depth, processor: TreeProcessor):
    for i, node in enumerate(root["content"]):
        if "key" in node.keys() and node["key"] == ',':
            processor.print_node(node, depth)
            if i != len(root["content"]) - 1:
                print(" ", end="")
        else:
            processor.print_node(node, depth)

def print_alg(root:dict, depth, processor: TreeProcessor):
    processor.print_node(root["content"][0], depth)
    print("\\\\")
    print((depth + 1) * "\\tb ", end="")
    processor.print_node(root["content"][1], depth + 1)
    print("\\\\")
    print((depth) * "\\tb ", end="")
    processor.print_node(root["content"][2], depth)

def print_if(root:dict, depth, processor: TreeProcessor):
    i = 0
    while root["content"][i]["key"] != "end if":
        processor.print_node(root["content"][i], depth)
        print(" ", end="")
        i += 1
        if root["content"][i-1]["key"] != "else":
            processor.print_node(root["content"][i], depth)
            print(" ", end="")
            i += 1
            processor.print_node(root["content"][i], depth)
            print(" ", end="")
            i += 1
        while "nonterm" in root["content"][i].keys() and root["content"][i]["nonterm"] == "ПРАГМА":
            processor.print_node(root["content"][i], depth)
            print(" ", end="")
            i += 1
        print("\\\\")
        print((depth + 1) * "\\tb ", end="")
        processor.print_node(root["content"][i], depth + 1)
        print("\\\\")
        i += 1
        print((depth) * "\\tb ", end="")
    processor.print_node(root["content"][i], depth)


def tex_textbf(term: str):
    return f'\\textbf{{{term}}}'

def name_format(value:str, processor: TreeProcessor):
    if not hasattr(processor, "names_formated"):
        processor.names_formated = {}
    return processor.names_formated.get(value, f"${value}$")

def number_format(value:str, processor: TreeProcessor):
    return f"${value}$"
        

nonterm_map = {
    'S': print_lines,
    'ALG': print_alg,
    'ВЕТВЛЕНИЕ': print_if,
    'WHILE': print_lines,
    'ПРАГМА': print_pragma,
    'БЛОК_КОДА': print_code_block,
    'НЕУПОРЯДОЧЕННАЯ_ПОСЛЕДОВАТЕЛЬНОСТЬ': print_set,
    'СПИСОК_ПАРАМЕТРОВ': print_comma_list,
    'СПИСОК_ЗНАЧЕНИЙ': print_comma_list,
}
term_map = {
    'ИМЯ': name_format,
    'ЧИСЛЕННАЯ_КОНСТАНТА': number_format,
}
key_map = {
    'end algorithm': tex_textbf('end algorithm'),
    'return': tex_textbf('return'),
    '(': '$($',
    ')': '$)$',
    '...': '$...$',
    ':=': '$:=$',
    'integer': '$\mathbb{N}$',
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
    '!=': "$\\neq$",
    '&': "$\\&$",
}