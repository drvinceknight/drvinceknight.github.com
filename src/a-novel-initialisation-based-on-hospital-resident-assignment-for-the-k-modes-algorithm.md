---
authors:
- Henry Wilde
- Vincent Knight
- Jon Gillard
details: Soft Computing, 27, pp. 9441–9457
direct_url: https://link.springer.com/article/10.1007/s00500-023-08407-2
keywords:
- machine learning
- clustering
- optimisation
- combinatorial algorithms
- hospital-resident assignment
preprint_direct_url: https://arxiv.org/abs/2002.02701
published_date: 2023
cover_image: /assets/thumbnails/k-modes.png
tags:
- article
title: A novel initialisation based on hospital-resident assignment for the k-modes
  algorithm
---

This paper presents a new way of selecting an initialisation for the k-modes algorithm
that allows for a notion of game theoretic fairness that classic initialisations,
namely those by Huang and Cao, do not. Our new method utilises the hospital-resident
assignment problem to find the set of initial cluster centroids which we compare with
two classical initialisation methods for k-modes: the original presented by Huang and
the next most popular method of Cao and co-authors. To highlight the merits of our
proposed method, two stages of analysis are presented. It is demonstrated that the
proposed method is often able to offer computational speed-up of the order of 50%. Improved
clustering, in terms of a commonly used cost-function, was witnessed in several cases
and can be of the order of 10%, particularly for more complex datasets.

```bibtex
@article{wilde2023novel,
  title   = {A novel initialisation based on hospital-resident assignment for
             the {k}-modes algorithm},
  author  = {Wilde, Henry and Knight, Vincent A. and Gillard, Jonathan},
  journal = {Soft Computing},
  volume  = {27},
  pages   = {9441--9457},
  year    = {2023},
  doi     = {10.1007/s00500-023-08407-2},
}
```