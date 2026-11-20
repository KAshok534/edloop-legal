# Probability: JEE Main Guide

Probability is a cornerstone topic in JEE Main mathematics, requiring logical modelling alongside combinatorial counting. Across the 162 papers conducted between 2019 and 2026, this chapter supplied 189 questions, accounting for 4.1 percent of all mathematics questions and securing rank 11 among the 29 chapters in the subject. It appeared in 154 of those 162 papers and has been tested every single year since 2019. Over the recent 2024 to 2026 examination cycles, it contributed 66 questions across 58 papers, averaging 1.1 questions per paper with a 4.3 percent subject share. Comparing the earlier 2002 to 2018 share of 4.3 percent against 2024 to 2026 shows that its long-term share is about the same, while comparing 2019 to 2026 with 2024 to 2026 also shows it is about the same. Across the complete historical record from 2002 to 2026 spanning 200 papers, 245 questions were asked in 191 papers, including 34 numerical answer questions between 2019 and 2026.

```
Probability in JEE Main (2019-2026)
Total questions: 189 | Rank: 11 of 29 chapters
Average per paper: 1.2 | Subject share: 4.1%
Shift occurrence: asked in 154 of 162 papers
```

## How often it comes up

Students can expect at least one probability problem in almost every examination sitting, with numerous shifts featuring two problems. Across the 162 papers from 2019 to 2026, 154 included questions from this chapter. In the 2024, 2025, and 2026 examination periods, the question tallies were 26, 22, and 18 questions respectively.

Probability problems frequently serve as the ultimate test of combinatorial enumeration. Because modern questions integrate conditional updating and discrete random variable distributions, methodical case listing and probability tree analysis are essential.

## Most-asked topics

Questions in this chapter organize across three primary subtopics:

1. **Random Variables & Distributions (68 questions, 2019-2026; 84 total, last asked 2026)**
The most frequent subtopic in recent testing. Covers discrete probability distributions, calculating the mean expectation and variance, probability mass functions defined in terms of an unknown parameter k, and binomial distributions involving repeated independent trials. Note that Bernoulli trials and binomial distributions were formally removed from the updated syllabus, yet general discrete random variables remain active.

2. **Basic Probability (67 questions, 2019-2026; 89 total, last asked 2026)**
Involves classical probability definitions using permutations and combinations, dice and card problems, divisibility conditions on randomly chosen integer subsets, geometry-based geometric probability, and mutually exclusive events.

3. **Conditional Probability (54 questions, 2019-2026; 72 total, last asked 2026)**
Covers conditional probability definitions, the multiplication rule for independent events, the theorem of total probability, and Bayes' theorem. Recurring formats include drawing items sequentially from two or more urns with transfer steps between them.

## What the questions look like

Examiners repeatedly use well-defined probabilistic architectures:

- **Urn Transfer and Bayes' Inversion**: A ball of unknown color is transferred from bag B to bag A, followed by drawing a ball from bag A. Problems ask for the total probability of drawing a specific color or the reverse conditional probability that the transferred ball was white.
- **Discrete Distribution with Parameter Constraints**: A discrete random variable X takes small non-negative integer values with probabilities proportional to powers of k. Normalising the total probability to unity fixes k, after which the mean or variance is evaluated.
- **Divisibility Constraints on Subset Products**: Selecting two or three distinct numbers from an initial integer sequence, followed by finding the probability that their product or sum satisfies divisibility requirements.
- **Independent Experiment Stopping Rules**: A game where two players toss dice alternately until a specific sum appears, asking for the probability that a particular participant wins.

## Questions to try first

Strengthen your probabilistic reasoning with these recent questions:

- Discrete distribution expectation and variance relation: [JEE Main 2026 21 Jan Shift 2](/q/q-2026-01-21-e-m16)
- Divisibility in random pairs: [JEE Main 2026 22 Jan Shift 1](/q/q-2026-01-22-m-m01)
- Two-bag transfer conditional probability: [JEE Main 2026 23 Jan Shift 2](/q/q-2026-01-23-e-m09)
- Parameterized discrete distribution probability: [JEE Main 2026 22 Jan Shift 1](/q/q-2026-01-22-m-m02)

## How to practise it

Accurate probability calculation balances systematic counting with conditional discipline:

- **Normalise probability distributions first**: In any discrete distribution problem, immediately sum all probability entries and set the total equal to unity. This determines unknown scalars like k before embarking on expectation or variance computations.
- **Map out two-stage experiments with probability trees**: For problems involving sequential draws or transfers between urns, draw a clear tree diagram showing intermediate transfer branches. Multiply probabilities along each path and sum over mutually exclusive branches.
- **Use complementary probability for at least one scenarios**: When computing the probability that an event occurs at least once across several independent trials, compute one minus the probability that the event never occurs.
- **Check independence criteria strictly**: Do not assume events are independent without verifying that the probability of their intersection equals the product of their individual probabilities.

## Frequently asked questions

### Is the binomial distribution still in the syllabus?
Bernoulli trials and the binomial distribution were officially removed from the NTA mathematics syllabus for JEE Main starting in 2024. While questions explicitly demanding the binomial distribution formula have subsided, general discrete probability distribution tables and expectation calculations remain core components of the syllabus.

### How do I recognize when Bayes' theorem is required?
Bayes' theorem is needed whenever a problem asks for the probability of a prior cause given that an observed outcome has already occurred. If you know the probability of drawing a white ball given that bag one was chosen, but the question asks for the probability that bag one was chosen given that the drawn ball is white, apply Bayes' inversion formula.

### Why do divisibility problems appear so often in probability?
Divisibility questions combine number theory classification with combinatorial selection. Partitioning the sample space into residue classes modulo the divisor allows favorable pairs or triples to be counted systematically. Step-by-step solutions for each one are in the EdLoop app.
