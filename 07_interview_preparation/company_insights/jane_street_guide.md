# Jane Street Interview Preparation Guide

Jane Street is known for its focus on probability, mental math, and market intuition. They don't just want the right answer; they want to see *how* you think and how you handle uncertainty.

## 🧠 Types of Questions

### 1. Probability Puzzles
*   **The Coin Flip Series:** "I flip a coin. If H, I stop. If T, I flip again. What is the expected number of flips?" (Geometric Distribution)
*   **Dice Games:** "We roll a die. You can choose to take the value in dollars or roll again. If you roll again, you *must* take the new value. What is the EV of this game? What if you have 2 re-rolls?" (Dynamic Programming / Backwards Induction)
*   **Stick Breaking:** "Break a stick at two random points. What is the probability the three pieces form a triangle?"

### 2. Market Making & Betting
*   **"Make me a market on..."**: They might ask you to make a bid-ask spread on something obscure (e.g., "The population of Nigeria") or mathematical (e.g., "The sum of 5 dice rolls").
*   **The Confidence Interval:** "Give me a 90% confidence interval for the number of Starbucks in NYC. Now, I will bet against you if you are too wide or too narrow."
    *   *Tip:* Being too wide means you are giving away "free option value". Being too narrow means you are exposed to "tail risk".

### 3. Estimations (Fermi Problems)
*   "How many piano tuners are there in Chicago?"
*   "How much does the Empire State Building weigh?"
    *   *Strategy:* Break it down. Volume * Density. Number of floors * Area per floor * ...

## 💡 Key Concepts to Master
1.  **Expected Value (EV):** $E[X] = \sum x_i p_i$. Always calculate the "fair value" first.
2.  **Conditional Probability:** Bayes' Theorem is your best friend.
3.  **Linearity of Expectation:** $E[A+B] = E[A] + E[B]$. Crucial for simplifying complex sums.
4.  **Sizing Bets:** Kelly Criterion $f^* = \frac{bp - q}{b}$. Don't bet the house on a 51% edge.

## 📝 Practice Problem
**Game:** You have a 100-sided die (1-100). You roll it once. You can choose to keep the roll ($) or pay $1 to roll again. You can do this as many times as you want. What is the fair value of this game?

**Solution Approach:**
Let $V$ be the value of the game.
If you roll $X$, you stop if $X > V - 1$.
$V = \frac{1}{100} \sum_{i=1}^{100} \max(i, V-1)$
(This requires recursive solving or estimating the threshold).
