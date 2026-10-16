---
type: problem-set
track: [quant-research, quant-dev]
tier: core
status: solid
prereqs: [covariance-matrices-and-psd, convex-optimization-and-kkt]
est_hours: 4
sources: [Zhou - A Practical Guide to Quantitative Finance Interviews ch 3, Strang - Introduction to Linear Algebra 5th ed, Joshi Denson and Downes - Quant Job Interview Questions and Answers 2nd ed, Boyd and Vandenberghe - Convex Optimization (Cambridge 2004), Horn and Johnson - Matrix Analysis 2nd ed]
---

# Linear Algebra Problem Set

## TL;DR

- Name the structure before computing: symmetric means real eigenvalues and orthogonal eigenvectors, rank one plus identity means Sherman-Morrison, row-stochastic means eigenvalue 1, projection means eigenvalues 0 and 1.
- Use invariants as checks: trace is the sum and determinant the product of eigenvalues; for $2 \times 2$, $\lambda^2 - (\text{tr})\lambda + \det = 0$.
- For correlation questions, reach for the PSD condition (determinant of the $3 \times 3$, the equal-weight portfolio for equicorrelation).
- For optimisation questions, write the Lagrangian, read the multiplier as a shadow price, and check convexity before claiming a global optimum.
- Speak the sanity check out loud: a limiting case ($\rho \to 1$, $n \to \infty$), a dimension count, or a numerical spot check.

## Learning objectives

- Answer rapid linear algebra and optimization questions from researcher interviews.
- Recognise which structural fact a question is testing from its wording.
- Reach interview speed: most cards in under three minutes, the worked examples in under ten.

## Core concepts

This note is a drill set; the theory is in the topic notes linked below.
The toolkit, with the signal in the question that should trigger each tool:

| Tool | Signal in the question | Example card |
| :--- | :--- | :--- |
| Trace and determinant as eigenvalue sum and product | "eigenvalues of a $2 \times 2$", "$\det(f(A))$" | `la-ps-det-trace-from-eigenvalues` |
| Rank-one structure, Sherman-Morrison | "all ones", "equicorrelated", "$I + uv^\top$" | `la-ps-inverse-identity-plus-ones` |
| PSD via determinant or equal-weight variance | "is this a valid correlation matrix", "how negative can" | `la-ps-third-correlation` |
| Spectral theorem and Rayleigh quotient | "maximise $x^\top Ax$ on the sphere" | `la-ps-courant-fischer-second` |
| Left eigenvector for eigenvalue 1 | "long-run", "stationary", transition matrix | `la-ps-three-state-markov` |
| Companion matrix | recurrence, AR($p$), Fibonacci | `la-ps-ar2-stationarity` |
| Projection geometry | "closest point", hat matrix, residuals | `la-ps-projection-onto-line` |
| Lagrange and KKT | "maximise subject to", "minimum variance" | `la-ps-lagrange-xy` |
| Taylor and Newton | "estimate quickly", "iterate" | `la-ps-newton-reciprocal` |

Topic notes: [Vectors, Matrices and Linear Maps](01-Vectors-Matrices-and-Linear-Maps.md), [Eigendecomposition](02-Eigendecomposition-and-Spectral-Theorem.md), [SVD](03-SVD-and-Low-Rank-Approximation.md), [Covariance and PSD](04-Covariance-Matrices-and-PSD.md), [PCA](05-PCA-and-Factor-Structure.md), [Numerical Linear Algebra](06-Numerical-Linear-Algebra.md), [Calculus and Taylor](07-Calculus-and-Taylor-Expansions.md), [Convex Optimization and KKT](08-Convex-Optimization-and-KKT.md), [QP Solvers](09-Quadratic-Programming-and-Portfolio-Solvers.md), [Root Finding](10-Numerical-Optimization-and-Root-Finding.md).

## Worked examples

### Everything about the equicorrelation matrix

"Four assets, all pairwise correlations 0.5. Eigenvalues, determinant, inverse, and the most negative common correlation allowed?"
"$C = 0.5I + 0.5J$ where $J = \mathbf{1}\mathbf{1}^\top$ has eigenvalues 4 (on $\mathbf{1}$) and 0 three times."
So $C$ has eigenvalues $0.5 + 0.5 \times 4 = 2.5$ once and $0.5$ three times, and $\det C = 0.5^3 \times 2.5 = 0.3125$.
Sherman-Morrison: $C^{-1} = \frac{1}{1 - \rho}\Big(I - \frac{\rho}{1 + (n - 1)\rho}J\Big) = 2(I - 0.2J)$, so diagonal entries $1.6$ and off-diagonal $-0.4$.
Smallest allowed common correlation: $1 + (n - 1)\rho \ge 0$, so $\rho \ge -1/3$.
"Sanity check: with equal vols the minimum-variance portfolio is equal-weighted by symmetry, and the solver agrees to rounding error."

### Is this a valid correlation matrix?

"$\rho_{12} = 0.9$, $\rho_{23} = 0.6$, $\rho_{13} = 0.2$. Valid?"
Given $\rho_{12}$ and $\rho_{23}$, $\rho_{13}$ must lie in $0.54 \pm\sqrt{0.19 \times 0.64} = [0.1913, 0.8887]$.
0.2 is just inside, and the determinant $1 - 0.81 - 0.04 - 0.36 + 2(0.9)(0.2)(0.6) = 0.006 > 0$ confirms it; the smallest eigenvalue is only $0.0034$.
Change $\rho_{13}$ to 0.1 and the determinant is $-0.072$: invalid.

### A three-state chain

"$P = \begin{pmatrix} 0.5 & 0.5 & 0 \\ 0.25 & 0.5 & 0.25 \\ 0 & 0.5 & 0.5\end{pmatrix}$. Long-run distribution and speed of convergence?"
Solve $\pi^\top P = \pi^\top$: by symmetry $\pi_1 = \pi_3$, and the first column gives $\pi_1 = 0.5\pi_1 + 0.25\pi_2$, so $\pi_2 = 2\pi_1$ and $\pi = (0.25, 0.5, 0.25)$.
Eigenvalues are 1, 0.5 and 0, so deviations from $\pi$ halve every step.

### Two-asset minimum variance

"Vols 20% and 30%, correlation 0.5. Minimum-variance weights and vol? And with correlation $-1$?"
$w_1 = \frac{\sigma_2^2 - \rho\sigma_1\sigma_2}{\sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2} = \frac{0.09 - 0.03}{0.07} = 6/7 = 0.857$, and the portfolio vol is $19.64\%$, barely below the 20% of asset 1.
With $\rho = -1$, $w_1 = \sigma_2/(\sigma_1 + \sigma_2) = 0.6$ makes the variance exactly 0.

### A Lagrangian with a shadow price

"Maximise $xy$ subject to $x + y = 10$."
$L = xy - \lambda(x + y - 10)$: $y = \lambda$, $x = \lambda$, so $x = y = 5$, value 25, $\lambda = 5$.
Check the shadow price: the value as a function of the budget $c$ is $c^2/4$, with derivative $c/2 = 5$ at $c = 10$.
"$xy$ is not concave (its Hessian has eigenvalues $\pm1$), but on the line $x + y = 10$ it is $x(10 - x)$, which is concave, so the stationary point is the maximum."

## Pitfalls

- Computing eigenvalues of a large structured matrix by brute force; look for $\mathbf{1}\mathbf{1}^\top$, block or circulant structure first.
- Forgetting that $AB \ne BA$, that $\det(A + B) \ne \det A + \det B$, and that the product of symmetric matrices is generally not symmetric.
- Treating a stationary point of a non-convex problem as a global optimum without an argument.
- Checking only $2 \times 2$ minors for a $3 \times 3$ correlation matrix; all pairwise correlations in $[-1, 1]$ is necessary, not sufficient.
- Mixing up right and left eigenvectors for Markov chains.
- Losing the sign convention of a multiplier when quoting a shadow price.

## Interview questions

> [!question]- la-ps-ones-matrix-eigenvalues | Eigenvalues of the $n \times n$ all-ones matrix $J$?
> $n$ once (eigenvector $\mathbf{1}$) and 0 with multiplicity $n - 1$ (anything orthogonal to $\mathbf{1}$). $J = \mathbf{1}\mathbf{1}^\top$ has rank 1 and trace $n$.

> [!question]- la-ps-equicorrelation-det | Determinant of the $4 \times 4$ equicorrelation matrix with $\rho = 0.5$?
> $0.3125$: eigenvalues $1 + 3\rho = 2.5$ and $1 - \rho = 0.5$ three times, product $0.5^3 \times 2.5$.

> [!question]- la-ps-equicorrelation-bound | Four assets share a common correlation $\rho$. How negative can it be?
> $-1/3$. The equal-weight portfolio has variance proportional to $1 + 3\rho \ge 0$.

> [!question]- la-ps-third-correlation | $\rho_{12} = 0.6$ and $\rho_{13} = 0.8$. Range of $\rho_{23}$?
> $[0, 0.96]$: $0.48 \pm\sqrt{0.64 \times 0.36} = 0.48 \pm 0.48$.

> [!question]- la-ps-valid-correlation-matrix | Is $\rho_{12} = 0.9$, $\rho_{23} = 0.6$, $\rho_{13} = 0.2$ a valid correlation matrix? What about $\rho_{13} = 0.1$?
> Yes, barely: $\rho_{13}$ must lie in $[0.1913, 0.8887]$ and the determinant is $0.006 > 0$. With $\rho_{13} = 0.1$ the determinant is $-0.072$, so no.

> [!question]- la-ps-det-trace-from-eigenvalues | $A$ is $3 \times 3$ with eigenvalues 1, 2, 3. Find $\det(A^2 + I)$ and $\text{tr}(A^{-1})$.
> $\det(A^2 + I) = (1 + 1)(4 + 1)(9 + 1) = 100$ and $\text{tr}(A^{-1}) = 1 + 1/2 + 1/3 = 11/6$, because $f(A)$ has eigenvalues $f(\lambda_i)$.

> [!question]- la-ps-two-by-two-eigenvectors | Eigenvectors of $\begin{pmatrix} 4 & 1 \\ 2 & 3\end{pmatrix}$?
> For $\lambda = 5$: $(1, 1)$; for $\lambda = 2$: $(1, -2)$. Solve $(A - \lambda I)v = 0$ from the first row: $(4 - \lambda)v_1 + v_2 = 0$. They are not orthogonal, because $A$ is not symmetric.

> [!question]- la-ps-rotation-eigenvalues | Eigenvalues of the 90-degree rotation $\begin{pmatrix} 0 & -1 \\ 1 & 0\end{pmatrix}$?
> $\pm i$: trace 0, determinant 1, so $\lambda^2 + 1 = 0$. No real eigenvector, since a rotation moves every direction; eigenvalues of orthogonal matrices lie on the unit circle.

> [!question]- la-ps-hat-matrix-trace | OLS with 100 observations and 5 regressors: eigenvalues and trace of the hat matrix?
> Five eigenvalues equal to 1 and 95 equal to 0, so the trace is 5. It is an orthogonal projection onto a 5-dimensional column space.

> [!question]- la-ps-quadratic-form-expectation | $x$ has mean $(1, 1, 1)$ and identity covariance; $A = \text{diag}(1, 2, 3)$. Find $E[x^\top Ax]$.
> 12: $\text{tr}(A\Sigma) + \mu^\top A\mu = 6 + 6$. A simulation with 400,000 draws from a fresh `default_rng(0)` gives about 12.00.

> [!question]- la-ps-three-state-markov | Stationary distribution of $P = \begin{pmatrix} 0.5 & 0.5 & 0 \\ 0.25 & 0.5 & 0.25 \\ 0 & 0.5 & 0.5\end{pmatrix}$?
> $(0.25, 0.5, 0.25)$, the left eigenvector for eigenvalue 1. The other eigenvalues are 0.5 and 0, so convergence halves the error each step.

> [!question]- la-ps-fibonacci-closed-form | What is $F_{50}$, and how do you get it fast?
> $12{,}586{,}269{,}025$. Either square the matrix $\begin{pmatrix} 1 & 1 \\ 1 & 0\end{pmatrix}$ repeatedly ($O(\log n)$ multiplications, exact in integers) or round $\varphi^{50}/\sqrt5$, which is exact in double precision at this size.

> [!question]- la-ps-ar2-stationarity | Is $x_t = 0.5x_{t-1} + 0.3x_{t-2} + \varepsilon_t$ stationary?
> Yes: the roots of $\lambda^2 - 0.5\lambda - 0.3 = 0$ are $0.852$ and $-0.352$, both inside the unit circle. The negative root adds a damped oscillating component.

> [!question]- la-ps-two-asset-gmv | Vols 20% and 30%, correlation 0.5. Minimum-variance weights and vol?
> $w_1 = (0.09 - 0.03)/(0.04 + 0.09 - 0.06) = 6/7 \approx 0.857$, $w_2 = 1/7$; vol $19.64\%$. With correlation this high, the second asset adds little diversification.

> [!question]- la-ps-zero-variance-hedge | Vols 20% and 30%, correlation $-1$. Which long-only mix has zero variance?
> $w_1 = \sigma_2/(\sigma_1 + \sigma_2) = 0.6$, $w_2 = 0.4$: then $0.6 \times 0.2 = 0.4 \times 0.3$, and the two perfectly offsetting moves cancel.

> [!question]- la-ps-equal-weight-diversification | 50 assets with vol 20% and pairwise correlation 0.3, equal weights. Portfolio vol, and the limit as $n \to \infty$?
> $\sigma\sqrt{\rho + (1 - \rho)/n} = 0.2\sqrt{0.314} = 11.21\%$; the limit is $\sigma\sqrt\rho = 10.95\%$. Correlation sets a floor that diversification cannot break.

> [!question]- la-ps-courant-fischer-second | For $A = \begin{pmatrix} 2 & 1 \\ 1 & 2\end{pmatrix}$, maximise $x^\top Ax$ over unit vectors orthogonal to $(1, 1)$.
> 1, at $x = (1, -1)/\sqrt2$. Orthogonal to the top eigenvector, the Rayleigh quotient's maximum is the next eigenvalue (Courant-Fischer); the unconstrained maximum would be 3.

> [!question]- la-ps-xy-nonconvex | Is $f(x, y) = xy$ convex, concave or neither?
> Neither: its Hessian $\begin{pmatrix} 0 & 1 \\ 1 & 0\end{pmatrix}$ has eigenvalues $+1$ and $-1$, so the origin is a saddle. Restricted to a line such as $x + y = c$ it becomes concave.

> [!question]- la-ps-uv-plus-vu-rank | Rank and eigenvalues of $uv^\top + vu^\top$ for $u = (1, 0, 0)$, $v = (1, 1, 0)$?
> Rank 2, eigenvalues $u^\top v \pm\lVert u\rVert\lVert v\rVert = 1 \pm\sqrt2$ (that is $2.414$ and $-0.414$) and 0. The matrix maps everything into $\text{span}\{u, v\}$ and is indefinite.

> [!question]- la-ps-inverse-identity-plus-ones | Invert $I + J$ for the $3 \times 3$ all-ones $J$.
> $I - J/4$, by Sherman-Morrison: $(I + \mathbf{1}\mathbf{1}^\top)^{-1} = I - \mathbf{1}\mathbf{1}^\top/(1 + n)$. The determinant is $1 + n = 4$ by the determinant lemma.

> [!question]- la-ps-near-singular-condition | Condition number of $\begin{pmatrix} 1 & 1 \\ 1 & 1.0001\end{pmatrix}$ and what it means?
> About 40,002: eigenvalues are about $2.00005$ and $0.00005$. Expect to lose four to five digits solving with it; two nearly identical hedge instruments give exactly this problem.

> [!question]- la-ps-newton-reciprocal | Compute $1/3$ without division using Newton's method from $x_0 = 0.3$.
> Newton on $f(x) = 1/x - 3$ gives $x \leftarrow x(2 - 3x)$: 0.33, 0.3333, 0.33333333, error $3.3 \times 10^{-9}$. The relative error squares each step, which is how hardware refines reciprocals.

> [!question]- la-ps-gd-step-size | For $f(x) = \tfrac12x^\top Ax$ with $\lambda_{\max}(A) = 100$, what fixed gradient step sizes converge?
> $0 < \eta < 2/\lambda_{\max} = 0.02$. Each eigencomponent is multiplied by $1 - \eta\lambda_i$, which must have modulus below 1.

> [!question]- la-ps-cholesky-2x2 | Cholesky factor of $\begin{pmatrix} 4 & 2 \\ 2 & 3\end{pmatrix}$?
> $L = \begin{pmatrix} 2 & 0 \\ 1 & \sqrt2\end{pmatrix}$: $L_{11} = \sqrt4$, $L_{21} = 2/2$, $L_{22} = \sqrt{3 - 1}$.

> [!question]- la-ps-sample-cov-rank | 100 assets, 60 monthly returns. Rank of the sample covariance and the consequence?
> At most 59: demeaning uses one degree of freedom. At least 41 zero eigenvalues, so it cannot be inverted and an optimiser sees riskless portfolios; use a factor model or shrinkage.

> [!question]- la-ps-lagrange-xy | Maximise $xy$ subject to $x + y = 10$; what is the multiplier worth?
> $x = y = 5$, value 25, $\lambda = 5$. The optimal value is $c^2/4$ for budget $c$, whose derivative $c/2 = 5$ equals $\lambda$: one more unit of budget adds about 5.

> [!question]- la-ps-projection-onto-line | Closest point to the origin on the line $x + 2y = 5$, and the distance?
> $(1, 2)$ at distance $\sqrt5$. Project along the normal $a = (1, 2)$: $x = 5a/\lVert a\rVert^2$, distance $5/\lVert a\rVert$.

> [!question]- la-ps-kkt-halfspace | Minimise $x^2 + y^2$ subject to $x + y \ge 2$, with the multiplier.
> $(1, 1)$, value 2, multiplier 2. Stationarity $2x = \lambda$, $2y = \lambda$ with the constraint binding gives $x = y = 1$, $\lambda = 2 \ge 0$, so KKT holds and the problem is convex.

> [!question]- la-ps-taylor-mental-math | Estimate $e^{0.05}$, $\ln 1.02$ and $\sqrt{1.04}$ in your head.
> $1 + 0.05 + 0.00125 = 1.05125$ (true $1.05127$); $0.02 - 0.0002 = 0.0198$ (true $0.019803$); $1 + 0.02 - 0.0002 = 1.0198$ (true $1.019804$). Two Taylor terms plus the quadratic correction.

> [!question]- la-ps-householder-reflector | Determinant and eigenvalues of $H = I - 2uu^\top$ with $\lVert u\rVert = 1$?
> $\det H = -1$; eigenvalue $-1$ on $u$ and $+1$ on the $(n - 1)$-dimensional complement. $H$ is a symmetric orthogonal reflection, the building block of Householder QR.

> [!question]- la-ps-product-of-pd | $A$ and $B$ are symmetric positive definite. Is $AB$ symmetric? Are its eigenvalues positive?
> Generally not symmetric (for $A = \begin{pmatrix} 2 & 1 \\ 1 & 2\end{pmatrix}$, $B = \text{diag}(1, 3)$, $AB$ is not), but its eigenvalues are real and positive ($4 \pm\sqrt7$ here) because $AB$ is similar to $B^{1/2}AB^{1/2}$, which is SPD.

> [!question]- la-ps-ata-zero | Show that $A^\top A = 0$ implies $A = 0$.
> $\text{tr}(A^\top A) = \sum_{ij}a_{ij}^2 = 0$ forces every entry to be 0. The same argument shows $A^\top A$ is PSD and has the same null space as $A$.

> [!question]- la-ps-nilpotent | $N^k = 0$ for some $k$. What are the eigenvalues of $N$, and is $I - N$ invertible?
> All eigenvalues are 0 ($Nv = \lambda v$ gives $\lambda^kv = 0$). $I - N$ is invertible with inverse $I + N + \dots + N^{k-1}$, a terminating geometric series.

## In this repo and SDE-Interview-Prep

- Code: [problem_set.py](code/problem_set.py) computes and asserts every number in the cards and worked examples, grouped by card id.
- SDE bridge: [matrix exponentiation](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/03-Data-Structures-Algorithms/04-Gold-Standard-Cpp-Patterns/Math-and-Bit-Manipulation/matrix_exponentiation.cpp) for the Fibonacci card.
- More drills: [Probability Problem Set](../01-Probability/15-Probability-Problem-Set.md), [Statistics Problem Set](../02-Statistics-and-Econometrics/14-Statistics-Problem-Set.md).

## Further reading

- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 3 (calculus and linear algebra).
- Gilbert Strang, *Introduction to Linear Algebra*, 5th edition.
- Mark Joshi, Nick Denson and Andrew Downes, *Quant Job Interview Questions and Answers*, 2nd edition.
- Stephen Boyd and Lieven Vandenberghe, *Convex Optimization*, Cambridge University Press 2004, chapter 5 exercises.
- Roger Horn and Charles Johnson, *Matrix Analysis*, 2nd edition.
