import numpy as np
import matplotlib.pyplot as plt

def euler_maruyama(drift_func, diffusion_func, x0, T, dt):
    """
    Euler-Maruyama Numerical Solver for SDE: dX = a(X,t)dt + b(X,t)dW
    """
    N = int(T / dt)
    t = np.linspace(0, T, N+1)
    X = np.zeros(N+1)
    X[0] = x0
    
    for i in range(N):
        dW = np.random.normal(0, np.sqrt(dt))
        X[i+1] = X[i] + drift_func(X[i], t[i]) * dt + diffusion_func(X[i], t[i]) * dW
        
    return t, X

# Example 1: Geometric Brownian Motion (GBM)
# dS = mu*S*dt + sigma*S*dW
mu = 0.1
sigma = 0.2

gbm_drift = lambda S, t: mu * S
gbm_diffusion = lambda S, t: sigma * S

t_gbm, S_gbm = euler_maruyama(gbm_drift, gbm_diffusion, x0=100, T=1, dt=0.001)

# Example 2: Vasicek Model (Mean Reverting)
# dr = kappa*(theta - r)*dt + sigma*dW
kappa = 3.0
theta = 0.05
sig_vas = 0.03

vas_drift = lambda r, t: kappa * (theta - r)
vas_diffusion = lambda r, t: sig_vas

t_vas, r_vas = euler_maruyama(vas_drift, vas_diffusion, x0=0.02, T=1, dt=0.001)

# Plotting
fig, ax = plt.subplots(2, 1, figsize=(10, 8))

ax[0].plot(t_gbm, S_gbm)
ax[0].set_title('GBM Simulation (Euler-Maruyama)')
ax[0].grid(True)

ax[1].plot(t_vas, r_vas, color='orange')
ax[1].set_title('Vasicek Model Simulation (Mean Reversion)')
ax[1].grid(True)

plt.tight_layout()
plt.show()
