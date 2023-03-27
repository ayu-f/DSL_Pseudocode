import json

def print_node(root:dict, depth):

    if "term" in root.keys():
        if "value" in root.keys():
            print(root["value"], end=" ")
        else:
            print(root["term"], end=" ")
    else:
        if root["nonterm"] == "КОМАНДА":
            print(depth * "\t", end="")
        if root["nonterm"] == "БЛОК_КОДА":
            depth += 1
        for node in root["content"]:
            print_node(node, depth)
        if root["nonterm"] == "КОМАНДА" or root["nonterm"] == "ЗАГОЛОВОК_АЛГОРИТМА":
            print()
                

file = open("test_tree.json", "r", encoding="UTF-8")
code = file.read()
res = json.loads(code)

print_node(res, depth=0)