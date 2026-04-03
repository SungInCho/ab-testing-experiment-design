"""
metrics.py
----------
Outcome metric construction for the A/B test analysis.

Primary metric: 4-week total household spend (ITT — zeros included)
Secondary metrics: conversion rate, basket size ($/trip), total trips

Key functions:
    compute_4wk_window_spend   — Aggregate spend for a specific 4-week window
    compute_iterable_windows   — Compute rolling 4-week window metrics
    compute_secondary_metrics  — Build secondary metric columns
"""

import pandas as pd
import numpy as np

# ─── Experiment constants ─────────────────────────────────────────────────────
EXPERIMENT_WEEKS = 4        # Length of the post-treatment window
MDE_4WK = 14.00             # Minimum Detectable Effect ($, 4-week total)


def compute_4wk_window_spend(
    weekly_hh: pd.DataFrame,
    eligible_keys: list,
    week_start: int,
    week_end: int,
    outcome_col: str = 'weekly_spend'
) -> pd.Series:
    """
    Compute ITT 4-week total spend for a given window.

    Households with zero transactions in the window are included as 0 (ITT).

    Parameters
    ----------
    weekly_hh : pd.DataFrame
        Weekly household spend table with columns:
        ['household_key', 'WEEK_NO', outcome_col]
    eligible_keys : list
        All eligible household keys (defines the ITT population).
    week_start, week_end : int
        Inclusive week range for the 4-week window.
    outcome_col : str
        Column name for spend (default: 'weekly_spend').

    Returns
    -------
    pd.Series
        Index = household_key, Values = 4-week total spend (zeros included).
    """
    window = weekly_hh[weekly_hh['WEEK_NO'].between(week_start, week_end)]
    hh_agg = window.groupby('household_key')[outcome_col].sum()

    # ITT: fill missing households with 0
    full = pd.Series(0.0, index=list(eligible_keys))
    full.update(hh_agg)

    return full


def compute_rolling_windows(
    weekly_hh: pd.DataFrame,
    eligible_keys: list,
    window_size: int = 4,
    post_start: int = 72,
    post_end: int = 102,
    outcome_col: str = 'weekly_spend'
) -> pd.DataFrame:
    """
    Compute rolling window statistics over the post-period.

    For each non-overlapping window of `window_size` weeks, compute:
    - std_spend_all: ITT σ (all eligible households, zeros included)
    - std_spend_active: σ for active-only households
    - mean_spend: mean 4-week total spend (ITT)
    - zero_rate: fraction with zero spend in window

    Parameters
    ----------
    weekly_hh : pd.DataFrame
        Weekly household spend table.
    eligible_keys : list
        Full ITT population keys.
    window_size : int
        Number of weeks per window (default: 4).
    post_start, post_end : int
        Post-period week range.
    outcome_col : str
        Spend column name.

    Returns
    -------
    pd.DataFrame
        One row per window with window boundaries and summary statistics.
    """
    records = []
    for ws in range(post_start, post_end - window_size + 2, window_size):
        we = ws + window_size - 1
        if we > post_end:
            break

        window = weekly_hh[weekly_hh['WEEK_NO'].between(ws, we)]
        hh_agg = window.groupby('household_key')[outcome_col].sum()

        # ITT population
        full = pd.Series(0.0, index=list(eligible_keys))
        full.update(hh_agg)

        active = full[full > 0]

        records.append({
            'week_start':       ws,
            'week_end':         we,
            'mean_spend_all':   full.mean(),
            'std_spend_all':    full.std(),      # ITT sigma — use for power analysis
            'std_spend_active': active.std(),    # Active-only sigma
            'zero_rate':        (full == 0).mean(),
            'n_active':         len(active),
            'n_total':          len(full),
        })

    return pd.DataFrame(records)


def compute_secondary_metrics(
    eligible: pd.DataFrame,
    spend_col: str = 'spend_4wk',
    trips_col: str = 'trips_4wk'
) -> pd.DataFrame:
    """
    Add secondary metric columns to the eligible DataFrame.

    Secondary metrics:
        - conversion (binary): 1 if any purchase in 4-week window
        - basket_size: spend / trips (0 if no trips)

    Parameters
    ----------
    eligible : pd.DataFrame
        Eligible households with spend_4wk and trips_4wk columns.

    Returns
    -------
    pd.DataFrame
        Input DataFrame with 'conversion' and 'basket_size_4wk' added.
    """
    df = eligible.copy()
    df['conversion'] = (df[spend_col] > 0).astype(int)
    df['basket_size_4wk'] = np.where(
        df[trips_col] > 0,
        df[spend_col] / df[trips_col],
        0.0
    )
    return df
