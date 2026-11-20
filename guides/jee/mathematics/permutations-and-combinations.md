## How often it comes up

Permutations and combinations develops discrete counting methods under Unit 4: Permutations and Combinations in the Class 11 curriculum, capturing rank 10 of 29 chapters with a 4.2% share of the mathematics section. During the 2019 to 2026 testing cycle, Permutations & Combinations accounted for 193 questions across 162 exam papers, making up 4.2% of the mathematics section and capturing rank 10 of 29 chapters. In the earlier 2002 to 2018 testing span, it registered 46 questions across 38 papers with a 3.5% share. Across recent 2024 to 2026 sessions, it yielded 68 questions across 58 papers, accounting for a 4.4% share. Comparing 2002 to 2018 against 2024 to 2026, the trend is up, whereas comparing 2019 to 2026 against 2024 to 2026, its testing share has remained about the same.

The chapter has appeared every year from 2019 to 2026. Across 2019 to 2026, students faced an average of 1.2 questions per paper, consistent with the 1.2 questions per paper recorded in the 2024 to 2026 timeframe. The chapter is an extraordinary source of numerical value questions: exactly 100 numerical answer questions were set between 2019 and 2026.

## Most-asked topics

The syllabus organizes across four major counting areas:

- Permutations: The leading topic with 75 total questions (59 in 2019 to 2026), evaluated continuously through 2026. Covers arrangement of words with repeated letters, dictionary ranking of words with and without duplicates, gap method and tie (bundle) method for conditional arrangements, and digit permutations under divisibility constraints.
- Combinations: Contributed 68 total questions (56 in 2019 to 2026), tested through 2026. Explores selecting teams or committees under gender or group restrictions, geometric counts (lines, triangles, and pentagons formed from points on intersecting lines), and subsets satisfying parity or divisibility properties.
- Distributions & Advanced Counting: Generated 48 total questions (42 in 2019 to 2026), active through 2026. Focuses on distributing identical objects into distinct bins using stars and bars ((n + r - 1)C(r - 1)), distributing distinct objects, non-negative integer solutions to linear equations, and derangements.
- Counting Principles: Produced 48 total questions (36 in 2019 to 2026), active through 2026. Examines multiplication rules, Legendre's formula finding the highest power of a prime p dividing n! via floor summations, and modular arithmetic selections.

## What the questions look like

Examiners present intricate word problems requiring case-by-case categorization. A prominent pattern asks candidates to form four-digit or five-digit numbers using a restricted set of digits such that the resulting number is divisible by three, four, or six, demanding careful modular residue grouping.

Another major question style involves word formation from collections containing repeated letters (like P, P, P, Q, Q, R, R), where students must partition cases by selection types (all different, two alike and two different, two pairs alike, or three alike) before applying multinomial arrangement formulas.

## Questions to try first

Solve these representative recent exam questions to sharpen your combinatorial logic:

- [Prime exponent in factorials](/q/q-2026-01-21-e-m18): Finding the largest integer exponent such that a prime power divides a given large factorial using Legendre's formula.
- [Subset selection with parity constraints](/q/q-2026-01-22-e-m22): Counting subsets of an integer set that contain at least two elements and yield an even product.
- [Identical object partition distribution](/q/q-2026-01-23-e-m20): Calculating total ways to distribute identical objects among distinct recipients with positive minimum allocations.
- [Multinomial letter word permutations](/q/q-2026-01-23-m-m22): Forming four-letter words from a multi-set containing repeated and distinct letters.
- [Dictionary rank of words](/q/q-2026-01-24-e-m07): Finding the alphabetical dictionary rank of a specified multi-letter word.

## How to practise it

Prepare for permutations and combinations through systematic case branching and algebraic identities:

1. Classify multi-set selections systematically: When choosing r items from a set with repetitions, branch into distinct cases based on multiplicity patterns before arranging.
2. Master identical object distribution: The number of non-negative integer solutions to x1 + x2 + ... + xr = n is (n + r - 1)C(r - 1). For strictly positive integers, substitute yi = xi - 1 to get (n - 1)C(r - 1).
3. Apply Legendre's formula accurately: The highest power of prime p dividing n! equals the sum of floor(n / p^k) for k >= 1. For composite bases like 40 = 2^3 * 5, evaluate prime factors separately and take the bottleneck minimum.
4. Distinguish gap method from tie method: When items must never be adjacent, seat the unrestricted items first and place the constrained items into the available gaps; when items must remain together, tie them into a single super-element.
5. Practise modular residue grouping: When counting numbers divisible by 3, classify available digits into sets of remainder 0, remainder 1, and remainder 2 mod 3 before selecting valid combinations.

## Frequently asked questions

### Why are there so many numerical answer questions in this chapter?
Permutations and Combinations naturally produces exact non-negative integer counts, making it ideal for numerical answer questions where 100 problems appeared between 2019 and 2026.

### How does the gap method work for non-adjacent arrangements?
First arrange the elements that have no restrictions. If there are m such elements in a row, they create m + 1 distinct gaps (including the two ends). Then choose from these gaps to place the elements that cannot be adjacent.

### How do I find the dictionary rank of a word with repeated letters?
Alphabetize the letters. Fix preceding letters at the first position and divide the factorial of remaining positions by the factorials of each repeated letter's frequency, summing these counts until reaching the target word. Step-by-step solutions for each one are in the EdLoop app.
