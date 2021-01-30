import sys
import os
from utils.arithmetic import *
from utils.branching import *
from utils.functions import *

# Diccionario de reemplazo de simbolos
symbols = {
    "local": "LCL",
    "argument": "ARG",
    "pointer": "3",
    "this": "THIS",
    "that": "THAT",
    "temp": "5",
}

# Dicionario con las funciones de traduccion
# de comandos aritmeticos
arithmetic = {
    "add": add,
    "sub": sub,
    "eq": eq,
    "neg": neg,
    "gt": gt,
    "lt": lt,
    "and": And,
    "or": Or,
    "not": Not,
}

branching = {
    "label": label,
    "goto": goto,
    "if-goto": if_goto,
}

functions = {
    "function": def_function,
    "call": call_function,
    "return": return_,
}


def incrementor():
    info = {"count": -1}

    def number():
        info["count"] += 1
        return info["count"]

    return number


def clear_line(i):
    # Remueve lineas que comiencen con comentarios
    i = ('' if i[0:2] == '//' else i)
    i = i.replace('\n', '')  # Remueve saltos de linea
    # Remueve comentarios en lineas de codigo
    i = (i.split('//')[0] if i != '' else i)
    return i


def clear_file(lines):
    # limpiamos todas las lineas del archivo
    lines = [clear_line(i) for i in lines]
    lines = [i for i in lines if '' != i]
    return lines

# Traduccion de instruccion: push constant i


def constant(i):
    line = [
        "@" + i,
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1"
    ]
    return line

# Traduccion de instruccion: push/pop static i


def static(i, j, fname):
    if j == 0:
        line = [
            "@" + fname+"." + i,
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    else:
        line = [
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@" + fname+"." + i,
            "M=D"
        ]
        pass
    return line

# Traduccion de instruccion: push/pop symbols[s] i


def memorySegments(s, i, j):
    if j == 0:
        line = [
            "@" + symbols[s],
            "D=M",
            "@" + i,
            "A=A+D",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    else:
        line = [
            "@" + symbols[s],
            "D=M",
            "@" + i,
            "D=A+D",
            "@R13",
            "M=D",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@R13",
            "A=M",
            "M=D"
        ]
    return line

# Traduccion de instruccion: push/pop pointer/temp i


def pointerTemp(s, i, j):
    if j == 0:
        line = [
            "@" + symbols[s],
            "D=A",
            "@" + i,
            "A=A+D",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    else:
        line = [
            "@" + symbols[s],
            "D=A",
            "@" + i,
            "D=A+D",
            "@R13",
            "M=D",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@R13",
            "A=M",
            "M=D"
        ]
    return line

# Si la funcion es push, traducimos dependiendo de memorysegment respectivo


def push(args, fname):
    if args[0] in ["constant"]:
        return constant(args[1])
    if args[0] in ["local", "argument", "this", "that"]:
        return memorySegments(args[0], args[1], 0)
    if args[0] in ["temp", "pointer"]:
        return pointerTemp(args[0], args[1], 0)
    if args[0] in ["static"]:
        return static(args[1], 0, fname)
    return args

# Si la funcion es pop, traducimos dependiendo del memorysegment respectivo


def pop(args, fname):
    if args[0] in ["local", "argument", "this", "that"]:
        return memorySegments(args[0], args[1], 1)
    if args[0] in ["temp", "pointer"]:
        return pointerTemp(args[0], args[1], 1)
    if args[0] in ["static"]:
        return static(args[1], 1, fname)
    return args


def error(iarith):
    return ["error"]
# Traduce la linea ingresada, identifica si es intruccion push/pop o aritmetica


def translate(line, iarith, ifunc, icall, fname):
    line = line.split(' ')

    opt = line[0]
    args = line[1:]

    if opt in ["push", "pop"]:
        line = eval(opt + "(args,fname)",
                    {"args": line[1:], "fname": fname, "push": push, "pop": pop})

    elif opt in ["label", "goto", "if-goto"]:
        line = branching.get(opt, error)(args)

    elif opt in ["function"]:
        line = functions.get(opt, error)(args, ifunc)
    elif opt in ["call"]:
        line = functions.get(opt, error)(args, icall)
    elif opt in ["return"]:
        line = functions.get(opt, error)()
    else:
        line = arithmetic.get(opt, error)(iarith)

    return line

# Funcion principal, limpia el archivo ingresado y traduce cad linea


def main():
    filename = sys.argv[1]
    tfile = []

    iarith = incrementor()
    ifunc = incrementor()
    icall = incrementor()

    if os.path.isdir(filename):
        files = [os.path.join(filename, f)
                 for f in os.listdir(filename) if f.endswith('.vm')]
        filepath = filename + "\\" + filename.split("\\")[-1] + ".asm"
        tfile += init_asm(icall)

    else:
        files = [filename]
        filepath = filename.replace('vm', 'asm')

    for file in files:


        fname = file.split("\\")[-1].split(".")[0]

        f = open(file, "r")

        lines = [i for i in f]
        lines = clear_file(lines)
        # autoincrementador para llevar conteo de los simbolos utilizados y diferenciarlos
        tlines = [translate(i, iarith, ifunc, icall, fname) for i in lines]
        tlines = [line for sublines in tlines for line in sublines]

        # for i in tlines:
        #     print(i)
        tfile += tlines

    with open(filepath, 'w') as file:
        for i in tfile:
            file.write(i + '\n')


if __name__ == "__main__":
    main()
