
# Two-Pass Assembler - Computer Organization (CSE 112) Project 1
The following Python program (`assm.py`) implements a 12 Bit architecture, two-pass assembler for Computer Organization Project up to the specifications required.
Team Members: 
1. Rohan Dhar        - Roll No: 2019443
2. Shabeg Singh Gill - Roll No: 20193

## Installation and Usage
The assembler is built in Python 3.0. To run it, Python 3.0 or any newer variant of Python must be installed on the system.

### Steps to Install
1. Download the file `assm.py` to a directory where your user has **read and write** privileges (like the Desktop) or alternatively, run `git clone https://github.com/rohan-dhar/co-assm` if GIT CLI is installed on the system.

2. Open terminal (on linux / macOS) / Command Prompt (on Windows) and navigate to the folder where the `assm.py` is located.

3. Create an assembly file / copy an existing assembly file to the folder where the Assembler is. An assembly file can have any extension (.txt , .asm etc.)

4. Run `python3 assm.py` to start the assembler.

5. You will be prompted to enter the file name of the assembly file, give the name of your assembly file. (including the extension, eg: test.asm);

6. If the assembly code is valid, a success message will be displayed and the binary code generated will be put in a file named `fileName.bin` where fileName was the original of the assembly file without the extension. Eg: `test.asm` will be assembled to `test.bin`.

7. If there are any errors or warnings (discussed later) , they will be displayed on the screen AND logged to a file called messsages.log in the same folder as the assmebler, for future reference. The log will also contain the date & time when the error occured. In case the assembly code could not be assembled (due to a fatal error), no binary file will be created.



## Supported Opcodes And Operations
1. `CLA`: Clears accumulator
	Takes 0 operands

2. `LAC`: Load accumulator from memory
	Takes 1 operands - The Symbol / Literal for the memory address.

3. `SAC`: Store Accumulator Contents to memory
	Takes 1 operands - The Symbol / Literal for the memory address.

4. `ADD`: Adds Memory address contents to Accumulator
	Takes 1 operands - The Symbol / Literal for the memory address.

5. `SUB`: Subtracts Memory address contents to Accumulator
	Takes 1 operands - The Symbol / Literal for the memory address.

6. `MUL`: Multiplies Accumulator value by the contents of the given Memory address
	Takes 1 operands - The Symbol / Literal for the memory address.

7. `DIV`: Divides Accumulator value by the contents of the given Memory address
	Takes 1 operands - The Symbol / Literal for the memory address.

8. `BRZ`: Branches to given Address if Accumulator has a positive value
	Takes 1 operands - The Symbol / Literal for the memory address.

9. `BRN`: Branches to given Address if Accumulator has a negative value
	Takes 1 operands - The Symbol / Literal for the memory address.

10. `BRP`: Branches to given Address if Accumulator has ZERO
	Takes 1 operands - The Symbol / Literal for the memory address.

11. `INP`: Inputs data to the given memory location
	Takes 1 operands - The Symbol / Literal for the memory address.

12. `DSP`: Displays data at the given memory location
	Takes 1 operands - The Symbol / Literal for the memory address.

13. `STP`: Stops execution
	Takes 0 Operands

14. `START`: Assembler Directive at the start of the code.
	Can be optionally followed by a Number indicating the memory location where the program should start. If the start location is not given, the program starts at 0 by default and a warning is generated at the time of assembly.

15. `END`: Assembler Directive denoting the end of the program. Has to be present otherwise a fatal error is generated.
	Takes 0 Operands

16. `DS`: Declares a Symbol. Has to be followed by a Valid symbol name (Discussed later). Symbol name can **optionally** be followed by a Number denoting
the initial value of the symbol. The address of the symbol is assigned automatically by the assembler 

18. `DS`: Declares a Literal / Constant. Has to be followed by a Valid literal name (Discussed later). Literal name **has to be** followed by a Number denoting
the initial value of the symbol. The address of the constant is assigned automatically by the assembler.

19. Labels (:): A label is declared by a valid Label name (Discussed later) followed by a colon (without a space).

## Syntax
### A note on the notation used in this documentation
In this documentation, following notation is used:
1. Any variable text like a name, like symbol name, or any value, or a general opcode is enclosed in angular brackets `<>`
2. Any optional code is enclosed in square brackets `[]`


### General
1. A line of may contain a Label, an Opcode, an Operand, an assembler directive, a value, or a comment. A line of code ends by a **new line**.
1. **START** - `START` should  be present at the start of code. However, `START` is optional, however, a warning is generated if START is not present. Start can be followed by a number denoting the start address for the program counter. The start address MUST:
	1. Be a non-negative integer
	2. Should be between 0 and 255.
	
	If `START` is not followed by a number, or if START is absent altogether, program starts at location 0, and a warning is raised at assembly time.
**Syntax**
```
START [<START_LOCATION>]
```
**Example**
```
START
START 20
START 0
```

2. **END** -  A program **must** contain **one and only one** `END` statement. A fatal error occurs if `END` is not present. Code can however, be present after the `END` statement, say to declare literals or symbols.

3. **Comments** - A comment is a part of assembly code which is not assembled. A comment starts with a Semi-colon (;) and all text after a comment is ignored. A comment can also be after a line if code. If after code, there must be a space between the comments semi-colon and last character of code.

**Syntax**
```
;[<COMMENT_TEXT>]
```
**Examples**
```
; This is a comment
DS A ;Declare A as a Symbol without any value
```
### Opcodes and Operands
Opcodes and operands are separated by one or more spaces and then line of code must be ended (by a new line) or followed by a comment. If no operands are present, the line of code should be ended. 
Some notable points:
	1. Opcode name are **case-insensitive**. Add and ADD are the same.
	2. Literal, Symbol and Label names are **case-sensitive**. Test and TeST are different.

**Syntax**
```
<OPCODE> [<OPERAND>]
```
**Examples**
```
DSP A
ADD B
DS A
DS B
CLA
```

### Literals
A literal or constant is declared using DC, followed **compulsorily** by a valid symbol name, and then **compulsorily** followed by a value indicating the initial value. If no initial value is provided, 0 is set as the value. DS, Symbol name and the initial (if any) are one (or more spaces) separated. A literal can take integer values between -128 and 127. 


**Syntax**
```
DS <SYMBOL_NAME> <INITAL_VALUE>
```
**Example**
```
DC A 10
DC Test 21
```

### Symbols
A symbol is declared using DS, followed **compulsorily** by a valid symbol name, and then **optionally** followed by a value indicating the initial value. If no initial value is provided, 0 is set as the value. DS, Symbol name and the initial (if any) are one (or more spaces) separated. A symbol can take integer values between -128 and 127. 

**Syntax**
```
DS <SYMBOL_NAME> [<INITAL_VALUE>]
```
**Example**
```
DS A 10
DS B
DC Test 21
```

### Labels
A label is defined by valid label name followed by a colon (:), **without a space**. A label can be directly be followed by a line of code **(with a space (or multiple spaces) after the colon)**, or code can be on a new line.
**Syntax**
```
<LABEL_NAME>: [<MORE_CODE>]
```
**Example**
```
Loop: DS A

TestLabel:
DS B
```
### Branches with BRN, BRP and BRZ
Any branch instruction (`BRN`, `BRP` and `BRZ`) **must only be followed by a defined Label.**
**Syntax**
```
BRN <LABEL_NAME>
BRP <LABEL_NAME>
BRZ <LABEL_NAME>
```
**Examples**
```
Loop: LAC A
ADD A
STA A
LAC B
SUB One
STA B
LAC B
BRZ Loop ;Branch followed by a Label
DS A
DS B
DC One 1
```
### Valid Symbol, Literal and Label names:
A valid name has the following features:
1. It does not contain any spaces
2. It may contain only Alpha-numeric characters or `_` and no other characters.
3. It can only start with an alphabet.
4. It can not be the same as an Opcode
5. It can not be already used as a Symbol, Literal or Label. Hence, a symbol, literal or label can not share the same name. 


**Valid names for Literals, Symbols and Labels**
```
Test
Name3
name_2
my_name
```
**Invalid names for Literals, Symbols and Labels**
```
12Test ; Starts with a non-alphabet character
_Test  ; Starts with a non-alphabet character
Name 2 ; Contains space
Add    ; Same as on opcode
Name.2 ; Contains an invalid character (.)
```
## Errors & Warnings

### Warnings

Warnings are generated when a non - fatal error occurs:

1. **Start statement missing** - When the start statement is missing. program starts at location 0 by default and a warning is generated.
2. **Start Address not provided** – When a start statement doesn’t have a start address associated, program starts at 0 by default and a warning is generated.

### Errors

Errors are generated when non-recoverable events happen or there are non-recoverable mistakes in the assembly code. If an error is encountered, the assembler can not generate a binary output.
1. File not found – When the filename to be assembled is not found, this error is generated.
2. Empty file – If the file to be assembled is an empty file, `Can not assemble an empty file` error is generated.
3. If an invalid start address is provided, invalid `Invalid start address provided` error is generated. A valid start address is a non-negative integer between 0 and 255.
4. End missing - If the END statement is missing, `End of program not found.` error is generated.
5. Multiple END statements - If multiple end statements are found in a program, `Multiple END statements found. Can only have one end` error is generated.
6. If statements other than `DS` or `DC` are found after the `END` statement, `Only DS and DC statements allowed after end` error is generated.
7. If incorrect number of operands are provided for an opcode, `Invalid number of operands given for the Instruction` is generated,
8. If invalid syntax is used to declare a symbol, `Invalid syntax to declare symbol` error is generated.
9. If an invalid value is given for a symbol, `Invalid value given for symbol` error is generated. A valid value is an integer between -128 and 127.
10. If invalid syntax is used to declare a literal, `Invalid syntax to declare literal` error is generated.
11. If an invalid value is given for a literal, `Invalid value given for literal` error is generated. A valid value is an integer between -128 and 127. 
12. Invalid value name for Symbol / Literal / Label - An error is generated if a token with invalid name is found. Valid names are discussed earlier.
13. Invalid Opcode - If an invalid opcode is found, an error is reported.
14. If the program counter exceeds 255 bits, `Not enough memory for program. Program can not exceed 255 bits.` error is generated.
15. If general incorrect syntax is found, an error is generated.
16. If some Literals / Symbols / Labels are used but not defined, an error is generated.

## The assembly process
The following happens during assembly:
1. The assembled is run using `python3`
2. Filename of the assembly file is entered. If the file is not found, an error is reported.
3. The assembly if the file begins if the file is found. If the assembly code is not valid, appropriate errors are reported.
4. If the code is valid, a table of Literals, Symbols and Labels is displayed with their name, assigned virtual address and their default value (all in decimal).
5. A table of all the Instructions with their proper operands' name & memory locations (in decimal) is also displayed

## The final binary output
The final output is generated in a file called `filename.bin` where filename is the original name of the assembly file (without the extension).
The binary file consists of a 4 BIT binary opcode followed by a space and then 8 BIT operand address for the given opcode, if there are any operands.
All instructions are on a new line.