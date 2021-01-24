import sys

symbols = {   
    "local":"LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",   
    
}


def clear_line(i):
    i = ('' if i[0:2] == '//' else i)        # Remueve lineas que comiencen con comentarios 
    i = i.replace('\n','')                   # Remueve saltos de linea               
    i = (i.split('//')[0] if i != '' else i) # Remueve comentarios en lineas de codigo
    return i

def clear_file(lines):
    lines = [  clear_line(i) for i in lines ]  # limpiamos todas las lineas del archivo
    lines = [ i for i in lines if '' != i]   
    return lines

def constant(i):
    line = [
        "@" + i ,
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

def add():
    line = [
        "@SP",
        "M=M-1",
        "@SP",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "@SP",
        "A=M",
        "M=M+D",
        "@SP",
        "M=M+1"
    ]    
    return line


aritmetic = {
    "add": add    
}
    

def translate(line): 
    line = line.split(' ')
    
    opt = line[0]
    if opt in ["push","pop"]:
        line= eval(opt + "(args)", {"args":line[1:], "push":push ,"pop":pop})
    else:
        line = aritmetic.get(opt, "error")()
    
    return line


def main():
    filename = sys.argv[1]   
    filepath = filename.replace('vm','asm')    
    f = open(filename, "r")
    
    lines = [ i for i in f]   
    lines = clear_file(lines)
        
        
    tlines = [ translate(i)  for i in lines]
    tlines = [ line for sublines in tlines for line in sublines]
    
    for i in tlines: 
        print(i)
    
    with open(filepath, 'w') as file:
        for i in tlines:
            file.write(i + '\n')


if __name__ == "__main__":
    main()     