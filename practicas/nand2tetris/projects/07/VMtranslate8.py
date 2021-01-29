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
def labelFuncion(s):
    line = [
        "(" + s +")"
    ]
    return line

def goto(s):
    line = [
        "@"+ s,
        "0;JPM"
    ]
    return line

def ifGoto(s):
    line = [
        "@SP"+ s,
        "AM=M-1",
        "D=M", 
        "M=0", 
        "@X",
        "D;JNE"
    ]
    return line

def FunReturn():
    line = [
        "@LCL",
	    "D=M",
	    "@FRAME",
	    "M=D",
	   " @5",
	    "D=D-A",
	    "A=D",
	    "D=M",
	    "@RETURN",
	    "M=D",
	    "@SP",
	    "A=M-1",
	    "D=M",
	    "@ARG",
	    "A=M",
	    "M=D",
	    "@ARG",
	    "D=M",
	    "@SP",
	    "M=D+1",
	    "@FRAME",
	    "AM=M-1",
	    "D=M",
	    "@THAT",
	    "M=D",
	    "@FRAME",
	    "AM=M-1",
	    "D=M",
	    "@THIS",
	    "M=D",
	    "@FRAME",
	    "AM=M-1",
	    "D=M",
	    "@ARG",
	    "M=D",
	    "@FRAME",
	    "AM=M-1",
	    "D=M",
	    "@LCL",
	    "M=D",
	    "@RETURN",
	    "A=M",
	    "0;JMP"
    ]
    return line

def call(s):
    line = [
        "@Return_FUNC_"+s,
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@LCL",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
                                    
        "@ARG",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
                                    
        "@THIS",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
                                    
        "@THAT",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
                                    
        "@SP",
        "D=M",
        "@N_ARG",
        "D=D-A",
        "@5",
        "D=D-A",
        "@ARG",
        "M=D",
                                    
        "@SP",
        "D=M",
        "@LCL",
        "M=D",
                                    
        "@_FUNC",
        "0;JMP",
        "(Return_FUNC_"+s+")"
    ]
    return line

    

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
        
    elif opt in ["label","funcion"]:
        line = labelFuncion(line[1])

    elif opt in ["goto"]:
        line = goto(line[1])

    elif opt in ["if-goto"]:
        line = ifGoto(line[1])

    elif opt in ["return"]:
        line = FunReturn()

    elif opt in ["call"]:
        line = call(line[1])

    #else:
        #line = arithmetic.get(opt, "error")(iarith)

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