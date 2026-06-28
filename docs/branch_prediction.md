# Branch Prediction

## Overview

Modern processors execute multiple instructions simultaneously using instruction pipelines. Conditional branch instructions introduce uncertainty because the processor does not immediately know which instruction should be fetched next.

Waiting until the branch is resolved would stall the pipeline and significantly reduce performance.

To minimize these stalls, this simulator implements a dynamic branch prediction system consisting of:

* Two-bit saturating counter predictor
* Branch Target Buffer (BTB)
* Speculative instruction fetch
* Branch resolution and recovery
* Prediction statistics

Together, these components allow the processor to continue fetching instructions before the actual branch outcome is known.

---

# Why Branch Prediction?

Consider the following code:

```assembly
BEQ x1, x2, target
ADD x3, x4, x5
SUB x6, x7, x8
```

When the processor fetches the `BEQ` instruction, it must decide which instruction to fetch next.

There are two possibilities:

```text
Branch Taken

↓

Fetch target
```

or

```text
Branch Not Taken

↓

Fetch next sequential instruction
```

However, the actual branch condition is evaluated later in the Execute (EX) stage.

Without branch prediction, the processor would have to stop fetching instructions until the branch is resolved.

```text
IF → ID → EX

       ↑
Wait here
```

This creates pipeline bubbles and reduces instruction throughput.

---

# Branch Prediction Pipeline

The implemented branch prediction flow is:

```text
Instruction Fetch
        │
        ▼
Is Branch?
        │
        ▼
Branch Predictor
        │
        ▼
Predict Taken?
      /      \
    Yes      No
    │         │
    ▼         ▼
Lookup BTB   PC + 4
    │
    ▼
Predicted Target
    │
    ▼
Speculative Fetch
```

Later, during execution:

```text
Execute Stage
      │
      ▼
Resolve Branch
      │
      ▼
Prediction Correct?
      │
 ┌────┴────┐
 │         │
Yes       No
 │         │
Continue  Flush Pipeline
```

---

# Two-Bit Saturating Counter

Each branch instruction is associated with a two-bit prediction counter.

Four states are used.

```text
00  Strongly Not Taken

01  Weakly Not Taken

10  Weakly Taken

11  Strongly Taken
```

Prediction rule:

```text
00 → Predict Not Taken

01 → Predict Not Taken

10 → Predict Taken

11 → Predict Taken
```

---

# State Transitions

After every branch, the predictor updates its state.

If the branch is taken:

```text
00 → 01

01 → 10

10 → 11

11 → 11
```

If the branch is not taken:

```text
11 → 10

10 → 01

01 → 00

00 → 00
```

Because two incorrect outcomes are required to change a strong prediction, the predictor is resistant to occasional mispredictions.

---

# Branch Target Buffer (BTB)

Predicting that a branch is taken is only half of the problem.

The processor must also know **where** to fetch the next instruction.

The Branch Target Buffer stores previously computed branch destinations.

Each BTB entry contains:

```text
Program Counter

↓

Target Address
```

Example:

```text
PC = 0x00000100

↓

Target = 0x00000240
```

During instruction fetch:

```text
Current PC

↓

BTB Lookup

↓

Target Found?

↓

Fetch Target Instruction
```

This eliminates the need to recompute the branch target every time.

---

# Speculative Fetch

Once both the predictor and BTB agree that a branch is likely to be taken, the processor immediately begins fetching instructions from the predicted destination.

Example:

```text
PC = 0x100

↓

Predict Taken

↓

BTB

↓

Target = 0x200

↓

Fetch 0x200
```

This occurs before the branch instruction has reached the Execute stage.

Speculative execution improves performance by keeping the pipeline busy.

---

# Branch Resolution

The actual branch condition is evaluated in the Execute stage.

The Branch Unit determines:

* Whether the branch is taken.
* The actual branch target.

The pipeline then compares:

```text
Prediction

↓

Actual Result
```

If both match:

```text
Prediction Correct

↓

Continue Execution
```

Otherwise:

```text
Misprediction

↓

Flush Pipeline

↓

Correct Program Counter

↓

Restart Fetch
```

---

# Pipeline Recovery

When a branch prediction is incorrect:

```text
IF
ID
EX
```

may already contain incorrectly fetched instructions.

The simulator performs:

```text
Pipeline Flush

↓

Discard Incorrect Instructions

↓

Fetch Correct Instruction

↓

Resume Execution
```

This restores architectural correctness while allowing aggressive speculative execution.

---

# Prediction Statistics

The simulator records prediction performance during execution.

Statistics include:

* Total Predictions
* Correct Predictions
* Mispredictions
* Prediction Accuracy

Example:

```text
========== Branch Prediction ==========
Total Predictions : 54
Correct           : 52
Mispredictions    : 2
Accuracy          : 96.30%
=======================================
```

These statistics provide insight into predictor effectiveness for different workloads.

---

# Integration with the Pipeline

Branch prediction is integrated into the Instruction Fetch stage.

Execution flow:

```text
Instruction Fetch
        │
        ▼
Branch Predictor
        │
        ▼
BTB Lookup
        │
        ▼
Speculative Fetch
        │
        ▼
Instruction Decode
        │
        ▼
Execute
        │
        ▼
Branch Resolution
        │
        ▼
Predictor Update
```

The predictor continuously learns from previous branch outcomes, improving accuracy over time.

---

# Advantages of Dynamic Prediction

Compared to always predicting "taken" or "not taken", the two-bit predictor offers several advantages:

* Learns program behavior dynamically.
* Handles loops efficiently.
* Avoids changing prediction after a single incorrect outcome.
* Improves instruction throughput.
* Reduces pipeline stalls.

---

# Current Implementation

Implemented features:

* Two-bit saturating counter predictor
* Branch Target Buffer (BTB)
* Dynamic predictor updates
* Speculative instruction fetch
* Pipeline flushing
* Branch recovery
* Prediction statistics

---

# Future Improvements

Potential enhancements include:

* Global History Predictor (GShare)
* Local History Predictor
* Tournament Predictor
* Return Address Stack (RAS)
* Indirect Branch Prediction
* Perceptron-based branch prediction
* Hybrid branch prediction schemes

These techniques are commonly found in modern superscalar processors and represent natural extensions to the current implementation.

---

# Summary

The branch prediction subsystem enables the processor to continue fetching and executing instructions before branch outcomes are known. By combining a two-bit saturating counter, a Branch Target Buffer, speculative fetch, and recovery mechanisms, the simulator models one of the most important performance optimization techniques used in modern pipelined processors.
