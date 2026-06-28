# Assembler

## Overview

The simulator includes a lightweight assembler that converts a subset of RISC-V assembly instructions into their corresponding 32-bit machine code. The assembler was developed specifically for testing the CPU simulator without relying on external toolchains.

Unlike a full-featured assembler, this implementation focuses on generating machine code for the instructions currently supported by the simulator. This allows test programs to be written directly in assembly and executed by the simulated processor.

---

# Why an Assembler?

Initially, machine code instructions were written manually in hexadecimal.

Example:

```text
0x00C585B3
```

Although this works, manually encoding instructions is:

* Error-prone
* Difficult to debug
* Time-consuming
* Not scalable for larger test programs

Instead, the assembler allows instructions to be written in a human-readable form.

Example:

```assembly
ADD x3, x1, x2
BEQ x1, x2, 8
ADDI x5, x0, 10
```

These instructions are automatically translated into their binary encoding before execution.

---

# Assembler Workflow

The assembler performs the following steps:

```text
Assembly Instruction
        │
        ▼
Parse Operands
        │
        ▼
Determine Instruction Format
        │
        ▼
Encode Bit Fields
        │
        ▼
Generate 32-bit Machine Code
```

The resulting machine code can then be loaded into the simulator's instruction memory.

---

# Supported Instruction Formats

The assembler currently supports the following RISC-V instruction formats.

## R-Type

Used for register-to-register arithmetic.

Examples:

```assembly
ADD x3, x1, x2
SUB x4, x5, x6
MUL x7, x8, x9
```

Encoding format:

```text
31-----25 24---20 19---15 14--12 11---7 6----0
funct7     rs2     rs1    funct3   rd   opcode
```

---

## I-Type

Used for immediate arithmetic and loads.

Examples:

```assembly
ADDI x5, x0, 10
LD   x6, 0(x1)
```

Encoding format:

```text
31-------------20 19---15 14--12 11---7 6----0
 immediate         rs1     funct3   rd   opcode
```

---

## S-Type

Used for store instructions.

Example:

```assembly
SD x2, 0(x1)
```

Encoding format:

```text
31-----25 24---20 19---15 14--12 11---7 6----0
imm[11:5] rs2     rs1    funct3 imm[4:0] opcode
```

---

## B-Type

Used for conditional branches.

Examples:

```assembly
BEQ x1, x2, 8
BNE x3, x4, -16
```

Encoding format:

```text
31 30---25 24---20 19---15 14--12 11---8 7 6----0
imm12 imm10:5 rs2 rs1 funct3 imm4:1 imm11 opcode
```

The assembler automatically rearranges branch immediates into the format required by the RISC-V specification.

---

## U-Type

Used for upper immediate instructions.

Examples:

```assembly
LUI x5, 0x10000
AUIPC x6, 0x20000
```

---

## J-Type

Used for unconditional jumps.

Example:

```assembly
JAL x1, 32
```

---

# Encoding Process

Each instruction is constructed by placing fields into their designated bit positions.

Example:

```assembly
ADD x3, x1, x2
```

Fields:

```text
opcode = 0110011
funct3 = 000
funct7 = 0000000
rd      = x3
rs1     = x1
rs2     = x2
```

The assembler combines these fields to produce a single 32-bit instruction.

---

# Branch Encoding

Branch instructions require special handling because the immediate value is not stored as one continuous field.

For example:

```assembly
BEQ x1, x2, 8
```

The immediate is divided into multiple bit groups before encoding.

```text
Immediate

↓

imm[12]
imm[10:5]
imm[4:1]
imm[11]

↓

Machine Code
```

The assembler performs this bit manipulation automatically.

---

# Output

The assembler returns the encoded instruction as a 32-bit integer.

Example:

```assembly
ADDI x1, x0, 10
```

Output:

```text
0x00A00093
```

This value can be written directly into the simulator's instruction memory.

---

# Integration with the Simulator

The assembler forms the first stage of the execution flow.

```text
Assembly Program
        │
        ▼
Assembler
        │
        ▼
Machine Code
        │
        ▼
Instruction Memory
        │
        ▼
Instruction Cache
        │
        ▼
Pipeline
        │
        ▼
Execution
```

This allows programs to be developed in assembly rather than manually encoding hexadecimal instructions.

---

# Current Supported Instructions

The assembler currently supports encoding for the instructions implemented by the simulator.

### Arithmetic

* ADD
* SUB
* XOR
* SLL
* SRL
* SRA
* SLT
* SLTU
* ADDI

### Multiplication Extension

* MUL
* DIV
* REM

### Memory

* LD
* SD

### Branches

* BEQ
* BNE
* BLT
* BGE
* BLTU
* BGEU

### Jumps

* JAL

### Upper Immediate

* LUI
* AUIPC

---

# Design Goals

The assembler was designed with the following objectives:

* Produce correct RV64I instruction encodings.
* Keep the implementation simple and easy to understand.
* Eliminate the need to manually write hexadecimal instructions.
* Integrate seamlessly with the CPU simulator.
* Provide a foundation for future support of labels, pseudo-instructions, and complete assembly programs.

---

# Future Improvements

Potential enhancements include:

* Multi-line assembly files
* Label support
* Symbol table generation
* Pseudo-instruction expansion
* Automatic binary generation
* ELF executable support
* Integration with a loader for complete program execution
