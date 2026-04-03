"""
variance.py
-----------
Variance estimation and outlier handling for the A/B test design.

Key functions:
    winsorize_series       — Clip outliers at specified percentile bounds
    estimate_sigma         — Estimate conservative sigma for power analysis
    pre_post_variance      — Compare pre vs post σ (scale-adjusted)
"""

import pandas as pd
import numpy as np


def winsorize_series(
    s: pd.Series,
    lower_pct: float = 0.01,
    upper_pct: float = 0.99
) -> pd.Series:
    """
    Winsorize a series by clipping at the given percentile bounds.

    Parameters
    ----------
    s : pd.Series
        Input series (e.g., 4-week total spend).
    lower_pct : float
        Lower percentile clip (default: 0.01 = 1st percentile).
    upper_pct : float
        Upper percentile clip (default: 0.99 = 99th percentile).

    Returns
    -------
    pd.Series
        Winsorized series with same index.
    """
    lower = s.quantile(lower_pct)
    upper = s.quantile(upper_pct)
    return s.clip(lower=lower, upper=upper)


def estimate_sigma(
    rolling_windows_df: pd.DataFrame,
    pre_sigma_weekly: float,
    experiment_weeks: int = 4,
    sigma_col: str = 'std_spend_all'
) -> dict:
    """
    Estimate a conservative sigma for power analysis.

    Uses the maximum of:
    - Pre-period σ scaled to experiment window: pre_sigma_weekly * sqrt(experiment_weeks)
    - Median post-period σ from 4-week rolling windows (ITT)

    Parameters
    ----------
    rolling_windows_df : pd.DataFrame
        Output from metrics.compute_rolling_windows().
    pre_sigma_weekly : float
        Standard deviation of average weekly spend in the pre-period.
    experiment_weeks : int
        Number of weeks in the experiment window (default: 4).
    sigma_col : str
        Column in rolling_windows_df to use for post sigma (default: 'std_spend_all').

    Returns
    -------
    dict with keys:
        pre_sigma_scaled: pre-period sigma scaled to experiment window
        post_sigma:       median rolling window sigma (ITT)
        sigma_for_power:  max(pre_sigma_scaled, post_sigma) — conservative
    """
    pre_sigma_scaled = pre_sigma_weekly * np.sqrt(experiment_weeks)
    post_sigma       = rolling_windows_df[sigma_col].median()
    sigma_for_power  = max(pre_sigma_scaled, post_sigma)

    print("=== Sigma Estimation for Power Analysis ===")
    print(f"  Pre σ (weekly):           ${pre_sigma_weekly:.2f}")
    print(f"  Pre σ scaled ({experiment_weeks}-wk):      ${pre_sigma_scaled:.2f}")
    print(f"  Post σ median (ITT 4-wk): ${post_sigma:.2f}")
    print(f"  sigma_for_power:          ${sigma_for_power:.2f}  [max — conservative]")

    return {
        'pre_sigma_scaled': pre_sigma_scaled,
        'post_sigma':       post_sigma,
        'sigma_for_power':  sigma_for_power,
    }


def pre_post_variance_comparison(
    pre_weekly_spend: pd.Series,
    rolling_windows_df: pd.DataFrame,
    experiment_weeks: int = 4
) -> pd.DataFrame:
    """
    Compare pre-period and post-period variance side-by-side.

    Parameters
    ----------
    pre_weekly_spend : pd.Series
        Average weekly spend in the pre-period (per household).
    rolling_windows_df : pd.DataFrame
        Output from metrics.compute_rolling_windows().
    experiment_weeks : int
        Number of weeks in the experiment window (default: 4).

    Returns
    -------
    pd.DataFrame
        Summary comparison table.
    """
    pre_mean  = pre_weekly_spend.mean() * experiment_weeks
    pre_std   = pre_weekly_spend.std()  * np.sqrt(experiment_weeks)
    post_mean = rolling_windows_df['mean_spend_all'].median()
    post_std  = rolling_windows_df['std_spend_all'].median()

    summary = pd.DataFrame({
        'Period':       ['Pre (scaled)', 'Post (rolling median)'],
        'Mean ($)':     [round(pre_mean, 2), round(post_mean, 2)],
        'Std Dev ($)':  [round(pre_std, 2),  round(post_std, 2)],
        'CV':           [round(pre_std / pre_mean, 3), round(post_std / post_mean, 3)],
    })

    return summary
