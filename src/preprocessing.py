"""
preprocessing.py
----------------
Data loading, joining, and feature engineering for the dunnhumby
Complete Journey dataset.

Key functions:
    load_raw_data          — Load all raw CSV files into DataFrames
    enrich_transactions    — Join transaction_data with product info
    build_hh_features      — Aggregate to household-level feature table
    join_demographics      — Left-join hh_demographic onto features
    join_campaign_history  — Summarize campaign and coupon redemption history
"""

import os
import pandas as pd
import numpy as np

# ─── Time period constants ────────────────────────────────────────────────────
PRE_WEEK_START  = 1
PRE_WEEK_END    = 71
POST_WEEK_START = 72
POST_WEEK_END   = 102


def load_raw_data(data_dir: str) -> dict[str, pd.DataFrame]:
    """
    Load all raw CSV files from data_dir into a dictionary of DataFrames.

    Parameters
    ----------
    data_dir : str
        Path to the directory containing the raw CSV files.

    Returns
    -------
    dict[str, pd.DataFrame]
        Keys: 'transactions', 'demographic', 'campaign_table',
              'campaign_desc', 'coupon', 'coupon_redempt', 'product', 'causal'
    """
    files = {
        'transactions':    'transaction_data.csv',
        'demographic':     'hh_demographic.csv',
        'campaign_table':  'campaign_table.csv',
        'campaign_desc':   'campaign_desc.csv',
        'coupon':          'coupon.csv',
        'coupon_redempt':  'coupon_redempt.csv',
        'product':         'product.csv',
        'causal':          'causal_data.csv',
    }
    data = {}
    for key, fname in files.items():
        path = os.path.join(data_dir, fname)
        data[key] = pd.read_csv(path)
        print(f"Loaded {key}: {data[key].shape}")
    return data


def enrich_transactions(transactions: pd.DataFrame,
                        product: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich transaction_data with product-level attributes (department, brand).

    Parameters
    ----------
    transactions : pd.DataFrame
        Raw transaction_data.
    product : pd.DataFrame
        Product master table.

    Returns
    -------
    pd.DataFrame
        Transactions merged with DEPARTMENT, COMMODITY_DESC, BRAND.
    """
    product_cols = ['PRODUCT_ID', 'DEPARTMENT', 'COMMODITY_DESC', 'BRAND']
    enriched = transactions.merge(
        product[product_cols],
        on='PRODUCT_ID',
        how='left'
    )
    return enriched


def build_hh_features(transactions: pd.DataFrame,
                      pre_start: int = PRE_WEEK_START,
                      pre_end: int = PRE_WEEK_END,
                      post_start: int = POST_WEEK_START,
                      post_end: int = POST_WEEK_END) -> pd.DataFrame:
    """
    Build a household-level analytical feature table from transaction data.

    Pre-period features: spend, frequency, recency, promotion responsiveness,
    category affinity, and stratification variables (spend_tier, recency_band).

    Post-period outcomes: total spend, avg weekly spend, trips, conversion.

    Parameters
    ----------
    transactions : pd.DataFrame
        Enriched transaction data (with product info).
    pre_start, pre_end : int
        Week range for the pre-period (inclusive).
    post_start, post_end : int
        Week range for the post-period (inclusive).

    Returns
    -------
    pd.DataFrame
        One row per household with pre-period features and post-period outcomes.
    """
    pre = transactions[transactions['WEEK_NO'].between(pre_start, pre_end)].copy()
    post = transactions[transactions['WEEK_NO'].between(post_start, post_end)].copy()

    n_pre_weeks  = pre_end - pre_start + 1
    n_post_weeks = post_end - post_start + 1

    # ── Pre-period aggregation ────────────────────────────────────────────────
    hh_pre = pre.groupby('household_key').agg(
        total_spend      = ('SALES_VALUE', 'sum'),
        total_trips      = ('BASKET_ID', 'nunique'),
        total_items      = ('QUANTITY', 'sum'),
        last_purchase_day= ('DAY', 'max'),
        n_departments    = ('DEPARTMENT', 'nunique'),
        top_department   = ('DEPARTMENT',
                            lambda x: x.value_counts().idxmax() if len(x) > 0 else None),
        total_coupon_disc= ('COUPON_DISC', 'sum'),
        total_retail_disc= ('RETAIL_DISC', 'sum'),
    ).reset_index()

    hh_pre['avg_weekly_spend'] = hh_pre['total_spend'] / n_pre_weeks
    hh_pre['avg_weekly_trips'] = hh_pre['total_trips'] / n_pre_weeks
    hh_pre['avg_basket_size']  = np.where(
        hh_pre['total_trips'] > 0,
        hh_pre['total_spend'] / hh_pre['total_trips'],
        0
    )
    hh_pre['coupon_usage_rate'] = np.where(
        hh_pre['total_trips'] > 0,
        (hh_pre['total_coupon_disc'] > 0).astype(float) / hh_pre['total_trips'],
        0
    )
    hh_pre['loyalty_disc_rate'] = np.where(
        hh_pre['total_spend'] > 0,
        hh_pre['total_retail_disc'] / hh_pre['total_spend'],
        0
    )

    # Recency (days since last purchase from end of pre-period)
    pre_end_day = pre['DAY'].max()
    hh_pre['days_since_last_purchase'] = pre_end_day - hh_pre['last_purchase_day']
    hh_pre['weeks_since_last_purchase'] = hh_pre['days_since_last_purchase'] / 7

    # Spend tiers (quartile-based)
    hh_pre['spend_tier'] = pd.qcut(
        hh_pre['avg_weekly_spend'],
        q=4,
        labels=['Low', 'Medium-Low', 'Medium-High', 'High']
    )

    # Recency bands
    hh_pre['recency_band'] = pd.cut(
        hh_pre['days_since_last_purchase'],
        bins=[-1, 7, 30, 90, float('inf')],
        labels=['0-7d', '8-30d', '31-90d', '90d+']
    )

    # ── Post-period aggregation ───────────────────────────────────────────────
    hh_post = post.groupby('household_key').agg(
        post_total_spend = ('SALES_VALUE', 'sum'),
        post_total_trips = ('BASKET_ID', 'nunique'),
    ).reset_index()

    hh_post['post_avg_weekly_spend'] = hh_post['post_total_spend'] / n_post_weeks
    hh_post['post_conversion'] = 1  # Any post-period purchase = converted

    # ── Combine pre + post ────────────────────────────────────────────────────
    hh = hh_pre.merge(hh_post, on='household_key', how='left')
    hh['post_total_spend']     = hh['post_total_spend'].fillna(0)
    hh['post_total_trips']     = hh['post_total_trips'].fillna(0)
    hh['post_avg_weekly_spend']= hh['post_avg_weekly_spend'].fillna(0)
    hh['post_conversion']      = hh['post_conversion'].fillna(0).astype(int)

    return hh


def join_demographics(hh_features: pd.DataFrame,
                      demographic: pd.DataFrame) -> pd.DataFrame:
    """
    Left-join demographic attributes onto the household feature table.

    ~800 of 2,498 households have demographics. Unmatched households
    will have NaN in demographic columns.
    """
    demo_cols = [
        'household_key', 'AGE_DESC', 'MARITAL_STATUS_CODE',
        'INCOME_DESC', 'HOMEOWNER_DESC', 'HH_COMP_DESC',
        'HOUSEHOLD_SIZE_DESC', 'KID_CATEGORY_DESC'
    ]
    return hh_features.merge(demographic[demo_cols], on='household_key', how='left')


def join_campaign_history(hh_features: pd.DataFrame,
                          campaign_table: pd.DataFrame,
                          coupon_redempt: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize campaign participation and coupon redemption history per household.

    Adds:
        n_campaigns_received  : number of campaigns the household was contacted in
        n_coupons_redeemed    : number of coupons redeemed
        coupon_redemption_rate: coupons redeemed / campaigns received (proxy)
    """
    campaign_summary = campaign_table.groupby('household_key').agg(
        n_campaigns_received=('CAMPAIGN', 'count')
    ).reset_index()

    redempt_summary = coupon_redempt.groupby('household_key').agg(
        n_coupons_redeemed=('COUPON_UPC', 'count')
    ).reset_index()

    hh = hh_features.merge(campaign_summary, on='household_key', how='left')
    hh = hh.merge(redempt_summary, on='household_key', how='left')
    hh['n_campaigns_received'] = hh['n_campaigns_received'].fillna(0)
    hh['n_coupons_redeemed']   = hh['n_coupons_redeemed'].fillna(0)
    hh['coupon_redemption_rate'] = np.where(
        hh['n_campaigns_received'] > 0,
        hh['n_coupons_redeemed'] / hh['n_campaigns_received'],
        0
    )
    return hh
