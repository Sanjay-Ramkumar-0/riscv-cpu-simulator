# Project Progress

## Overview

This project is a Python-based architectural simulator of a 64-bit RISC-V (RV64I) processor. The simulator models the behavior of a modern pipelined processor by implementing key architectural components as independent, modular units.

The primary objective of the project is to understand and simulate processor execution at the architectural level while maintaining a clean and extensible codebase.

---

# Project Structure

The simulator is organized into modular components.

```text
python/

├── assembler/
├── cpu/
├── execution/
├── frontend/
├── isa/
├── memory/
├── tests/
└── utils/
```

Each directory represents a different subsystem of the processor.

---

# Implemented Features

## Instruction Set Architecture (ISA)

Implemented RV64I instructions include:

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

### Memory Operations

* LD
* SD

### Branch Instructions

* BEQ
* BNE
* BLT
* BGE
* BLTU
* BGEU

### Jump Instructions

* JAL

### Upper Immediate Instructions

* LUI
* AUIPC

---

# Five-Stage Pipeline

A complete in-order five-stage pipeline has been implemented.

Pipeline stages:

* Instruction Fetch (IF)
* Instruction Decode (ID)
* Execute (EX)
* Memory Access (MEM)
* Write Back (WB)

The simulator models instruction flow through pipeline registers between each stage.

---

# Pipeline Registers

Implemented pipeline registers:

* IF/ID
* ID/EX
* EX/MEM
* MEM/WB

These registers preserve instruction state between clock cycles and enable concurrent execution of multiple instructions.

---

# Hazard Handling

The pipeline includes mechanisms for handling common execution hazards.

Implemented features:

* RAW (Read After Write) hazard detection
* Pipeline stalling
* Data forwarding
* Pipeline flushing after branch mispredictions

---

# Branch Prediction

The processor includes a dynamic branch prediction subsystem.

Implemented features:

* Two-bit saturating counter predictor
* Branch Target Buffer (BTB)
* Dynamic predictor updates
* Branch resolution
* Speculative instruction fetch
* Prediction accuracy statistics

The predictor continuously adapts to branch behavior during execution.

---

# Cache Subsystem

The simulator models separate instruction and data caches.

Implemented features:

* Direct-mapped cache organization
* 32 KB cache size
* 64-byte cache lines
* Address decoding
* Cache lookup
* Cache line allocation
* Read path
* Write path
* Write-through policy
* Write-allocate policy
* Cache hit/miss statistics

Both caches are integrated into the processor pipeline.

---

# Memory System

Implemented memory features:

* Byte-addressable main memory
* Instruction loading
* Data storage
* Cache-backed memory accesses

---

# Assembler

A lightweight assembler has been developed for generating machine code from supported RISC-V assembly instructions.

Implemented capabilities:

* Instruction encoding
* Immediate encoding
* Branch offset encoding
* Generation of 32-bit machine instructions
* Test program generation

---

# Execution Units

Implemented execution modules include:

* Arithmetic Logic Unit (ALU)
* Branch Unit
* Multiply/Divide Unit
* Immediate decoding
* Instruction decoder

Each execution unit is implemented independently to simplify testing and future extension.

---

# Performance Monitoring

The simulator collects execution statistics during runtime.

Implemented statistics include:

### Branch Prediction

* Total predictions
* Correct predictions
* Mispredictions
* Prediction accuracy

### Cache

* Read hits
* Read misses
* Write hits
* Write misses
* Overall cache hit rate

These statistics are displayed after program execution to aid performance analysis.

---

# Testing

Individual modules have been tested independently before integration.

Implemented test coverage includes:

* Instruction decoding
* Pipeline execution
* Branch prediction
* Branch recovery
* Cache read/write operations
* Cache statistics
* Assembler instruction generation

---

# Current Architecture

```text
                     CPU
                      │
              Five-Stage Pipeline
                      │
      IF → ID → EX → MEM → WB
       │               │
       │               ▼
       │          Data Cache
       ▼
 Instruction Cache
       │
       ▼
 Main Memory

Branch Predictor
        │
        ▼
       BTB
```

---

# Current Status

| Component              | Status        |
| ---------------------- | ------------- |
| RV64I Instruction Set  | ✅ Implemented |
| RV64M Extension        | ✅ Implemented |
| Five-Stage Pipeline    | ✅ Implemented |
| Pipeline Registers     | ✅ Implemented |
| Hazard Detection       | ✅ Implemented |
| Data Forwarding        | ✅ Implemented |
| Branch Unit            | ✅ Implemented |
| Branch Predictor       | ✅ Implemented |
| Branch Target Buffer   | ✅ Implemented |
| Speculative Fetch      | ✅ Implemented |
| Instruction Cache      | ✅ Implemented |
| Data Cache             | ✅ Implemented |
| Cache Statistics       | ✅ Implemented |
| Performance Statistics | ✅ Implemented |
| Lightweight Assembler  | ✅ Implemented |

---

# Summary

At its current stage, the simulator models the core architectural behavior of a modern in-order RISC-V processor. It includes a five-stage pipeline, hazard handling mechanisms, branch prediction, speculative execution, instruction and data caches, and a lightweight assembler for generating executable machine code. The modular organization of the project allows each subsystem to be developed, tested, and understood independently while contributing to a complete processor simulation.
