keys = [
    ';',
    '@@',
    '@set',
    '@value',
    '@unary',
    '@infix',
    '@type',
    '@set',
    '@seq',
    'factorial',
    'floor',
    'ceil',
    'abs',
    'end algorithm',
    'end while',
    'end if',
    'end for',
    '->',
    '-',
    'return',
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
    ',',
    '...',
    '..',
    '.',
    ':=',
    ':',
    'for',
    'do',
    'if',
    'then',
    'elseif',
    'else',
    'while',
    'next for',
    'repeat',
    'until',
    'yield',
    'select',
    'goto',
    'proc',
    'func',
    'iter',
    'array',
    'of',
    'struct',
    '\\uparrow',
    'natural',
    'integer',
    'rational',
    'binary',
    '==',
    '!=',
    '+',
    '/',
    '*',
    'div',
    'mod',
    '&',
    '|',
    '\\cup',
    '\\cap',
    '\\in',
    '\\notin',
    '\\subset',
    '\\',
    'pow',
    '<=',
    '>=',
    '<',
    '>',
]

def read_name(src:str):
    if src[0].isdigit():
        return None
    pos = 0
    while pos < len(src) and (src[pos].isalpha() or src[pos] == '_' or src[pos].isdigit()):
        pos += 1
    if pos > 0:
        return src[:pos]
    return None

def read_str(src:str):
    if src[0] != '\"':
        return None
    pos = 1
    while pos < len(src):
        if src[pos] == '\"':
            return src[:pos+1]
        if src[pos] == '\n':
            return None
        pos += 1
    return None

def read_number(src:str):
    pos = 0
    while pos < len(src) and src[pos].isdigit():
        pos += 1
    if pos > 0:
        return src[:pos]
    return None

def is_key(self, name=None):
    return ('key' in self.keys() and (name is None or self['key'] == name))

def is_term(self, name=None):
    return ('term' in self.keys() and (name is None or self['term'] == name))

def get_lexem_list(src:str):
    lexem_list = []
    pos = 0
    while pos < len(src):
        if src[pos] == ' ' or src[pos] == '\t':
            pos += 1
            continue
        if src[pos] == '\n':
            lexem_list.append({'key': '\\n'})
            pos += 1
            continue
        key_found = None
        for key in keys:
            if src[pos : pos + len(key)] == key:
                if key[-1].isalpha() and pos + len(key) < len(src) and (src[pos + len(key)].isalpha() or src[pos + len(key)].isdigit() or src[pos + len(key)] == '_'):
                    continue
                key_found = key
                break
        if not key_found is None:
            lexem_list.append({'key': key_found})
            pos += len(key_found)
            continue
        term = read_name(src[pos:])
        if not term is None:
            lexem_list.append({'term': 'ИМЯ', 'value': term})
            pos += len(term)
            continue
        term = read_str(src[pos:])
        if not term is None:
            lexem_list.append({'term': 'СТРОКА', 'value': term})
            pos += len(term)
            continue
        term = read_number(src[pos:])
        if not term is None:
            lexem_list.append({'term': 'ЧИСЛЕННАЯ_КОНСТАНТА', 'value': term})
            pos += len(term)
            continue
        return None
    return lexem_list

class CantGet(Exception):
    pass


class nonterm_CODE_BLOCK():
    def __init__(self, lexems:list[dict]):
        pos = 0
        self.nonterm = 'БЛОК_КОДА'
        self.content = []
        COMMAND_OR_PRAGMA = self.get_command_or_pragma(lexems[pos:])
        self.content.append(COMMAND_OR_PRAGMA)
        pos += COMMAND_OR_PRAGMA.lex_len
        while pos < len(lexems) and (is_key(lexems[pos], ';') or is_key(lexems[pos], '\\n')):
            try:
                COMMAND_OR_PRAGMA = self.get_command_or_pragma(lexems[pos+1:])
                self.content.append(lexems[pos])
                self.content.append(COMMAND_OR_PRAGMA)
                pos += 1 + COMMAND_OR_PRAGMA.lex_len
            except CantGet:
                break
        self.lex_len = pos

    
    def get_command_or_pragma(self, lexems:list[dict]):
        try:
            return nonterm_COMMAND(lexems)
        except CantGet:
            pass
        try:
            return nonterm_PRAGMA(lexems)
        except CantGet:
            raise CantGet()


class nonterm_PRAGMA():
    def __init__(self, lexems:list[dict]):
        pos = 0
        self.content = []
        if not is_key(lexems[pos], '@@'):
            raise CantGet
        self.content.append(lexems[pos])
        pos += 1
        PRAGMA_NAME = nonterm_PRAGMA_NAME(lexems[pos:])
        self.content.append(PRAGMA_NAME)
        pos += PRAGMA_NAME.lex_len

    def read_optional(self, lexems:list[dict]):
        pos = 0
        if pos < len(lexems) and is_key(lexems[pos], '{'):
            optional = [lexems[pos]]
            pos += 1
            if pos >= len(lexems) or not is_term(lexems[pos], 'СТРОКА'):

        


class nonterm_PRAGMA_NAME():
    def __init__(self, lexems:list[dict]):
        if not is_term(lexems[0], 'ИМЯ'):
            raise CantGet
        self.content = [lexems[0]]
        self.lex_len = 1


class nonterm_ALG():
    def __init__(self, lexems:list[dict]):
        return


class nonterm_ALG_HEAD():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_ALG_TYPE():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_FUNC_NAME():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_ALG_IN():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_ALG_OUT():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_COMMAND():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_CONTROL_COMMAND():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_JUMP_COMMAND():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_ASSIGN_COMMAND():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_VAR_DECLARATE():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_IF():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_CICLE():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_FOR():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_NEXT_FOR():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_CICLE_VAR():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_WHILE():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_UNTIL():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_RETURN():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_RETURN():
    def __init__(self, lexems:list[dict]):
        pass


class nonterm_S():
    def __init__(self, lexems:list[dict]):
        self.nonterm = 'S'
        self.content = []
        pos = 0
        while pos < len(lexems):
            try:
                ALG = nonterm_ALG(lexems[pos:])
                if pos + ALG.lex_len >= len(lexems):
                    self.content.append(ALG)
                    pos += ALG.lex_len
                    break
                if is_key(lexems[pos + ALG.lex_len], '\\n'):
                    self.content.append(ALG)
                    self.content.append(lexems[pos + ALG.lex_len])
                    pos += ALG.lex_len + 1
                    continue
                else:
                    raise CantGet()
            except CantGet:
                pass
            try:
                CODE_BLOCK = nonterm_CODE_BLOCK(lexems[pos:])
                if pos + CODE_BLOCK.lex_len >= len(lexems):
                    self.content.append(CODE_BLOCK)
                    pos += CODE_BLOCK.lex_len
                    break
                if is_key(lexems[pos + CODE_BLOCK.lex_len], '\\n'):
                    self.content.append(CODE_BLOCK)
                    self.content.append(lexems[pos + CODE_BLOCK.lex_len])
                    pos += CODE_BLOCK.lex_len + 1
                    continue
                else:
                    raise CantGet()
            except CantGet:
                raise CantGet()
            
    def __init__(self, lexems:list[dict]):
        pos = 0
        self.nonterm = 'S'
        self.content = []
        ALG_OR_CODE_BLOCK = self.get_alg_or_code_block(lexems[pos:])
        self.content.append(ALG_OR_CODE_BLOCK)
        pos += ALG_OR_CODE_BLOCK.lex_len
        while pos < len(lexems) and is_key(lexems[pos], '\\n'):
            try:
                ALG_OR_CODE_BLOCK = self.get_alg_or_code_block(lexems[pos+1:])
                self.content.append(lexems[pos])
                self.content.append(ALG_OR_CODE_BLOCK)
                pos += 1 + ALG_OR_CODE_BLOCK.lex_len
            except CantGet:
                break
        self.lex_len = pos

    
    def get_alg_or_code_block(self, lexems:list[dict]):
        try:
            return nonterm_ALG(lexems)
        except CantGet:
            pass
        try:
            return nonterm_CODE_BLOCK(lexems)
        except CantGet:
            raise CantGet()


a = '''func GetSet (n : natural) -> @@comment{"Множество $B$ целых чисел от $2$ до $n$"}
    B := @set(2, 3, 4, 5, ..., n)
    return B
end algorithm
    @@set_name_formatted{"gcd", "\\textrm{gcd}"}
    @@begin_enumerate
func gcd (a : natural, b : natural) -> @@comment{"НОД чисел $a$ и $b$"}
    while a != 0 & b != 0 do
        if a > b then a := a mod b else b := b mod a end if
    end while
    return a + b
end algorithm
    @@end_enumerate
func EratosphenGrid (n : natural) -> @@comment{"Множество $B$ простых чисел, не превосходящих $n$"}
    B := @set(2, 3, 4, 5, ..., n)
    while B != @value{"$\\emptyset$"} do
        x := min(B)
    end while
    return B
end algorithm'''

print(get_lexem_list(a))