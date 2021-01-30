def label(args):
    line = ["(%s)" % args[0]]
    return line

def goto(args):
    line = [
        "@%s" % args[0],
        "0;JMP"
    ]
    return line

def if_goto(args):
    line = [
        "@SP",
        "AM=M-1",
        "D=M",
        "@%s" % args[0], 
        "D;JNE"
    ]

    return line