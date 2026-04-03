"""
randomization.py
----------------
Stratified randomization for the A/B test experiment.

Stratification variables:
    spend_tier   (4 levels: Low, Medium-Low, Medium-High, High)
    recency_band (4 levels: 0-7d, 8-30d, 31-90d, 90d+)

Within each stratum (spend_tier x recency_band), households are shuffled and
split 50/50 into Treatment and Control groups.

Key functions:
    stratified_randomize     — Assign treatment/control labels
    check_balance            — Compare covariate means across groups
    check_srm                — Sample Ratio Mismatch test (binomial)
    check_duplicates         — Verify no household appears twice
"""

import numpy as np
import pandas as pd
from scipy import stats


def stratified_randomize(
    df: pd.DataFrame,
    strata_cols: list = None,
    seed: int = 42
) -> pd.DataFrame:
    """
    Perform stratified 50/50 randomization.

    Within each stratum defined by strata_cols, households are randomly shuffled
    and split into Treatment/Control. If a stratum has an odd number of households,
    one group gets floor(n/2) and the other gets ceil(n/2).

    Parameters
    ----------
    df : pd.DataFrame
        Eligible household DataFrame (must include strata_cols).
    strata_cols : list
        Columns defining stratification (default: ['spend_tier', 'recency_band']).
    seed : int
        Random seed for reproducibility (default: 42).

    Returns
    -------
    pd.DataFrame
        Input DataFrame with 'group' column added ('Treatment' or 'Control').
    """
    if strata_cols is None:
        strata_cols = ['spend_tier', 'recency_band']

    rng = np.random.RandomState(seed)
    assignments = pd.Series(index=df.index, dtype=str)

    for name, group in df.groupby(strata_cols, observed=True):
        idx = group.index.values.copy()
        rng.shuffle(idx)
        mid = len(idx) // 2
        assignments.loc[idx[:mid]]  = 'Treatment'
        assignments.loc[idx[mid:]]  = 'Control'

    result = df.copy()
    result['group'] = assignments

    n_t = (result['group'] == 'Treatment').sum()
    n_c = (result['group'] == 'Control').sum()
    print(f"Randomization complete: {n_t} Treatment, {n_c} Control")

    return result


def check_srm(
    n_treatment: int,
    n_control: int,
    expected_ratio: float = 0.5,
    alpha: float = 0.01
) -> dict:
    """
    Sample Ratio Mismatch (SRM) test using a binomial test.

    Tests whether the observed treatment proportion significantly deviates
    from the expected 50/50 split.

    Parameters
    ----------
    n_treatment : int
        Number of households in treatment group.
    n_control : int
        Number of households in control group.
    expected_ratio : float
        Expected proportion of treatment (default: 0.5).
    alpha : float
        Significance level for SRM alert (default: 0.01).

    Returns
    -------
    dict with keys: n_total, n_treatment, n_control, observed_ratio, p_value, srm_detected
    """
    n_total = n_treatment + n_control
    result  = stats.binomtest(n_treatment, n_total, p=expected_ratio)
    p_value = result.pvalue
    srm     = p_value < alpha

    print("=== SRM Test ===")
    print(f"  N total:          {n_total:,}")
    print(f"  N treatment:      {n_treatment:,} ({n_treatment/n_total:.2%})")
    print(f"  N control:        {n_control:,}   ({n_control/n_total:.2%})")
    print(f"  p-value:          {p_value:.4f}")
    print(f"  SRM detected:     {'YES ⚠️' if srm else 'NO ✓'}")

    return {
        'n_total':          n_total,
        'n_treatment':      n_treatment,
        'n_control':        n_control,
        'observed_ratio':   n_treatment / n_total,
        'p_value':          p_value,
        'srm_detected':     srm,
    }


def check_balance(
    df: pd.DataFrame,
    group_col: str = 'group',
    continuous_cols: list = None,
    categorical_cols: list = None,
    alpha: float = 0.05
) -> pd.DataFrame:
    """
    Check covariate balance between Treatment and Control.

    - Continuous variables: Welch's t-test
    - Categorical variables: Chi-squared test

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with group assignments and covariate columns.
    group_col : str
        Column containing group labels ('Treatment' / 'Control').
    continuous_cols : list
        Continuous covariate columns to test.
    categorical_cols : list
        Categorical covariate columns to test.
    alpha : float
        Significance level for flagging imbalance.

    Returns
    -------
    pd.DataFrame
        Balance check summary with mean/proportion by group and p-values.
    """
    if continuous_cols is None:
        continuous_cols = ['avg_weekly_spend', 'total_trips', 'days_since_last_purchase']
    if categorical_cols is None:
        categorical_cols = []

    t_group = df[df[group_col] == 'Treatment']
    c_group = df[df[group_col] == 'Control']

    rows = []
    for col in continuous_cols:
        if col not in df.columns:
            continue
        t_vals = t_group[col].dropna()
        c_vals = c_group[col].dropna()
        t_stat, p = stats.ttest_ind(t_vals, c_vals, equal_var=False)
        rows.append({
            'Variable':        col,
            'Type':            'continuous',
            'Treatment Mean':  round(t_vals.mean(), 3),
            'Control Mean':    round(c_vals.mean(), 3),
            'Diff':            round(t_vals.mean() - c_vals.mean(), 3),
            'p-value':         round(p, 4),
            'Significant?':    'YES ⚠️' if p < alpha else 'NO ✓',
        })

    for col in categorical_cols:
        if col not in df.columns:
            continue
        ct = pd.crosstab(df[col], df[group_col])
        chi2, p, dof, _ = stats.chi2_contingency(ct)
        rows.append({
            'Variable':        col,
            'Type':            'categorical',
            'Treatment Mean':  '-',
            'Control Mean':    '-',
            'Diff':            '-',
            'p-value':         round(p, 4),
            'Significant?':    'YES ⚠️' if p < alpha else 'NO ✓',
        })

    return pd.DataFrame(rows)


def check_duplicates(df: pd.DataFrame, key_col: str = 'household_key') -> dict:
    """
    Verify that no household appears more than once in the assignment table.

    Parameters
    ----------
    df : pd.DataFrame
        Randomized DataFrame.
    key_col : str
        Household identifier column.

    Returns
    -------
    dict with keys: n_total, n_unique, n_duplicates, duplicates_found
    """
    n_total     = len(df)
    n_unique    = df[key_col].nunique()
    n_duplicates = n_total - n_unique
    dupes       = df[df.duplicated(subset=key_col, keep=False)]

    print("=== Duplicate Check ===")
    print(f"  Total rows:       {n_total:,}")
    print(f"  Unique keys:      {n_unique:,}")
    print(f"  Duplicate keys:   {n_duplicates}")
    if n_duplicates > 0:
        print("  ⚠️  Duplicates detected!")
        print(dupes[[key_col]].value_counts().head(10))
    else:
        print("  ✓  No duplicates found.")

    return {
        'n_total':          n_total,
        'n_unique':         n_unique,
        'n_duplicates':     n_duplicates,
        'duplicates_found': n_duplicates > 0,
    }
