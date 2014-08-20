---
layout        : page
categories    : outreach
title : Geometry, Probability and Integration
keywords      : outreach, integration, geometry
comments      : false
---

### Requirements:

Sufficient copies of the [grid.pdf](http://drvinceknight.github.io/GeometryProbabilityandIntegration/grid.pdf) file and ten sided dice (depending on numbers students can be paired up).


### Instructions

The activity starts with a rather cryptic set of instructions:

1. Roll dice so as to obtain random coordinates for 10 points;
2. Place these points on the grid (don't worry where they go in the boxes);
3. Count the points that sit under the curve.

Once this is done, ask the students what values they have obtained and if they know what this might be about?

Keep track of the numbers of the board and finally carry out a calculation over the total number of points.


### Explanations

As a group explain that probability of any given point landing under the curve is given by:

$$P(\text{point under curve})=\frac{\text{Area under curve}}{\text{Area of square}}$$

As the square is taken to have length 1 this gives:

$$P(\text{point under curve})=\text{Area under curve}$$

Our data however gives us an **estimate** of \\(P(\text{point under curve})\\):

$$P(\text{point under curve})\approx \frac{n}{N}$$

Thus we have:

$$\int_{0}^{1}1-x^2\approx \frac{n}{N}$$

At this point ask if what would make the experiment everyone did better? (Answer: more data).


### Code

Ideally some students might realise that another approach to doing this would be to get a computer to calculate this for us.
The following is some [Sage](http://sagemath.org/) code that will simulate the points and plot them as well:

    def simpoints(N=1000):
        """
        Defines a function that will simulate N points
        """
        points = [[random() , random()] for k in range(N)]  # Create all our points
        pointsundercurve = [k for k in points if 1 - k[0] ^ 2  >= k[1]]  #  Count the ones that are in the circle
        p = list_plot(pointsundercurve, color='blue')  # Plot the ones in the circle in blue
        p += list_plot([k for k in points if k not in pointsundercurve], color='black')  # Plot the others in black
        p.show()  # Show the plot
        return len(pointsundercurve) / N  # Return the approximated value of pi

    simpoints(1000)  # Run the above for 1000 points
