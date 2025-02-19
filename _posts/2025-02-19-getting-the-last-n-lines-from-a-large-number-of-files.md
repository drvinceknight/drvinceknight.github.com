---
layout: post
title: "Getting specific contents of a large number of files"
date: 2025-02-18
comments: true
---

This is a short post showing how to `cat` the contents of a large number of
files (too large to use a standard approach) to a file.

The command is:

```python
$ find data/ -type f -exec tail -n+2 {} \; > main.csv
```

This will search through all the files in `data`, execute the `tail` command and
skip the first line (perhaps a header) and then cat it in to `main.csv`.
