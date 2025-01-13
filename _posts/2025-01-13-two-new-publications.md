---
layout: post
title: "Properties of winning strategies"
date: 2025-01-13
categories: research
comments: true
---

Over the Christmas period my co-authors and I got news of the acceptance of a
paper:

["Properties of winning Iterated Prisoner's Dilemma strategies"](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012644&?utm_id=plos111&utm_source=internal&utm_medium=email&utm_campaign=author). u
This the last paper from [Dr. Glynatsi](https://nikoleta-v3.github.io)'s PhD thesis. It is quite a neat piece
of work as it revisits Axelrod's original rules for good performance in the
Iterated Prisoners Dilemma. Whereas Axelrod's rules were somewhat of a
generalisation from the particular: he ran 2 tournaments that were quite similar. The work in this paper
does the opposite as it makes use of the [Axelrod library](https://github.com/Axelrod-Python/Axelrod) to generate a [dataset](https://zenodo.org/records/10246248)
of 45,686 tournaments without different combinations of strategies, different
number of players and different tournament parameters (turn length, noise
etc...). This dataset was then analysed to conclude with the following guidelines:

1. Be "nice" in non-noisy environments or when game lengths are longer
2. Be provocable in tournaments with short matches, and generous in tournaments with noise
3. Be a little bit envious
4. Be clever
5. Adapt to the environment (including the population of strategies).
