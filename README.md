# Thread-Level Parallelism (TLP) in Shared-Memory Multiprocessors

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20WSL-green.svg)](https://docs.microsoft.com/en-us/windows/wsl/)
[![Gem5](https://img.shields.io/badge/simulator-gem5-orange.svg)](https://www.gem5.org/)
[![Language](https://img.shields.io/badge/language-C%20%7C%20Python-blue.svg)](https://github.com/avrulesyou/Thread-Level-Parallelism-TLP-in-Shared-Memory-Multiprocessors)

A comprehensive exploration of Thread-Level Parallelism (TLP) in shared-memory multiprocessors using the gem5 simulator. This project investigates the performance characteristics of multi-threaded workloads and analyzes the trade-offs between operation latency and issue latency in functional units.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
- [Building and Running](#building-and-running)
- [Simulation Results](#simulation-results)
- [Performance Analysis](#performance-analysis)
- [Key Findings](#key-findings)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This assignment explores Thread-Level Parallelism (TLP) through two main components:

1. **Critical Review**: An in-depth analysis of contemporary TLP research, covering historical development, core concepts, current challenges, and future directions
2. **Practical Implementation**: Simulation of multi-threaded DAXPY kernels using gem5 to investigate functional unit design trade-offs

### Key Research Questions
- How do operation latency (opLat) and issue latency (issueLat) affect multi-threaded performance?
- What is the optimal functional unit configuration for parallel workloads?
- How does thread count impact performance scalability?

## 📁 Project Structure

```
Thread-Level-Parallelism-TLP-in-Shared-Memory-Multiprocessors/
├── README.md                 # This file
├── daxpy_multi.c            # Multi-threaded DAXPY implementation
├── hello.c                  # Simple test program
├── multicore_config.py      # Gem5 configuration script
```

### Core Files Description

| File | Description |
|------|-------------|
| `daxpy_multi.c` | Multi-threaded DAXPY kernel with configurable thread count |
| `multicore_config.py` | Gem5 configuration script for multicore simulation |
| `hello.c` | Simple validation program for gem5 setup |

## 🛠 Environment Setup

### Prerequisites

- **Operating System**: Windows 11 with WSL (Windows Subsystem for Linux)
- **Linux Distribution**: Ubuntu (recommended)
- **Dependencies**: Python 3.x, GCC, build tools

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/avrulesyou/Thread-Level-Parallelism-TLP-in-Shared-Memory-Multiprocessors.git
   cd Thread-Level-Parallelism-TLP-in-Shared-Memory-Multiprocessors
   ```

2. **Install Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install python3-dev libprotobuf-dev m4 gcc g++ make
   ```

3. **Build gem5 Simulator**
   ```bash
   # Navigate to gem5 directory
   cd gem5
   
   # Build for X86 architecture
   scons build/X86/gem5.opt -j$(nproc)
   
   # Verify build
   ./build/X86/gem5.opt --version
   ```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing Python headers | `sudo apt-get install python3-dev` |
| Missing protobuf | `sudo apt-get install libprotobuf-dev` |
| Missing M4 macro processor | `sudo apt-get install m4` |
| Build fails with dependencies | Ensure all build tools are installed: `sudo apt-get install build-essential` |

## 🚀 Building and Running

### Compiling the DAXPY Program

```bash
# Compile with default 4 threads
gcc -o daxpy_multi daxpy_multi.c -lpthread

# Compile with custom thread count
gcc -DNUM_THREADS=8 -o daxpy_multi_8t daxpy_multi.c -lpthread

# Compile hello program
gcc -o hello hello.c
```

### Running Simulations

```bash
# Basic simulation with 2 cores
python3 multicore_config.py --num-cpus 2 --cmd ./daxpy_multi

# Advanced simulation with custom FU latencies
python3 multicore_config.py \
    --num-cpus 4 \
    --opLat 1 \
    --issueLat 6 \
    --cmd ./daxpy_multi

# Run hello validation
python3 multicore_config.py --num-cpus 1 --cmd ./hello
```

### Configuration Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `--num-cpus` | Number of CPU cores | 1 | 1-8 |
| `--opLat` | Operation latency for FloatSimdFU | 4 | 1-10 |
| `--issueLat` | Issue latency for FloatSimdFU | 4 | 1-10 |
| `--cmd` | Workload to execute | Required | Any executable |

## 📊 Simulation Results

### Performance Metrics Summary

The following table presents unified performance results across different functional unit configurations:

| FU Config (opLat, issueLat) | 2 Threads | 4 Threads | 8 Threads |
|----------------------------|-----------|-----------|-----------|
| | Sim Ticks (×10³) | Speedup | IPC | Sim Ticks (×10³) | Speedup | IPC | Sim Ticks (×10³) | Speedup | IPC |
| **(6, 1)** | 145,230 | 1.71× | 0.85 | 99,870 | 2.48× | 0.89 | 76,440 | 3.24× | 0.91 |
| **(4, 3)** | 139,880 | 1.77× | 0.91 | 98,654 | 2.51× | 0.94 | 74,990 | 3.30× | 0.95 |
| **(1, 6)** | 132,540 | 1.87× | 0.96 | 88,110 | 2.81× | 1.02 | 69,500 | 3.56× | 1.05 |

*Baseline single-threaded execution: 248,300,000 ticks*

## 📈 Performance Analysis

### Key Observations

1. **Issue Latency Dominance**: Lower `issueLat` values consistently outperform higher ones across all thread counts
2. **Scalability Trends**: Performance shows diminishing returns beyond 4 threads due to memory system pressure
3. **IPC Improvement**: Instruction Per Cycle (IPC) increases with deeper pipelining (lower `issueLat`)

### Performance Characteristics

```mermaid
graph LR
    A[Low issueLat] --> B[Deep Pipelining]
    B --> C[High Instruction Throughput]
    C --> D[Better TLP Utilization]
    D --> E[Higher Speedup]
```

### Optimal Configuration

**Best Performance**: `opLat=1, issueLat=6`
- **Maximum Speedup**: 3.56× with 8 threads
- **Highest IPC**: 1.05 across all configurations
- **Reasoning**: Deep pipelining enables rapid instruction acceptance from multiple threads

## 🔍 Key Findings

### 1. Functional Unit Design Impact
- **Issue latency** is more critical than operation latency for multi-threaded workloads
- Deep pipelining (low `issueLat`) maximizes instruction throughput
- Optimal configuration achieves 3.56× speedup with 8 threads

### 2. Scalability Limitations
- Performance plateaus around 4 threads due to memory system bottlenecks
- Cache coherence overhead becomes significant with higher core counts
- Amdahl's Law limitations become apparent with increased parallelism

### 3. Workload Distribution
- Fixed a critical bug in workload distribution ensuring all vector elements are processed
- Proper thread synchronization prevents race conditions and data corruption

### 4. Real-World Implications
- Results suggest that modern processors should prioritize instruction issue rate over single-instruction latency
- Memory system design becomes the primary bottleneck in many-core systems
- Software optimization must consider both parallelism and memory access patterns

## 🎓 Academic Context

This project addresses key concepts in **MSCS-531: Computer Architecture and Design**:

- **Thread-Level Parallelism**: Understanding parallel execution models
- **Shared-Memory Architectures**: Cache coherence and synchronization
- **Performance Evaluation**: Metrics and analysis methodologies
- **Simulation-Based Research**: Using gem5 for architectural exploration

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow C coding standards for new implementations
- Add comprehensive comments for complex algorithms
- Include test cases for new functionality
- Update documentation for significant changes

## 📚 References

1. **Gem5 Simulator**: [Official Documentation](https://www.gem5.org/documentation/)
2. **Thread-Level Parallelism**: Modern processor design principles
3. **Shared-Memory Architectures**: Cache coherence protocols and synchronization
4. **Performance Analysis**: Metrics and evaluation methodologies

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Abhishek Vishwakarma**
- **Course**: MSCS-531 - Computer Architecture and Design
- **Instructor**: Dr. Vanessa Cooper
- **Institution**: University of the Cumberlands
- **Semester**: Fall 2025

---

*For questions or support, please open an issue on GitHub or contact the author.*

## 🏷 Keywords

`Thread-Level Parallelism`, `TLP`, `Shared-Memory`, `Multiprocessors`, `gem5`, `Computer Architecture`, `Performance Analysis`, `Multi-threading`, `DAXPY`, `Functional Units`, `Latency`, `Throughput`
