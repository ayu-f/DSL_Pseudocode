import json
from print_node import print_node
import latex_print_style


file = open("test_tree.json", "r", encoding="UTF-8")
code = file.read()
res = json.loads(code)

print_node(res, 0, latex_print_style.nonterm_map, latex_print_style.term_map)