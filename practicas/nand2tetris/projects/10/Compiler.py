import sys
import os


LEXICAL_ELEMENTS = {
    0: "keyword",
    1: "symbol",
    2: "integerConstant",
    3: "identifier",
    4: "stringConstant"}

KEYWORDS = ["class", "constructor", "function",
            "method", "field", "static", "var", "int",
            "char", "boolean", "void", "true", "false",
            "null", "this", "let", "do", "if", "else",
            "while", "return"]

KEYWORDS_CONS = ["true", "false", "null", "this"]

OPERATIONS = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

UNARY_OPT = ["-", "~"]

SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";",
           "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]


class Token():
    def __init__(self, value, lex_type):
        self.value = value
        if lex_type in LEXICAL_ELEMENTS.values():
            self.lex_type = lex_type
        else:
            raise NameError("tipo no valido")

        self.special = {
            "<": "&lt",
            ">": "&gt",
            "&": "&amp"
        }

    def __str__(self):
        if self.value in self.special.keys():
            line = f"<{self.lex_type}> {self.special[self.value]} </{self.lex_type}>\n"
        else:
            line = f"<{self.lex_type}> {self.value} </{self.lex_type}>\n"
        return line


class JackTokenizer:
    def __init__(self, path):
        self.load(path)

    def __str__(self):
        tokens = [str(t) for t in self.tokens]
        tokens = ''.join(tokens)
        return tokens

    def load(self, path):
        self.reset()
        self.path = path

        file = open(path, 'r')
        lines = [i for i in file]
        lines = [self.clear_line(i) for i in lines]
        lines = [i for i in lines if "" != i]
        self.file = ''.join(lines)

        file.close()
        print("Archivo cargado")

    def split(self):
        file_split = self.file.split('"')
        for i, string in enumerate(file_split):
            if i % 2 == 0:
                space = []
                _ = [space.append(f" {c} ") if c in SYMBOLS
                     else space.append(c) for c in string]
                self.cast_token(''.join(space).split())
            else:
                self.cast_token([f'"{string}"'])

    def check_token(self, token):
        itoken, num = token, None

        if token in KEYWORDS:
            num = 0
        elif token in SYMBOLS:
            num = 1
        elif token.isdigit():
            num = 2
        elif not token[0].isdigit():
            num = 3
        elif '"' in token:
            itoken = token[1:-1]
            num = 4

        token = Token(itoken, LEXICAL_ELEMENTS[num])
        return token

    def cast_token(self, tokens):
        _ = [self.tokens.append(self.check_token(t)) for t in tokens]

    def write(self):
        nPath = self.path.replace(".jack", "T_.xml")
        nfile = open(nPath, 'w')
        print(str(self))
        nfile.write(str(self))
        nfile.close()
        self.reset()

    def clear_line(self, line):
        line = line.strip()

        if line != "":
            line = ("" if line[:2] == "//" or line[:3] ==
                    "/**" or (line[0] == "*" and line.find("*/")) else line)
            line = (line[:line.find('//')].strip()
                    if line.find('//') != -1 else line.strip())
        return line

    def reset(self):
        self.file = ""
        self.tokens = []


class Grammar():
    def __init__(self, name):
        self.name = name
        self.rules = []

    def __str__(self):
        text = f"<{self.name}>\n"

        for rule in self.rules:
            if type(rule).__name__ == "Grammar":
                txt = str(rule).split('\n')[:-1]
                txt = ["\t"+t+"\n" for t in txt]
                text = text + ''.join(txt)
            else:
                text = text + '\t' + str(rule)
        
        return text + f"</{self.name}>\n"

    def add_rule(self, rule):
        self.rules.append(rule)


def main():
    print("work")

    return 0


if __name__ == "__main__":
    main()
