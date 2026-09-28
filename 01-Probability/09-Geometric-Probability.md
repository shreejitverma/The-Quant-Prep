---
type: concept
track: [quant-trader, quant-research]
tier: advanced
status: solid
prereqs: [joint-distributions-and-transformations]
est_hours: 3
sources: [Mosteller - Fifty Challenging Problems in Probability, Zhou - A Practical Guide to Quantitative Finance Interviews, Blitzstein and Hwang - Introduction to Probability (2nd ed.), Wendel - A Problem in Geometric Probability (Math. Scand. 1962)]
---

# Geometric Probability

## TL;DR

- Uniform points in a region turn probabilities into area (or volume) ratios: draw the sample space, shade the event, divide.
- Broken stick at two uniform points forms a triangle with probability $1/4$: each piece must be shorter than $1/2$.
- $n$ uniform points on a circle lie in a common semicircle with probability $n/2^{n-1}$; three points' triangle contains the centre (is acute) with probability $1/4$.
- Four uniform points on a sphere span a tetrahedron containing the centre with probability $1/8$, by pairing each point with its antipode.
- "Random chord" is ambiguous (Bertrand): the answer depends on the sampling rule, so state the rule before computing.

## Learning objectives

- Solve broken-stick, points-on-a-circle and random-chord problems.
- Use area and volume ratios over the unit square, simplex or cube.
- Use symmetry (antipodal pairing, rotation, exchangeable gaps) to avoid integration.
- Recognise and resolve Bertrand-style ambiguity in "random" geometric objects.

## Core concepts

### Area ratios

If $(X,Y)$ is uniform on a region $R$, then $P((X,Y) \in A) = |A \cap R| / |R|$.
Standard shapes to recognise in the unit square:

- $|X - Y| < t$: the complement is two corner triangles of total area $(1-t)^2$, so the probability is $1 - (1-t)^2$.
- $X + Y < s$ for $s \le 1$: triangle of area $s^2/2$; for $1 \le s \le 2$ it is $1 - (2-s)^2/2$.
- $XY < t$: area $t - t \ln t$, found by integrating $\min(1, t/x)$.
- $X^2 + Y^2 < 1$: quarter disc, $\pi/4$.

In $n$ dimensions, $P(U_1 + \dots + U_n < 1) = 1/n!$, the volume of the corner simplex.
Useful facts: $E|X - Y| = 1/3$ on $[0,1]$, the distance from a uniform point in the unit disc to the centre has density $2r$ and mean $2/3$.

### Gaps on a circle

Drop $n$ uniform points on a circle of circumference 1.
They cut it into $n$ gaps that are exchangeable, each distributed like the min of $n-1$ uniforms (mean $1/n$).
Many circle problems reduce to "is the largest gap bigger than $1/2$?".

The semicircle result: all $n$ points lie in some semicircle iff some point $i$ has all others within the clockwise half-circle starting at $i$.
These $n$ events are disjoint (at most one point can be the "first" of a semicircle containing all), and each has probability $(1/2)^{n-1}$, so

$$
P(\text{all in a semicircle}) = \frac{n}{2^{n-1}} .
$$

For $n = 3$ this is $3/4$, so the triangle contains the centre with probability $1/4$.
A triangle inscribed in a circle is acute iff it contains the centre, so a random inscribed triangle is acute with probability $1/4$.

### Antipodal pairing and Wendel's theorem

Wendel's theorem: $n$ uniform points on the sphere $S^{d-1}$ lie in a common hemisphere with probability $2^{-(n-1)} \sum_{k=0}^{d-1} \binom{n-1}{k}$.
For $d = 2$ it recovers $n/2^{n-1}$; for $d = 3$, $n = 4$ it gives $7/8$, so the tetrahedron contains the centre with probability $1/8$.
The interview proof pairs each point with its antipode (see the worked example).

### Broken sticks

Break $[0,1]$ at $n-1$ uniform points into $n$ pieces.
The pieces are exchangeable, with $E[\text{shortest}] = 1/n^2$ and $E[\text{longest}] = H_n / n$; for three pieces these are $1/9$ and $11/18$, with the middle piece $5/18$.
A triangle needs every piece shorter than half the stick, which fails for exactly one piece at a time.

### Bertrand's paradox

"Pick a random chord of the unit circle. What is the probability it is longer than $\sqrt{3}$, the side of the inscribed equilateral triangle?"

| Sampling rule | Probability |
| :--- | :--- |
| Two uniform endpoints on the circle | $1/3$ |
| Uniform distance from the centre along a random radius | $1/2$ |
| Uniform midpoint in the disc | $1/4$ |

Each rule is a legitimate "uniform" and they disagree, because "uniform" depends on the parametrisation.
The senior answer is to name the paradox, ask which mechanism generates the chord, and solve for that one.

### Buffon's needle

A needle of length $\ell \le d$ dropped on a floor with parallel lines spaced $d$ apart crosses a line with probability $2\ell/(\pi d)$.
The slick proof: by linearity, the expected number of crossings of any rigid curve is proportional to its length; a circle of diameter $d$ always crosses exactly twice and has length $\pi d$, so the constant is $2/(\pi d)$.

## Worked examples

### Broken stick: three versions

"Version 1: break at two independent uniform points $X, Y$. The pieces form a triangle iff each is less than $1/2$."
"In the unit square, the condition carves out two small triangles (one for $X<Y$, one for $X>Y$), each of area $1/8$, so the probability is $1/4$."
"Faster argument: the left piece is the smaller cut point, and it exceeds $1/2$ iff both cuts land in the right half, probability $1/4$."
"The three pieces are exchangeable, so each exceeds $1/2$ with probability $1/4$, and at most one can, so $P(\text{no triangle}) = 3 \times 1/4 = 3/4$."
"Circle trick: close the stick into a circle with three uniform points; no triangle iff the three points lie in a semicircle, $3/4$."
"Version 2: break once, then break the longer piece at a uniform point. With the first break at $x < 1/2$, the long piece is $1-x$ and we need the second cut within $1/2$ of each end, a window of length $x$ out of $1-x$."
"So $P = 2\int_0^{1/2} \frac{x}{1-x}\,dx = 2\ln 2 - 1 \approx 0.386$."
"Version 3: break once, then break a randomly chosen piece. Choosing the short piece never works, so the answer halves to $\ln 2 - 1/2 \approx 0.193$."

### Points on a circle in a semicircle

"Four uniform points on a circle. For point $i$, let $A_i$ be the event that the other three lie within the half-circle clockwise from $i$. That has probability $(1/2)^3$."
"The $A_i$ are disjoint: if all points are in the clockwise semicircle from $i$, then $i$ is the first point, and only one point can be first."
"All four lie in some semicircle iff some $A_i$ holds, so the probability is $4/8 = 1/2$."
"In general $n/2^{n-1}$: $3/4$, $1/2$, $5/16$ for $n = 3, 4, 5$."

### Tetrahedron containing the centre of a sphere

"Pick three random lines through the centre, then choose for each an endpoint, and pick the fourth point $P_4$ independently."
"Fix the fourth point. The three lines give $2^3 = 8$ equally likely sign choices for $P_1, P_2, P_3$."
"The tetrahedron contains the centre iff $-P_4$ lies in the cone spanned by $P_1, P_2, P_3$."
"The 8 cones spanned by $\pm P_1, \pm P_2, \pm P_3$ tile space, so with probability one exactly one sign choice puts $-P_4$ in its cone."
"So the probability is $1/8$."
"The same argument in the plane gives $1/4$ for the triangle, matching the semicircle result."

### Meeting problem

"Two traders each arrive at a uniform time between noon and 1pm and wait 15 minutes. What is the probability they meet?"
"In the unit square with $X, Y$ the arrival times in hours, they meet iff $|X - Y| \le 1/4$."
"The complement is two corner triangles with legs $3/4$, total area $(3/4)^2 = 9/16$, so $P = 7/16 \approx 0.44$."

### Closer to the centre than to the edge

"A point is uniform in the unit square. What is the probability it is closer to the centre than to the nearest side?"
"By the 8-fold symmetry, restrict to the triangle $0 \le y \le x \le 1/2$ with the centre at the origin, where the nearest side is $x = 1/2$."
"The condition $\sqrt{x^2 + y^2} < 1/2 - x$ is the inside of the parabola $x < 1/4 - y^2$."
"The parabola meets $y = x$ at $x = (\sqrt{2} - 1)/2$; integrating the region and multiplying by 8 gives $(4\sqrt{2} - 5)/3 \approx 0.219$."
"Sanity check: the region contains the disc of radius $1/4$ around the centre (area $\pi/16 \approx 0.196$) and is contained in the inscribed disc of radius $1/2$, so $0.219$ is plausible."

## Pitfalls

- Using "random chord" or "random triangle" without fixing the distribution; Bertrand shows the answer is not defined until you do.
- Forgetting that the semicircle events $A_i$ are disjoint only because points are continuous; you cannot use the same union trick for an arc longer than half the circle.
- Breaking a stick "at random twice" can mean independent cuts on the original stick or sequential cuts; the answers are $1/4$, $0.386$ and $0.193$ depending on the rule.
- Integrating over a region without first exploiting symmetry: most interview problems have a 2-, 4- or 8-fold symmetry that turns a messy integral into a triangle.
- Mistaking the distance from a uniform disc point to the centre for uniform on $[0,1]$: its density is $2r$, because area grows like $r^2$.

## Interview questions

> [!question]- prob-geo-broken-stick-triangle | A stick is broken at two independent uniform points. What is the probability the three pieces form a triangle?
> $1/4$. A triangle needs every piece below $1/2$; at most one piece can exceed $1/2$ and each does with probability $1/4$, so $P = 1 - 3/4$.

> [!question]- prob-geo-break-longer-piece-triangle | Break a stick at a uniform point, then break the longer piece at a uniform point. Probability the pieces form a triangle?
> $2\ln 2 - 1 \approx 0.386$. With first cut $x < 1/2$, the second cut must fall in a window of length $x$ inside a piece of length $1-x$: $2\int_0^{1/2} x/(1-x)\,dx$.

> [!question]- prob-geo-broken-stick-expected-pieces | A unit stick is broken at two uniform points. What are the expected lengths of the shortest and longest pieces?
> Shortest $1/9$, longest $11/18$ (middle $5/18$). In general for $n$ pieces $E[\text{shortest}] = 1/n^2$ and $E[\text{longest}] = H_n/n$.

> [!question]- prob-geo-semicircle-n-points | $n$ points are uniform on a circle. What is the probability they all lie in some semicircle?
> $n/2^{n-1}$. The events "all others lie clockwise within a half-circle of point $i$" are disjoint, each with probability $2^{-(n-1)}$.

> [!question]- prob-geo-triangle-contains-center | Three uniform points on a circle form a triangle. What is the probability it contains the centre (equivalently, is acute)?
> $1/4$. It contains the centre iff the points are not in a common semicircle, and that has probability $1 - 3/4$.

> [!question]- prob-geo-sphere-tetrahedron-center | Four uniform points on a sphere. What is the probability their tetrahedron contains the centre?
> $1/8$. Fix three lines through the centre and the fourth point; exactly one of the 8 equally likely endpoint sign choices works.

> [!question]- prob-geo-meeting-problem | Two people arrive uniformly between 12:00 and 13:00 and each waits 15 minutes. Probability they meet?
> $7/16$. They meet iff $|X-Y| \le 1/4$; the complement is two corner triangles of total area $(3/4)^2$.

> [!question]- prob-geo-expected-distance-unit-interval | Two uniform points on $[0,1]$. What is their expected distance?
> $1/3$. $|X - Y|$ has density $2(1-t)$ on $[0,1]$, or: two points make three exchangeable gaps and the middle one has mean $1/3$.

> [!question]- prob-geo-expected-chord-length | Two uniform points on the unit circle. What is the expected length of the chord between them?
> $4/\pi \approx 1.27$. With central angle $\theta \sim U(0, 2\pi)$ the chord is $2|\sin(\theta/2)|$, whose mean is $4/\pi$.

> [!question]- prob-geo-bertrand-paradox | What is the probability that a random chord of a circle is longer than the side of the inscribed equilateral triangle?
> It depends on the sampling rule: $1/3$ for uniform endpoints, $1/2$ for a uniform distance along a random radius, $1/4$ for a uniform midpoint in the disc. State the rule first.

> [!question]- prob-geo-buffon-needle | A needle of length $\ell$ falls on lines spaced $d \ge \ell$ apart. Probability it crosses a line?
> $2\ell/(\pi d)$. Expected crossings are proportional to length, and a circle of diameter $d$ (length $\pi d$) always crosses twice.

> [!question]- prob-geo-product-of-uniforms | $X, Y$ i.i.d. $U(0,1)$. What is $P(XY < 1/2)$?
> $1/2 + (\ln 2)/2 \approx 0.847$. $P(XY < t) = \int_0^1 \min(1, t/x)\,dx = t - t\ln t$.

> [!question]- prob-geo-sum-of-uniforms-simplex | What is the probability that the sum of $n$ i.i.d. uniforms is less than 1?
> $1/n!$. It is the volume of the corner simplex; for three uniforms, $1/6$.

> [!question]- prob-geo-disc-distance-to-center | A point is uniform in the unit disc. What is its expected distance to the centre?
> $2/3$. $P(R \le r) = r^2$, so the density is $2r$ and $E[R] = \int_0^1 2r^2\,dr$.

> [!question]- prob-geo-closer-to-center-than-edge | A point is uniform in the unit square. Probability it is closer to the centre than to the boundary?
> $(4\sqrt{2} - 5)/3 \approx 0.219$. By 8-fold symmetry work in one eighth, where the region is bounded by the parabola $x = 1/4 - y^2$ and the line $y = x$.

## Further reading

- Frederick Mosteller, *Fifty Challenging Problems in Probability*, problems on broken sticks, Buffon's needle and random chords.
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 4.
- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 7 (joint distributions over regions).
- J. G. Wendel, "A Problem in Geometric Probability", *Mathematica Scandinavica* 11 (1962).
