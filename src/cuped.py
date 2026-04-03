"""
cuped.py
--------
CUPED (Controlled-experiment Using Pre-Experiment Data) variance reduction.

CUPED adjusts the post-period outcome using a correlated pre-period covariate
to remove predictable variation, reducing variance and increasing test power.

Formula:
    Y_cuped_i = Y_post_i - theta * (X_pre_i - mean(X_pre))
    theta      = Cov(Y_post, X_pre) / Var(X_pre)
    Var(Y_cuped) = Var(Y_post) * (1 - rho^2)

Granularity alignment (important):
    Y_post: 4-week total spend (the actual experiment metric)
    X_pre:  pre-period avg weekly spend * 4 (scaled to same 4-week unit)

Key functions:
    compute_cuped            — Apply CUPED adjustment and return results
    cuped_variance_reduction — Report variance reduction from CUPED
"""

import numpy as np
import pandas as pd


def compute_cuped(
    y_post: pd.Series,
    x_pre: pd.Series,
) -> dict:
    """
    Apply CUPED adjustment to the post-period outcome.

    Parameters
    ----------
    y_post : pd.Series
        Post-period outcome (4-week total spend).
        Must be aligned with x_pre by index.
    x_pre : pd.Series
        Pre-period covariate (avg weekly spend * EXPERIMENT_WEEKS).
        Must be aligned with y_post by index.

    Returns
    -------
    dict with keys:
        y_cuped           : pd.Series — CUPED-adjusted outcome
        theta             : float     — regression coefficient
        rho               : float     — pre-post correlation
        sigma_original    : float     — std dev of Y_post
        sigma_cuped       : float     — std dev of Y_cuped
        variance_reduction: float     — fractional variance reduction (0–1)
    """
    # Align on common index
    common = y_post.index.intersection(x_pre.index)
    y = y_post.loc[common]
    x = x_pre.loc[common]

    rho   = y.corr(x)
    theta = np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1)

    y_cuped = y - theta * (x - x.mean())

    sigma_original = y.std()
    sigma_cuped    = y_cuped.std()
    var_reduction  = 1 - (sigma_cuped**2 / sigma_original**2)

    print("=== CUPED Variance Reduction (4-Week Total Spend) ===")
    print(f"  Pre-post correlation (rho):    {rho:.4f}")
    print(f"  theta (regression coeff):      {theta:.4f}")
    print(f"  sigma (original):              ${sigma_original:.2f}")
    print(f"  sigma (CUPED):                 ${sigma_cuped:.2f}")
    print(f"  Variance reduction (1 - rho^2):{var_reduction:.2%}")
    print(f"  Theoretical:                   {1 - rho**2:.2%}")

    return {
        'y_cuped':            y_cuped,
        'theta':              theta,
        'rho':                rho,
        'sigma_original':     sigma_original,
        'sigma_cuped':        sigma_cuped,
        'variance_reduction': var_reduction,
    }


def cuped_adjusted_sigma(sigma: float, rho: float) -> float:
    """
    Compute the CUPED-adjusted sigma given raw sigma and pre-post correlation.

    Parameters
    ----------
    sigma : float
        Raw standard deviation of the outcome.
    rho : float
        Pearson correlation between pre-period covariate and post-period outcome.

    Returns
    -------
    float
        CUPED-adjusted sigma = sigma * sqrt(1 - rho^2)
    """
    return sigma * np.sqrt(1 - rho**2)
