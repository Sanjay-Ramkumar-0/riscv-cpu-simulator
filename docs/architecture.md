# CPU Architecture

## Overview

This project is a Python-based architectural simulator of a **64-bit RISC-V (RV64I)** processor. The primary objective is to model the behavior of a modern pipelined processor while keeping the implementation modular, readable, and extensible.

The simulator focuses on architectural correctness rather than execution speed. Each hardware component is implemented as an independent Python module, making the project suitable for learning processor architecture concepts and serving as a reference model for future RTL implementations.

---

# High-Level Architecture

```text
                     +----------------------+
                     |        CPU           |
                     +----------------------+
                               |
                               |
                   +-----------------------+
                   |   5-Stage Pipeline    |
                   +-----------------------+
          IF  →  ID  →  EX  →  MEM  →  WB
            |                 |
            |                 |
     +--------------+    +--------------+
     | Branch Unit  |    |  Load/Store  |
     +--------------+    +--------------+
            |
     +--------------+
     | Branch       |
     | Predictor    |
     +--------------+
            |
     +--------------+
     | Branch Target|
     | Buffer (BTB) |
     +--------------+
            |
     +--------------+
     | Instruction  |
     | Cache        |
     +--------------+
            |
     +--------------+
     | Data Cache   |
     +--------------+
            |
     +--------------+
     | Main Memory  |
     +--------------+
```

---

# Project Structure

```
python/

├── assembler/
├── cpu/
├── execution/
├── frontend/
├── isa/
├── memory/
├── programs/
├── tests/
└── utils/
```

Each directory models a specific hardware subsystem.

---

# Major Components

## CPU

The CPU module acts as the top-level processor model.

Responsibilities include:

* Managing hardware threads
* Connecting all architectural components
* Providing access to caches and memory
* Executing the processor pipeline

---

## Pipeline

The processor implements a classic five-stage pipeline.

```
Instruction Fetch
        ↓
Instruction Decode
        ↓
Execute
        ↓
Memory Access
        ↓
Write Back
```

Each stage communicates through pipeline registers.

Pipeline hazards are handled using forwarding, hazard detection, and branch recovery mechanisms.

---

## Instruction Fetch (IF)

Responsibilities:

* Fetch instruction from the Instruction Cache
* Perform branch prediction
* Access the Branch Target Buffer
* Perform speculative fetch
* Update the program counter

---

## Instruction Decode (ID)

Responsibilities:

* Decode RV64I instructions
* Read register operands
* Generate immediate values
* Detect RAW hazards
* Stall the pipeline when required

---

## Execute (EX)

Responsibilities:

* Integer ALU operations
* Branch evaluation
* Address generation
* Multiply/Divide operations
* Forwarding support

---

## Memory Stage (MEM)

Responsibilities:

* Load instructions
* Store instructions
* Data Cache access
* Cache statistics updates

---

## Write Back (WB)

Responsibilities:

* Write computation results back to the register file
* Complete instruction execution

---

# Branch Prediction

The processor includes a dynamic branch predictor consisting of:

* Two-bit saturating counter predictor
* Branch Target Buffer (BTB)
* Speculative instruction fetch
* Branch misprediction recovery

Prediction states:

```
00  Strongly Not Taken
01  Weakly Not Taken
10  Weakly Taken
11  Strongly Taken
```

The predictor continuously updates itself based on actual branch outcomes.

---

# Cache Hierarchy

The simulator models separate instruction and data caches.

## Instruction Cache

Responsible for instruction fetches.

```
CPU
 ↓
I-Cache
 ↓
Main Memory
```

---

## Data Cache

Responsible for all load and store operations.

```
CPU
 ↓
D-Cache
 ↓
Main Memory
```

Current cache implementation:

* Direct mapped
* 32 KB
* 64-byte cache line
* Write-through
* Write-allocate
* Cache hit/miss statistics

---

# Main Memory

Main memory acts as the backing storage for both caches.

Responsibilities:

* Store program instructions
* Store application data
* Provide data during cache misses

---

# Instruction Set

Currently implemented instructions include:

### Arithmetic

* ADD
* SUB
* ADDI
* XOR
* SLL
* SRL
* SRA
* SLT
* SLTU

### Multiplication Extension

* MUL
* DIV
* REM

### Branches

* BEQ
* BNE
* BLT
* BGE
* BLTU
* BGEU

### Memory

* LD
* SD

### Jumps

* JAL

### Upper Immediate

* LUI
* AUIPC

---

# Pipeline Features

Implemented:

* Five-stage pipeline
* Pipeline registers
* RAW hazard detection
* Data forwarding
* Branch prediction
* Speculative fetch
* Branch Target Buffer
* Instruction cache
* Data cache
* Cache statistics

---

# Design Philosophy

The simulator emphasizes modularity.

Each architectural component is implemented independently.

Examples include:

* Decoder
* ALU
* Branch Unit
* Branch Predictor
* BTB
* Cache
* Memory
* Pipeline

This modular organization makes it easier to replace or extend individual components without affecting the rest of the processor.

---

# Current Status

Implemented:

* RV64I Instruction Set
* RV64M Multiply/Divide Extension
* Five-stage pipeline
* Hazard detection
* Data forwarding
* Two-bit branch predictor
* Branch Target Buffer
* Speculative fetch
* Instruction Cache
* Data Cache
* Performance statistics

---

# Future Work

Planned enhancements include:

* Set-associative caches
* Cache replacement policies (LRU/FIFO/Random)
* Cache miss penalties
* Memory latency simulation
* Multi-threading (SMT2)
* Out-of-order execution experiments
* Reusable SystemVerilog IP implementation based on this architectural model

---

# Purpose

This simulator serves as the architectural reference model for a future hardware implementation of a reusable RISC-V processor platform in SystemVerilog. The long-term objective is to develop reusable IP blocks—including caches, pipeline stages, execution units, and memory interfaces—that can be integrated into custom CPU and SoC designs.
