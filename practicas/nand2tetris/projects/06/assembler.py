import sys

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