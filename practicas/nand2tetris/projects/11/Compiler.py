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
        nfile.write(str(self))
        nfile.close()
        self.reset()

    # Limpia cada linea, remueve espacios y comentarios
    def clear_line(self, line):
        line = line.strip()

        if line != "":
            line = ("" if line[:2] == "//" or line[:3] ==
                    "/**" or (line[0] == "*" and line.find("*/")) or line[0] == "*" else line)
            line = (line[:line.find('//')].strip()
                    if line.find('//') != -1 else line.strip())
        return line

    # Reseteamos la clase para ser usada con una ruta diferente
    def reset(self):
        self.file = ""
        self.tokens = []

# Grammar, Anida otra Grammar o serie de statements


class Grammar():
    def __init__(self, value):
        self.value = value
        self.rules = []

    def __str__(self):
        text = f"<{self.value}>\n"

        for rule in self.rules:
            if type(rule).__name__ == "Grammar":
                txt = str(rule).split('\n')[:-1]
                txt = ["\t"+t+"\n" for t in txt]
                text = text + ''.join(txt)
            else:
                text = text + '\t' + str(rule)

        return text + f"</{self.value}>\n"

    def add_rule(self, rule):
        self.rules.append(rule)

# Clase JackAnalizer
# Conviertne el archivo tokenizer
# en el archivo .xml con los arboles de Grammars apropiados


class TokenVar:

    def __init__(self, token, cat, lex_type=None, indice=None, rol=None):
        self.value = token.value
        self.lex_type = token.lex_type
        if cat == "field":
            self.cat = "this"
        else:
            self.cat = cat
        if cat not in ['class', 'subroutine']:
            self.tipo_dato = lex_type
            self.ind = indice
            self.rol = rol

    def __str__(self):

        if self.cat == "this":
            cat = "field"
        else:
            cat = self.cat
        if cat not in ['class', 'subroutine']:
            return f"<{self.lex_type}> {self.value} </{self.lex_type}> {[cat, self.tipo_dato, self.ind, self.rol]}\n"
        else:
            return f"<{self.lex_type}> {self.value} </{self.lex_type}> {[cat]}\n"

    def clase(self):
        return "tokenVar"


class SymbolTable:

    def __init__(self):
        self._tabla = [{"field": [], "static": []}]

    def __str__(self):
        txt = ''
        for dic in self._tabla:
            for key, value in dic.items():
                for ind, row in enumerate(value):
                    txt = txt + str(row+[key, ind]) + "\n"
        return txt

    def sub(self):
        self._tabla.append({"argument": [], "local": []})

    def deleteSub(self):
        self._tabla.pop()

    def add(self, token, tipo, clase):
        if clase in ["field", "static"]:
            self._tabla[0][clase].append([token.value, tipo])
        else:
            self._tabla[-1][clase].append([token.value, tipo])

    def get(self, token, clase):
        if clase in ["field", "static"]:
            tabla = self._tabla[0][clase]
        else:
            tabla = self._tabla[-1][clase]

        for ind, reg in enumerate(tabla):
            if reg[0] == token.value:
                return TokenVar(token, clase, reg[1], ind, 'def')

    def find(self, token):
        tabla = dict(self._tabla[0], **self._tabla[-1])
        for clase, value in tabla.items():
            for ind, reg in enumerate(value):
                if reg[0] == token.value:
                    return TokenVar(token, clase, reg[1], ind, 'use')


class FullAnalizer:

    def __init__(self, ruta):
        self._ruta = ruta
        tokenizer = JackTokenizer(ruta)
        tokenizer.split()
        self._tokens = tokenizer.tokens
        self._tabla = SymbolTable()
        self._pos = 0
        self._Grammars = None

    def __str__(self):
        return str(self._Grammars)

    def analizer(self):
        self._Grammars = self.compile_class()
        if not self._Grammars:
            raise NameError(
                f"ERROR: Hay un error de sintaxis. Por favor revise su código")

    def write(self):
        archivo = open(self._ruta.replace(".jack", "ST_.xml"), 'w')
        archivo.write(str(self))
        archivo.close()

    def compile_class(self):
        ini = self._pos
        gram = Grammar("class")
        token = self._sig()
        if token.value == "class":
            gram.add_rule(token)
            token = self._sig()
            if token.lex_type == "identifier":
                gram.add_rule(TokenVar(token, 'class'))
                token = self._sig()
                if token.value == "{":
                    gram.add_rule(token)
                    varc = self.compile_vars_class()
                    while varc:
                        gram.add_rule(varc)
                        varc = self.compile_vars_class()
                    dsr = self.compile_dcl_subr()
                    while dsr:
                        gram.add_rule(dsr)
                        dsr = self.compile_dcl_subr()
                    token = self._sig()
                    if token.value == "}":
                        gram.add_rule(token)
                        return gram
        self._repos(ini)
        return None

    def compile_vars_class(self):
        ini = self._pos
        gram = Grammar("classVarDec")
        token = self._sig()
        if token.value in ['static', 'field']:
            cat = token.value
            gram.add_rule(token)
            token = self._sig()
            if self.tipo(token):
                if token.lex_type == "identifier":   # Se mira si el tipo declarado es una clase
                    token = TokenVar(token, 'class')
                tipo = token.value
                gram.add_rule(token)
                token = self._sig()
                if token.lex_type == "identifier":
                    # Se agrega la variable a la tabla
                    self._tabla.add(token, tipo, cat)
                    # Se find el indice del token en la tabla
                    token = self._tabla.get(token, cat)
                    gram.add_rule(token)
                    token = self._sig()
                    while token.value == ",":
                        tok_aux = self._sig()
                        if tok_aux.lex_type == "identifier":
                            # Se agrega la variable a la tabla
                            self._tabla.add(tok_aux, tipo, cat)
                            # Se find el indice del token en la tabla
                            tok_aux = self._tabla.get(tok_aux, cat)
                            gram.add_rule(token)
                            gram.add_rule(tok_aux)
                            token = self._sig()
                        else:
                            self._dev()
                            self._dev()
                            return None
                    if token.value == ";":
                        gram.add_rule(token)
                        return gram
        self._repos(ini)
        return None

    def compile_dcl_subr(self):
        ini = self._pos
        gram = Grammar("subroutineDec")
        self._tabla.sub()   # Se añade una nueva subrutina
        token = self._sig()
        if token.value in ['constructor', 'function', 'method']:
            gram.add_rule(token)
            if token.value == 'method':
                self._tabla.add(Token('this', 'keyword'),
                                'pointer', 'argument')
            token = self._sig()
            if self.tipo(token) or token.value == "void":
                if token.lex_type == "identifier":   # Se mira si el tipo declarado es una clase
                    token = TokenVar(token, 'class')
                gram.add_rule(token)
                token = self._sig()
                if token.lex_type == "identifier":
                    gram.add_rule(TokenVar(token, 'subroutine'))
                    token = self._sig()
                    if token.value == "(":
                        gram.add_rule(token)
                        gram.add_rule(self.compile_params())
                        token = self._sig()
                        if token.value == ")":
                            gram.add_rule(token)
                            csr = self.compile_bdy_subr()
                            if csr:
                                gram.add_rule(csr)
                                return gram
        self._repos(ini)
        return None

    def compile_params(self):
        ini = self._pos
        gram = Grammar("parameterList")
        token1 = self._sig()
        token2 = self._sig()
        if self.parametro(token1, token2):
            if token1.lex_type == "identifier":   # Se mira si el tipo declarado es una clase
                token1 = TokenVar(token1, 'class')
            tipo = token1.value
            # Se agrega la variable a la tabla
            self._tabla.add(token2, tipo, "argument")
            # Se find el indice del token en la tabla
            token2 = self._tabla.get(token2, "argument")
            gram.add_rule(token1)
            gram.add_rule(token2)
            token = self._sig()
            while token.value == ",":
                token1 = self._sig()
                token2 = self._sig()
                if self.parametro(token1, token2):
                    if token1.lex_type == "identifier":   # Se mira si el tipo declarado es una clase
                        token1 = TokenVar(token1, 'class')
                    tipo = token1.value
                    # Se agrega la variable a la tabla
                    self._tabla.add(token2, tipo, "argument")
                    # Se find el indice del token en la tabla
                    token2 = self._tabla.get(token2, "argument")
                    gram.add_rule(token)
                    gram.add_rule(token1)
                    gram.add_rule(token2)
                    token = self._sig()
                else:
                    self._dev()
                    self._dev()
                    self._dev()
                    return gram
            self._dev()
            return gram
        self._repos(ini)
        return gram

    def compile_bdy_subr(self):
        ini = self._pos
        gram = Grammar("subroutineBody")
        token = self._sig()
        if token.value == "{":
            gram.add_rule(token)
            var = self.compile_var()
            while var:
                gram.add_rule(var)
                var = self.compile_var()
            gram.add_rule(self.compile_dcls())
            token = self._sig()
            if token.value == "}":
                gram.add_rule(token)
                return gram
        self._repos(ini)
        return None

    def compile_var(self):
        ini = self._pos
        gram = Grammar("varDec")
        token = self._sig()
        if token.value == "var":
            gram.add_rule(token)
            token = self._sig()
            if self.tipo(token):
                if token.lex_type == "identifier":   # Se mira si el tipo declarado es una clase
                    token = TokenVar(token, 'class')
                tipo = token.value
                gram.add_rule(token)
                token = self._sig()
                if token.lex_type == "identifier":
                    # Se agrega la variable a la tabla
                    self._tabla.add(token, tipo, 'local')
                    # Se find el indice del token en la tabla
                    token = self._tabla.get(token, 'local')
                    gram.add_rule(token)
                    token = self._sig()
                    while token.value == ",":
                        tok_aux = self._sig()
                        if tok_aux.lex_type == "identifier":
                            # Se agrega la variable a la tabla
                            self._tabla.add(tok_aux, tipo, 'local')
                            # Se find el indice del token en la tabla
                            tok_aux = self._tabla.get(tok_aux, 'local')
                            gram.add_rule(token)
                            gram.add_rule(tok_aux)
                            token = self._sig()
                        else:
                            self._dev()
                            self._dev()
                            return None
                    if token.value == ";":
                        gram.add_rule(token)
                        return gram
        self._repos(ini)
        return None

    def compile_dcls(self):
        ini = self._pos
        gram = Grammar("statements")
        dec = self.compile_declaration()
        while dec:
            gram.add_rule(dec)
            dec = self.compile_declaration()
        return gram

    def compile_declaration(self):
        token = self._sig()
        self._dev()
        if token.value == "let":
            return self.copile_let()
        elif token.value == "if":
            return self.compile_if()
        elif token.value == "while":
            return self.compile_while()
        elif token.value == "do":
            return self.compile_do()
        elif token.value == "return":
            return self.compile_return()
        else:
            return None

    def copile_let(self):
        ini = self._pos
        gram = Grammar("letStatement")
        token = self._sig()
        if token.value == "let":
            gram.add_rule(token)
            token = self._sig()
            if token.lex_type == "identifier":
                token = self._tabla.find(token)
                gram.add_rule(token)
                token = self._sig()
                if token.value == "=":
                    gram.add_rule(token)
                    exp = self.compile_expression()
                    if exp:
                        gram.add_rule(exp)
                        token = self._sig()
                        if token.value == ";":
                            gram.add_rule(token)
                            return gram
                elif token.value == "[":
                    gram.add_rule(token)
                    exp = self.compile_expression()
                    if exp:
                        gram.add_rule(exp)
                        token = self._sig()
                        if token.value == "]":
                            gram.add_rule(token)
                            token = self._sig()
                            if token.value == "=":
                                gram.add_rule(token)
                                exp = self.compile_expression()
                                if exp:
                                    gram.add_rule(exp)
                                    token = self._sig()
                                    if token.value == ";":
                                        gram.add_rule(token)
                                        return gram
        self._repos(ini)
        return None

    def compile_if(self):
        ini = self._pos
        gram = Grammar("ifStatement")
        token = self._sig()
        if token.value == "if":
            gram.add_rule(token)
            token = self._sig()
            if token.value == "(":
                gram.add_rule(token)
                exp = self.compile_expression()
                if exp:
                    gram.add_rule(exp)
                    token = self._sig()
                    if token.value == ")":
                        gram.add_rule(token)
                        token = self._sig()
                        if token.value == "{":
                            gram.add_rule(token)
                            stm = self.compile_dcls()
                            if stm:
                                gram.add_rule(stm)
                                token = self._sig()
                                if token.value == "}":
                                    gram.add_rule(token)
                                    token = self._sig()
                                    if token.value != "else":
                                        self._dev()
                                        return gram
                                    else:
                                        gram.add_rule(token)
                                        token = self._sig()
                                        if token.value == "{":
                                            gram.add_rule(token)
                                            stm = self.compile_dcls()
                                            if stm:
                                                gram.add_rule(stm)
                                                token = self._sig()
                                                if token.value == "}":
                                                    gram.add_rule(token)
                                                    return gram
        self._repos(ini)
        return None

    def compile_while(self):
        ini = self._pos
        gram = Grammar("whileStatement")
        token = self._sig()
        if token.value == "while":
            gram.add_rule(token)
            token = self._sig()
            if token.value == "(":
                gram.add_rule(token)
                exp = self.compile_expression()
                if exp:
                    gram.add_rule(exp)
                    token = self._sig()
                    if token.value == ")":
                        gram.add_rule(token)
                        token = self._sig()
                        if token.value == "{":
                            gram.add_rule(token)
                            stm = self.compile_dcls()
                            if stm:
                                gram.add_rule(stm)
                                token = self._sig()
                                if token.value == "}":
                                    gram.add_rule(token)
                                    return gram
        self._repos(ini)
        return None

    def compile_do(self):
        ini = self._pos
        gram = Grammar("doStatement")
        token = self._sig()
        if token.value == "do":
            gram.add_rule(token)
            token = self._sig()
            if token.lex_type == "identifier":
                ti = token
                token = self._sig()
                if token.value == "(":
                    gram.add_rule(TokenVar(ti, 'subroutine'))
                    gram.add_rule(token)
                    exl = self.compile_list_expr()
                    if exl:
                        gram.add_rule(exl)
                        token = self._sig()
                        if token.value == ")":
                            gram.add_rule(token)
                            token = self._sig()
                            if token.value == ";":
                                gram.add_rule(token)
                                return gram
                elif token.value == ".":
                    # mira si es el nombre de una variable o una clase
                    busqueda = self._tabla.find(ti)
                    if busqueda:
                        gram.add_rule(busqueda)
                    else:
                        gram.add_rule(TokenVar(ti, 'class'))
                    gram.add_rule(token)
                    token = self._sig()
                    if token.lex_type == "identifier":
                        gram.add_rule(TokenVar(token, 'subroutine'))
                        token = self._sig()
                        if token.value == "(":
                            gram.add_rule(token)
                            exl = self.compile_list_expr()
                            if exl:
                                gram.add_rule(exl)
                                token = self._sig()
                                if token.value == ")":
                                    gram.add_rule(token)
                                    token = self._sig()
                                    if token.value == ";":
                                        gram.add_rule(token)
                                        return gram
        self._repos(ini)
        return None

    def compile_return(self):
        ini = self._pos
        gram = Grammar("returnStatement")
        token = self._sig()
        if token.value == "return":
            gram.add_rule(token)
            exp = self.compile_expression()
            if exp:
                gram.add_rule(exp)
            token = self._sig()
            if token.value == ";":
                gram.add_rule(token)
                return gram
        self._repos(ini)
        return None

    def compile_list_expr(self):
        ini = self._pos
        gram = Grammar("expressionList")
        exp = self.compile_expression()
        if exp:
            gram.add_rule(exp)
            token = self._sig()
            while token.value == ",":
                exp = self.compile_expression()
                if exp:
                    gram.add_rule(token)
                    gram.add_rule(exp)
                    token = self._sig()
                else:
                    self._dev()
                    return gram
            self._dev()
            return gram
        return gram

    def compile_expression(self):
        ini = self._pos
        gram = Grammar("expression")
        ter = self.compile_term()
        if ter:
            gram.add_rule(ter)
            token = self._sig()
            while token.value in OPERATIONS:
                ter = self.compile_term()
                if ter:
                    gram.add_rule(token)
                    gram.add_rule(ter)
                    token = self._sig()
                else:
                    self._dev()
                    return gram
            self._dev()
            return gram
        self._repos(ini)
        return None

    def compile_term(self):
        ini = self._pos
        gram = Grammar("term")
        token = self._sig()
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
                token = self._sig()
                if token.value == ")":
                    gram.add_rule(token)
                    return gram
        elif token.value in UNARY_OPT:
            gram.add_rule(token)
            ter = self.compile_term()
            if ter:
                gram.add_rule(ter)
                return gram
        elif token.lex_type == "identifier":
            ti = token   # Guardo momentariamente el token
            token = self._sig()
            if token.value == "[":
                # Busco el token en la tabla porque es una variable
                gram.add_rule(self._tabla.find(ti))
                gram.add_rule(token)
                exp = self.compile_expression()
                if exp:
                    gram.add_rule(exp)
                    token = self._sig()
                    if token.value == "]":
                        gram.add_rule(token)
                        return gram
            elif token.value == "(":
                # Añado el token como subrutina
                gram.add_rule(TokenVar(ti, 'subroutine'))
                gram.add_rule(token)
                exl = self.compile_list_expr()
                if exl:
                    gram.add_rule(exl)
                    token = self._sig()
                    if token.value == ")":
                        gram.add_rule(token)
                        return gram
            elif token.value == ".":
                # mira si es el nombre de una variable o una clase
                busqueda = self._tabla.find(ti)
                if busqueda:
                    gram.add_rule(busqueda)
                else:
                    gram.add_rule(TokenVar(ti, 'class'))
                # gram.add_rule(TokenVar(ti, 'class'))   # Añado el token como clase
                gram.add_rule(token)
                token = self._sig()
                if token.lex_type == "identifier":
                    # Añado el token como subrutina
                    gram.add_rule(TokenVar(token, 'subroutine'))
                    token = self._sig()
                    if token.value == "(":
                        gram.add_rule(token)
                        exl = self.compile_list_expr()
                        if exl:
                            gram.add_rule(exl)
                            token = self._sig()
                            if token.value == ")":
                                gram.add_rule(token)
                                return gram
            else:
                # Busco el token en la tabla porque es una variable
                gram.add_rule(self._tabla.find(ti))
                self._dev()
                return gram
        self._repos(ini)
        return None

    def rules(self):
        return self._Grammars

    def _sig(self):
        self._pos = self._pos + 1
        return self._tokens[self._pos-1]

    def _dev(self):
        self._pos = self._pos - 1

    def _repos(self, pos):
        self._pos = pos

    def keywordConstant(self, token):
        return token.value in ["true", "false", "null", "this"]

    def unaryOp(self, token):
        return token.value in ["-", "~"]

    def tipo(self, token):
        return token.value in ['int', 'char', 'boolean'] or token.lex_type == "identifier"

    def parametro(self, token1, token2):
        return self.tipo(token1) and token2.lex_type == "identifier"


class codeGenerator:

    def __init__(self, ruta):
        fa = FullAnalizer(ruta)
        fa.analizer()
        self._gramaticas = fa.rules()  # Nodo clase del árbol
        self._vm = []
        self._clase = ''
        self._ruta = ruta
        self._subrutinas = {}
        self.nif = 0
        self.nwhile = 0

    def __str__(self):
        txt = ''
        for ins in self._vm:
            txt = txt + ins + "\n"
        return txt

    def write(self):
        nPath = self._ruta.replace(".jack", ".vm")
        nfile = open(nPath, 'w')
        nfile.write(str(self))
        nfile.close()

    def generar(self):
        sub = self._gramaticas.rules  # Nodos hijos del nodo clase:
        self.define_metodos(sub)
        self._clase = sub[1].value  # Guarda el nombre de la clase
        if len(sub)-4 > 0:
            for i in range(3, len(sub)-1):
                subdec = sub[i].rules
                if sub[i].value == "subroutineDec":
                    # print(self._subrutinas[subdec[2].value][1])
                    self._vm.append(
                        # f"function {self._clase}.{subdec[2].value} { ( self._subrutinas[subdec[2].value][2] > 1 )*( self._subrutinas[subdec[2].value][2] - 1) }")
                        f"function {self._clase}.{subdec[2].value} {  self._subrutinas[subdec[2].value][-1] }")
                    # input("Stop")
                    if subdec[0].value == "method":
                        self._vm.append("push argument 0")
                        self._vm.append("pop pointer 0")
                    if subdec[0].value == "constructor":
                        self._vm.append(
                            f"push constant {self.cuenta_campos(sub)}")
                        self._vm.append("call Memory.alloc 1")
                        self._vm.append("pop pointer 0")
                    # Entra a los hijos de subroutineBody
                    body=subdec[-1].rules
                    # Solo se para como parametro los Statement y Clases
                    self.escribe_cuerpo(body[1:-1])


    def define_metodos(self, sub):
        if len(sub)-4 > 0:
            for i in range(3, len(sub)-1):
                subdec=sub[i].rules
                if sub[i].value == "subroutineDec":
                    # Entra a los nodos hijos del primer subroutineDec
                    subdec=sub[i].rules
                    nom_subrut=subdec[2].value
                    fcm_subrut=subdec[0].value
                    tipo_subrut=subdec[1].value
                    argum = 0
                    if fcm_subrut == "method":
                        # Enrta a los nodos hijos de parameter list
                        param=subdec[4].rules
                        # Encuentra el número de parametros a pedir
                        param=len(param)//3 + 1 + (nom_subrut == "method")
                        argum = self.cuenta_parametros(subdec[-1].rules) 
                    elif fcm_subrut == "function":
                        param=self.cuenta_parametros(subdec[-1].rules)
                    else:
                        param=0
   
                    print([nom_subrut, fcm_subrut, tipo_subrut, param, argum])
                    self._subrutinas[nom_subrut]=[
                        fcm_subrut, tipo_subrut, param, argum]

    def cuenta_parametros(self, body):
        params= 1
        for bdy in body:
            if bdy.value == "varDec":
                params=params + len(bdy.rules[1:-1])/2  - 1
        return int(params) 

    def cuenta_campos(self, sub):
        campos=0
        for s in sub:
            if s.value == "classVarDec":
                campos=campos + len(s.rules[1:-1])/2
        return int(campos)

    def escribe_cuerpo(self, body):
        for bdy in body:
            if bdy.value == "statements":
                stat=bdy.rules
                self.escribe_declaraciones(stat)

    def escribe_declaraciones(self, sts):
        ni=self.nif
        nw=self.nwhile
        for dec in sts:
            if dec.value == "letStatement":
                self.escribe_let(dec.rules)
            elif dec.value == "ifStatement":
                self.nif=self.nif + 1
                self.escribe_if(dec.rules, ni)
            elif dec.value == "whileStatement":
                self.nwhile=self.nwhile + 1
                self.escribe_while(dec.rules, nw)
            elif dec.value == "doStatement":
                self.escribe_do(dec.rules)
            elif dec.value == "returnStatement":
                self.escribe_return(dec.rules)

    def escribe_let(self, let):
        if(len(let) == 8):
            self.escribe_expresion(let[3].rules)
            self._vm.append(f"push {let[1].cat} {let[1].ind}")
            self._vm.append("add")
            self.escribe_expresion(let[6].rules)
            self._vm.append("pop temp 0")
            self._vm.append("pop pointer 1")
            self._vm.append("push temp 0")
            self._vm.append("pop that 0")
        else:
            self.escribe_expresion(let[3].rules)
            self._vm.append(f"pop {let[1].cat} {let[1].ind}")

    def escribe_if(self, ifs, n):
        self.escribe_expresion(ifs[2].rules)
        if len(ifs) == 11:
            self._vm.append("if-goto " + self._clase + ".IF-TRUE"+str(n))
            self._vm.append("goto " + self._clase + ".IF-FALSE"+str(n))
            self._vm.append("label " + self._clase + ".IF-TRUE"+str(n))
            self.escribe_declaraciones(ifs[5].rules)
            self._vm.append("goto " + self._clase + ".IF-END"+str(n))
            self._vm.append("label " + self._clase + ".IF-FALSE"+str(n))
            self.escribe_declaraciones(ifs[9].rules)
            self._vm.append("label " + self._clase + ".IF-END"+str(n))
        else:
            self._vm.append("not")
            self._vm.append("if-goto IF-END"+str(n))
            self.escribe_declaraciones(ifs[5].rules)
            self._vm.append("label IF-END"+str(n))

    def escribe_while(self, whiles, n):
        self._vm.append("label WHILE-EXP"+str(n))
        self.escribe_expresion(whiles[2].rules)
        self._vm.append("not")
        self._vm.append("if-goto WHILE-END"+str(n))
        self.escribe_declaraciones(whiles[5].rules)
        self._vm.append("goto WHILE-EXP"+str(n))
        self._vm.append("label WHILE-END"+str(n))

    def escribe_do(self, do):
        if do[1].cat == "subroutine":
            par=self._subrutinas[do[1].value][-1]
            
            print(self._subrutinas[do[1].value][0] )
            
            if self._subrutinas[do[1].value][0] == "method":
                self._vm.append("push pointer 0")
                par=par + 1
            self.escribe_lista_expresiones(do[3].rules)
            self._vm.append(f"call {self._clase}.{do[1].value} {par -1 }")
            self._vm.append("pop temp 0")
        elif do[1].cat == "class":
            self.escribe_lista_expresiones(do[5].rules)
            self._vm.append(
                f"call {do[1].value}.{do[3].value} {(len(do[5].rules)+1)//2}")
            self._vm.append("pop temp 0")
        else:
            self._vm.append(f"push {do[1].cat} {do[1].ind}")
            self.escribe_lista_expresiones(do[5].rules)
            self._vm.append(
                f"call {do[1].tipo_dato}.{do[3].value} {(len(do[5].rules)+1)//2}")
            self._vm.append("pop temp 0")

    def escribe_return(self, returns):
        if len(returns) == 2:
            self._vm.append("push constant 0")
        elif returns[1].value == 'this':
            self._vm.append("push pointer 0")
        else:
            self.escribe_expresion(returns[1].rules)
        self._vm.append("return")

    def escribe_lista_expresiones(self, lista):
        if len(lista) > 0:
            self.escribe_expresion(lista[0].rules)
            for ind in range(2, len(lista), 2):
                self.escribe_expresion(lista[ind].rules)

    def escribe_expresion(self, exp):
        self.escribe_termino(exp[0].rules)
        for ind in range(2, len(exp), 2):
            self.escribe_termino(exp[ind].rules)
            self._vm.append(self._op(exp[ind-1].value))

    def escribe_termino(self, term):
        tok1=term[0]
        if tok1.lex_type == "integerConstant":
            self._vm.append(f"push constant {tok1.value}")
        elif tok1.lex_type == "stringConstant":
            self._vm.append(f"push constant {len(tok1.value)}")
            self._vm.append("call String.new 1")
            for c in tok1.value:
                self._vm.append(f"push constant {ord(c)}")
                self._vm.append(f"call String.appendChar 2")
        elif tok1.value == "true":
            self._vm.append("push constant 0")
            self._vm.append("not")
        elif tok1.value == "false":
            self._vm.append("push constant 0")
        elif tok1.value == "null":
            self._vm.append("push constant 0")
        elif tok1.value == "this":
            self._vm.append("push pointer 0")
        elif tok1.value == "(":
            self.escribe_expresion(term[1].rules)
        elif tok1.lex_type == "symbol":
            self.escribe_termino(term[1].rules)
            self._vm.append(self._un(tok1.value))
        elif tok1.cat == "subroutine":
            if self._subrutinas[term[0].value][0] == "method":
                self._vm.append("push pointer 0")
            self.escribe_lista_expresiones(term[2].rules)
            self._vm.append(
                f"call {self._clase}.{term[0].value} {self._subrutinas[term[0].value][-1]}")
            if self._subrutinas[term[0].value][0] != "method":
                self._vm.append("pop temp 0")
        elif tok1.cat == "class":
            self.escribe_lista_expresiones(term[4].rules)
            self._vm.append(
                f"call {term[0].value}.{term[2].value} {(len(term[4].rules)+1)//2}")
            # self._vm.append("pop temp 0")
        elif tok1.cat == "pointer" and len(term) == 6:
            self._vm.append(f"push {tok1.cat} {tok1.ind}")
            self.escribe_lista_expresiones(term[4].rules)
            self._vm.append(
                f"call corregir.{term[2].value} {(len(term[4].rules)+1)//2}")
        elif len(term) == 4:
            self.escribe_expresion(term[2].rules)
            self._vm.append(f"push {tok1.cat} {tok1.ind}")
            self._vm.append("add")
            self._vm.append("pop pointer 1")
            self._vm.append("push that 0")
        else:
            self._vm.append(f"push {tok1.cat} {tok1.ind}")

    def _op(self, operador):
        oper={'+': "add", '-': "sub", '*': "call Math.multiply 2",
                '/': "call Math.divide  2", '&': "and", '|': "or", '<': "lt", '>': "gt", '=': "eq"}
        return oper[operador]

    def _un(self, operador):
        ops={'-': "neg", '~': "not"}
        return ops[operador]

# Dada una ruta dada
# Realiza su traducción
def main():
    path=sys.argv[1]
    vm=codeGenerator(path)
    vm.generar()
    vm.write()

    return 0


if __name__ == "__main__":
    main()
