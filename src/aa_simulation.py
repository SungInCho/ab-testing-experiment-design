"""
aa_simulation.py
----------------
A/A simulation framework for the A/B test design.

An A/A simulation randomly splits the population (with no treatment)
and runs many two-sample t-tests. Under the null hypothesis, we expect:
- False positive rate (FPR) ≈ alpha (typically 5%)
- p-value distribution uniform on [0, 1]

This validates that:
1. The test has correct type I error rate under the null
2. The noise floor (distribution of mean differences) is smaller than the MDE
3. The MDE is realistically detectable above the noise

Key functions:
    run_aa_simulation      — Run n_simulations A/A tests
    plot_aa_results        — Summarize simulation results
    check_mde_feasibility  — Check if MDE is above the noise floor
"""

import numpy as np
import pandas as pd
from scipy import stats


def run_aa_simulation(
    spend_data: pd.Series,
    n_simulations: int = 1000,
    alpha: float = 0.05,
    seed: int = 42
) -> pd.DataFrame:
    """
    Run A/A simulations: randomly split population and test for a difference.

    Parameters
    ----------
    spend_data : pd.Series
        4-week total spend for the eligible population (ITT, zeros included).
    n_simulations : int
        Number of random splits to run (default: 1000).
    alpha : float
        Significance level for false positive detection (default: 0.05).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        One row per simulation with columns:
        [diff_means, p_value, ci_lower, ci_upper, significant]
    """
    rng = np.random.RandomState(seed)
    n = len(spend_data)
    values = spend_data.values.copy()

    records = []
    for _ in range(n_simulations):
        # Random 50/50 split
        idx = rng.permutation(n)
        mid = n // 2
        group_a = values[idx[:mid]]
        group_b = values[idx[mid:]]

        t_stat, p_val = stats.ttest_ind(group_a, group_b, equal_var=False)

        diff = group_a.mean() - group_b.mean()
        se   = np.sqrt(group_a.var(ddof=1)/len(group_a) +
                       group_b.var(ddof=1)/len(group_b))
        t_crit = stats.t.ppf(1 - alpha/2, df=len(group_a)+len(group_b)-2)
        ci_lower = diff - t_crit * se
        ci_upper = diff + t_crit * se

        records.append({
            'diff_means': diff,
            'p_value':    p_val,
            'ci_lower':   ci_lower,
            'ci_upper':   ci_upper,
            'significant': int(p_val < alpha),
        })

    df = pd.DataFrame(records)

    fpr = df['significant'].mean()
    print(f"=== A/A Simulation Results ({n_simulations} runs) ===")
    print(f"  False Positive Rate (FPR): {fpr:.3f}  [expected ≈ {alpha:.2f}]")
    print(f"  Mean |diff|:               ${df['diff_means'].abs().mean():.2f}")
    print(f"  95th pct |diff|:           ${df['diff_means'].abs().quantile(0.95):.2f}")
    print(f"  Std of diff:               ${df['diff_means'].std():.2f}")

    return df


def check_mde_feasibility(
    aa_results: pd.DataFrame,
    mde: float,
    noise_percentile: float = 0.95
) -> dict:
    """
    Check whether the target MDE is above the A/A noise floor.

    The noise floor is the 95th percentile of |mean differences| under the null.
    If MDE > noise_floor, the experiment can plausibly detect the effect.

    Parameters
    ----------
    aa_results : pd.DataFrame
        Output from run_aa_simulation().
    mde : float
        Target Minimum Detectable Effect (same unit as spend_data).
    noise_percentile : float
        Percentile to use for noise floor (default: 0.95).

    Returns
    -------
    dict with keys: mde, noise_floor, signal_to_noise, feasible
    """
    noise_floor     = aa_results['diff_means'].abs().quantile(noise_percentile)
    signal_to_noise = mde / noise_floor
    feasible        = mde > noise_floor

    print(f"=== MDE Feasibility Check ===")
    print(f"  MDE target:          ${mde:.2f}")
    print(f"  Noise floor ({int(noise_percentile*100)}th pct): ${noise_floor:.2f}")
    print(f"  Signal-to-noise:     {signal_to_noise:.2f}x")
    print(f"  MDE feasible:        {'YES ✓' if feasible else 'NO ⚠️ — consider increasing MDE or sample'}")

    return {
        'mde':              mde,
        'noise_floor':      noise_floor,
        'signal_to_noise':  signal_to_noise,
        'feasible':         feasible,
    }
