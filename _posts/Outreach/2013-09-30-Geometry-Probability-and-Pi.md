---
layout        : page
categories    : outreach
title : Geometry, Probability and pi
keywords      : outreach, pi, geometry
comments      : false
---

### Requirements:

Sufficient copies of the [grid.pdf](http://drvinceknight.github.io/GeometryProbabilityandPi/grid.pdf) file and ten sided dice (depending on numbers students can be paired up).


### Instructions

The activity starts with a rather cryptic set of instructions:

1. Roll dice so as to obtain random coordinates for 10 points;
2. Place these points on the grid (don't worry where they go in the boxes);
3. Count the points that sit within the circle and perform the requested calculations.

Once this is done, ask the students what values they have obtained and if they know what this might be about?

Keep track of the numbers of the board and finally carry out a calculation over the total number of points.


### Explanations

As a group explain that probability of any given point landing in the circle is given by:

$$P(\text{point in circle})=\frac{\text{Area of circle}}{\text{Area of square}}$$

If we let \\(r\\) denote the radius of the circle this gives:

$$P(\text{point in circle})=\frac{\pi r^2}{(2r)^2}=\frac{\pi}{4}$$

Our data however gives us an **estimate** of \\(P(\text{point in circle})\\):

$$P(\text{point in circle})\approx \frac{n}{N}$$

Thus we have:

$$\pi\approx 4\frac{n}{N}$$

At this point ask if what would make the experiment everyone did better? (Answer: more data).


### Code

Ideally some students might realise that another approach to doing this would be to get a computer to calculate this for us.
The following is some [Sage](http://sagemath.org/) code that will simulate the points and plot them as well:

    def simpoints(N=1000):
        """
        Defines a function that will simulate N points
        """
        points = [[2 * (random() - .5), 2 * (random() - .5)] for k in range(N)]  # Create all our points
        pointsincircle = [k for k in points if k[0] ^ 2 + k[1] ^ 2 <= 1]  #  Count the ones that are in the circle
        p = list_plot(pointsincircle, color='blue')  # Plot the ones in the circle in blue
        p += list_plot([k for k in points if k not in pointsincircle], color='black')  # Plot the others in black
        p.show()  # Show the plot
        return 4 * len(pointsincircle) / N  # Return the approximated value of pi

    simpoints(1000)  # Run the above for 1000 points


### Alternative

As can be seen in the following gif this **is not** an efficient way of calculating pi:

![](http://drvinceknight.github.io/EmbeddedEnterpriseExchange/Images/darts.gif)

Here is a formula by Srinivasa Ramanujan (1887-1920) that is much more efficient:

$$\pi = \frac{9801}{\sqrt{8}}\left(\sum_{k=0}^{\infty}\frac{(4k)!(1103+26390k)}{(k!)^4396^{4k}}\right)^{-1}$$

The following Sage code shows that just the first two terms of our sum give a great approximation of \\(\pi\\):

    k = var('k')
    f = lambda n : 9801 / sqrt(8) * (sum((factorial((4*k))*(1103 + 26390 * k))/((factorial(k))^4 * 396 ^ (4 * k)),k,0,n))^(-1)
    float(f(1))

