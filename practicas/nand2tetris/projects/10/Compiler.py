import sys
import os


# Etiquetas de cada toquen
LEXICAL_ELEMENTS = {
    0: "keyword",
    1: "symbol",
    2: "integerConstant",
    3: "identifier",
    4: "stringConstant"}

# Palabras clave
KEYWORDS = ["class", "constructor", "function",
            "method", "field", "static", "var", "int",
            "char", "boolean", "void", "true", "false",
            "null", "this", "let", "do", "if", "else",
            "while", "return"]

# Claves constantes
KEYWORDS_CONS = ["true", "false", "null", "this"]

# Operaciones
OPERATIONS = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

# Operaciones unitarias
UNARY_OPT = ["-", "~"]

# Simbolos
SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";",
           "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]


# Clase Token
# recibe un string y su lext_type
# convierte de la forma <tipo> valor </tipo>
class Token():
    def __init__(self, value, lex_type):
        self.value = value
        if lex_type in LEXICAL_ELEMENTS.values():
            self.lex_type = lex_type
        else:
            raise NameError("tipo no valido")

        self.special = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;"
        }

    def __str__(self):
        if self.value in self.special.keys():
            line = f"<{self.lex_type}> {self.special[self.value]} </{self.lex_type}>\n"
        else:
            line = f"<{self.lex_type}> {self.value} </{self.lex_type}>\n"
        return line

# Clase JackTokenizer
# Descompone el input en sus respectivos simbolos
# y lo pasa a todos por la clase tokens
class JackTokenizer:
    def __init__(self, path):
        self.load(path)

    def __str__(self):
        tokens = [str(t) for t in self.tokens]
        tokens = ''.join(tokens)
        return f"<tokens>\n {tokens} </tokens>\n"

    # Funcion carga del archivo
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

    # Divide por espacios cada linea
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

    # Identifica el lex_type al que pertenece el token
    def check_token(self, token):
        itoken, num = token, None

        if token in KEYWORDS:
            num = 0
        elif token in SYMBOLS:
            num = 1
        elif token.isdigit():
            num = 2
        elif not token[0].isdigit() and token[0] != '"':
            num = 3
        elif '"' in token:
            itoken = token[1:-1]
            num = 4

        token = Token(itoken, LEXICAL_ELEMENTS[num])
        return token

    # convierte en token los tokens dados
    def cast_token(self, tokens):
        _ = [self.tokens.append(self.check_token(t)) for t in tokens]

    # Escribe el archivo filenaname.jack en filenameT_.xml
    def write(self):
        nPath = self.path.replace(".jack", "T_.xml")
        nfile = open(nPath, 'w')
        print(str(self))
        nfile.write(str(self))
        nfile.close()
        self.reset()

    # Limpia cada linea, remueve espacios y comentarios
    def clear_line(self, line):
        line = line.strip()

        if line != "":
            line = ("" if line[:2] == "//" or line[:3] ==
                    "/**" or (line[0] == "*" and line.find("*/")) else line)
            line = (line[:line.find('//')].strip()
                    if line.find('//') != -1 else line.strip())
        return line

    # Reseteamos la clase para ser usada con una ruta diferente
    def reset(self):
        self.file = ""
        self.tokens = []

# Gramatica, Anida otra gramatica o serie de statements
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

# Clase JackAnalizer
# Conviertne el archivo tokenizer
# en el archivo .xml con los arboles de gramaticas apropiados
class JackAnalizer:

    def __init__(self, path):
        self.path = path
        tokenizer = JackTokenizer(path)
        tokenizer.split()
        self.tokens = tokenizer.tokens
        self.pos = 0
        self.grammars = None

    # retorna el archivo
    def __str__(self):
        return str(self.grammars)

    # convercion tokenizer a compileEngine
    def analizer(self):
        self.grammars = self.compile_class()

    # Escribe el archivo filename.jack a filename_.xml
    def write(self):
        file = open(self.path.replace(".jack", "_.xml"), 'w')
        file.write(str(self))
        file.close()

    # Pasa al siguiente token
    def sig(self):
        self.pos = self.pos + 1
        return self.tokens[self.pos-1]

    # mantiene su posicion
    def repos(self, pos):
        self.pos = pos

    # regresa una posicion
    def dev(self):
        self.pos = self.pos - 1

    # defino si el tipo de token es un tipo de dato int, char , boolean o identifier
    def tipo(self, token):
        return token.value in ['int', 'char', 'boolean'] or token.lex_type == "identifier"

    # define si es parametro
    def param(self, token1, token2):
        return self.tipo(token1) and token2.lex_type == "identifier"

    # Anidados y traducimos una clase
    def compile_class(self):
        ini = self.pos
        gram = Grammar("class")
        token = self.sig()
        if token.value == "class":
            gram.add_rule(token)
            token = self.sig()
            if token.lex_type == "identifier":
                gram.add_rule(token)
                token = self.sig()
                if token.value == "{":
                    gram.add_rule(token)
                    varc = self.compile_vars()
                    while varc:
                        gram.add_rule(varc)
                        varc = self.compile_vars()
                    dsr = self.compile_subrutine()
                    while dsr:
                        gram.add_rule(dsr)
                        dsr = self.compile_subrutine()
                    token = self.sig()
                    if token.value == "}":
                        gram.add_rule(token)
                        return gram
        self.repos(ini)
        return None

    # Anidamos y traducimos variables
    def compile_vars(self):
        ini = self.pos
        gram = Grammar("classVarDec")
        token = self.sig()
        if token.value in ['static', 'field']:
            gram.add_rule(token)
            token = self.sig()
            if self.tipo(token):
                gram.add_rule(token)
                token = self.sig()
                if token.lex_type == "identifier":
                    gram.add_rule(token)
                    token = self.sig()
                    while token.value == ",":
                        tok_aux = self.sig()
                        if tok_aux.lex_type == "identifier":
                            gram.add_rule(token)
                            gram.add_rule(tok_aux)
                            token = self.sig()
                        else:
                            self.dev()
                            self.dev()
                            return None
                    if token.value == ";":
                        gram.add_rule(token)
                        return gram
        self.repos(ini)
        return None

    # Traducimos una subrutina
    def compile_subrutine(self):
        ini = self.pos
        gram = Grammar("subroutineDec")
        token = self.sig()
        if token.value in ['constructor', 'function', 'method']:
            gram.add_rule(token)
            token = self.sig()
            if self.tipo(token) or token.value == "void":
                gram.add_rule(token)
                token = self.sig()
                if token.lex_type == "identifier":
                    gram.add_rule(token)
                    token = self.sig()
                    if token.value == "(":
                        gram.add_rule(token)
                        gram.add_rule(self.compile_params())
                        token = self.sig()
                        if token.value == ")":
                            gram.add_rule(token)
                            csr = self.compile_body_subrutine()
                            if csr:
                                gram.add_rule(csr)
                                return gram
        self.repos(ini)
        return None

    # Compilamos parametros
    def compile_params(self):
        ini = self.pos
        gram = Grammar("parameterList")
        token1 = self.sig()
        token2 = self.sig()
        if self.param(token1, token2):
            gram.add_rule(token1)
            gram.add_rule(token2)
            token = self.sig()
            while token.value == ",":
                token1 = self.sig()
                token2 = self.sig()
                if self.param(token1, token2):
                    gram.add_rule(token)
                    gram.add_rule(token1)
                    gram.add_rule(token2)
                    token = self.sig()
                else:
                    self.dev()
                    self.dev()
                    self.dev()
                    return gram
            self.dev()
            return gram
        self.repos(ini)
        return gram

    # Compilamos el cuerpo de la subrutina
    def compile_body_subrutine(self):
        ini = self.pos
        gram = Grammar("subroutineBody")
        token = self.sig()
        if token.value == "{":
            gram.add_rule(token)
            var = self.compile_var()
            while var:
                gram.add_rule(var)
                var = self.compile_var()
            gram.add_rule(self.compile_declarations())
            token = self.sig()
            if token.value == "}":
                gram.add_rule(token)
                return gram
        self.repos(ini)
        return None

    # Compilamos una variable
    def compile_var(self):
        ini = self.pos
        gram = Grammar("varDec")
        token = self.sig()
        if token.value == "var":
            gram.add_rule(token)
            token = self.sig()
            if self.tipo(token):
                gram.add_rule(token)
                token = self.sig()
                if token.lex_type == "identifier":
                    gram.add_rule(token)
                    token = self.sig()
                    while token.value == ",":
                        tok_aux = self.sig()
                        if tok_aux.lex_type == "identifier":
                            gram.add_rule(token)
                            gram.add_rule(tok_aux)
                            token = self.sig()
                        else:
                            self.dev()
                            self.dev()
                            return None
                    if token.value == ";":
                        gram.add_rule(token)
                        return gram
        self.repos(ini)
        return None

    # Compilamos varias declaraciones
    def compile_declarations(self):
        gram = Grammar("statements")
        dec = self.compile_declaration()
        while dec:
            gram.add_rule(dec)
            dec = self.compile_declaration()
        return gram

    # Compilamos una declaración
    # Identificamos si es una declaracion:
    # let, if , while do o return
    def compile_declaration(self):
        token = self.sig()
        self.dev()
        if token.value == "let":
            return self._let()
        elif token.value == "if":
            return self._if()
        elif token.value == "while":
            return self._while()
        elif token.value == "do":
            return self._do()
        elif token.value == "return":
            return self._return()
        else:
            return None

    # Traduccion de let
    def _let(self):
        ini = self.pos
        gram = Grammar("letStatement")
        token = self.sig()
        if token.value == "let":
            gram.add_rule(token)
            token = self.sig()
            if token.lex_type == "identifier":  # nombre de variable
                gram.add_rule(token)
                token = self.sig()
                if token.value == "=":
                    gram.add_rule(token)
                    exp = self.compile_expression()
                    if exp:
                        gram.add_rule(exp)
                        token = self.sig()
                        if token.value == ";":
                            gram.add_rule(token)
                            return gram
                elif token.value == "[":
                    gram.add_rule(token)
                    exp = self.compile_expression()
                    if exp:
                        gram.add_rule(exp)
                        token = self.sig()
                        if token.value == "]":
                            gram.add_rule(token)
                            token = self.sig()
                            if token.value == "=":
                                gram.add_rule(token)
                                exp = self.compile_expression()
                                if exp:
                                    gram.add_rule(exp)
                                    token = self.sig()
                                    if token.value == ";":
                                        gram.add_rule(token)
                                        return gram
        self.repos(ini)
        return None

    # Traduccion del if
    def _if(self):
        ini = self.pos
        gram = Grammar("ifStatement")
        token = self.sig()
        if token.value == "if":
            gram.add_rule(token)
            token = self.sig()
            if token.value == "(":
                gram.add_rule(token)
                exp = self.compile_expression()
                if exp:
                    gram.add_rule(exp)
                    token = self.sig()
                    if token.value == ")":
                        gram.add_rule(token)
                        token = self.sig()
                        if token.value == "{":
                            gram.add_rule(token)
                            stm = self.compile_declarations()
                            if stm:
                                gram.add_rule(stm)
                                token = self.sig()
                                if token.value == "}":
                                    gram.add_rule(token)
                                    token = self.sig()
                                    if token.value != "else":
                                        self.dev()
                                        return gram
                                    else:
                                        gram.add_rule(token)
                                        token = self.sig()
                                        if token.value == "{":
                                            gram.add_rule(token)
                                            stm = self.compile_declarations()
                                            if stm:
                                                gram.add_rule(stm)
                                                token = self.sig()
                                                if token.value == "}":
                                                    gram.add_rule(token)
                                                    return gram
        self.repos(ini)
        return None

    # Traduccion del while
    def _while(self):
        ini = self.pos
        gram = Grammar("whileStatement")
        token = self.sig()
        if token.value == "while":
            gram.add_rule(token)
            token = self.sig()
            if token.value == "(":
                gram.add_rule(token)
                exp = self.compile_expression()
                if exp:
                    gram.add_rule(exp)
                    token = self.sig()
                    if token.value == ")":
                        gram.add_rule(token)
                        token = self.sig()
                        if token.value == "{":
                            gram.add_rule(token)
                            stm = self.compile_declarations()
                            if stm:
                                gram.add_rule(stm)
                                token = self.sig()
                                if token.value == "}":
                                    gram.add_rule(token)
                                    return gram
        self.repos(ini)
        return None

    # Traduccion del do
    def _do(self):
        ini = self.pos
        gram = Grammar("doStatement")
        token = self.sig()
        if token.value == "do":
            gram.add_rule(token)
            token = self.sig()
            if token.lex_type == "identifier":
                gram.add_rule(token)
                token = self.sig()
                if token.value == "(":
                    gram.add_rule(token)
                    exl = self.compile_list_expression()
                    if exl:
                        gram.add_rule(exl)
                        token = self.sig()
                        if token.value == ")":
                            gram.add_rule(token)
                            token = self.sig()
                            if token.value == ";":
                                gram.add_rule(token)
                                return gram
                elif token.value == ".":
                    gram.add_rule(token)
                    token = self.sig()
                    if token.lex_type == "identifier":  # nombre subrutina
                        gram.add_rule(token)
                        token = self.sig()
                        if token.value == "(":
                            gram.add_rule(token)
                            exl = self.compile_list_expression()
                            if exl:
                                gram.add_rule(exl)
                                token = self.sig()
                                if token.value == ")":
                                    gram.add_rule(token)
                                    token = self.sig()
                                    if token.value == ";":
                                        gram.add_rule(token)
                                        return gram
        self.repos(ini)
        return None

    # Traduccion del return
    def _return(self):
        ini = self.pos
        gram = Grammar("returnStatement")
        token = self.sig()
        if token.value == "return":
            gram.add_rule(token)
            exp = self.compile_expression()
            if exp:
                gram.add_rule(exp)
            token = self.sig()
            if token.value == ";":
                gram.add_rule(token)
                return gram
        self.repos(ini)
        return None

    # Compilamos uan expressionList
    def compile_list_expression(self):
        gram = Grammar("expressionList")
        exp = self.compile_expression()
        if exp:
            gram.add_rule(exp)
            token = self.sig()
            while token.value == ",":
                exp = self.compile_expression()
                if exp:
                    gram.add_rule(token)
                    gram.add_rule(exp)
                    token = self.sig()
                else:
                    self.dev()
                    return gram
            self.dev()
            return gram
        return gram

    # Compialamos una expression
    def compile_expression(self):
        ini = self.pos
        gram = Grammar("expression")
        ter = self.compile_term()
        if ter:
            gram.add_rule(ter)
            token = self.sig()
            while token.value in OPERATIONS:
                ter = self.compile_term()
                if ter:
                    gram.add_rule(token)
                    gram.add_rule(ter)
                    token = self.sig()
                else:
                    self.dev()
                    return gram
            self.dev()
            return gram
        self.repos(ini)
        return None

    # Compialmos un termino
    def compile_term(self):
        ini = self.pos
        gram = Grammar("term")
        token = self.sig()
        if token.lex_type == "integerConstant":
            gram.add_rule(token)
            return gram
        elif token.lex_type == "stringConstant":
            gram.add_rule(token)
            return gram
        elif token.value in KEYWORDS_CONS:
            gram.add_rule(token)
            return gram
        elif token.value == "(":
            gram.add_rule(token)
            exp = self.compile_expression()
            if exp:
                gram.add_rule(exp)
                token = self.sig()
                if token.value == ")":
                    gram.add_rule(token)
                    return gram
        elif token.value in UNARY_OPT:
            gram.add_rule(token)
            ter = self.compile_term()
            if ter:
                gram.add_rule(ter)
                return gram
        # nombre Subrutina, clase, variable, variable(arreglo)
        elif token.lex_type == "identifier":
            gram.add_rule(token)
            token = self.sig()
            if token.value == "[":
                gram.add_rule(token)
                exp = self.compile_expression()
                if exp:
                    gram.add_rule(exp)
                    token = self.sig()
                    if token.value == "]":
                        gram.add_rule(token)
                        return gram
            elif token.value == "(":
                gram.add_rule(token)
                exl = self.compile_list_expression()
                if exl:
                    gram.add_rule(exl)
                    token = self.sig()
                    if token.value == ")":
                        gram.add_rule(token)
                        return gram
            elif token.value == ".":
                gram.add_rule(token)
                token = self.sig()
                if token.lex_type == "identifier":  # nombre subrutina
                    gram.add_rule(token)
                    token = self.sig()
                    if token.value == "(":
                        gram.add_rule(token)
                        exl = self.compile_list_expression()
                        if exl:
                            gram.add_rule(exl)
                            token = self.sig()
                            if token.value == ")":
                                gram.add_rule(token)
                                return gram
            else:
                self.dev()
                return gram
        self.repos(ini)
        return None

# Dada una ruta dada
# Realiza su tokenizer y analizer
def main():
    path = sys.argv[1]
    print(path)
    
    Tok = JackTokenizer(path) 
    Tok.split()
    Tok.write()

    An = JackAnalizer(path)
    An.analizer()
    An.write()
    
    print(An)
    
    return 0


if __name__ == "__main__":
    main()
