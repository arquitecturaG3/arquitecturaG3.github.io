(Class2.set)
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@StaticsTest.0
M=D
@ARG
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@StaticsTest.1
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@FRAME
M=D
 @5
D=D-A
A=D
D=M
@RETURN
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME
AM=M-1
D=M
@THAT
M=D
@FRAME
AM=M-1
D=M
@THIS
M=D
@FRAME
AM=M-1
D=M
@ARG
M=D
@FRAME
AM=M-1
D=M
@LCL
M=D
@RETURN
A=M
0;JMP
(Class2.get)
@StaticsTest.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@StaticsTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1
sub
@LCL
D=M
@FRAME
M=D
 @5
D=D-A
A=D
D=M
@RETURN
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@FRAME
AM=M-1
D=M
@THAT
M=D
@FRAME
AM=M-1
D=M
@THIS
M=D
@FRAME
AM=M-1
D=M
@ARG
M=D
@FRAME
AM=M-1
D=M
@LCL
M=D
@RETURN
A=M
0;JMP
