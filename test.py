import sys
sys.path.append("./dsl_generator_pseudocode")
sys.path.append("./tree_processor")

import json
from tree_processor.latex_print_style import LatexTreeProcessor, LatexSourceTreeProcessor
from tree_processor.unformated_print_style import SourceTreeProcessor
from dsl_generator_pseudocode.process_pseudocode import process

syntaxInfo = {
    "type": "virt",
    "info": {
        "supportInfo": "pseudocode/pseudocode.sgi",
        "diagrams": "pseudocode"
    }
}

file = open("test_code.txt", "r", encoding="UTF-8")
code = file.read()
res = json.loads(process(code, syntaxInfo, "other"))

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