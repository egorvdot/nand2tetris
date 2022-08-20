// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

  @R2
  M=0     // Multiplication result

  @R0
  D=M
  @END
  D; JEQ  // If R0==0 then JUMP to END

  @R1
  D=M
  @END
  D; JEQ  // If R1==0 then JUMP to END

  @i
  M=0
(LOOP)
  @i
  D=M
  @R1
  D=M-D   // D=R1-i
  @END
  D; JEQ  // if R1-i == 0 then END

  @R0
  D=M
  @R2
  M=M+D

  @i
  M=M+1   // i++
  @LOOP
  0; JMP

(END)
  @END
  0; JMP

