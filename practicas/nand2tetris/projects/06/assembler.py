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


# funcion comp, retorna en binario
# el codigo correspondiente a la
# operacion indicada
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

# Funcion jump, retorna en binario
# el codigo correspondiente a la condicion
# jump indicada
def jump(input): 
    jump_dict= {'': [0,0,0], 
    'JGT':[0,0,1],
    'JEQ':[0,1,0],
    'JGE':[0,1,1],
    'JLT':[1,0,0], 
    'JNE':[1,0,1],
    'JLE':[1,1,0],
    'JMP':[1,1,1]}          
    return jump_dict[input]

# Funcion clear_line, sera usada
# en la Funcion clear_file para
# limpiar cada linea de forma indpendiente
def clear_line(i):
    i = ('' if i[0:2] == '//' else i)        # Remueve lineas que comiencen con comentarios 
    i = i.replace('\n','')                   # Remueve saltos de linea
    i = i.replace(' ' ,'')                   # Remuve espacios en blanco
    i = (i.split('//')[0] if i != '' else i) # Remueve comentarios en lineas de codigo
    return i


# Funcion clear_file, retorna el archivo
# limpio, y sin simbolos, esta dividio en:
def clear_file(lines):
    
    # Creamos el diccionario symbols en donde almacenamidos los simbolos predefinidos
    symbols = {        
    }    
    _ = [ symbols.update({'R'+str(i) : i }) for i in range(16)]
    names = ['SCREEN','KBD','SP','LCL','ARG','THIS','THAT']
    values =    [16384,24576,0,1,2,3,4]    
    _ = [ symbols.update({i:j}) for i,j in zip(names,values)]     
         
   
    lines = [  clear_line(i) for i in lines ]  # limpiamos todas las lineas del archivo
    lines = [ i for i in lines if '' != i]     # eliminamos lineas vacias
    
    # Agregamos al diccionario symbols los labels symbols
    # A su vez lo removemos del las lineas que componen el archivo
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
    
    # Remplazamos el label symbols por su valor respectivo
    lines = [ ( '@' + str(symbols[i[1:]]) if i[0] == '@' and i[1:]  in symbols.keys() else i) for i in lines ]    
    
    # Agregamos las variable @nombre_variable al diccionario symbols
    variables =  [ i[1:] for i in lines if i[0] == '@' and  not i[1:].isnumeric() ]  
    variables = list(dict.fromkeys(variables))            
    indices = list(range(16, 16+len(variables)))     
    _ = [ symbols.update({i:j}) for i,j in zip(variables,indices)]     
    
    # Reemplazamos las variables por su valor respectivo
    lines = [ ( '@' + str(symbols[i[1:]])  if  i[0] == '@' and  not i[1:].isnumeric() else i ) for i in lines  ]      
    
    return lines


# Funcion para imprimir el archivo linea por linea en consola
def print_file(lines):
    for i in lines:
        print(i)

# Funcion getBinario15, retorna
# un arreglo de enteros en binario la entrada p
def getBinario15(p):
    binario = bin(int(p))[2:]    
    numBin = [ int(i) for i in binario]
    return numBin

# Funcion toA, retorna en binario la intruccion A
# de la forma @value como un vector de 16 posiciones
def toA(x):
    x = int(x[1:len(x)])
    final = [0]*16
    binario = getBinario15(x)
    final[-len(binario):] = binario
    return final

# Funcion toC, retorna en binario la intruccion C
# de la forma dest = comp ; jump
def toC(x):
    dest_str = None
    comp_str = None
    jump_str = None
        
    # Asignacion de la parte dest, si no hay igual (=) 
    # dest es igual a vacio
    dest_str , rest = ( x.split('=') if '=' in x else ('' , x) )
    
    # Asignacion de la parte comp y jump
    # si no hay punto y coma (;) jump es vacio 
    comp_str , jump_str = ( rest.split(';') if ';' in rest else (rest,'') ) 
    
    # Creamos el arreglo de 16 posiciones el cual contendra la traduccion
    # de la entrada x, de la forma:
    # [1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3]    
    line = [1,1,1] + comp(comp_str) + dest(dest_str) + jump(jump_str)    
    return line

# Funcion translate
# traduce la entrada i, identificando si es
# una intruccion A o C
def translate(i):
    line = None
    
    if i[0] == '@':
        line = toA(i)
    else:
        line = toC(i)       
    
    # Una vez se retorna el arreglo de 16 posiciones
    # lo convertimos en un string de 16 posiciones
    line = ''.join( [str(j) for j in line ] )    
    return line

# Funcion main, se autoejecuta cuando es llamada
# desde la linea de comando, lee el argumento proporcionado
# el cual contendra la ruta del archivo file.asm a traducir
def main():
    filename = sys.argv[1]   
    filepath = filename.replace('asm','hack')
    print(filepath)
    
    # leemos el archivo y lo guardamos en un vector
    # donde cada posicion es una linea del archivo
    f = open(filename, "r")
    lines = [ i for i in f]                  
    lines = clear_file(lines)                 # limpiamos el archivo
    tlines = [ translate(i) for i in lines ]  # lo traducimos a binario

    # Muestra en consola el archivo en limpio
    print('----------ARCHIVO LIMPIO----------')
    print_file(lines)
    # Muestra en consola el archivo traducido
    print('----------ARCHIVO TRADUCIDO----------')       
    print_file(tlines)
        
    # Guardamos el archivo como filename.hack linea por linea
    with open(filepath, 'w') as file:
        for i in tlines:
            file.write(i + '\n')

if __name__ == "__main__":
    main()              
