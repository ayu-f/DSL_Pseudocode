import json
from print_node import print_node
from unformated_nonterm_print_map import unformated_nonterm_print_map


file = open("test_tree.json", "r", encoding="UTF-8")
code = file.read()
res = json.loads(code)

print_node(res, 0, unformated_nonterm_print_map)