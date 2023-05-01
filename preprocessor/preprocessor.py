import copy
import codecs
import re

new_command_regex = r"@@[\s]*new_command[\s]*{[\s]*(?P<name>\\?[a-zA-Z_@][\w]*)[\s]*}(?:[\s]*\[[\s]*(?P<arg_count>(?:[1-9][0-9]*)|[0-9])?[\s]*\])?[\s]*{[\s]*(?P<content>(?:[\s]*(?P<string1>(?P<formated1>f\"(?:\\.|[^\"])*\")|(?P<unformated1>\"[^\"]*\"))[\s]*,[\s]*)*(?P<string2>(?P<formated2>f\"(?:\\.|[^\"])*\")|(?P<unformated2>\"[^\"]*\")))[\s]*}"
replace_regex = r"@@[\s]*replace[\s]*{[\s]*(?P<string0>(?P<formated0>f\"(?:\\.|[^\"])*\")|(?P<unformated0>\"[^\"]*\"))[\s]*}[\s]*{[\s]*(?P<content>(?:[\s]*(?P<string1>(?P<formated1>f\"(?:\\.|[^\"])*\")|(?P<unformated1>\"[^\"]*\"))[\s]*,[\s]*)*(?P<string2>(?P<formated2>f\"(?:\\.|[^\"])*\")|(?P<unformated2>\"[^\"]*\")))[\s]*}"
include_regex = r"@@[\s]*include[\s]*{[\s]*(?P<string0>(?P<formated0>f\"(?:\\.|[^\"])*\")|(?P<unformated0>\"[^\"]*\"))[\s]*}"
string_regex = r"(?P<string>(?P<formated>f\"(?P<formated_content>(?:\\.|[^\"])*)\")|(?P<unformated>\"(?P<unformated_content>[^\"]*)\"))"
macros_args_regex = r"{[\s]*(?P<content>(?:[\s]*(?P<string1>(?P<formated1>f\"(?:\\.|[^\"])*\")|(?P<unformated1>\"[^\"]*\"))[\s]*,[\s]*)*(?P<string2>(?P<formated2>f\"(?:\\.|[^\"])*\")|(?P<unformated2>\"[^\"]*\"))?)[\s]*}"
comment_regex = r"%.*$"
class Macros:
    def __init__(self, name:str, arg_count:str, content:str) -> None:
        self.name = name
        self.arg_count = 0
        if arg_count:
            self.arg_count = int(arg_count)
        self.string = ""
        strings, _ = parse_content(content)
        self.string = "\n".join(strings)

            
def parse_content(content:str):
    strings = []
    strings_unformated = []
    pos = 0
    while pos < len(content):
        if content[pos].isspace():
            pos += 1
            continue
        if content[pos] == ",":
            pos += 1
            continue
        result = re.match(string_regex, content[pos:])
        if not result:
            raise Exception("invalid macros deffinition")
        if result.group("formated"):
            string = result.group("formated_content")
            string = codecs.getencoder("raw_unicode_escape")(string)[0]
            string = codecs.getdecoder("unicode_escape")(string)[0]
        if result.group("unformated"):
            string = result.group("unformated_content")
        strings.append(string)
        strings_unformated.append(result.group("string"))
        pos += len(result.group(0))
    return strings, strings_unformated

def remove_comments(code: str):
    pos = 0
    while pos < len(code):
        result = re.match(comment_regex, code[pos:], flags=re.MULTILINE)
        if result:
            code = code[:pos] + code[pos+len(result.group(0)):]
            continue
        pos += 1
    return code

def preprocess(code: str):
    macroses = {}
    output = remove_comments(code)
    pos = 0
    while pos < len(output):
        result = re.match(new_command_regex, output[pos:])
        if result:
            macroses[result.group("name")] = Macros(result.group("name"),result.group("arg_count"),result.group("content"))
            output = output[:pos] + output[pos+len(result.group(0)):]
            continue
        result = re.match(replace_regex, output[pos:])
        if result:
            replacement = parse_content(result.group("string0"))[0][0]
            args, args_unformated = parse_content(result.group("content"))
            if len(args) % 2 != 0:
                raise Exception("invalid \"@@replace\" arg count")
            for i in range(len(args)//2):
                marker = args[2*i]
                replacement = replacement.replace("#" + marker, args[2*i+1])
                replacement = replacement.replace("@" + marker, args_unformated[2*i+1])
            output = output[:pos] + replacement + output[pos+len(result.group(0)):]
            continue
        result = re.match(include_regex, output[pos:])
        if result:
            inclupe_path = parse_content(result.group("string0"))[0][0]
            inclide_code = ""
            with open(inclupe_path, "r", encoding="UTF-8") as file:
                inclide_code = remove_comments(file.read())
            output = output[:pos] + inclide_code + output[pos+len(result.group(0)):]
            continue
        for _, macros in macroses.items():
            if output[pos:].startswith(macros.name):
                macros_start = pos
                pos += len(macros.name)
                macros_end = pos
                while output[pos].isspace() and pos < len(output):
                    pos += 1
                replacement = macros.string
                strings = []
                result = re.match(macros_args_regex, output[pos:])
                if result:
                    strings, strings_unformated = parse_content(result.group("content"))
                    macros_end = pos + len(result.group(0))
                for i in range(macros.arg_count):
                    if i < len(strings):
                        replacement = replacement.replace(f"#{i+1}", strings[i])
                    else:
                        replacement = replacement.replace(f"#{i+1}", "")
                for i in range(macros.arg_count):
                    if i < len(strings):
                        replacement = replacement.replace(f"@{i+1}", strings_unformated[i])
                    else:
                        replacement = replacement.replace(f"@{i+1}", "")
                output = output[:macros_start] + replacement + output[macros_end:]
                pos = macros_start
                break
        if not result:
            pos += 1
    return output