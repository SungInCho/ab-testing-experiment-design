# Data Preparation

**Notebook:** `notebooks/01_data_preparation_and_eda.ipynb` (Section 1–3)

---

## Overview

The dunnhumby "Complete Journey" dataset contains 2 years of household-level grocery transactions for approximately 2,500 frequent shoppers at a regional grocery retailer. This document describes how the raw data files are loaded, joined, and transformed into a household-level analytical table suitable for experiment design.

---

## Raw Data Sources

| Table | Rows (approx.) | Description |
|---|---|---|
| `transaction_data` | ~2.6M | Line-item receipts: household × basket × product |
| `hh_demographic` | ~800 | Demographic attributes (subset of households) |
| `campaign_table` | ~7,200 | Household campaign participation records |
| `campaign_desc` | 30 | Campaign type and week range metadata |
| `coupon` | ~1,600 | Coupon-to-product mappings |
| `coupon_redempt` | ~2,300 | Actual coupon redemption events |
| `product` | ~92,000 | Product master: department, category, brand |
| `causal_data` | ~4.7M | Weekly display and mailer flags by product/store |

---

## Time Period Definitions

The dataset spans weeks 1–102 (~2 years). We partition it into two periods:

| Period | Weeks | Duration | Purpose |
|---|---|---|---|
| **Pre-period (baseline)** | 1–71 | ~17 months | Feature engineering, variance estimation, stratification |
| **Post-period (holdout)** | 72–102 | ~7 months | Metric validation, power calibration proxy |

**Rationale for 71-week split:** The pre-period is long enough to compute stable behavioral features (spend averages, recency) while the post-period provides a sufficiently long holdout for rolling window variance estimation.

---

## Feature Engineering

### Step 1: Enrich Transactions with Product Info

Transaction records are joined with the product master on `PRODUCT_ID` to add `DEPARTMENT`, `COMMODITY_DESC`, and `BRAND` to each transaction line.

### Step 2: Aggregate to Household Level (Pre-Period)

For each household, we compute the following features from the pre-period (weeks 1–71):

**Spend features:**
| Feature | Definition |
|---|---|
| `total_spend` | Sum of SALES_VALUE in pre-period |
| `avg_weekly_spend` | total_spend / 71 weeks |
| `avg_basket_size` | total_spend / total_trips |

**Frequency features:**
| Feature | Definition |
|---|---|
| `total_trips` | Count of distinct BASKET_IDs |
| `avg_weekly_trips` | total_trips / 71 weeks |
| `total_items` | Sum of QUANTITY |

**Recency features:**
| Feature | Definition |
|---|---|
| `last_purchase_day` | Max DAY value in pre-period |
| `days_since_last_purchase` | pre_end_day − last_purchase_day |
| `weeks_since_last_purchase` | days_since_last_purchase / 7 |

**Promotion responsiveness:**
| Feature | Definition |
|---|---|
| `coupon_usage_rate` | Fraction of trips with coupon discount |
| `loyalty_disc_rate` | Total loyalty discount / total spend |
| `avg_discount_per_trip` | Total discount / total trips |

**Category affinity:**
| Feature | Definition |
|---|---|
| `top_department` | Most frequently purchased department |
| `n_departments` | Number of distinct departments purchased |

**Stratification variables:**
| Feature | Definition |
|---|---|
| `spend_tier` | Quartile of avg_weekly_spend: Low / Medium-Low / Medium-High / High |
| `recency_band` | 0–7d / 8–30d / 31–90d / 90d+ (days since last purchase) |

### Step 3: Join Demographics

Demographics from `hh_demographic` are left-joined. Only ~800 of 2,498 households have demographic data. Missing values are preserved; demographics are used only for subgroup analysis (not eligibility or primary analysis).

### Step 4: Join Campaign & Coupon History

Campaign participation count (`n_campaigns_received`) and coupon redemption count (`n_coupons_redeemed`) are aggregated from `campaign_table` and `coupon_redempt`.

### Step 5: Compute Post-Period Outcomes

Post-period outcomes (weeks 72–102) are aggregated for each household:
- `post_total_spend`
- `post_avg_weekly_spend`
- `post_total_trips`
- `post_conversion` (1 if any post-period purchase)

---

## Output

The resulting `hh_features.csv` contains **2,498 rows** (one per household) and **~50 columns** covering all pre-period features and post-period outcomes.

This table is the primary input for Notebook 2 (Experiment Design).
