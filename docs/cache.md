# Cache Subsystem

## Overview

Modern processors execute instructions much faster than data can be fetched from main memory. This difference in speed creates a significant performance bottleneck.

To reduce memory access latency, this simulator implements separate **Instruction Cache (I-Cache)** and **Data Cache (D-Cache)** modules. These caches store recently accessed memory blocks, allowing future accesses to be serviced much faster than reading directly from main memory.

The current implementation models a **direct-mapped, write-through, write-allocate cache**, providing a simplified but realistic representation of an L1 cache.

---

# Why Caches?

Without a cache, every instruction fetch or data access must read from main memory.

```text
CPU
 │
 ▼
Main Memory
```

Since memory is significantly slower than the processor, the CPU would spend many cycles waiting for data.

By introducing a cache:

```text
CPU
 │
 ▼
Cache
 │
 ▼
Main Memory
```

recently accessed instructions and data are stored closer to the processor, reducing average memory access time.

---

# Cache Hierarchy

The simulator implements separate caches for instructions and data.

```text
                 CPU
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 Instruction Cache     Data Cache
        │                   │
        └─────────┬─────────┘
                  ▼
             Main Memory
```

### Instruction Cache (I-Cache)

* Used during instruction fetch.
* Supplies instructions to the IF stage.
* Reduces instruction fetch latency.

### Data Cache (D-Cache)

* Used during load and store operations.
* Supplies data to the MEM stage.
* Reduces data memory latency.

Separating instruction and data caches allows instruction fetches and data accesses to proceed independently, similar to the Harvard architecture used in many processors.

---

# Cache Organization

Current cache configuration:

| Parameter             |          Value |
| --------------------- | -------------: |
| Cache Type            |  Direct-Mapped |
| Cache Size            |          32 KB |
| Cache Line Size       |       64 Bytes |
| Number of Cache Lines |            512 |
| Write Policy          |  Write-Through |
| Allocation Policy     | Write-Allocate |

---

# Cache Line

Each cache line stores one block of memory.

```text
+-------------------------------------------------------------+
| Valid | Tag |                 Data (64 Bytes)               |
+-------------------------------------------------------------+
```

Each cache line contains:

* **Valid Bit** – Indicates whether the entry contains valid data.
* **Tag** – Identifies which memory block is stored.
* **Data** – One cache line (64 bytes).

---

# Address Breakdown

Every memory address is divided into three fields.

```text
Address
 │
 ├── Tag
 ├── Index
 └── Offset
```

## Tag

Identifies which block of main memory is stored in the cache line.

---

## Index

Selects which cache line to access.

Example:

```text
512 cache lines

↓

Index = 0 ... 511
```

---

## Offset

Specifies the byte inside the cache line.

Example:

```text
Cache Line (64 Bytes)

+----------------------------------------------------------+
| Byte0 Byte1 Byte2 ... Byte63 |
+----------------------------------------------------------+
                    ↑
                 Offset
```

If the CPU requests address 100:

```text
Line Start = 64

Offset = 100 − 64 = 36
```

---

# Cache Lookup

Every memory access begins with a cache lookup.

```text
CPU Request
      │
      ▼
Decode Address
      │
      ▼
Select Cache Line
      │
      ▼
Compare Tag
      │
 ┌────┴────┐
 │         │
Hit      Miss
```

A cache hit occurs when:

* The cache line is valid.
* The stored tag matches the requested tag.

Otherwise, a cache miss occurs.

---

# Cache Read

The read operation follows this sequence.

```text
Read Request
      │
      ▼
Lookup
      │
 ┌────┴────┐
 │         │
Hit      Miss
 │         │
 │     Read Memory
 │         │
 │     Fill Cache Line
 │         │
 └────┬────┘
      ▼
Return Requested Data
```

On a miss, the entire 64-byte memory block is loaded into the cache before the requested byte is returned.

---

# Cache Fill

The simulator loads one complete cache line during a miss.

Example:

```text
Requested Address = 100

↓

Load Addresses

64
65
66
...
127
```

Only one byte may be requested, but all 64 bytes are cached because nearby memory locations are likely to be accessed soon.

This behavior exploits **spatial locality**.

---

# Cache Write

The simulator uses:

* **Write-Through**
* **Write-Allocate**

Write sequence:

```text
Write Request
      │
      ▼
Lookup
      │
 ┌────┴────┐
 │         │
Hit      Miss
 │         │
 │     Allocate Cache Line
 │         │
 └────┬────┘
      ▼
Update Cache
      │
      ▼
Update Main Memory
```

---

# Write-Through Policy

Every write updates both:

* Cache
* Main Memory

```text
CPU
 │
 ▼
Cache
 │
 ▼
Main Memory
```

Advantages:

* Simple implementation.
* Memory always contains the latest data.
* Easier debugging.

Disadvantages:

* Higher memory traffic.

---

# Write-Allocate Policy

When a write misses:

```text
Cache Miss
      │
      ▼
Load Cache Line
      │
      ▼
Perform Write
```

This ensures future accesses to nearby addresses become cache hits.

---

# Cache Statistics

The simulator records cache performance during execution.

Statistics include:

* Read Hits
* Read Misses
* Write Hits
* Write Misses
* Overall Hit Rate

Example:

```text
========== Cache ==========
Read Hits      : 120
Read Misses    : 15
Write Hits     : 40
Write Misses   : 5
Hit Rate       : 91.67%
===========================
```

These metrics provide insight into cache efficiency and program locality.

---

# Integration with the CPU

Instruction Fetch:

```text
Program Counter
        │
        ▼
Instruction Cache
        │
        ▼
Pipeline IF Stage
```

Memory Operations:

```text
Load / Store
       │
       ▼
Data Cache
       │
       ▼
Main Memory
```

The pipeline interacts only with the cache. Main memory is accessed only when a cache miss occurs.

---

# Current Implementation

Implemented features:

* Direct-mapped cache
* Address decoding
* Cache lookup
* Cache line filling
* Read path
* Write path
* Write-through policy
* Write-allocate policy
* Instruction cache integration
* Data cache integration
* Cache performance statistics

---

# Future Improvements

Planned enhancements include:

* Set-associative caches
* Fully associative caches
* LRU replacement policy
* FIFO replacement policy
* Random replacement policy
* Dirty-bit support
* Write-back cache
* Cache miss penalties
* Multi-level cache hierarchy (L1/L2)
* Prefetching
* Victim cache

---

# Design Goals

The cache subsystem was designed to:

* Demonstrate the role of caches in reducing memory latency.
* Model realistic cache behavior while remaining easy to understand.
* Integrate seamlessly with the five-stage pipeline.
* Provide a foundation for future RTL cache implementations in SystemVerilog.

---

# Summary

The cache subsystem models one of the most important performance optimizations in modern processors. By implementing direct-mapped instruction and data caches with write-through and write-allocate policies, the simulator demonstrates how memory hierarchy reduces average access time while maintaining architectural correctness. The modular design also provides a clear path toward more advanced cache organizations and hardware implementations.
