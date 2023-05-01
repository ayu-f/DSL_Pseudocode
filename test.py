import sys
sys.path.append("./dsl_generator_pseudocode")
sys.path.append("./tree_processor")
sys.path.append("./preprocessor")

import json
from preprocessor.preprocessor import preprocess
from tree_processor.latex_print_style import LatexTreeProcessor, LatexSourceTreeProcessor
from tree_processor.unformated_print_style import SourceTreeProcessor
from dsl_generator_pseudocode.process_pseudocode import process
syntaxInfo = {
    "type": "virt",
    "info": {
        "supportInfo": "pseudocode/pseudocode.json",
        "diagrams": "pseudocode"
    }
}


code = ''
with open("test_code.txt", "r", encoding="UTF-8") as file:
    code = file.read()

output = preprocess(code)

with open("test_preprocessed.txt", "w", encoding="UTF-8") as file:
    file.write(output)

ast_json = ""
ast_json = process(output, syntaxInfo)

with open("test_tree.json", "w", encoding="UTF-8") as file:
    file.write(ast_json)

ast = json.loads(ast_json)

with open("source_reconstructed.txt", "w", encoding="UTF-8") as file:
    processor = SourceTreeProcessor(file)
    processor.print_tree(ast)

with open("source_publication.tex", "w", encoding="UTF-8") as file:
    processor = LatexSourceTreeProcessor(file)
    processor.print_tree(ast)

with open("publication.tex", "w", encoding="UTF-8") as file:
    processor = LatexTreeProcessor(file)
    processor.print_tree(ast)