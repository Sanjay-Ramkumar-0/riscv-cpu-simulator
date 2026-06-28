# RISC-V RV64I CPU Simulator

A Python-based architectural simulator of a **64-bit RISC-V (RV64I)** processor featuring a five-stage pipeline, branch prediction, speculative instruction fetch, and a direct-mapped cache hierarchy.

This project was developed to understand the internal architecture of modern processors by implementing each hardware component as an independent software module.

---

## Features

### Processor Core

* RV64I Instruction Set
* RV64M Multiplication Extension
* Modular CPU Design
* Byte-addressable Main Memory

### Five-Stage Pipeline

* Instruction Fetch (IF)
* Instruction Decode (ID)
* Execute (EX)
* Memory Access (MEM)
* Write Back (WB)

### Hazard Handling

* RAW Hazard Detection
* Data Forwarding
* Pipeline Stalling
* Pipeline Flushing

### Branch Prediction

* Two-bit Saturating Counter
* Branch Target Buffer (BTB)
* Speculative Instruction Fetch
* Branch Recovery
* Prediction Statistics

### Cache Subsystem

* Direct-Mapped Instruction Cache
* Direct-Mapped Data Cache
* Write-Through Policy
* Write-Allocate Policy
* Cache Statistics

### Assembler

* Lightweight RISC-V Instruction Encoder
* Machine Code Generation
* Branch Immediate Encoding

---

# Project Structure

```text
python/

├── assembler/
├── cpu/
├── docs/
├── execution/
├── frontend/
├── isa/
├── memory/
├── tests/
└── utils/
```

---

# Architecture

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

# Documentation

Detailed documentation for each subsystem is available in the `docs/` directory.

| Document               | Description                                 |
| ---------------------- | ------------------------------------------- |
| `architecture.md`      | Overall processor architecture              |
| `pipeline.md`          | Five-stage pipeline implementation          |
| `branch_prediction.md` | Branch predictor, BTB and speculative fetch |
| `cache.md`             | Instruction and data cache implementation   |
| `assembler.md`         | RISC-V instruction encoding                 |
| `roadmap.md`           | Current project progress                    |

---

# Running the Simulator

Clone the repository:

```bash
git clone https://github.com/Sanjay-Ramkumar-0/riscv-cpu-simulator.git
```

Move into the project directory:

```bash
cd riscv-cpu-simulator
```

---

## Run the Pipeline

```bash
python3 -m cpu.pipeline
```

---

## Run Cache Tests

```bash
python3 -m memory.cache
```

---

## Run the Assembler

```bash
python3 -m assembler.assembler
```

---

# Example Output

```text
===== Cycle 1 =====
FETCH PC = 0x00000000

ICACHE MISS : 0x00000000

===== Cycle 2 =====
FETCH PC = 0x00000004

ICACHE HIT : 0x00000004

BRANCH PREDICTION
Accuracy : 96.30%
```

---

# Technologies Used

* Python 3
* Object-Oriented Programming
* RISC-V ISA (RV64I/RV64M)

---

# Current Status

Implemented:

* RV64I Instruction Set
* RV64M Extension
* Five-Stage Pipeline
* Pipeline Registers
* Hazard Detection
* Data Forwarding
* Branch Prediction
* Branch Target Buffer (BTB)
* Speculative Fetch
* Instruction Cache
* Data Cache
* Lightweight Assembler
* Performance Statistics

---

# Repository Goals

The project focuses on demonstrating the architectural concepts used in modern processors, including:

* Instruction pipelining
* Hazard handling
* Dynamic branch prediction
* Cache hierarchy
* Memory organization
* Modular processor design

The modular structure also makes it easy to extend individual subsystems independently.

---

# License

This project is licensed under the MIT License.

---

# Author

**Sanjay Ramkumar**

B.Tech Electronics and Communication Engineering (ECE)

Vellore Institute of Technology, Chennai
