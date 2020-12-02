// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@status
    M=-1        // Estado=0xFFFF
    D=0         // Argumento - Configuar bits en pantalla
    @SETSCREEN
    0;JMP



(LOOP)
    @KBD
    D=M         // D = Caracter actual en el teclado
    @SETSCREEN
    D;JEQ       // Si no se presiona una tecla, configurar la pantalla con bits ceros
    D=-1        // Si se presiona una tecla, configurar la pantalla con bits 1



(SETSCREEN)     // D=Nuevo estado
    @ARG
    M=D         // Guardar nuevo esatdo
    @status     // FFFF=Negro, 0=Blanco - Estado de toda la pantalla
    D=D-M       // D=Nuevo estado
    @LOOP
    D;JEQ        // Si estado inicial es igual al anterior no hacer nada

    @ARG
    D=M
    @status
    M=D         // Estado = ARG

    @SCREEN
    D=A         // D=Dirección de pantalla
    @8192
    D=D+A       // D=Byte justo después de la última dirección de pantalla
    @i
    M=D         // i=Dirección de pantalla



(SETLOOP)
    @i
    D=M-1
    M=D         // i=i-1
    @LOOP
    D;JLT       // Si i<0 hacer una iteración

    @status
    D=M         // D=Estado
    @i
    A=M         // Indirecto
    M=D         // M[Dirección acutal de pantalla]=Estado
    @SETLOOP
    0;JMP