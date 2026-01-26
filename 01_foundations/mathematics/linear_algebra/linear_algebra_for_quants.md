# Linear Algebra for Quant Finance

Linear Algebra is the engine room of quantitative finance, powering everything from Portfolio Optimization to Machine Learning.

## 🔑 Key Concepts

### 1. Eigenvalues and Eigenvectors
*   **Definition:** $Av = \lambda v$.
*   **Application:** **Principal Component Analysis (PCA)**.
    *   Used to reduce the dimensionality of stock returns.
    *   The *Eigenvectors* of the covariance matrix represent "Market Factors" (e.g., Market mode, Sector mode).
    *   The *Eigenvalues* represent the variance explained by that factor.

### 2. Matrix Decompositions
*   **Cholesky Decomposition ($A = LL^T$):**
    *   Used to generate correlated random variables for Monte Carlo simulations.
    *   If you need to simulate correlated stock paths, you decompose the Correlation Matrix $\Sigma$.
*   **SVD (Singular Value Decomposition):**
    *   Robust way to perform PCA and solve linear least squares.

### 3. Positive Definite Matrices
*   **Covariance Matrices** MUST be Positive Semi-Definite (PSD).
*   **Why?** Variance ($w^T \Sigma w$) cannot be negative.
*   **Problem:** Empirical covariance matrices might not be PSD due to missing data. You need to "fix" them (e.g., finding the nearest correlation matrix).

### 4. Least Squares (OLS)
*   **Formula:** $\beta = (X^T X)^{-1} X^T y$.
*   **Application:** Calculating Hedge Ratios, Beta, and Factor Loadings.
*   **Numerical Stability:** Solving $Ax=b$ via `inv(X'X)` is numerically unstable. Use QR decomposition or SVD instead.

## 📝 Common Interview Questions
1.  **"What is the geometric interpretation of the determinant?"** (Volume scaling factor).
2.  **"How do you generate correlated random normals?"** (Cholesky Decomposition).
3.  **"What happens if your Covariance Matrix is not invertible?"** (Multicollinearity - use Ridge Regression or PCA).
