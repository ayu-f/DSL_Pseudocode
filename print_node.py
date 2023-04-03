def print_node(root:dict, depth, nonterm_handler_map:dict):

    if "term" in root.keys():
        if "value" in root.keys():
            print(root["value"], end=" ")
        else:
            print(root["term"], end=" ")
    else:
        nonterm_name = root["nonterm"]
        node_handler = print_default
        if nonterm_name in nonterm_handler_map.keys():
            node_handler = nonterm_handler_map[nonterm_name]
        node_handler(root, depth, nonterm_handler_map)
        

def print_default(root:dict, depth, nonterm_handler_map:dict):
    for node in root["content"]:
        print_node(node, depth, nonterm_handler_map)


def print_new_line(root:dict, depth, nonterm_handler_map:dict):
    print(depth * "\t", end="")
    for node in root["content"]:
        print_node(node, depth, nonterm_handler_map)
    print()
    