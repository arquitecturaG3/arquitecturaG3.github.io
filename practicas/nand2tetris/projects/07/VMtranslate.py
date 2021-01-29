import sys
from utils.arithmetic import *

symbols = {
    "local": "LCL",
    "argument": "ARG",
    "pointer": "3",
    "this": "THIS",
    "that": "THAT",
    "temp": "5",
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

def static(i,j):
    name = sys.argv[1].split("\\")[2].split(".")[0]
    if j==0:
        line = [
            "@"+name+"." + i,
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
            "@"+name+"." + i,
            "M=D"
        ]
        pass
    return line

def memorySegments(s, i, j):
    if j==0:
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

def pointerTemp(s, i, j):
    if j==0:
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

def push(args):
    if args[0] in ["constant"]:
        return constant(args[1])
    if args[0] in ["local", "argument","this","that"]:
        return memorySegments(args[0], args[1], 0)
    if args[0] in ["temp", "pointer"]:
        return pointerTemp(args[0], args[1], 0)
    if args[0] in ["static"]:
        return static(args[1], 0)
    return args


def pop(args):
    if args[0] in ["local", "argument","this","that"]:
        return memorySegments(args[0], args[1], 1)
    if args[0] in ["temp", "pointer"]:
        return pointerTemp(args[0], args[1], 1)
    if args[0] in ["static"]:
        return static(args[1], 1)
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