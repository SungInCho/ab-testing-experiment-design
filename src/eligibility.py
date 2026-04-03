"""
eligibility.py
--------------
Eligibility filtering for the A/B test experiment design.

Eligibility criteria (all must be met):
    1. Active in pre-period (has ≥1 transaction in weeks 1–71)
    2. At least 2 trips in the pre-period
    3. Recency ≤ 90 days from the end of the pre-period
    4. Has received at least 1 campaign historically (contactable via mail)

The resulting eligible population forms the ITT (Intent-to-Treat) analysis set.
"""

import pandas as pd


def filter_eligible_households(
    hh_features: pd.DataFrame,
    min_trips: int = 2,
    max_recency_days: int = 90,
    min_campaigns: int = 1
) -> pd.DataFrame:
    """
    Apply eligibility criteria and return the eligible subset.

    Parameters
    ----------
    hh_features : pd.DataFrame
        Household-level feature table from preprocessing.build_hh_features()
        (must include: total_trips, days_since_last_purchase, n_campaigns_received)
    min_trips : int
        Minimum number of pre-period trips required (default: 2)
    max_recency_days : int
        Maximum days since last purchase (default: 90)
    min_campaigns : int
        Minimum number of campaigns previously received (default: 1)

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame of eligible households, with eligibility flags added.
    """
    df = hh_features.copy()

    # Apply each criterion as a boolean flag
    df['elig_min_trips']     = df['total_trips'] >= min_trips
    df['elig_recency']       = df['days_since_last_purchase'] <= max_recency_days
    df['elig_campaign']      = df['n_campaigns_received'] >= min_campaigns

    # Combined eligibility
    df['eligible'] = (
        df['elig_min_trips'] &
        df['elig_recency'] &
        df['elig_campaign']
    )

    eligible = df[df['eligible']].copy()

    print("=== Eligibility Filter Summary ===")
    print(f"  Total households:           {len(df):,}")
    print(f"  Fail min_trips ({min_trips}):         "
          f"{(~df['elig_min_trips']).sum():,}")
    print(f"  Fail recency (>{max_recency_days}d):        "
          f"{(~df['elig_recency']).sum():,}")
    print(f"  Fail campaign history:      "
          f"{(~df['elig_campaign']).sum():,}")
    print(f"  Eligible households:        {len(eligible):,}")
    print(f"  Eligibility rate:           {len(eligible)/len(df):.1%}")

    return eligible


def describe_eligible_population(eligible: pd.DataFrame) -> None:
    """
    Print a descriptive summary of the eligible population.
    """
    print("=== Eligible Population Summary ===")
    print(f"  N eligible: {len(eligible):,}")
    print()
    print("  Avg weekly spend:")
    print(eligible['avg_weekly_spend'].describe().round(2))
    print()
    print("  Spend tier distribution:")
    print(eligible['spend_tier'].value_counts().sort_index())
    print()
    print("  Recency band distribution:")
    print(eligible['recency_band'].value_counts().sort_index())
