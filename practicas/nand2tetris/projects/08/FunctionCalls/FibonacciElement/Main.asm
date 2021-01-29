function
Main.fibonacci
0
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
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
lt





















@SPIF_TRUE
AM=M-1
D=M
M=0
@X
D;JNE
@IF_FALSE
0;JPM
(IF_TRUE)
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
(IF_FALSE)
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
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
sub
@Return_FUNC_Main.fibonacci
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@N_ARG
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@_FUNC
0;JMP
(Return_FUNC_Main.fibonacci)
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
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
sub
@Return_FUNC_Main.fibonacci
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@N_ARG
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@_FUNC
0;JMP
(Return_FUNC_Main.fibonacci)
add




















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
