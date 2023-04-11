from tree_processor import TreeProcessor, print_default

def print_code_block(root:dict, depth, processor: TreeProcessor):
    print_default(root, depth + 1, processor)

def print_comma_list(root:dict, depth, processor: TreeProcessor):
    for i, node in enumerate(root["content"]):
        if "key" in node.keys() and node["key"] == ',':
            processor.print_node(node, depth)
            if i != len(root["content"]) - 1:
                print(" ", end="")
        else:
            processor.print_node(node, depth)


key_map = {
    '\\n': '\n',
    
}
term_map = {
    
}
nonterm_map = {
    'БЛОК_КОДА': print_code_block,
    'СПИСОК_ПАРАМЕТРОВ': print_comma_list,
    'СПИСОК_ЗНАЧЕНИЙ': print_comma_list,
}