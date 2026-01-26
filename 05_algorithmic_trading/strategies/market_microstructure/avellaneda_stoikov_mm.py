import numpy as np
import matplotlib.pyplot as plt

class AvellanedaStoikovSimulator:
    """
    Simulates the Avellaneda-Stoikov Market Making model.
    
    Reference: "High-frequency trading in a limit order book" (2008)
    
    Key Concepts:
    - Inventory Risk: As q (inventory) deviates from 0, we skew quotes to revert.
    - Reservation Price: r(s, t, q) = s - q * gamma * sigma^2 * (T - t)
    - Optimal Spread: Depends on kappa (market order arrival intensity).
    """
    
    def __init__(self, S0=100, T=1.0, sigma=2, dt=0.005, gamma=0.1, k=1.5, A=140):
        self.S0 = S0       # Initial Price
        self.T = T         # Total Time
        self.sigma = sigma # Volatility
        self.dt = dt       # Time step
        self.gamma = gamma # Risk aversion
        self.k = k         # Order book liquidity param
        self.A = A         # Order arrival rate param
        
        self.M = int(T/dt)
        self.time = np.linspace(0, T, self.M+1)
        
    def run(self):
        S = np.zeros(self.M+1)
        q = np.zeros(self.M+1) # Inventory
        cash = np.zeros(self.M+1)
        wealth = np.zeros(self.M+1)
        
        S[0] = self.S0
        
        for i in range(1, self.M+1):
            # 1. Evolve Mid-Price (Geometric Brownian Motion)
            dW = np.random.normal(0, np.sqrt(self.dt))
            S[i] = S[i-1] + self.sigma * dW
            
            # 2. Calculate Reservation Price and Quotes
            # r = S - q * gamma * sigma^2 * (T - t)
            remaining_time = self.T - self.time[i-1]
            reservation_price = S[i-1] - q[i-1] * self.gamma * (self.sigma**2) * remaining_time
            
            # spread = gamma * sigma^2 * (T - t) + (2/gamma) * ln(1 + gamma/k)
            spread = self.gamma * (self.sigma**2) * remaining_time + (2/self.gamma) * np.log(1 + self.gamma/self.k)
            
            bid = reservation_price - spread/2
            ask = reservation_price + spread/2
            
            # 3. Simulate Market Order Arrivals (Poisson Process)
            # Prob of fill decays exponentially with distance from mid-price (delta)
            delta_b = S[i-1] - bid
            delta_a = ask - S[i-1]
            
            lambda_b = self.A * np.exp(-self.k * delta_b)
            lambda_a = self.A * np.exp(-self.k * delta_a)
            
            prob_b = lambda_b * self.dt
            prob_a = lambda_a * self.dt
            
            # Execution
            q[i] = q[i-1]
            cash[i] = cash[i-1]
            
            # Did someone hit our bid? (We buy)
            if np.random.rand() < prob_b:
                q[i] += 1
                cash[i] -= bid
                
            # Did someone lift our ask? (We sell)
            if np.random.rand() < prob_a:
                q[i] -= 1
                cash[i] += ask
                
            wealth[i] = cash[i] + q[i] * S[i]
            
        return self.time, S, q, wealth

if __name__ == "__main__":
    sim = AvellanedaStoikovSimulator()
    t, S, q, W = sim.run()
    
    fig, ax = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    ax[0].plot(t, S, label='Mid Price')
    ax[0].set_title('Stock Price')
    ax[0].grid(True)
    
    ax[1].plot(t, q, label='Inventory (q)', color='orange')
    ax[1].set_title('Inventory Position')
    ax[1].grid(True)
    
    ax[2].plot(t, W, label='Total Wealth', color='green')
    ax[2].set_title('P&L (Wealth)')
    ax[2].grid(True)
    
    plt.show()
