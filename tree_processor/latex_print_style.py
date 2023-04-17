from .unformated_print_style import SourceTreeProcessor
def tex_textbf(term: str):
    return f'\\textbf{{{term}}}'

class LatexSourceTreeProcessor(SourceTreeProcessor):
    def __init__(self):
        super().__init__()
        self.key_map = self.key_map = {
            '{': '\\{',
            '}': '\\}',
            ',': '$,$',
            '\\uparrow': '$\\backslash$uparrow',
            '/': '$\\slash$',
            '&': "\\&",
            '|': "\\|",
            '\\cup': "$\\backslash$cup",
            '\\cap': "$\\backslash$cap",
            '\\': "$\\backslash",
            '\\in': "$\\backslash$in",
            '\\notin': "$\\backslash$notin",
            '\\subset': "$\\backslash$subset",
        }
        self.term_map = {
            'name': self.any_format,
            'number': self.any_format,
            'string': self.any_format,
        }


    def any_format(self, value:str):
        value = value.replace("\\", "\\backslash")
        value = value.replace("{", "\\{")
        value = value.replace("}", "\\}")
        value = value.replace("_", "\\_")
        value = value.replace("/", "\\slash")
        value = value.replace("&", "\\&")
        value = value.replace("|", "\\|")
        value = value.replace("$", "\\$")
        value = value.replace(",", "$,$")
        value = value.replace("\\backslash", "$\\backslash$")
        value = value.replace("\\slash", "$\\slash$")
        return value
    
    def print_new_line(self, depth):
        print(depth * "\\tb ", end="")
        self.is_new_line = False

    def print_end_line(self):
        print("\\\\")
        self.is_new_line = True


class LatexTreeProcessor(SourceTreeProcessor):
    def __init__(self):
        super().__init__()
        self.key_map = {
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
        self.term_map = {
            'name': self.name_format,
            'number': self.number_format,
        }
        self.nonterm_map = {
            'PRAGMA': self.print_pragma,
            'ПОЛЬЗОВАТЕЛЬСКОЕ_ВЫРАЖЕНИЕ_ЗНАЧЕНИЕ': self.print_user_defined,
            'ПОЛЬЗОВАТЕЛЬСКАЯ_ПЕРЕМЕННАЯ': self.print_user_defined,
            'ПОЛЬЗОВАТЕЛЬСКИЙ_ОПЕРАТОР_УНАРНЫЙ': self.print_user_defined,
            'ПОЛЬЗОВАТЕЛЬСКИЙ_ОПЕРАТОР_ИНФИКСНЫЙ': self.print_user_defined,
            'ПОЛЬЗОВАТЕЛЬСКИЙ_ТИП': self.print_user_defined,
            'НЕУПОРЯДОЧЕННАЯ_ПОСЛЕДОВАТЕЛЬНОСТЬ': self.print_set,
        }
        self.is_enumerated = False
        self.names_formated = {}
    
    def print_new_line(self, depth):
        if self.is_enumerated:
            print("\\item", end="")
        print(depth * "\\tb ", end="")
        self.is_new_line = False

    def print_end_line(self):
        if self.is_enumerated or self.is_new_line:
            print()
        else:
            print("\\\\")
        self.is_new_line = True

    def begin_enumerate(self):
        print("\\begin{enumerate}", end="")
        self.is_enumerated = True

    def end_enumerate(self):
        print("\\end{enumerate}", end="")
        self.is_enumerated = False

    def print_tree(self, root:dict):
        self.print_node(root, 0)
        if self.is_enumerated:
            print("\n\\end{enumerate}")

    class PragmaCommand:
        
        def __init__(self, root:dict):
            self.name = root["content"][1]["content"][0]["value"]
            self.args = []
            for child in root["content"]:
                if "term" in child.keys() and child["term"] == "string":
                    self.args.append(child["value"][1:-1])
    class UserDefined:
        def __init__(self, root:dict):
            self.name = root["content"][0]["key"][1:]
            self.args = []
            for child in root["content"]:
                if "term" in child.keys() and child["term"] == "string":
                    self.args.append(child["value"][1:-1])

    def print_pragma(self, root:dict, depth) -> bool:
        pragma_command = self.PragmaCommand(root)
        if pragma_command.name == "comment":
            if self.is_new_line:
                self.print_new_line(depth)
            print("//", *pragma_command.args, end="")
            return True
        elif pragma_command.name == "set_name_formatted":
            self.names_formated[pragma_command.args[0]] = pragma_command.args[1]
            return True
        elif pragma_command.name == "begin_enumerate":
            self.begin_enumerate()
            return True
        elif pragma_command.name == "end_enumerate":
            self.end_enumerate()
            return True
        #elif pragma_command.name == "tex":
        return False

    def print_user_defined(self, root:dict, depth):
        if self.is_new_line:
            self.print_new_line(depth)
        user_defined = self.UserDefined(root)
        print(user_defined.args[0], end="")

    def print_set(self, root:dict, depth):
        if self.is_new_line:
            self.print_new_line(depth)
        print('$\\{$', end='')
        self.print_node(root["content"][2], depth)
        print('$\\}$', end='')

    def name_format(self, value:str):
        return self.names_formated.get(value, f"${value}$")

    def number_format(self, value:str):
        return f"${value}$"
    