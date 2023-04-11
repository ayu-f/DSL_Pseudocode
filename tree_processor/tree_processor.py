class TreeProcessor():
    def __init__(self, key_map:dict, term_map:dict, nonterm_map:dict):
        self.key_map = key_map
        self.term_map = term_map
        self.nonterm_map = nonterm_map
        self.curr_line_number = 0
    
    def print_new_line(self, depth):
        self.curr_line_number += 1
        print(f"{self.curr_line_number}", end="")
        print(depth * "\\tb ", end="")


    def print_node(self, root:dict, depth):

        if "key" in root.keys():
            key_name = root["key"]
            str = key_name
            if key_name in self.key_map.keys():
                str = self.key_map[key_name]
            print(str, end="")

        elif "term" in root.keys():
            term_name = root["term"]
            term_value = root["value"]
            str = f"{term_value}"
            if term_name in self.term_map.keys():
                str = self.term_map[term_name](term_value, self)
            print(str, end="")

        elif "nonterm" in root.keys():
            nonterm_name = root["nonterm"]
            node_handler = print_default
            if nonterm_name in self.nonterm_map.keys():
                node_handler = self.nonterm_map[nonterm_name]
            node_handler(root, depth, self)
            

def print_default(root:dict, depth, processor: TreeProcessor):
    for i, node in enumerate(root["content"]):
        processor.print_node(node, depth)
        if "key" in node.keys() and node["key"] == "\\n":
            if "nonterm" in root["content"][i+1] and root["content"][i+1]["nonterm"] == "БЛОК_КОДА":
                processor.print_new_line(depth+1)
            else:
                processor.print_new_line(depth)
        if i != len(root["content"]) - 1:
            print(" ", end="")
        