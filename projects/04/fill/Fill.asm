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

  @filled
  M=0
(MAIN_LOOP)
  @KBD
  D=M

  @FILL_SCREEN
  D; JNE
  (FILL_SCREEN_CALL)
  @KBD
  D=M
  @MAIN_LOOP_END
  D; JNE

  @CLEAN
  0; JMP
  (CLEAN_CALL)

  (MAIN_LOOP_END)
  @MAIN_LOOP
  0; JMP


(FILL)  // R0 - return address, R1 - value for filling
  @SCREEN
  D=A
  @address
  M=D
  @KBD
  D=A
  @last_address
  M=D  
  (FILL_LOOP)
    @last_address
    D=M
    @address
    D=D-M
    @FILL_LOOP_END
    D; JEQ

    @R1
    D=M
    @address
    A=M
    M=D
    @address
    M=M+1

    @FILL_LOOP
    0; JMP    
  (FILL_LOOP_END)
  @R0
  A=M
  0; JMP


(CLEAN)
  @filled
  D=M
  @CLEAN_RETURN
  D; JEQ                // If filled==0 then return

  @filled
  M=0
  @R1
  M=0
  @FILL_CALL_FOR_CLEAN
  D=A
  @R0
  M=D

  @FILL
  0; JMP
  (FILL_CALL_FOR_CLEAN)

  (CLEAN_RETURN)
  @CLEAN_CALL
  0; JMP


(FILL_SCREEN)
  @filled
  D=M
  @FILL_SCREEN_RETURN
  D; JGT

  @filled
  M=1
  @R1
  M=-1
  @FILL_CALL
  D=A
  @R0
  M=D

  @FILL
  0; JMP
  (FILL_CALL)

  (FILL_SCREEN_RETURN)
  @FILL_SCREEN_CALL
  0; JMP

