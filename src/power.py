"""
power.py
--------
Sample size and statistical power calculations for the A/B test.

Primary metric: 4-week total household spend (continuous)
Test: Two-sample Welch's t-test (equal allocation, two-sided)

Key functions:
    sample_size_two_sample_ttest  — Required n per arm (continuous metric)
    achieved_power                — Compute power given n and sigma
    power_curve_table             — Sample size table across MDE/sigma scenarios
    binary_sample_size            — Required n per arm (binary metric / z-test)
"""

import numpy as np
import pandas as pd
from scipy import stats


def sample_size_two_sample_ttest(
    sigma: float,
    delta: float,
    alpha: float = 0.05,
    power: float = 0.80,
    two_sided: bool = True
) -> int:
    """
    Required sample size per arm for a two-sample t-test (equal allocation).

    Formula:
        n = 2 * sigma^2 * (z_{1-alpha/2} + z_{1-beta})^2 / delta^2

    Parameters
    ----------
    sigma : float
        Standard deviation of the outcome (4-week total spend).
    delta : float
        Minimum Detectable Effect (same unit as sigma, e.g., dollars per 4 weeks).
    alpha : float
        Significance level (default: 0.05).
    power : float
        Desired power 1 - beta (default: 0.80).
    two_sided : bool
        Use two-sided test (default: True).

    Returns
    -------
    int
        Required sample size per arm (rounded up).
    """
    z_a = stats.norm.ppf(1 - alpha / 2) if two_sided else stats.norm.ppf(1 - alpha)
    z_b = stats.norm.ppf(power)
    n   = 2 * sigma**2 * (z_a + z_b)**2 / delta**2
    return int(np.ceil(n))


def achieved_power(
    n: int,
    sigma: float,
    delta: float,
    alpha: float = 0.05,
    two_sided: bool = True
) -> float:
    """
    Compute the statistical power achieved for a given sample size.

    Parameters
    ----------
    n : int
        Sample size per arm.
    sigma : float
        Standard deviation of the outcome.
    delta : float
        Effect size to detect (same unit as sigma).
    alpha : float
        Significance level.
    two_sided : bool
        Use two-sided critical value.

    Returns
    -------
    float
        Achieved power (0 to 1).
    """
    z_a = stats.norm.ppf(1 - alpha / 2) if two_sided else stats.norm.ppf(1 - alpha)
    se  = np.sqrt(2 * sigma**2 / n)
    ncp = delta / se          # non-centrality parameter
    pwr = 1 - stats.norm.cdf(z_a - ncp) + stats.norm.cdf(-z_a - ncp)
    return pwr


def power_curve_table(
    mde_range: list,
    sigma_scenarios: dict,
    alpha: float = 0.05,
    power: float = 0.80
) -> pd.DataFrame:
    """
    Build a sample-size table across MDE values and sigma scenarios.

    Parameters
    ----------
    mde_range : list
        List of MDE values (in the same unit as sigma).
    sigma_scenarios : dict
        Dictionary of {label: sigma_value} for each variance scenario.
        E.g., {'Raw': 90.0, 'Winsorized': 78.0, 'CUPED': 58.0}
    alpha : float
        Significance level.
    power : float
        Desired power.

    Returns
    -------
    pd.DataFrame
        Rows = MDE values, Columns = sigma scenarios, Values = n per arm.
    """
    rows = []
    for delta in mde_range:
        row = {'MDE ($)': delta}
        for label, sigma in sigma_scenarios.items():
            row[f'n/arm ({label})'] = sample_size_two_sample_ttest(
                sigma, delta, alpha, power
            )
        rows.append(row)
    return pd.DataFrame(rows)


def binary_sample_size(
    p_control: float,
    p_treatment: float,
    alpha: float = 0.05,
    power: float = 0.80,
    two_sided: bool = True
) -> int:
    """
    Required sample size per arm for a two-proportion z-test (binary outcome).

    Used for secondary metric: conversion rate.

    Formula:
        n = (z_{1-alpha/2} + z_{1-beta})^2 * [p_C(1-p_C) + p_T(1-p_T)] / (p_T - p_C)^2

    Parameters
    ----------
    p_control : float
        Baseline conversion rate in control group.
    p_treatment : float
        Expected conversion rate in treatment group.
    alpha : float
        Significance level.
    power : float
        Desired power.
    two_sided : bool
        Use two-sided test.

    Returns
    -------
    int
        Required sample size per arm (rounded up).
    """
    z_a = stats.norm.ppf(1 - alpha / 2) if two_sided else stats.norm.ppf(1 - alpha)
    z_b = stats.norm.ppf(power)
    delta = p_treatment - p_control
    var   = p_control * (1 - p_control) + p_treatment * (1 - p_treatment)
    n     = (z_a + z_b)**2 * var / delta**2
    return int(np.ceil(n))
