import sys
import re

def remove_comments(text):
    pattern = r"%.*(\n|$)"
    text = re.sub(pattern, "\n", text, flags=re.MULTILINE)
    return text


def main():
    try:
        input_file_name = sys.argv[1]
    except IndexError:
        input_file_name = 'input.txt'

    try:
        input_file = open(input_file_name, 'r')
    except FileNotFoundError:
        print("No file provided! Exit...")
        exit(1)

    text = input_file.read()
    text = remove_comments(text)
    print(text)

if __name__ == '__main__':
    main()

