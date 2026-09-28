---
type: concept
track: [quant-dev]
tier: core
status: seed
prereqs: [order-book-and-matching-engine]
est_hours: 4
sources: []
---

# Market Data Feed Handlers and Protocols

> [!info] Seed note
> Not written yet. The objectives below define what "done" looks like; use the references to study it now.

## Learning objectives

- Parse ITCH, OUCH, FIX and SBE messages and rebuild books from incremental feeds.
- Handle gaps, A/B arbitration, snapshots and recovery.

## In this repo and SDE-Interview-Prep

- Protocol guides in this repo: [ITCH](../08-Market-Making/Quant-Dev-MM-Guide/07_ITCH_Protocol_Mastery_Guide.md), [OUCH](../08-Market-Making/Quant-Dev-MM-Guide/08_OUCH_Protocol_Mastery_Guide.md), [FIX](../08-Market-Making/Quant-Dev-MM-Guide/09_FIX_Protocol_Mastery_Guide.md); specs in [protocol-specs](protocol-specs/).
- Code: [itch_parser_mock.py](code/python/itch_parser_mock.py) and [udp_receiver_mock.cpp](code/cpp/udp_receiver_mock.cpp).
- [UDP multicast and A/B arbitration (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/06%20-%20Networking/UDP%20Multicast%20Market%20Data%20and%20A-B%20Feed%20Arbitration.md)
- [Lab: zero-copy ITCH parser (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/10%20-%20Protocols%20%26%20Codecs/Lab%20-%2010%20Zero-Copy%20NASDAQ%20ITCH%205.0%20Parser.md)
