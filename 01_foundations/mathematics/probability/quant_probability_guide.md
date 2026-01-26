# Probability & Statistics for Quant Interviews

The "Green Book" (*A Practical Guide to Quantitative Finance Interviews*) is the bible. Here are the core concepts you MUST master.

##  1. Expected Value (EV) & Linearity
*   **Concept:** $E[X+Y] = E[X] + E[Y]$ regardless of independence.
*   **Problem:** "A stick is broken at two random points. What is the average length of the middle piece?"
*   **Intuition:** By symmetry, all 3 pieces have the same distribution. Length is $1/3$.

##  2. Conditional Probability & Bayes
*   **Formula:** $P(A|B) = \frac{P(B|A)P(A)}{P(B)}$
*   **Problem:** "You have 2 coins. One is fair, one is 2-headed. You pick one and flip H. What is the prob it's the 2-headed coin?"
    *   $P(2H | H) = \frac{1 \cdot 0.5}{1 \cdot 0.5 + 0.5 \cdot 0.5} = \frac{0.5}{0.75} = 2/3$.

##  3. Markov Chains & Random Walks
*   **Gambler's Ruin:** Probability of hitting $A$ before $B$ starting at $k$: $P_k = k/N$ (if fair).
*   **Stopping Times:** Expected time to reach boundary.

##  4. Distributions
*   **Normal:** Central Limit Theorem.
*   **Lognormal:** Stock prices (BSM model).
*   **Poisson:** Arrival of orders in HFT.
*   **Geometric:** "Number of flips to get a Head". $E[X] = 1/p$.

##  Top Practice Questions
1.  **World Series:** Team A wins with prob 0.6. What is prob they win in 7 games?
2.  **Dice Sum:** Roll a die until sum > 100. What is the expected overshoot? (Renewal Theory).
3.  **Birthday Paradox:** How many people to have 50% chance of same birthday? (~23).
