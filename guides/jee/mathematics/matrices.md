## How often it comes up

Matrices provides tools for linear transformations and solving systems of linear equations under Unit 3: Matrices and Determinants in the Class 12 curriculum, standing at rank 4 of 29 chapters with a 5.7% share of all mathematics questions. In the 2019 to 2026 testing cycle, Matrices contributed 260 questions across 162 exam papers, delivering 5.7% of all mathematics questions and standing at rank 4 of 29 chapters. During the earlier 2002 to 2018 timeframe, it produced 52 questions across 38 papers with a 4.0% share. In the recent 2024 to 2026 window, question volume reached 88 questions across 58 papers, accounting for a 5.7% share. Comparing 2002 to 2018 against 2024 to 2026, the trend is up, whereas comparing 2019 to 2026 against 2024 to 2026, its testing share has remained about the same.

The chapter has appeared every year from 2019 to 2026. Across 2019 to 2026, candidates faced an average of 1.6 questions per paper, and 1.5 questions per paper between 2024 and 2026. It yielded 66 numerical answer questions from 2019 to 2026, making it one of the largest numerical question sources in the exam.

## Most-asked topics

The syllabus organizes across three core topics:

- Systems of Linear Equations: The highest-volume topic with 118 total questions (104 in 2019 to 2026), evaluated consistently through 2026. Focuses on homogeneous and non-homogeneous linear systems in three variables, using determinant conditions to identify unique solutions, infinite solutions (consistency), and no solutions (inconsistency).
- Inverse & Adjoint: Contributed 115 total questions (93 in 2019 to 2026), tested through 2026. Explores determinant identities involving adjoints: |adj A| = |A|^(n-1), |adj(adj A)| = |A|^((n-1)^2), adj(kA) = k^(n-1) adj A, inverse properties (AB)^-1 = B^-1 A^-1, and orthogonal matrices.
- Matrix Algebra: Generated 79 total questions (63 in 2019 to 2026), active through 2026. Centers on non-commutativity of matrix multiplication, symmetric and skew-symmetric decompositions (A = 1/2(A + A^T) + 1/2(A - A^T)), mathematical induction for high powers A^n, characteristic equations, and trace identities.

## What the questions look like

Examiners test both algorithmic determinant equations and multi-step matrix identity simplifications. A very common pattern gives a system of three linear equations in x, y, and z containing unknown parameters, asking students to determine parameter values that produce infinitely many solutions or no solution.

Another prominent question style involves nested adjoint expressions, such as computing the determinant of adj(k adj(A^m adj(pA))) for an n by n matrix with known determinant. Questions on matrix powers often provide a matrix A whose square reveals a simple periodic pattern or nilpotence, allowing rapid evaluation of A^15 or higher powers.

## Questions to try first

Review these selected recent exam questions to assess your mastery:

- [Matrix power linear combination](/q/q-2026-01-21-e-m12): Finding non-zero vector solutions to a matrix equation involving high powers of a 2x2 matrix.
- [Three-variable system inconsistency condition](/q/q-2026-01-21-e-m20): Determining parameter values that cause a system of three linear equations to possess no solution.
- [Adjoint matrix vector system](/q/q-2026-01-22-e-m09): Reconstructing coordinate solution components to AX = B when provided with the adjoint matrix.
- [Skew-symmetric matrix nested adjoint determinant](/q/q-2026-01-22-m-m21): Evaluating scalar determinants of deeply nested adjoints formed from skew-symmetric matrices.
- [Scalar and power adjoint transformations](/q/q-2026-01-23-m-m25): Computing the numerical determinant of compound adjoint structures for an order-3 square matrix.

## How to practise it

Prepare for matrices by mastering algebraic determinant shortcuts alongside linear system consistency criteria:

1. Memorize adjoint formulas for order n: |adj A| = |A|^(n-1); adj(adj A) = |A|^(n-2) * A; |adj(adj A)| = |A|^((n-1)^2); adj(AB) = (adj B)(adj A); adj(kA) = k^(n-1) adj A.
2. Analyze linear systems systematically: For a 3x3 system AX = B, calculate Delta. If Delta is non-zero, the system has a unique solution. If Delta = 0, evaluate Delta_x, Delta_y, and Delta_z: if at least one is non-zero, the system has no solution; if all are zero, investigate plane co-linearity or parallel planes to distinguish infinite solutions from no solution.
3. Exploit Cayley-Hamilton theorem: Every square matrix satisfies its own characteristic polynomial det(A - lambda I) = 0. Use this to express high powers A^n as linear combinations of A and the identity matrix I.
4. Remember skew-symmetric determinant properties: The determinant of any odd-order skew-symmetric matrix is always zero.
5. Practise rapid 3x3 determinant expansions: Calculation precision without algebraic sign errors is paramount for the 66 numerical questions set in recent years.

## Frequently asked questions

### When does a system of three linear equations have no solution if all delta determinants are zero?
When all four determinants (Delta, Delta_x, Delta_y, Delta_z) equal zero, the system usually has infinitely many solutions. However, if the equations represent distinct parallel planes, the system has no solution despite all deltas vanishing. Always verify whether two equations are parallel and inconsistent.

### What is the effect of multiplying a matrix by a scalar k on its adjoint?
For an n by n square matrix A, adj(kA) = k^(n-1) adj A. Notice the exponent is n-1 rather than n, because each cofactor entry omits one row and one column.

### How do I find high powers of a matrix quickly?
Compute A^2 and A^3 to detect emerging arithmetic or geometric patterns. Alternatively, if the matrix satisfies an identity like A^2 = A (idempotent) or A^2 = I (involutary), high powers collapse directly into lower terms. Step-by-step solutions for each one are in the EdLoop app.
