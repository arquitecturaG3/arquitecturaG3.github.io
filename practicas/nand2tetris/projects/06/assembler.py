import sys

def comp(cadena):
    dic = {
    '0': [0, 1, 0, 1, 0, 1, 0], 
    '1': [0, 1, 1, 1, 1, 1, 1], 
    '-1': [0, 1, 1, 1, 0, 1, 0], 
    'D': [0, 0, 0, 1, 1, 0, 0], 
    'A': [0, 1, 1, 0, 0, 0, 0], 
    '!D': [0, 0, 0, 1, 1, 0, 1], 
    '!A': [0, 1, 1, 0, 0, 0, 1], 
    '-D': [0, 0, 0, 1, 1, 1, 1], 
    '-A': [0, 1, 1, 0, 0, 1, 1], 
    'D+1': [0, 0, 1, 1, 1, 1, 1], 
    'A+1': [0, 1, 1, 0, 1, 1, 1], 
    'D-1': [0, 0, 0, 1, 1, 1, 0], 
    'A-1': [0, 1, 1, 0, 0, 1, 0], 
    'D+A': [0, 0, 0, 0, 0, 1, 0], 
    'D-A': [0, 0, 1, 0, 0, 1, 1], 
    'A-D': [0, 0, 0, 0, 1, 1, 1], 
    'D&A': [0, 0, 0, 0, 0, 0, 0], 
    'D|A': [0, 0, 1, 0, 1, 0, 1], 
    'M': [1, 1, 1, 0, 0, 0, 0], 
    '!M': [1, 1, 1, 0, 0, 0, 1], 
    '-M': [1, 1, 1, 0, 0, 1, 1], 
    'M+1': [1, 1, 1, 0, 1, 1, 1], 
    'M-1': [1, 1, 1, 0, 0, 1, 0], 
    'D+M': [1, 0, 0, 0, 0, 1, 0], 
    'D-M': [1, 0, 1, 0, 0, 1, 1], 
    'M-D': [1, 0, 0, 0, 1, 1, 1], 
    'D&M': [1, 0, 0, 0, 0, 0, 0], 
    'D|M': [1, 0, 1, 0, 1, 0, 1]}
    return dic[cadena]

def compDest(inDest): #metodo dest
    Dest = {'None': [0,0,0], 
           'M':[0,0,1], 
           'D':[0,1,0], 
           'MD':[0,1,1], 
           'A':[1,0,0], 
           'AM':[1,0,1], 
           'AD':[1,1,0], 
           'AMD':[1,1,1] }
    return Dest[inDest]
print(compDest("MD"))

def jump_comp(jump): #funcion para definir el jump
    jumps= {'None': [0,0,0], 
    'JGT':[0,0,1],
    'JEQ':[0,1,0],
    'JGE':[0,1,1],
    'JLT':[1,0,0], 
    'JNE':[1,0,1],
    'JLE':[1,1,0],
    'JMp':[1,1,1]}
    return jumps[jump]


def clear_file(lines):
    lines = [  ( '' if i[0:2] == '//' else i) for i in lines ]
    lines = [ i.replace('\n','') for i in lines]
    lines = [ i for i in lines if '' != i ]
    return lines

def print_file(lines):
    for i in lines:
        print(i)

def main():
    filename = sys.argv[1]   

    f = open(filename, "r")
    lines = [ i for i in f]

    print('----------ARCHIVO ORIGINAL----------')
    print_file(lines)
    lines = clear_file(lines)

    print('----------ARCHIVO LIMPIO----------')
    print_file(lines)
    

if __name__ == "__main__":
    main()              
