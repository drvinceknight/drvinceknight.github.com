---
comments: true
date: 2026-11-25
cover_image: /assets/thumbnails/traitors-paper.png
tags:
  - post
  - article
title: "Vote-Left: A Deterministic Coordination Strategy for the Faithful in The Traitors"
published_date: 2026
authors:
  - Vincent Knight
preprint_direct_url: https://arxiv.org/abs/2605.10233
---

In May I [posted a preprint](/posts/2026-05-12-traitors-paper/) about how the
Faithful should vote in [The Traitors][traitors]. I have just posted a new version,
and it corrects the main result of the first one.

The idea is the same: everyone votes for the next player in an agreed order (for
example the person to their left), so every player gets exactly one vote and the
tie-break picks someone at random. That gives the same outcome as random voting,
but anyone who breaks the rule is seen straight away and can be voted out the next
day.

The first version claimed that nobody could ever do better by breaking this rule.
A referee read the paper carefully and sent back two short counterexamples showing
that this was wrong. Near the end of the game the punishment arrives too late: a
player can break the rule and win before anyone gets to vote them out.

The fix is simple. Vote left during most of the game, and once there are at most
$2m + 2$ players left (where $m$ is the number of Traitors still in), go back to
voting at random. With that switch:

1. Nobody gains by breaking the rule before the last few rounds, whether alone or
   with the other Traitors.
2. With a single Traitor left, the protocol is an equilibrium of the whole game.
3. Against colluding Traitors, the Faithful are about four times as likely to win
   with three Traitors, and between 62 and 84 times as likely with four.

What the Faithful should do in the last few rounds when there are two or more
Traitors is still open.

All the numbers in the paper are now exact, thanks to a new algorithm in
[backstab](https://vknight.org/backstab/) (version 0.2.1). The data and code are
[on Zenodo](https://doi.org/10.5281/zenodo.24528818).

I am very grateful to the referee. Only one person agreed to review the paper, and
they found the hole in the main theorem and handed me two clean examples of it.
That is peer review working exactly as it should.

You can read the new version [here](https://arxiv.org/abs/2605.10233).

I have also recorded a [short video](https://youtu.be/8UsLF8RT3dU) that walks
through the revised result:

<iframe
  style="width: 100%; aspect-ratio: 16 / 9; border: 0;"
  src="https://www.youtube-nocookie.com/embed/8UsLF8RT3dU"
  title="Vote-Left: A Deterministic Coordination Strategy for the Faithful in The Traitors"
  allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowfullscreen></iframe>

[traitors]: https://www.bbc.co.uk/showsandtours/take-part/the-traitors

```bibtex
@misc{knight2026vote,
  title         = {Vote-Left: A Deterministic Coordination Strategy for the
                   Faithful in {The Traitors}},
  author        = {Knight, Vincent A.},
  year          = {2026},
  eprint        = {2605.10233},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2605.10233},
}
```
