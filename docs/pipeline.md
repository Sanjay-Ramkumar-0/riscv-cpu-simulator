# Five-Stage Pipeline

## Overview

The processor implements a classic **five-stage in-order pipeline**, allowing multiple instructions to execute simultaneously by dividing instruction execution into independent stages.

Instead of completing one instruction before starting the next, different instructions occupy different pipeline stages at the same time, significantly improving instruction throughput.

The implemented stages are:

```text
Instruction Fetch (IF)
        │
        ▼
Instruction Decode (ID)
        │
        ▼
Execute (EX)
        │
        ▼
Memory Access (MEM)
        │
        ▼
Write Back (WB)
```

Each stage performs a specific task and communicates with the next stage through pipeline registers.

---

# Why Pipelining?

Without pipelining, instructions execute sequentially.

```text
Cycle

1   IF
2   ID
3   EX
4   MEM
5   WB
```

The next instruction starts only after the previous instruction completes.

With pipelining:

```text
Cycle

1   IF

2   ID   IF

3   EX   ID   IF

4   MEM  EX   ID   IF

5   WB   MEM  EX   ID   IF
```

Multiple instructions are active simultaneously, increasing overall throughput.

---

# Pipeline Organization

```text
                 CPU

                  │

      +-----------------------+
      |     Instruction       |
      |       Fetch (IF)      |
      +-----------------------+
                  │
             IF/ID Register
                  │
      +-----------------------+
      |      Decode (ID)      |
      +-----------------------+
                  │
             ID/EX Register
                  │
      +-----------------------+
      |     Execute (EX)      |
      +-----------------------+
                  │
            EX/MEM Register
                  │
      +-----------------------+
      |   Memory Access (MEM) |
      +-----------------------+
                  │
           MEM/WB Register
                  │
      +-----------------------+
      |    Write Back (WB)    |
      +-----------------------+
```

---

# Instruction Fetch (IF)

Responsibilities:

* Fetch instructions from the Instruction Cache.
* Read the current Program Counter (PC).
* Consult the Branch Predictor.
* Access the Branch Target Buffer (BTB).
* Perform speculative fetch.
* Update the Program Counter.

Pipeline register:

```text
IF/ID

Program Counter

Instruction

Prediction Information

Predicted Target
```

---

# Instruction Decode (ID)

Responsibilities:

* Decode the fetched instruction.
* Identify opcode and instruction format.
* Read source registers.
* Generate immediate values.
* Detect RAW hazards.
* Stall the pipeline when necessary.

Pipeline register:

```text
ID/EX

Decoded Instruction

Source Operand Values

Immediate Value

Program Counter
```

---

# Execute (EX)

Responsibilities:

* Integer arithmetic
* Logical operations
* Shift operations
* Branch evaluation
* Address generation
* Multiply/Divide operations
* Data forwarding

The Branch Unit also determines:

* Branch Taken / Not Taken
* Actual Branch Target

This stage resolves branch instructions and updates the branch predictor.

Pipeline register:

```text
EX/MEM

Execution Result

Memory Address

Decoded Instruction
```

---

# Memory Access (MEM)

Responsibilities:

* Execute load instructions.
* Execute store instructions.
* Access the Data Cache.
* Handle cache hits and misses.

Memory instructions include:

```text
LD

SD
```

Pipeline register:

```text
MEM/WB

Result

Decoded Instruction
```

---

# Write Back (WB)

Responsibilities:

* Write ALU results to the destination register.
* Write loaded data to the register file.
* Complete instruction execution.

Example:

```text
ADDI x3, x1, 10

↓

Register x3 Updated
```

---

# Pipeline Registers

Pipeline registers separate each stage.

Implemented registers:

```text
IF/ID

ID/EX

EX/MEM

MEM/WB
```

Each register stores the information required by the following stage.

Without these registers, later stages would overwrite information still needed by earlier instructions.

---

# Pipeline Hazards

The pipeline encounters three primary classes of hazards.

## Data Hazards

Example:

```assembly
ADD x3, x1, x2
SUB x4, x3, x5
```

The second instruction requires the result of the first before it has been written back.

Solution:

* Data Forwarding
* Pipeline Stall (if necessary)

---

## Control Hazards

Example:

```assembly
BEQ x1, x2, target
```

The processor does not know which instruction should be fetched until the branch is resolved.

Solution:

* Branch Predictor
* BTB
* Speculative Fetch
* Pipeline Flush

---

## Structural Hazards

Structural hazards occur when two stages compete for the same hardware resource.

This simulator avoids structural hazards by using separate Instruction and Data Caches.

```text
Instruction Fetch

↓

Instruction Cache

Load / Store

↓

Data Cache
```

---

# Data Forwarding

Rather than waiting for Write Back, execution results can be forwarded directly to dependent instructions.

Example:

```assembly
ADD x3, x1, x2
SUB x4, x3, x5
```

Instead of waiting several cycles:

```text
EX Result

↓

Forward

↓

Next EX Stage
```

This significantly reduces stalls.

---

# Hazard Detection

Some hazards cannot be solved by forwarding.

Example:

```assembly
LD x3, 0(x1)
ADD x4, x3, x5
```

The loaded value is not available until the Memory stage.

The Hazard Detection Unit inserts a bubble into the pipeline.

```text
Instruction

↓

Hazard Detected

↓

Pipeline Stall

↓

Resume Execution
```

---

# Branch Prediction

Instruction Fetch integrates with:

* Two-bit saturating counter predictor
* Branch Target Buffer
* Speculative fetch

Example:

```text
Fetch

↓

Predict Taken?

↓

BTB Lookup

↓

Speculative Fetch
```

If the prediction is incorrect:

```text
Execute

↓

Resolve Branch

↓

Pipeline Flush

↓

Correct Program Counter

↓

Continue Execution
```

---

# Speculative Fetch

Instead of waiting for branch resolution:

```text
Predict Branch

↓

Fetch Predicted Instruction

↓

Continue Pipeline
```

Speculative execution improves instruction throughput by reducing idle pipeline cycles.

---

# Pipeline Flush

A mispredicted branch invalidates instructions already inside the pipeline.

Example:

```text
IF

ID

EX
```

Incorrect instructions are discarded.

The Program Counter is updated to the correct target before instruction fetch resumes.

---

# Pipeline Performance

The pipeline aims to complete approximately one instruction every cycle after the pipeline has been filled.

Although hazards and cache misses may temporarily reduce throughput, pipelining dramatically improves performance compared to sequential execution.

---

# Integration with Other Components

The pipeline interacts with multiple processor subsystems.

```text
Instruction Fetch
        │
        ▼
Instruction Cache
        │
        ▼
Branch Predictor
        │
        ▼
Branch Target Buffer
        │
        ▼
Instruction Decode
        │
        ▼
Execute
        │
        ▼
Data Cache
        │
        ▼
Write Back
```

Each subsystem is implemented independently, allowing individual components to be modified without redesigning the entire processor.

---

# Current Implementation

Implemented features:

* Five-stage pipeline
* Pipeline registers
* In-order execution
* Hazard detection
* Data forwarding
* Branch prediction
* Branch Target Buffer
* Speculative fetch
* Pipeline flush
* Instruction cache integration
* Data cache integration

---

# Future Improvements

Potential enhancements include:

* Multi-cycle execution units
* Dual-issue pipeline
* Out-of-order execution
* Register renaming
* Reorder Buffer (ROB)
* Reservation Stations
* SMT2 (Simultaneous Multi-Threading)
* Superscalar execution
* Non-blocking caches

These features would extend the simulator toward modern high-performance processor architectures.

---

# Summary

The five-stage pipeline forms the core of the processor architecture. By dividing instruction execution into Fetch, Decode, Execute, Memory, and Write Back stages, the simulator demonstrates how modern processors improve throughput while maintaining correctness. Integrated hazard detection, forwarding, branch prediction, speculative execution, and cache support allow the simulator to model many of the architectural techniques found in contemporary RISC-V and general-purpose processors.
