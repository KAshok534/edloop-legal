# Statistics: JEE Main Guide

Statistics provides a highly formula-driven, dependable scoring opportunity in JEE Main mathematics. Across the 162 papers administered between 2019 and 2026, the examination included 121 questions from this chapter, representing 2.6 percent of all mathematics questions and placing it at rank 19 among the 29 chapters in the subject. It appeared in 121 of those 162 papers and has been tested every year since 2019. Over the recent 2024 to 2026 examination cycles, it supplied 38 questions across 58 papers, averaging 0.7 questions per paper with a 2.5 percent subject share. Comparing the earlier 2002 to 2018 share of 3.0 percent against 2024 to 2026 shows that its long-term share is down, while comparing 2019 to 2026 with 2024 to 2026 indicates that it is about the same. Across the complete historical record from 2002 to 2026 spanning 200 papers, 160 questions appeared in 156 papers, with 37 numerical answer questions asked between 2019 and 2026.

```
Statistics in JEE Main (2019-2026)
Total questions: 121 | Rank: 19 of 29 chapters
Average per paper: 0.7 | Subject share: 2.6%
Paper presence: featured in 121 of 162 papers
```

## How often it comes up

Students can expect a statistics question in roughly three out of every four examination shifts. Between 2019 and 2026, 121 of the 162 examination shifts presented a problem from this chapter. The annual question totals for 2024, 2025, and 2026 were 14, 8, and 16 questions respectively.

Statistics questions in JEE Main are renowned for following highly repetitive algebraic recipes. Most problems focus on determining two missing observations from given values of the mean and variance, or correcting erroneous data entries, making thorough computational accuracy the decisive success factor.

## Most-asked topics

Questions in this chapter divide between two primary areas:

1. **Measures of Dispersion (108 questions, 2019-2026; 134 total, last asked 2026)**
The vast majority of questions appear here. Involves calculating the variance and standard deviation of discrete and grouped data, mean deviation about the mean or median, effects of linear transformations on dispersion, and setting up simultaneous equations to identify missing or altered observations.

2. **Measures of Central Tendency (13 questions, 2019-2026; 26 total, last asked 2026)**
Focuses on the arithmetic mean, median, and mode for individual data points and grouped frequency distributions. Questions often require solving for unknown frequencies given the overall sample mean or median.

## What the questions look like

Examiners test statistics through several structured analytical formats:

- **Two Missing Observations**: A dataset has n observations, of which n minus two values are known explicitly. Given the overall arithmetic mean and variance of the full dataset, candidates set up simultaneous equations for the sum and sum of squares of the two missing values.
- **Data Correction and Modified Entries**: An observation was recorded incorrectly or replaced by a new value. Students determine the correct mean and the revised variance by adjusting the sum of observations and the sum of squared observations.
- **Linear Transformation of Data**: Every observation xi is replaced by a linear function a xi plus b. Candidates apply the scaling rules: the new mean equals a multiplied by the old mean plus b, while the new variance equals a squared multiplied by the old variance.
- **Mean Deviation About the Median**: Evaluating the average of absolute deviations from the median for arithmetic progression sequences or grouped frequency distributions.

## Questions to try first

Sharpen your computational accuracy with these recent problems:

- Missing observations from mean and variance: [JEE Main 2026 21 Jan Shift 1](/q/q-2026-01-21-m-m20)
- Frequency table with unknown frequency: [B Tech 2nd Apr 2026 Shift 1](/q/q-2026-04-02-m-m08)
- Mean deviation of progression terms: [JEE Main 2026 22 Jan Shift 2](/q/q-2026-01-22-e-m05)
- Grouped data variance and unknown parameters: [JEE Main 2026 23 Jan Shift 2](/q/q-2026-01-23-e-m02)

## How to practise it

Consistency in statistics depends on systematic arithmetic habits:

- **Use the sum of squares variance identity**: Express the variance as one over n multiplied by the sum of xi squared, minus the square of the arithmetic mean. This formulation is far faster and less prone to fractional errors than summing the squares of deviations from the mean.
- **Track the sum and sum of squares separately**: When solving for missing observations, let the unknown values be u and v. The mean gives the linear sum u plus v, while the variance gives the sum of squares u squared plus v squared. Squaring the linear sum and subtracting isolates twice the product uv, converting the problem into a simple quadratic.
- **Remember variance invariance under shifts**: Adding or subtracting a constant to every observation changes the mean by that constant, but leaves the variance and standard deviation completely unchanged. Multiplying by a constant scales the standard deviation by the absolute value of that constant and the variance by its square.
- **Arrange data in order for median calculations**: Never attempt to evaluate mean deviation about the median without sorting the dataset in ascending order first. Identifying the exact middle element or the average of the two central elements is essential before computing absolute differences.

## Frequently asked questions

### What is the difference between variance and standard deviation?
The variance is the average of the squared deviations from the arithmetic mean, while the standard deviation is the positive square root of the variance. Standard deviation retains the original physical units of the measurement data, whereas variance is expressed in squared units.

### How does changing the origin and scale affect variance?
If each observation xi is transformed to yi equals (xi minus A) divided by h, the mean shifts according to the same transformation. However, the variance of the original data equals h squared multiplied by the variance of the transformed data yi. The shift constant A has zero impact on the variance.

### Can variance ever be negative?
No, the variance can never assume a negative value because it represents an average of squared real quantities. If a calculation yields a negative variance, an arithmetic mistake occurred in computing the sum of squared observations or the square of the sample mean. Step-by-step solutions for each one are in the EdLoop app.
