class SourceTreeProcessor():
    def __init__(self):
        self.key_map = {
        }
        self.term_map = {
        }
        self.nonterm_map = {
        }
        self.is_new_line = True
        self.default_separator = " "
    
    def print_new_line(self, depth):
        print(depth * "    ", end="")
        self.is_new_line = False

    def print_end_line(self):
        print()
        self.is_new_line = True

    def get_separator(self, root:dict, left:dict, right:dict):
        if "key" in right.keys() and right["key"] == ",":
            return ""
        if "key" in right.keys() and right["key"] == "(":
            return ""
        if "key" in left.keys() and left["key"] == "(":
            return ""
        if "key" in right.keys() and right["key"] == ")":
            return ""
        if "key" in left.keys() and left["key"] == ")":
            return ""
        if "key" in left.keys() and left["key"] == "@@":
            return ""
        if "key" in right.keys() and right["key"] == "{":
            return ""
        if "key" in left.keys() and left["key"] == "{":
            return ""
        if "key" in right.keys() and right["key"] == "}":
            return ""
        if "key" in left.keys() and left["key"] == "}":
            return ""
        if "key" in right.keys() and right["key"] == ";":
            return ""
        return self.default_separator
        
    def print_tree(self, root:dict):
        self.print_node(root, 0)
        print()

    def print_node(self, root:dict, depth):
        if "nonterm" in root.keys():
            nonterm_name = root["nonterm"]
            node_handler = self.print_default
            if nonterm_name in self.nonterm_map.keys():
                node_handler = self.nonterm_map[nonterm_name]
            node_handler(root, depth)
            return
        
        if "key" in root.keys():
            key_name = root["key"]
            if key_name == "\\n":
                self.print_end_line()
                return
            if self.is_new_line:
                self.print_new_line(depth)
            str = key_name
            if key_name in self.key_map.keys():
                str = self.key_map[key_name]
            print(str, end="")

        elif "term" in root.keys():
            if self.is_new_line:
                self.print_new_line(depth)
            term_name = root["term"]
            term_value = root["value"]
            str = f"{term_value}"
            if term_name in self.term_map.keys():
                str = self.term_map[term_name](term_value)
            print(str, end="")

    def print_default(self, root:dict, depth):
        if root["nonterm"] == "CODE_BLOCK":
            depth += 1
        for i, node in enumerate(root["content"]):
            self.print_node(node, depth)
            if i != len(root["content"]) - 1 and not self.is_new_line:
                print(self.get_separator(root, root["content"][i], root["content"][i+1]), end="")

