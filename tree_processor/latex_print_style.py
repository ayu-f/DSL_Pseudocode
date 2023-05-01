import codecs
from .unformated_print_style import SourceTreeProcessor, is_key, is_term, is_nonterm

class LatexSourceTreeProcessor(SourceTreeProcessor):
    def __init__(self, file=None):
        super().__init__(file)
        self.key_map['{'] = '\\{'
        self.key_map['}'] = '\\}'
        self.key_map[','] = '$,$'
        self.key_map['\\uparrow'] = '$\\backslash$uparrow'
        self.key_map['/'] = '$\\slash$'
        self.key_map['&'] = "\\&"
        self.key_map['|'] = "\\|"
        self.key_map['\\cup'] = "$\\backslash$cup"
        self.key_map['\\cap'] = "$\\backslash$cap"
        self.key_map['\\'] = "$\\backslash"
        self.key_map['\\in'] = "$\\backslash$in"
        self.key_map['\\notin'] = "$\\backslash$notin"
        self.key_map['\\subset'] = "$\\backslash$subset"

        self.term_map['name'] = self.any_format
        self.term_map['number'] = self.any_format
        self.term_map['string'] = self.any_format


    def any_format(self, value:str):
        value = value.replace("\\", "\\backslash")
        value = value.replace("{", "\\{")
        value = value.replace("}", "\\}")
        value = value.replace("#", "\\#")
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
        print(depth * "\\tb ", end="", file=self.file)
        self.is_new_line = False

    def print_end_line(self):
        print("\\\\", file=self.file)
        self.is_new_line = True


class LatexTreeProcessor(SourceTreeProcessor):
    def __init__(self, file=None):
        super().__init__(file)
        self.key_map[';'] = '#value'
        self.key_map[':'] = '#value'
        self.key_map['end algorithm'] = '#value'
        self.key_map['->'] = '#value'
        self.key_map['return'] = '#value'
        self.key_map['('] = '$#value$'
        self.key_map[')'] = '$#value$'
        self.key_map['['] = '$#value$'
        self.key_map[']'] = '$#value$'
        self.key_map['{'] = '\\{'
        self.key_map['}'] = '\\}'
        self.key_map[','] = '$#value$'
        self.key_map['...'] = '$#value$'
        self.key_map['..'] = '$#value$'
        self.key_map['.'] = '$#value$'
        self.key_map[':='] = '$#value$'
        self.key_map['for'] = '#value'
        self.key_map['do'] = '#value'
        self.key_map['end for'] = '#value'
        self.key_map['if'] = '#value'
        self.key_map['then'] = '#value'
        self.key_map['elif'] = '#value'
        self.key_map['else'] = '#value'
        self.key_map['end if'] = '#value'
        self.key_map['while'] = '#value'
        self.key_map['end while'] = '#value'
        self.key_map['next for'] = '#value'
        self.key_map['repeat'] = '#value'
        self.key_map['until'] = '#value'
        self.key_map['yield'] = '#value'
        self.key_map['select'] = '#value'
        self.key_map['goto'] = '#value'
        self.key_map['proc'] = '#value'
        self.key_map['func'] = '#value'
        self.key_map['iter'] = '#value'
        self.key_map['array'] = '#value'
        self.key_map['of'] = '#value'
        self.key_map['struct'] = '#value'
        self.key_map['\\uparrow'] = '$#value$'
        self.key_map['natural'] = '$\\mathbb{N}$'
        self.key_map['integer'] = '$\\mathbb{Z}$'
        self.key_map['rational'] = '$\\mathbb{Q}$'
        self.key_map['binary'] = '$0..1$'
        self.key_map['<'] = '$#value$'
        self.key_map['>'] = '$#value$'
        self.key_map['<='] = '$\\leq$'
        self.key_map['>='] = '$\\geq$'
        self.key_map['=='] = '$=$'
        self.key_map['!='] = "$\\neq$"
        self.key_map['+'] = '$#value$'
        self.key_map['-'] = '$#value$'
        self.key_map['/'] = '$#value$'
        self.key_map['*'] = '$#value$'
        self.key_map['div'] = '#value'
        self.key_map['mod'] = '#value'
        self.key_map['&'] = "$\\&$"
        self.key_map['|'] = "$\\vee$"
        self.key_map['\\cup'] = '$#value$'
        self.key_map['\\cap'] = '$#value$'
        self.key_map['\\'] = "$\\backslash$"
        self.key_map['\\in'] = '$#value$'
        self.key_map['\\notin'] = '$#value$'
        self.key_map['\\subset'] = '$#value$'
        self.key_map['pow'] =  '#value'

        self.term_map['name'] = self.name_format
        self.term_map['float'] = self.number_format
        self.term_map['number'] = self.number_format
        
        self.nonterm_map['PRAGMA'] = self.print_pragma
        self.nonterm_map['CUSTOM_EXPRESSION_VALUE'] = self.print_user_defined
        self.nonterm_map['CUSTOM_VAR'] = self.print_user_defined
        self.nonterm_map['CUSTOM_UNARY_OPERATOR'] = self.print_user_defined
        self.nonterm_map['CUSTOM_INFIX_OPERATOR'] = self.print_user_defined
        self.nonterm_map['CUSTOM_TYPE'] = self.print_user_defined
        self.nonterm_map['SET'] = self.print_set
        self.nonterm_map['SEQUENCE'] = self.print_seq
        self.nonterm_map['VAR_NAME'] = self.print_var_name
        self.nonterm_map['FUNC_NAME'] = self.print_func_name
        self.nonterm_map['MARK_NAME'] = self.print_goto_mark_name

        self.is_enumerated = False
        self.names_formated = {}
        self.one_line = 0

        self.default_key_format = "$#value$"
        self.default_var_name_format = "$#value$"
        self.default_func_name_format = "$\\textrm{#value}$"
        self.default_goto_mark_name_format = "#value"
    
    def print_new_line(self, depth):
        if self.is_enumerated:
            print("\\item", end="", file=self.file)
        print(depth * "\\tb ", end="", file=self.file)
        self.is_new_line = False

    def print_end_line(self):
        if self.one_line > 0:
            return
        if self.is_enumerated or self.is_new_line:
            print(file=self.file)
        else:
            print("\\\\", file=self.file)
        self.is_new_line = True

    def begin_enumerate(self):
        print("\\begin{enumerate}", end="", file=self.file)
        self.is_enumerated = True

    def end_enumerate(self):
        print("\\end{enumerate}", end="", file=self.file)
        self.is_enumerated = False

    def print_tree(self, root:dict):
        self.print_node(root, 0)
        if self.is_enumerated:
            print("\n\\end{enumerate}", file=self.file)

    class PragmaCommand:
        
        def __init__(self, root:dict):
            self.name = root["content"][1]["content"][0]["value"]
            self.args = []
            for child in root["content"]:
                if is_term(child, "string"):
                    string = child["value"][1:-1]
                    self.args.append(string)
    class UserDefined:
        def __init__(self, root:dict):
            self.name = root["content"][0]["key"][1:]
            self.args = []
            for child in root["content"]:
                if is_term(child, "string"):
                    string = child["value"][1:-1]
                    self.args.append(string)

    def print_pragma(self, root:dict, depth) -> bool:
        pragma_command = self.PragmaCommand(root)
        if pragma_command.name == "comment":
            if self.is_new_line:
                self.print_new_line(depth)
            print("//", *pragma_command.args, end="", file=self.file)
            return True
        elif pragma_command.name == "set_name_formatted":
            prev_format = self.names_formated.get(pragma_command.args[0])
            if prev_format:
                self.names_formated[pragma_command.args[0]] = pragma_command.args[1].replace("#prev", prev_format)
            else:
                self.names_formated[pragma_command.args[0]] = pragma_command.args[1]
            return True
        elif pragma_command.name == "set_key_formatted":
            prev_format = self.key_map.get(pragma_command.args[0])
            if prev_format:
                self.key_map[pragma_command.args[0]] = pragma_command.args[1].replace("#prev", prev_format)
            else:
                self.key_map[pragma_command.args[0]] = pragma_command.args[1]
            return True
        elif pragma_command.name == "set_default_var_name_format":
            prev_format = self.default_var_name_format
            self.default_var_name_format = pragma_command.args[0].replace("#prev", prev_format)
            return True
        elif pragma_command.name == "set_default_func_name_format":
            prev_format = self.default_func_name_format
            self.default_func_name_format = pragma_command.args[0].replace("#prev", prev_format)
            return True
        elif pragma_command.name == "set_default_goto_mark_name_format":
            prev_format = self.default_goto_mark_name_format
            self.default_goto_mark_name_format = pragma_command.args[0].replace("#prev", prev_format)
            return True
        elif pragma_command.name == "begin_enumerate":
            self.begin_enumerate()
            return True
        elif pragma_command.name == "end_enumerate":
            self.end_enumerate()
            return True
        elif pragma_command.name == "begin_oneline":
            self.one_line += 1
            return True
        elif pragma_command.name == "end_oneline":
            self.one_line -= 1
            return True
        elif pragma_command.name == "tex":
            print(*pragma_command.args, sep="\n", end="", file=self.file)
        return False

    def print_user_defined(self, root:dict, depth):
        if self.is_new_line:
            self.print_new_line(depth)
        user_defined = self.UserDefined(root)
        print(user_defined.args[0], end="", file=self.file)
        
    def print_var_name(self, root:dict, depth):
        if self.is_new_line:
            self.print_new_line(depth)
        print(self.name_format(root["content"][0]["value"], self.default_var_name_format), end="", file=self.file)
        
    def print_func_name(self, root:dict, depth):
        if self.is_new_line:
            self.print_new_line(depth)
        print(self.name_format(root["content"][0]["value"], self.default_func_name_format), end="", file=self.file)
        
    def print_goto_mark_name(self, root:dict, depth):
        if self.is_new_line:
            self.print_new_line(depth)
        print(self.name_format(root["content"][0]["value"], self.default_goto_mark_name_format), end="", file=self.file)

    def print_set(self, root:dict, depth):
        if self.is_new_line:
            self.print_new_line(depth)
        print('$\\{$', end='', file=self.file)
        self.print_node(root["content"][2], depth)
        print('$\\}$', end='', file=self.file)
    
    def print_seq(self, root:dict, depth):
        if self.is_new_line:
            self.print_new_line(depth)
        print('$($', end='', file=self.file)
        self.print_node(root["content"][2], depth)
        print('$)$', end='', file=self.file)

    def name_format(self, value:str, default=None):
        if not default:
            default = self.default_key_format
        return self.names_formated.get(value, default).replace("#value", value)

    def number_format(self, value:str):
        return f"${value}$"
    