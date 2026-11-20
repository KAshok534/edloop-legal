# JEE Main Quadratic Equations: PYQ Trends & Preparation Guide

Quadratic Equations serves as a core algebraic building block throughout the JEE Main syllabus. The chapter investigates relations between roots and coefficients, symmetric functions of roots, Newton's sums, sign and sign changes of quadratic expressions, location of roots relative to specified real numbers, equations reducible to quadratic forms (modulus, exponential, and logarithmic variants), and common root conditions.

## How often it comes up

In the 2019 to 2026 exam window, Quadratic Equations accounted for 185 questions across 162 test papers, delivering 4.0% of the mathematics section and holding rank 12 of 29 chapters. During the earlier 2002 to 2018 testing span, it contributed 53 questions across 38 papers with an identical 4.0% share. Over the recent 2024 to 2026 sessions, question volume reached 68 questions across 58 papers, capturing a 4.4% share. Comparing both earlier periods against 2024 to 2026, the chapter's share of mathematics questions has remained about the same.

Questions have appeared every year from 2019 to 2026. Students faced an average of 1.1 questions per paper across 2019 to 2026, and 1.2 questions per paper between 2024 and 2026. A substantial 52 numerical answer questions were set between 2019 and 2026, frequently asking for parameter bounds or counts of distinct real solutions.

## Most-asked topics

The syllabus organizes across three key topics:

- Roots & Coefficients: The largest topic with 115 total questions (82 in 2019 to 2026), examined continuously through 2026. Key concepts evaluate Vieta's formulas relating sum (alpha + beta) and product (alpha * beta) to polynomial coefficients, symmetric root expressions like alpha^n + beta^n via Newton's recurrence relation, forming new equations with transformed roots, and common root conditions.
- Higher Degree & Special Equations: Generated 94 total questions (81 in 2019 to 2026), active through 2026. Focuses on equations involving absolute values like |x - a|, biquadratic equations in x^2, logarithmic equations reducible to quadratics, and real solution counting across piecewise domains.
- Quadratic Expressions & Location of Roots: Contributed 29 total questions (22 in 2019 to 2026), tested through 2026. Explores discriminant conditions (D >= 0 for real roots), vertex coordinates (-b/2a), sign of a * f(k) ensuring roots lie on opposite sides or one side of a specified number k, and global extrema on bounded intervals.

## What the questions look like

Test problems combine algebraic identities with case-by-case boundary analysis. A very frequent pattern introduces equations featuring absolute values, such as x|x + a| + b|x + c| + d = 0, requiring candidates to split the real number line across critical points and check for valid solutions within each region.

Another staple pattern involves Newton's identity: given an equation like ax^2 + bx + c = 0 with roots alpha and beta and setting S_n = alpha^n + beta^n, students exploit a * S_n + b * S_{n-1} + c * S_{n-2} = 0 to rapidly compute complex fraction ratios without evaluating roots explicitly. Location of roots questions typically ask for parameter ranges such that both roots exceed a given value or a specified number lies strictly between the roots.

## Questions to try first

Explore these selected recent exam questions to consolidate your understanding:

- [Location of roots between boundaries](/q/q-2026-01-21-e-m03): Finding parameter intervals ensuring a specified integer lies strictly between quadratic roots.
- [Absolute value equation root sum](/q/q-2026-01-21-m-m13): Splitting a quadratic containing absolute values into cases and calculating the total sum of distinct roots.
- [Difference of roots parameter bounds](/q/q-2026-01-22-e-m10): Finding integer parameter values when the absolute difference of roots satisfies double inequality constraints.
- [Piecewise real solution counting](/q/q-2026-01-22-m-m19): Determining the count of distinct real solutions for an equation containing multiple linear modulus terms.
- [Biquadratic distinct real roots condition](/q/q-2026-01-24-e-m14): Finding the smallest positive integer parameter allowing a fourth-degree biquadratic equation to possess four real distinct roots.

## How to practise it

Develop fluency in Vieta transformations alongside geometric graphing of parabolas:

1. Master Newton's sums: For any quadratic ax^2 + bx + c = 0 with roots alpha and beta, write a * (alpha^n + beta^n) + b * (alpha^{n-1} + beta^{n-1}) + c * (alpha^{n-2} + beta^{n-2}) = 0 to evaluate high-power root combinations.
2. Sketch parabolas for location of roots: Translate verbal conditions into visual graphs. Both roots greater than k requires D >= 0, -b/2a > k, and a * f(k) > 0; k lying between roots simply requires a * f(k) < 0.
3. Solve modulus equations systematically: Identify all critical boundary points where expressions inside absolute value bars change sign. Solve the corresponding quadratic in each sub-interval and reject roots falling outside the domain.
4. Check substitution validity in special equations: When substituting t = x^2, remember that each positive value of t yields two real values of x, t = 0 yields one, and negative t yields zero real roots.
5. Review common root conditions: For two quadratics to share both roots, their corresponding coefficients must be proportional; for one common root, eliminate the quadratic term using cross-multiplication.

## Frequently asked questions

### What is the most efficient way to compute alpha^10 + beta^10 for quadratic roots?
Do not solve for the roots directly. Apply Newton's recurrence formula a * S_n + b * S_{n-1} + c * S_{n-2} = 0 sequentially to evaluate high-power root sums directly from lower powers.

### Why is a * f(k) < 0 sufficient when k lies between the roots?
If the leading coefficient a is positive and f(k) is negative, the continuous parabolic curve dips below the x-axis at x = k, ensuring that the parabola must intersect the x-axis on both sides of k without needing to check the discriminant separately.

### How do I handle equations reducible to quadratics with logarithms?
Express all logarithmic terms using a single common base, substitute t = log_b(x), solve the resulting quadratic equation for t, and finally convert back to find x while verifying that all argument domains remain strictly positive. Step-by-step solutions for each one are in the EdLoop app.
