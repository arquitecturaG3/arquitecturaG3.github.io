NUM_SEGMENTS = 5


def push_on_stack(segment):
    line = [
        "@%s" % segment,
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
    ]
    return line


def restore_call(segment, iframe):
    line = [
        "@%s" % iframe,
        "D=A",
        "@R13",
        "A=M-D",
        "D=M",
        "@%s" % segment,
        "M=D"
    ]
    return line


def def_function(args, ifunc):
    i = ifunc()
    line = [
        "(%s)" % args[0],
        "@%s" % args[1],
        "D=A",
        "(LOOP.ADD_LOCALS.%s)" % i,
        "@NO_LOCALS.%s" % i,
        "D;JEQ",
        "@SP",
        "A=M",
        "M=0",
        "@SP",
        "M=M+1",
        "D=D-1",
        "@LOOP.ADD_LOCALS.%s" % i,
        "D;JNE",
        "(NO_LOCALS.%s)" % i
    ]

    return line


def call_function(args, icall):
    i = icall()

    line = [
        "@RET_ADDRESS.%s" % i,
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        *push_on_stack("LCL"),
        *push_on_stack("ARG"),
        *push_on_stack("THIS"),
        *push_on_stack("THAT"),
        "@SP",
        "D=M",
        "@%s" % args[1],
        "D=D-A",
        "@%s" % NUM_SEGMENTS,
        "D=D-A",
        "@ARG",
        "M=D",
        "@SP",
        "D=M",
        "@LCL",
        "M=D",
        "@%s" % args[0],
        "0;JMP",
        "(RET_ADDRESS.%s)" % i,
    ]

    return line


def return_():
    line = [
        "@LCL",
        "D=M",
        "@R13",
        "M=D",
        "@5",
        "D=A",
        "@R13",
        "A=M-D",
        "D=M",
        "@R14",
        "M=D",
        "@SP",
        "AM=M-1",
        "D=M",
        "@ARG",
        "A=M",
        "M=D",
        "@ARG",
        "D=M+1",
        "@SP",
        "M=D",
        *restore_call("THAT",1),
        *restore_call("THIS",2),
        *restore_call("ARG",3),
        *restore_call("LCL",4),
        "@R14",
        "A=M",
        "0;JMP"
    ]
    return line

def init_asm(icall):
    line = [
        "@256",
        'D=A',
        '@SP',
        'M=D'
    ]

    line += call_function(["Sys.init", "0"], icall)

    return line
