# Candidate work for Verizon computer vision C++ job

This repository contains work just to convince www.Verizon.com to hire me for a contract job they currently have open.

- Verizon-created computer vision programming challenge [here](challenge/challenge.md).
- Super Smash Bros. computer vision pipeline demonstration
- Verizon-specific writeup [here](verizon.md).

## Models

- Binary classification, whether or not gameplay footage is present (menu,
  stages, etc.)

- Multiclassification stages: 26 stages

- Multiclassification stages and characters

- Multiclassification character moves


## Docker demonstration

```
git clone https://github.com/mavas/verizon
cd verizon
docker build -t verizon .
```
