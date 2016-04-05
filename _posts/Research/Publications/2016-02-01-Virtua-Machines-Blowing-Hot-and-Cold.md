---
layout     : publication
categories : publications
title      : "Virtual Machine Warmup Blows Hot and Cold"
date       : 2016-02-01
journal    : arXiv
authors    : Edd Barrett, Carl Friedrich Bolz, Rebecca Killick, Vincent Knight, Sarah Mount, Laurence Tratt
keywords   : statistics, virtual machines, programming
pub_url    : "https://arxiv.org/abs/1602.00602"
comments   : true
---

The abstract is:

Virtual Machines (VMs) with Just-In-Time (JIT) compilers are traditionally
thought to execute programs in two phases: first the warmup phase determines
which parts of a program would most benefit from dynamic compilation; after
compilation has occurred the program is said to be at peak performance. When
measuring the performance of JIT compiling VMs, data collected during the
warmup phase is generally discarded, placing the focus on peak performance. In
this paper we run a number of small, deterministic benchmarks on a variety of
well known VMs. In our experiment, less than one quarter of the benchmark/VM
pairs conform to the traditional notion of warmup, and none of the VMs we
tested consistently warms up in the traditional notion. This raises a number of
questions about VM benchmarking, which are of interest to both VM authors and
end users.

The paper is on the arXiv, you can read it here:
[arxiv.org/abs/1602.00602](https://arxiv.org/abs/1602.00602).
