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
    'JMP':[1,1,1]}
    return jumps[jump]


def clear_file(lines):
    symbols = {        
    }    
    _ = [ symbols.update({'R'+str(i) : i }) for i in range(16)]
    names = ['SCREEN','KBD','SP','LCL','ARG','THIS','THAT']
    values = [16384,24576,0,1,2,3,4]    
    _ = [ symbols.update({i:j}) for i,j in zip(names,values)]          
    lines = [  ( '' if i[0:2] == '//' else i) for i in lines ]
    lines = [ i.replace('\n','') for i in lines]    
    lines = [ i.replace(' ' ,'') for i in lines]
    lines = [ i.split('//')[0] for i in lines if '' != i]
    cant = 0    
    temp = []
    for i,j in zip(lines,range(len(lines))):
        if i[0] + i[-1] == '()':
            symbols[i[1:-1]] = j - cant
            cant += 1     
        else:
            temp.append(i)     
    lines = temp
    del temp
    del cant
    print(symbols)
    lines = [ ( '@' + str(symbols[i[1:]]) if i[0] == '@' and i[1:]  in symbols.keys() else i) for i in lines ]
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
