import sys
from utils.arithmetic import *

symbols = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}

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


def incrementor():
    info = {"count": -1}

    def number():
        info["count"] += 1
        return info["count"]

    return number


def clear_line(i):
    i = ('' if i[0:2] == '//' else i)  # Remueve lineas que comiencen con comentarios
    i = i.replace('\n', '')  # Remueve saltos de linea
    i = (i.split('//')[0] if i != '' else i)  # Remueve comentarios en lineas de codigo
    return i


def clear_file(lines):
    lines = [clear_line(i) for i in lines]  # limpiamos todas las lineas del archivo
    lines = [i for i in lines if '' != i]
    return lines


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


def push(args):
    if args[0] in ["constant"]:
        return constant(args[1])

    return args


def pop(args):
    return args


def translate(line, iarith):
    line = line.split(' ')

    opt = line[0]
    if opt in ["push", "pop"]:
        line = eval(opt + "(args)", {"args": line[1:], "push": push, "pop": pop})
    else:
        line = arithmetic.get(opt, "error")(iarith)

    return line


def main():
    filename = sys.argv[1]
    filepath = filename.replace('vm', 'asm')
    f = open(filename, "r")

    lines = [i for i in f]
    lines = clear_file(lines)

    iarith = incrementor()
    tlines = [translate(i, iarith) for i in lines]
    tlines = [line for sublines in tlines for line in sublines]

    for i in tlines:
        print(i)

    with open(filepath, 'w') as file:
        for i in tlines:
            file.write(i + '\n')


if __name__ == "__main__":
    main()
