def is_key(node, name=None):
    return ('key' in node.keys() and (name is None or node['key'] == name))

def is_term(node, name=None):
    return ('term' in node.keys() and (name is None or node['term'] == name))

def is_nonterm(node, name=None):
    return ('nonterm' in node.keys() and (name is None or node['nonterm'] == name))

class SourceTreeProcessor():
    def __init__(self, file=None):
        self.file = file
        self.key_map = {}
        self.term_map = {}
        self.nonterm_map = {}
        self.nonterm_map['S'] = self.nonterm_print_S
        self.is_new_line = True
        self.default_separator = " "
    
    def print_new_line(self, depth):
        print(depth * "    ", end="", file=self.file)
        self.is_new_line = False

    def print_end_line(self):
        print(file=self.file)
        self.is_new_line = True

    def get_separator(self, root:dict, left:dict, right:dict):
        if is_key(right, ","):
            return ""
        if is_key(right, "("):
            return ""
        if is_key(left, "("):
            return ""
        if is_key(right, ")"):
            return ""
        if is_key(left, ")"):
            return ""
        if is_key(left, "@@"):
            return ""
        if is_key(right, "{"):
            return ""
        if is_key(left, "{"):
            return " "
        if is_key(right, "}"):
            return " "
        if is_key(left, "}"):
            return ""
        if is_key(right, ";"):
            return ""
        if is_key(right, "["):
            return ""
        if is_key(left, "["):
            return ""
        if is_key(right, "]"):
            return ""
        if is_key(left, "]"):
            return ""
        if is_key(right, "."):
            return ""
        if is_key(left, "."):
            return ""
        if is_key(right, ".."):
            return ""
        if is_key(left, ".."):
            return ""
        
        return self.default_separator
        
    def print_tree(self, root:dict):
        self.print_node(root, 0)
        print(file=self.file)

    def print_node(self, root:dict, depth):
        if is_nonterm(root):
            nonterm_name = root["nonterm"]
            node_handler = self.print_default
            if nonterm_name in self.nonterm_map.keys():
                node_handler = self.nonterm_map[nonterm_name]
            node_handler(root, depth)
            return
        
        if is_key(root):
            key_name = root["key"]
            if is_key(root, "nl"):
                self.print_end_line()
                return
            if self.is_new_line:
                self.print_new_line(depth)
            str = key_name
            if key_name in self.key_map.keys():
                str = self.key_map[key_name].replace("#value", key_name)
            print(str, end="", file=self.file)

        elif is_term(root):
            if self.is_new_line:
                self.print_new_line(depth)
            term_name = root["term"]
            term_value = root["value"]
            str = f"{term_value}"
            if term_name in self.term_map.keys():
                str = self.term_map[term_name](term_value)
            print(str, end="", file=self.file)

    def print_default(self, root:dict, depth):
        if is_nonterm(root, "CODE_BLOCK"):
            depth += 1
        for i, node in enumerate(root["content"]):
            self.print_node(node, depth)
            if i != len(root["content"]) - 1 and not self.is_new_line:
                print(self.get_separator(root, root["content"][i], root["content"][i+1]), end="", file=self.file)
    
    def nonterm_print_S(self, root:dict, depth):
        for i, node in enumerate(root["content"]):
            if is_nonterm(root, "CODE_BLOCK"):
                self.print_node(node, depth - 1)
            else:
                self.print_node(node, depth)
            if i != len(root["content"]) - 1 and not self.is_new_line:
                print(self.get_separator(root, root["content"][i], root["content"][i+1]), end="", file=self.file)

