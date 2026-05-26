---
authors:
- Henry Wilde
- Vincent Knight
- Jon Gillard
details: Applied Intelligence
direct_url: https://link.springer.com/article/10.1007/s10489-019-01592-4
keywords:
- machine learning
- evolutionary algorithms
- optimisation
- clustering
- data science
preprint_direct_url: https://arxiv.org/abs/1907.13508
published_date: 2020
tags:
- article
title: 'Evolutionary Dataset Optimisation: Learning algorithm quality through evolution'
---

**Abstract:** In this paper we propose a novel method for learning how algorithms perform.
Classically, algorithms are compared on a finite number of existing (or newly simulated)
benchmark datasets based on some fixed metrics. The algorithm(s) with the smallest value
of this metric are chosen to be the best performing. We offer a new approach to flip
this paradigm. We instead aim to gain a richer picture of the performance of an
algorithm by generating artificial data through genetic evolution, the purpose of which
is to create populations of datasets for which a particular algorithm performs well on a
given metric. These datasets can be studied so as to learn what attributes lead to a
particular progression of a given algorithm. Following a detailed description of the
algorithm as well as a brief description of an open source implementation, a case study
in clustering is presented. This case study demonstrates the performance and nuances of
the method which we call Evolutionary Dataset Optimisation. In this study, a number of
known properties about preferable datasets for the clustering algorithms known as
k-means and DBSCAN are realised in the generated datasets.

```bibtex
@article{wilde2020evolutionary,
  title   = {Evolutionary Dataset Optimisation: learning algorithm quality
             through evolution},
  author  = {Wilde, Henry and Knight, Vincent A. and Gillard, Jonathan},
  journal = {Applied Intelligence},
  volume  = {50},
  number  = {4},
  pages   = {1172--1191},
  year    = {2020},
  doi     = {10.1007/s10489-019-01592-4},
}
```