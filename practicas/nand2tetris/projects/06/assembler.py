import sys
  
"""
Ensamblador implementado en python el cual
traduce programas escritos en el lenguaje
simbolico de ensamblador Hack Languaje
a codigo binario

Intrucciones de ejecucion:

Para traducir un archivo file.asm ejecute la
siguiente estructura de comando en consola

> python assembler.py route/to/file.asm

El programa leera el archivo indicado en la ruta
como argumento y escribira un archivo con el mismo
nombre con extension .hack este contendra 
la traduccion a codigo binario

Nota: El comando debe ser ejecutado dentro de la carpeta
que contenga el archivo assembler.py

"""    


def getBinario15(p):
    binario = bin(int(p))[2:]    
    numBin = [ int(i) for i in binario]
    return numBin


def comp(input):
    comp_dict = {
    '0':   [0, 1, 0, 1, 0, 1, 0], 
    '1':   [0, 1, 1, 1, 1, 1, 1], 
    '-1':  [0, 1, 1, 1, 0, 1, 0], 
    'D':   [0, 0, 0, 1, 1, 0, 0], 
    'A':   [0, 1, 1, 0, 0, 0, 0], 
    '!D':  [0, 0, 0, 1, 1, 0, 1], 
    '!A':  [0, 1, 1, 0, 0, 0, 1], 
    '-D':  [0, 0, 0, 1, 1, 1, 1], 
    '-A':  [0, 1, 1, 0, 0, 1, 1], 
    'D+1': [0, 0, 1, 1, 1, 1, 1], 
    'A+1': [0, 1, 1, 0, 1, 1, 1], 
    'D-1': [0, 0, 0, 1, 1, 1, 0], 
    'A-1': [0, 1, 1, 0, 0, 1, 0], 
    'D+A': [0, 0, 0, 0, 0, 1, 0], 
    'D-A': [0, 0, 1, 0, 0, 1, 1], 
    'A-D': [0, 0, 0, 0, 1, 1, 1], 
    'D&A': [0, 0, 0, 0, 0, 0, 0], 
    'D|A': [0, 0, 1, 0, 1, 0, 1], 
    'M':   [1, 1, 1, 0, 0, 0, 0], 
    '!M':  [1, 1, 1, 0, 0, 0, 1], 
    '-M':  [1, 1, 1, 0, 0, 1, 1], 
    'M+1': [1, 1, 1, 0, 1, 1, 1], 
    'M-1': [1, 1, 1, 0, 0, 1, 0], 
    'D+M': [1, 0, 0, 0, 0, 1, 0], 
    'D-M': [1, 0, 1, 0, 0, 1, 1], 
    'M-D': [1, 0, 0, 0, 1, 1, 1], 
    'D&M': [1, 0, 0, 0, 0, 0, 0], 
    'D|M': [1, 0, 1, 0, 1, 0, 1]}
    return comp_dict[input]

def dest(input): #metodo dest
    dest_dict = {'': [0,0,0], 
    'M'  :[0,0,1], 
    'D'  :[0,1,0], 
    'MD' :[0,1,1], 
    'A'  :[1,0,0], 
    'AM' :[1,0,1], 
    'AD' :[1,1,0], 
    'AMD':[1,1,1] }
    return dest_dict[input]


def jump(input): #funcion para definir el jump
    jump_dict= {'': [0,0,0], 
    'JGT':[0,0,1],
    'JEQ':[0,1,0],
    'JGE':[0,1,1],
    'JLT':[1,0,0], 
    'JNE':[1,0,1],
    'JLE':[1,1,0],
    'JMP':[1,1,1]}          
    return jump_dict[input]


def clear_line(i):
    i = ('' if i[0:2] == '//' else i)   
    i = i.replace('\n','')
    i = i.replace(' ' ,'')
    i = (i.split('//')[0] if i != '' else i)
    return i


def clear_file(lines):
    symbols = {        
    }    
    _ = [ symbols.update({'R'+str(i) : i }) for i in range(16)]
    names = ['SCREEN','KBD','SP','LCL','ARG','THIS','THAT']
    values =    [16384,24576,0,1,2,3,4]    
    _ = [ symbols.update({i:j}) for i,j in zip(names,values)]     
         
    lines = [  clear_line(i) for i in lines ]
    lines = [ i for i in lines if '' != i]   
    
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
    
    lines = [ ( '@' + str(symbols[i[1:]]) if i[0] == '@' and i[1:]  in symbols.keys() else i) for i in lines ]    
    
    variables = []    
    variables =  [ i[1:] for i in lines if i[0] == '@' and  not i[1:].isnumeric() ]  
    variables = list(dict.fromkeys(variables))    
        
    indices = list(range(16, 16+len(variables)))     
    _ = [ symbols.update({i:j}) for i,j in zip(variables,indices)]     
    lines = [ ( '@' + str(symbols[i[1:]])  if  i[0] == '@' and  not i[1:].isnumeric() else i ) for i in lines  ]      
    return lines

def print_file(lines):
    for i in lines:
        print(i)
     
        
def toA(x):
    x = int(x[1:len(x)])
    final = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    binario = getBinario15(x)
    final[-len(binario):] = binario
    return final


def toC(x):
    dest_str = None
    comp_str = None
    jump_str = None
        
    dest_str , rest = ( x.split('=') if '=' in x else ('' , x) )
    comp_str , jump_str = ( rest.split(';') if ';' in rest else (rest,'') )    
    line = [1,1,1] + comp(comp_str) + dest(dest_str) + jump(jump_str)    
    return line


def translate(i):
    line = None
    
    if i[0] == '@':
        line = toA(i)
    else:
        line = toC(i)       
    
    line = ''.join( [str(j) for j in line ] )    
    return line


def main():
    filename = sys.argv[1]   
    filepath = filename.replace('asm','hack')
    print(filepath)

    f = open(filename, "r")
    lines = [ i for i in f]
    lines = clear_file(lines)

    print('----------ARCHIVO LIMPIO----------')
    print_file(lines)
    print('----------ARCHIVO TRADUCIDO----------')
    
    tlines = [ translate(i) for i in lines ]    
    
    for i in tlines:
        print(i)
        
    with open(filepath, 'w') as file:
        for i in tlines:
            file.write(i + '\n')

if __name__ == "__main__":
    main()              
