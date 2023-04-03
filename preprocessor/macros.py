import re
from pyparsing import nestedExpr


class Macros:
    body_str = ""
    args_count = int(0)
    name = str("")
    args = []

    def get_body(self):
        return nestedExpr('{', '}').parseString(self.body_str).asList()
