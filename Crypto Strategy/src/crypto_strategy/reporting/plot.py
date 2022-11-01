import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from crypto_strategy.data import join_path
from .base import generate_cscv


def plot_indicators(portfolio, output_path=None, filename=None, show_fig=False):
    items = ['final_value', 'sharpe_ratio', 'sortino_ratio']
    fig, axes = plt.subplots(1, len(items), figsize=(15, 3),
                             sharey=False, sharex=False, constrained_layout=False)
    fig.subplots_adjust(top=0.75)
    fig.suptitle('Partial Differentiation')

    final_value = portfolio.final_value()
    if isinstance(final_value.index, pd.MultiIndex):
        index_names = final_value.index.names
    else:
        index_names = [final_value.index.name]

    for i, item in enumerate(items):
        results = {}
        for name in index_names:
            s = getattr(portfolio, item)()
            s = s.replace([np.inf, -np.inf], np.nan)
            results[name] = s.groupby(name).mean()
        results = pd.DataFrame(results)
        axes[i].title.set_text(item)
        results.plot(ax=axes[i])

    if output_path and filename:
        file_diff = join_path(output_path, filename + '-diff.png')
        plt.savefig(file_diff)

    results = generate_cscv(portfolio)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5),
                             sharey=False, sharex=False, constrained_layout=False)
    fig.subplots_adjust(bottom=0.5)
    fig.suptitle('Combinatorially Symmetric Cross-validation')

    pbo_test = round(results['pbo_test'] * 100, 2)
    axes[0].title.set_text(f'Probability of overfitting: {pbo_test} %')
    axes[0].hist(x=[r for r in results['logits'] if r > -10000], bins='auto')
    axes[0].set_xlabel('Logits')
    axes[0].set_ylabel('Frequency')

    # performance degradation
    axes[1].title.set_text('Performance degradation')
    x, y = pd.DataFrame([results['R_n_star'], results['R_bar_n_star']]).dropna(axis=1).values
    sns.regplot(x, y, ax=axes[1])
    # axes[1].set_xlim(min(results['R_n_star']) * 1.2,max(results['R_n_star']) * 1.2)
    # axes[1].set_ylim(min(results['R_bar_n_star']) * 1.2,max(results['R_bar_n_star']) * 1.2)
    axes[1].set_xlabel('In-sample Performance')
    axes[1].set_ylabel('Out-of-sample Performance')

    # first and second Stochastic dominance
    axes[2].title.set_text('Stochastic dominance')
    if len(results['dom_df']) != 0:
        results['dom_df'].plot(ax=axes[2], secondary_y=['SD2'])
    axes[2].set_xlabel('Performance optimized vs non-optimized')
    axes[2].set_ylabel('Frequency')

    if output_path and filename:
        file_cscv = join_path(output_path, filename + '-cscv.png')
        plt.savefig(file_cscv)

    if show_fig:
        plt.show()


def plot_returns(btc_acc_returns, eth_acc_returns, pf_acc_returns, start_date):
    fig, ax = plt.subplots()
    btc_acc_returns.plot(figsize=(8, 6), label='BTC')
    ax.annotate(f'{btc_acc_returns[-1]:.2f}', (btc_acc_returns.index[-1], btc_acc_returns[-1]))
    eth_acc_returns.plot(label='ETH')
    ax.annotate(f'{eth_acc_returns[-1]:.2f}', (eth_acc_returns.index[-1], eth_acc_returns[-1]))
    pf_acc_returns.plot(label='Portfolio')
    ax.annotate(f'{pf_acc_returns[-1]:.2f}', (pf_acc_returns.index[-1], pf_acc_returns[-1]))
    ax.legend()
    ax.set_title(f'{start_date}-day Portfolio Return')
    fig.tight_layout()
