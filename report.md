# Paged Replacement Algorithms Project Report

## Introduction
This report documents the implementation and simulation of five paged replacement algorithms: FIFO, LRU, MRU, OPTIMAL, and SECOND CHANCE. It includes sample outputs showing the memory states, failure/success rates, step-by-step manual computations, and a real-world operating system analysis for each algorithm.

---

## Operating System Analysis

### 1. FIFO (First In First Out)
**Concept:** Replaces the oldest page in memory.
**OS Analysis:** 
- **Usage:** Pure FIFO is rarely used in modern operating systems for main memory replacement because it suffers from Belady's Anomaly (where increasing frames can increase page faults) and ignores how often or recently a page is used. 
- **Real-World Examples:** VAX/VMS operating systems used a variation of FIFO along with a secondary "page pool" to mitigate its rigid performance. Standard FIFO is often seen in secondary buffer caches or simpler hardware implementations rather than advanced system paging.

### 2. LRU (Least Recently Used)
**Concept:** Replaces the page that has not been accessed for the longest period of time.
**OS Analysis:**
- **Usage:** A very popular theoretical algorithm that performs close to Optimal, but historically expensive to implement strictly in hardware due to the need for timestamps or priority queues for every access.
- **Real-World Examples:** Many systems (like **Linux** and **macOS**) use "pseudo-LRU" algorithms. Linux memory management uses an active list and an inactive list of pages (known as Two-handed Clock or LRU variant) to approximate LRU behavior to efficiently keep actively used pages in memory.

### 3. MRU (Most Recently Used)
**Concept:** Replaces the most recently accessed page.
**OS Analysis:**
- **Usage:** MRU is counterintuitive for general paging because the most recently used page is likely to be used again soon (temporal locality). However, MRU is highly effective for access patterns where data is read once and never again (e.g., sequential scans of large files).
- **Real-World Examples:** Certain specific database buffer managers (like **PostgreSQL** or **Oracle** cache managers) apply MRU replacement strategies when dealing with large sequential table scans, knowing that the recently read blocks will not be re-read.

### 4. OPTIMAL
**Concept:** Replaces the page that will not be used for the longest period of time in the future.
**OS Analysis:**
- **Usage:** The Optimal algorithm requires future knowledge of reference strings, making it impossible to implement in a real-time operating system.
- **Real-World Examples:** It is instead used as a theoretical benchmark to evaluate the performance of other algorithms. Researchers use offline workload traces from actual OS environments to measure how close their practical algorithms (like LRU variants) get to the Optimal baseline.

### 5. SECOND CHANCE (Clock Algorithm)
**Concept:** A modification of FIFO that uses a reference bit to avoid replacing pages that are frequently accessed. When considering a page for replacement, if its bit is 1, it is set to 0 and given a "second chance" while moving to the next.
**OS Analysis:**
- **Usage:** This is the most practical way operating systems approximate LRU with low overhead, as it relies on hardware "use bits" provided by typical MMUs (Memory Management Units).
- **Real-World Examples:** Variations of the Clock algorithm (Second Chance) are ubiquitous. The **Windows NT/10** working set manager evaluates pages similar to a clock algorithm. Older versions of **Unix** and **Linux** extensively use multi-hand clock algorithms where a sweeping pointer checks and clears reference bits set by the hardware.

---

## Sample Outputs & Manual Computations

> **Instructions:** Run `page_replacement.py` and capture screenshots for both the standard simulator output and the "Textbook Manual Calculation Grid". Repeat this with at least two different inputs (e.g. changing the number of frames or string length) for each algorithm below.

### FIFO Output
**CLI Output Simulation:**
*(Insert Screenshot 1 Here)*
*(Insert Screenshot 2 Here)*

**Manual Computation Verification:**
*(Insert Screenshot of the Textbook Manual Calculation Grid)*

### LRU Output
**CLI Output Simulation:**
*(Insert Screenshot 1 Here)*
*(Insert Screenshot 2 Here)*

**Manual Computation Verification:**
*(Insert Screenshot of the Textbook Manual Calculation Grid)*

### MRU Output
**CLI Output Simulation:**
*(Insert Screenshot 1 Here)*
*(Insert Screenshot 2 Here)*

**Manual Computation Verification:**
*(Insert Screenshot of the Textbook Manual Calculation Grid)*

### OPTIMAL Output
**CLI Output Simulation:**
*(Insert Screenshot 1 Here)*
*(Insert Screenshot 2 Here)*

**Manual Computation Verification:**
*(Insert Screenshot of the Textbook Manual Calculation Grid)*

### SECOND CHANCE Output
**CLI Output Simulation:**
*(Insert Screenshot 1 Here)*
*(Insert Screenshot 2 Here)*

**Manual Computation Verification:**
*(Insert Screenshot of the Textbook Manual Calculation Grid)*

---

## References

1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). John Wiley & Sons. 
2. Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems* (4th ed.). Pearson.
3. Arpaci-Dusseau, R. H., & Arpaci-Dusseau, A. C. (2018). *Operating Systems: Three Easy Pieces*. Arpaci-Dusseau Books.
4. Bovet, D. P., & Cesati, M. (2005). *Understanding the Linux Kernel* (3rd ed.). O'Reilly Media.
5. Russinovich, M. E., Solomon, D. A., & Ionescu, A. (2012). *Windows Internals, Part 2* (6th ed.). Microsoft Press.
