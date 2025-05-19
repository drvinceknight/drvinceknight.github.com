---
layout: post
title: "Python for Mathematics Book"
date: 2025-05-19
comments: true
---

Over the weekend, I received my author copies of _Python for Mathematics_.

As I posted over on [Mastodon](https://fosstodon.org/@vinceknight):

> I'm quite proud of this book. It’s the result of learning from the Python community and from years of working with first-year mathematics students.
>
> The publisher was great and worked with me to ensure there’s an online version of the book, which you can find (in its current form) here: [https://vknight.org/pfm/cover.html](https://vknight.org/pfm/cover.html).  
> That version still needs a bit of updating — getting the print version ready took priority — but I’ll be sorting that out soon.

In the opening chapter (which isn’t yet updated online), I talk about how this book takes a different route than most programming texts. It essentially flips the usual order in which topics are introduced:

A traditional structure might look more like this:

1. [Using Notebooks](https://vknight.org/pfm/tools-for-mathematics/01-using-notebooks/introduction/main.html)
2. Variables – covered in [Chapter 10](https://vknight.org/pfm/building-tools/01-variables-conditionals-loops/introduction/main.html)
3. Conditionals – also in [Chapter 10](https://vknight.org/pfm/building-tools/01-variables-conditionals-loops/introduction/main.html)
4. Loops – again, [Chapter 10](https://vknight.org/pfm/building-tools/01-variables-conditionals-loops/introduction/main.html)
5. Functions – covered in [Chapter 11](https://vknight.org/pfm/building-tools/02-functions-and-data-structures/introduction/main.html)
6. Data structures – also in [Chapter 11](https://vknight.org/pfm/building-tools/02-functions-and-data-structures/introduction/main.html)
7. Recursion – [Chapter 7](https://vknight.org/pfm/tools-for-mathematics/07-sequences/introduction/main.html)
8. Objects – [Chapter 12](https://vknight.org/pfm/building-tools/03-objects/introduction/main.html)
9. SymPy – drawing on content from [Chapters 2–4](https://vknight.org/pfm/tools-for-mathematics/02-algebra/introduction/main.html) and [9](https://vknight.org/pfm/tools-for-mathematics/09-differential-equations/introduction/main.html)
10. Combinatorics – [Chapter 5](https://vknight.org/pfm/tools-for-mathematics/05-combinations-permutations/introduction/main.html)
11. Probability – [Chapter 6](https://vknight.org/pfm/tools-for-mathematics/06-probability/introduction/main.html)
12. Statistics – [Chapter 8](https://vknight.org/pfm/tools-for-mathematics/08-statistics/introduction/main.html)
13. Command line – [Chapter 13](https://vknight.org/pfm/building-tools/04-editor-and-cli/introduction/main.html)
14. Modularisation – [Chapter 14](https://vknight.org/pfm/building-tools/05-modularisation/introduction/main.html)
15. Documentation – [Chapter 15](https://vknight.org/pfm/building-tools/06-documentation/introduction/main.html)
16. Testing – [Chapter 16](https://vknight.org/pfm/building-tools/07-testing/introduction/main.html)

Instead, the book takes this different path on purpose:

> “The choice to _flip_ this structure and start with real use cases (and not code recipes) is deliberate.  
> The tools covered in Chapters 2 to 9 can be used with little to no programming knowledge — they mostly require just some maths.”

> “After that, the programming basics in Chapters 10 to 12 help build on that experience,  
> and the topics in Chapters 13 to 16 give a taste of how modern research software is built.”

This structure reflects how my own approach to teaching programming has evolved. Rather than starting with the basics and asking students to believe that these abstract pieces will come together _eventually_, I try to start by showing what’s already possible — right now — using powerful, existing tools.

Another way to frame it might be: I’m not flipping the structure at all. I’m just starting with the bit that’s often missing.

And one more point about this book:

> **I don’t think universities should (ethically) be teaching commercial software —  
> I’ll write up more thoughts on that at some point.**

But really, we don’t have to — at least not in my field (others may vary).  
The tools in this book are freely available, easy to use, and just as powerful.  
I don’t even go into some of the other incredible tools out there like [SageMath](https://www.sagemath.org),  
or domain-specific libraries like [Ciw for queuing processes](https://ciw.readthedocs.io).
