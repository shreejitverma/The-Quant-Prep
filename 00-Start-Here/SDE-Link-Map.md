---
type: guide
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
sources: []
---

# SDE-Interview-Prep Link Map

This repo owns quantitative finance: probability, statistics, pricing, microstructure, market making, alpha research, risk and firm preparation.
[SDE-Interview-Prep](https://github.com/shreejitverma/SDE-Interview-Prep) owns general software engineering: data structures and algorithms, languages, system design, low-latency systems and behavioural preparation.
Nothing is copied between the two repos; this page is the bridge.

Links point at `https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/...`, so they work on GitHub and in any browser.
`./qp check` verifies every such link against your local clone (`SDE_REPO`, default `../SDE-Interview-Prep`), so a rename in that repo shows up here as a failing check.

## By role

| You are preparing for | Study here | Study in SDE-Interview-Prep |
| :--- | :--- | :--- |
| Quant trader | Sections 01, 05, 07, 08, 11, 13 | Coding screens only: [DSA topics](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/03-Data-Structures-Algorithms/01-Topics/README.md) |
| Quant researcher | Sections 01-04, 09, 10, 13 | [Python advanced guide](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/Python/Ultimate-Python-Advanced-Guide.md), [LeetCode quant set (Python)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/Python/LeetCode-Quant-Complete-Python-Full.md) |
| Quant developer | Sections 07, 08, 12 plus the maths the desk uses | Most of it: see below |

## Quant developer: what to take from SDE-Interview-Prep

### Languages

- [C++ advanced guide](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/Ultimate-CPP-Advanced-Guide.md) and the [STL reference](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/stl_complete_reference.md).
- [C++ design patterns](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/Ultimate-CPP-Design-Patterns.md).
- [Python advanced guide](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/Python/Ultimate-Python-Advanced-Guide.md).

### Data structures and algorithms

- [Topics by pattern](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/03-Data-Structures-Algorithms/01-Topics/README.md).
- [LeetCode quant set in C++](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/LeetCode-Quant-Complete-CPP-Full.md) and [in Python](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/Python/LeetCode-Quant-Complete-Python-Full.md).
- [NeetCode 150 in C++](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/NeetCode-150-CPP.md).

### Low-latency systems vault

The [low-latency vault home](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/00%20Home.md) is the deep reference for trading infrastructure. The most interview-relevant notes:

- [Latency numbers every trading engineer knows](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/04%20-%20Hardware%20Mechanical%20Sympathy/Latency%20Numbers%20Every%20Trading%20Engineer%20Knows.md).
- [C++ memory model and memory orders](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/08%20-%20Low-Latency%20Programming/C%2B%2B%20Memory%20Model%20and%20Memory%20Orders.md).
- [Lock-free SPSC ring buffer design](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/08%20-%20Low-Latency%20Programming/Lock-Free%20SPSC%20Ring%20Buffer%20Design.md).
- [Order book data structures](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/03%20-%20Matching%20Engine%20Internals/Order%20Book%20Data%20Structures.md).
- [The sequenced-stream architecture](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/02%20-%20Exchange%20Architecture/The%20Sequenced-Stream%20Architecture.md).
- [Pre-trade risk checks at wire speed](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/02%20-%20Exchange%20Architecture/Pre-Trade%20Risk%20Checks%20at%20Wire%20Speed.md).
- [UDP multicast and A/B feed arbitration](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/06%20-%20Networking/UDP%20Multicast%20Market%20Data%20and%20A-B%20Feed%20Arbitration.md).
- [Coordinated omission](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/07%20-%20Time%20%26%20Measurement/Coordinated%20Omission%20in%20Low%20Latency%20Systems.md).

### System design and performance

- [System design](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/04-System-Design/README.md).
- [Performance engineering](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/12-Performance-Engineering/README.md) and the [profiling guide](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/12-Performance-Engineering/02-Profiling/profiling_guide.md).

## Everyone: behavioural and application

- [STAR method](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/06-Interview-Prep/01-Behavioral/star_method.md).
- [Resume guide](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/06-Interview-Prep/02-Resume/resume_guide.md).
- Role hubs with skill matrices and question banks: [Quant Dev](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/16-Interview-Command-Center/01-Roles/Quant-Dev/_Hub.md) and [Quant Research](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/16-Interview-Command-Center/01-Roles/Quant-Research/_Hub.md).

## Ownership rule

When a note would fit both repos, it lives where its core skill lives: a pricing model belongs here even if its code is C++; a lock-free queue belongs in SDE-Interview-Prep even though trading firms ask about it.
Bridge notes in [12-Quant-Development](../12-Quant-Development/README.md) summarise what a quant developer needs and link across.
