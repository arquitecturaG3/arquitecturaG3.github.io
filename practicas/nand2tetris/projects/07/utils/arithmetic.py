# Modulo arithmetic, funciones que traducen cada comando airtmetico
# En su respectivas intrucciones en el lenguaje ASM

def add(i):
    line = [
        # SP--
        "@SP",
        "M=M-1",
        
        "@SP",
        "A=M",
        "D=M",
        
        # SP--
        "@SP",
        "M=M-1",
        
        "@SP",
        "A=M",
        "M=M+D",
        
        # SP++
        "@SP",
        "M=M+1"
    ]    
    return line

def sub(i):
    line = [
        # SP--
        "@SP",
        "M=M-1",
        
        "@SP",
        "A=M",
        "D=M",
        
        # SP--
        "@SP",
        "M=M-1",
        
        "@SP",
        "A=M",
        "M=M-D",
        
        # SP++
        "@SP",
        "M=M+1"
    ]    
    return line

def neg(i):
    line = [
        # SP--
        "@SP",
        "M=M-1",
        
        "@SP",
        "A=M",
        "D=0",
        "M=D-M",
        
        # SP++
        "@SP",
        "M=M+1"
    ]
    return line

def eq(i):
    ci = i()
    line = [
        # SP--
        "@SP",
        "M=M-1",
        
        "@SP",
        "A=M",
        "D=M",
        
        # SP--
        "@SP",
        "M=M-1",
        
        "@SP",
        "A=M",
        "D=M-D",
        
        "@TRUE%s" % ci,
        "D;JEQ",
        "@SP",
        "A=M",
        "M=0",
        "@END%s" % ci,
        "0;JMP",
        
        "(TRUE%s)" %ci,
        "@SP",
        "A=M",
        "M=-1",
        "(END%s)" % ci,
        
        # SP++
        "@SP",
        "M=M+1"
    ]
    return line

def gt(i):
    ci = i()
    line = [
        # SP--
        "@SP",
        "M=M-1",
        
        "@SP",
        "A=M",
        "D=M",
        
        # SP--
        "@SP",
        "M=M-1",
        
        "@SP",
        "A=M",
        "D=M-D",
        "@TRUE%s" % ci,
        "D;JGT",
        
        "@SP",
        "A=M",
        "M=0",
        "@END%s" % ci,
        "0;JMP",
        
        "(TRUE%s)" % ci,        
        "@SP",
        "A=M",
        "M=-1",
        "(END%s)" % ci,
        
        # SP++
        "@SP",
        "M=M+1"        
    ]
    return line

def lt(i):
    ci = i()
    line = [
        # SP--
        "@SP",
        "M=M-1",

        "@SP",
        "A=M",
        "D=M",
        
        # SP--
        "@SP",
        "M=M-1",

        "@SP",
        "A=M",
        "D=M-D",

        "@TRUE%s" % ci,
        "D;JLT",
        "@SP",
        "A=M",
        "M=0",
        "@END%s" % ci,
        "0;JMP",

        "(TRUE%s)" % ci,
        "@SP",
        "A=M",
        "M=-1",
        "(END%s)" % ci,

        # SP++
        "@SP",
        "M=M+1"
    ]    
    return line

def And(i):
    line = [
        # SP--
        "@SP",
        "M=M-1",

        "@SP",
        "A=M",
        "D=M",

        # SP--
        "@SP",
        "M=M-1",

        "@SP",
        "A=M",
        "M=M&D",

        # SP++
        "@SP",
        "M=M+1",
    ]    
    return line
    
def Or(i):
    line = [
        # SP--
        "@SP",
        "M=M-1",

        "@SP",
        "A=M",
        "D=M",
        
        # SP--
        "@SP",
        "M=M-1",

        "@SP",
        "A=M",
        "M=M|D",

        # SP++
        "@SP",
        "M=M+1",
    ]
    return line

def Not(i):
    line = [
        # SP--
        "@SP",
        "M=M-1",

        "@SP",
        "A=M",
        "M=!M",
        
        # SP++
        "@SP",
        "M=M+1", 
    ]
    return line