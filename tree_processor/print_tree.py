import json
from latex_print_style import LatexTreeProcessor, LatexSourceTreeProcessor
from unformated_print_style import SourceTreeProcessor

file = open("test_tree.json", "r", encoding="UTF-8")
code = file.read()
res = json.loads(code)

processor = SourceTreeProcessor()
processor.print_tree(res)
print()
print()
processor = LatexSourceTreeProcessor()
processor.print_tree(res)
print()
print()
processor = LatexTreeProcessor()
processor.print_tree(res)