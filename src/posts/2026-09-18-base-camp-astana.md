---
comments: true
date: 2026-09-18
tags:
  - post
title: 'Base Camp: nine days of mathematics in Astana'
---

I have just finished two weeks teaching in Astana, the opening nine days
of the science foundation year (for Computer Science, Civil Engineering and
Geology students) at Cardiff University's campus in Kazakhstan. I
wrote about my first trip there [in
February](/posts/2026-02-24-teaching-in-qazaqstan/); this time I was back with
a new course I designed with the goal of motivating students and hopefully
having fun.

I called the course Base Camp, constantly emphasising that it was NOT a **boot**
camp. I taught for nine days with the cohort split into two groups, each taught for 110
minutes, so every day runs twice. Everything a student touched was paper, printed
on arrival. No screens were needed.

The structure was four activities, each given two days. On the first day the room
played. On the second day I showed the room what it had done. That tick and tock
was the whole engine: the students made the data and left not knowing what it
said, and I was banking on that being a reason to come back.

I chose the four activities so that in each one the whole room was a single system
that nobody was steering, and so that what I revealed was collective rather than
personal. The room ran its own tournament, drew its own network, caught its own
epidemic, and fed its own common pot. The subject matter and the thing happening
in the room were the same thing.

I never stated the point of an activity before it had been played, and that was
the rule I was strictest with myself about. The reveal has to earn the meaning,
and if I explain first there is nothing left to find out.

Everything is now in [a public repository](https://github.com/drvinceknight/bc): the
day plans, the slides, the printables, and a small Python package that does the
analysis in the reveals. None of it was public while the course was running and
the students never saw any of it ahead of time, which is the whole point: a reveal
only works if nobody has read the ending. The students' own data is not in there,
and none of the reveals ever showed a name.

## Days one and two: cooperation

Pods of five wrote down a strategy for a repeated Prisoner's Dilemma, sealed it,
and handed it in before playing a single round. Forty-two strategies came back,
and I sorted them into families.

![The number of pods writing each kind of strategy: fifteen clever with
conditions, twelve copycats, eight always nasty, four grudge-holders, three always
nice](/assets/static/2026-09-18-base-camp-astana/day1-strategies.png)

Nineteen of the forty-two pods planned to betray on the first move, and ten wrote
a strategy that cooperates the whole way and then betrays on the last turn. Some
of them worked out the arithmetic of that final turn entirely unprompted, which
was a good thing to read at midnight with a stack of forms.

The part I liked most was the prediction each pod made about everybody else.
Twenty-three pods predicted that most pods would betray first. In fact nineteen of
forty-two did, so the room expected each other to be worse than they turned out to
be. When each tribe then picked one strategy to play a round-robin at the front,
five of the nine tribes chose a copycat, and across the twenty matches 63% of all
moves played were cooperation.

## Days three and four: connections

Every student filled in a tick list of thirty-two things that might be true of
them: where they are from, what they play, what they can cook, what they were best
at in school. Two people were joined if they shared at least three of those
things. Nobody drew an edge to a friend: the edges came out of the ticks.

![The morning cohort's network: 104 people in a single connected cloud, coloured
by subject, with computer science, engineering and geology mixed throughout rather
than in separate
clusters](/assets/static/2026-09-18-base-camp-astana/day3-network.png)

The morning group's network had 104 people and 3,345 edges in it. It was a single
connected component with nobody left out, the average person was joined to 64
others, and the longest chain between any two people in the room was three steps.

Before I showed them, each tribe wrote down how many people they thought the
average person would be joined to. The five morning tribes guessed 6, 4, 40, 5 and
5. The answer was 64. They had been in the room together for three days and every
one of them underestimated how much they had in common, most of them by an order
of magnitude.

The colours in that picture are the three subjects, and they are mixed all the way
through. The network did not split by what anybody was there to study, which was
the part I most wanted them to see.

## Days five and six: spread

This was a game of catching something, and the idea for it is originally [Paul
Harper's](/collaborators/paul-harper/) rather than mine. One person started
infectious, a roll of two dice decided whether a meeting passed it on, and you
stayed infectious for three rounds before sitting at the side. We played it twice
and I did not tell them what was different. In Run A you met one person a round.
In Run B you met everybody in your tribe.

![Two panels showing the percentage of each tribe on their feet each round. In Run
A every tribe stays near zero. In Run B every tribe rises to a peak between 35 and
65 per cent around round four and then
falls](/assets/static/2026-09-18-base-camp-astana/day5-epidemic.png)

In Run A, 7 of the 109 students present ever caught it. In Run B, 92 did. Same
disease, same dice, same three rounds of being infectious. The only thing that
changed was how many people you met, and the reproduction number goes with it:
about 0.25 in Run A and about 7 in Run B.

Run B was also the first time most of them had seen a curve that rises and then
falls for a reason other than people getting better. It falls because the disease
runs out of people to give it to.

The second half of the reveal brings back the network from day three. Their own
network is a much better model of how something spreads than a tribe where
everybody meets everybody, so I ran the same epidemic over it and asked the room
who they would vaccinate. Tribes called out badge numbers and we tried them.

The heuristic we ended up comparing them against is a simple one: vaccinate
whoever is joined to the most people who are not yet vaccinated, take them out,
and count again, so a busy person whose friends are already covered drops down the
list.

![The same network twice, with crosses marking the people the heuristic picks.
With twenty vaccinated the crosses sit in the middle of the cloud and 78 of the
other 84 still catch it. With sixty vaccinated most of the centre is crossed out
and 17 of the other 44 catch
it](/assets/static/2026-09-18-base-camp-astana/day6-vaccination.png)

Vaccinating twenty people barely helps: 78 of the remaining 84 still catch it,
against 80 if you had picked twenty people at random. This network is too well
connected for a handful of hubs to matter, with the average person joined to 64
others.

Where the choice does start to pay is further along. At sixty vaccinated, picking
the busiest leaves 17 people catching it, where choosing sixty at random leaves
39. At eighty it is 1 against 18. Who you choose only matters once you are
choosing enough of them, which is not the lesson I expected to be teaching.

## Days seven and eight: the pot

Six pods to a tribe, six dice each, and a pile in the middle. Every round each pod
held out a closed fist with a die in it or not, and all six opened together. A die
kept in your hand is worth three to your pod. A die in the middle is worth one to
every pod in the tribe, so it is worth six in total. Giving is always worse for you
and always better for your tribe, in every round, with no exceptions.

![How many of the six pods gave to the middle in each round, for five tribes and
for the champions at the front. Most tribes fall away within two rounds; the
champions hold at six for four rounds before
collapsing](/assets/static/2026-09-18-base-camp-astana/day7-pot.png)

The five tribes finished with piles of 22, 21, 8, 6 and 3 dice. Two tribes nearly
emptied their hands into the middle and one gave away three dice in total. Every
tribe's last round was its lowest.

The line that surprised me was the dashed one. Those were the champions, one from
each tribe, playing the same game at the front of the room in public with everyone
watching. It was also the only version of the game that paid out: their points
were worth chocolate, one chocolate a point, out of a box sitting where everybody
could see it. I gave out a lot of chocolate.

![An open box of individually wrapped
chocolates](/assets/static/2026-09-18-base-camp-astana/chocolates.jpg){: style="max-width: 320px" }

They gave away 30 of their 36 dice, more than any tribe sitting at a table with
its friends, and they did it with the only real stakes in the room. Every champion
finished on between 30 and 36 points. 

## Day nine: forty players of werewolf

Day nine was deliberately slack. Four activities at two days each fills eight, and
I wanted one spare in case something earlier overran. I also wanted to finish on
something more relaxing than a ninth day of being measured.

So: no data, no sheets, nothing to type. Motived by [my preprint from earlier
this year](/posts/2026-05-12-traitors-paper/) I planned to play some werewolf.
In the morning we played a lot of smaller games with 15 players or so but in 
the afternoon we played a game with 40 players...

![A large circle of students seated around an open floor in the middle of a game
of werewolf](/assets/static/2026-09-18-base-camp-astana/werewolf.jpg)


## What I would change

The two-day rhythm works. The reveal days are the ones students talk about, and
holding back the point of an activity until after it has been played is the single
decision I would keep above all the others.

What I underestimated was the evening. Every capture day ends with me typing up
paper, and on day seven that was fifty slips read one at a time. Some of that
should move to a form next time, though not all of it: there is something about
handing in a sealed piece of paper that a web form does not replicate.

## The students

They were the best part of it. They were curious, motivated and fun to spend two
weeks with.

I am scheduled to return in November and I am looking forward to seeing them.

![A group photograph with some of the students at the end of the last
day](/assets/static/2026-09-18-base-camp-astana/group.jpg)

## Also on this trip

- I recorded some short social media pieces about our [MSc AI + Data
  Science](https://cardiff.edu.kz/courses/artificial-intelligence-and-data-science-msc/)
  at Cardiff. It is a conversion course, so no prior coding is needed:
  applications close on **8 October** and it starts on **25 October**. Filming to
  camera is not something I am naturally good at, but the social media team were
  very patient with me.
- I gave a talk at the [Kazakh University of Technology and Business named after
  K. Kulazhanov](https://www.kaztbu.edu.kz/faculties?locale=en) on the mathematics
  of cooperation from Axelrod to now: the 1980 tournaments, our work replicating
  and extending them, extortion in international trade, *The Traitors*, and a
  queueing model of the handover between ambulance services and emergency
  departments.
- I played basketball with the students. As in February they were faster, fitter
  and considerably more skilful than me, and as in February that is exactly why it
  is fun.

![The basketball group in the sports hall after playing, lined up across the
court](/assets/static/2026-09-18-base-camp-astana/basketball.jpg)
