import json
from tree_processor import TreeProcessor
import latex_print_style as latex_style
import unformated_print_style as unformated_style


file = open("test_tree.json", "r", encoding="UTF-8")
code = file.read()
res = json.loads(code)

processor = TreeProcessor(unformated_style.key_map, unformated_style.term_map, unformated_style.nonterm_map)
processor.print_node(res, 0)
print()
print()
processor = TreeProcessor(latex_style.key_map, latex_style.term_map, latex_style.nonterm_map)
processor.print_node(res, 0)