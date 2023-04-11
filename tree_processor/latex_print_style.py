from tree_processor import TreeProcessor, print_default

class PragmaCommand:
    
    def __init__(self, root:dict):
        self.name = root["content"][1]["content"][0]["value"]
        self.args = []
        for child in root["content"]:
            if "term" in child.keys() and child["term"] == "СТРОКА":
                self.args.append(child["value"][1:-1])
class UserDefined:
    def __init__(self, root:dict):
        self.name = root["content"][0]["key"][1:]
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

def print_user_defined(root:dict, depth, processor: TreeProcessor):
    user_defined = UserDefined(root)
    print(user_defined.args[0], end="")

def print_code_block(root:dict, depth, processor: TreeProcessor):
    print_default(root, depth + 1, processor)

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


def tex_textbf(term: str):
    return f'\\textbf{{{term}}}'

def name_format(value:str, processor: TreeProcessor):
    if not hasattr(processor, "names_formated"):
        processor.names_formated = {}
    return processor.names_formated.get(value, f"${value}$")

def number_format(value:str, processor: TreeProcessor):
    return f"${value}$"
        

nonterm_map = {
    'ПРАГМА': print_pragma,
    'ПОЛЬЗОВАТЕЛЬСКОЕ_ВЫРАЖЕНИЕ_ЗНАЧЕНИЕ': print_user_defined,
    'ПОЛЬЗОВАТЕЛЬСКАЯ_ПЕРЕМЕННАЯ': print_user_defined,
    'ПОЛЬЗОВАТЕЛЬСКИЙ_ОПЕРАТОР_УНАРНЫЙ': print_user_defined,
    'ПОЛЬЗОВАТЕЛЬСКИЙ_ОПЕРАТОР_ИНФИКСНЫЙ': print_user_defined,
    'ПОЛЬЗОВАТЕЛЬСКИЙ_ТИП': print_user_defined,
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
    '\\n': '\\\\\n',
    ';': ';',
    ':': ':',
    'end algorithm': tex_textbf('end algorithm'),
    '->': '->',
    'return': tex_textbf('return'),
    '(': '$($',
    ')': '$)$',
    '[': '$[$',
    ']': '$]$',
    '{': '\\{',
    '}': '\\}',
    ',': '$,$',
    '...': '$...$',
    '..': '$..$',
    '.': '$.$',
    ':=': '$:=$',
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
    'array': tex_textbf('array'),
    'of': tex_textbf('of'),
    'struct': tex_textbf('struct'),
    '\\uparrow': '$\\uparrow$',
    'natural': '$\\mathbb{N}$',
    'integer': '$\\mathbb{Z}$',
    'rational': '$\\mathbb{Q}$',
    'binary': '$0..1$',
    '<': '$<$',
    '>': '$>$',
    '<=': '$\\leq$',
    '>=': '$\\geq$',
    '==': '$=$',
    '!=': "$\\neq$",
    '+': '$+$',
    '-': '$-$',
    '/': '$/$',
    '*': '$*$',
    'div': tex_textbf('div'),
    'mod': tex_textbf('mod'),
    '&': "$\\&$",
    '|': "$\\vee$",
    '\\cup': "$\\cup$",
    '\\cap': "$\\cap$",
    '\\': "$\\backslash$",
    '\\in': "$\\in$",
    '\\notin': "$\\notin$",
    '\\subset': "$\\subset$",
    'pow':  tex_textbf('pow'),
}