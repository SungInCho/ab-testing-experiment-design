# Data Preparation

**Notebook:** `notebooks/01_data_preparation_and_eda.ipynb` (Steps 1–3)

---

## Overview

The dunnhumby "The Complete Journey" dataset captures approximately 2 years of household-level grocery transactions for ~2,500 frequent shoppers at a regional grocery retailer. This document covers how the eight raw data files are loaded, cleaned, joined, and transformed into a household-level analytical table used for experiment design.

---

## Raw Data Sources

| Table | Rows (approx.) | Description |
|---|---|---|
| `transaction_data` | ~2.6M | Line-item receipts: `household_key` × basket × product |
| `hh_demographic` | ~800 | Demographic attributes for a subset of households |
| `campaign_table` | ~7,200 | Household × campaign participation records |
| `campaign_desc` | 30 | Campaign type metadata and week ranges |
| `coupon` | ~1,600 | Coupon-to-product mappings |
| `coupon_redempt` | ~2,300 | Actual coupon redemption events |
| `product` | ~92,000 | Product master: department, commodity, brand |
| `causal_data` | ~4.7M | Weekly display and mailer flags by product/store |

---

## Time Period Definitions

The dataset spans weeks 1–102 (~2 years). The data is split into two non-overlapping periods:

| Period | Weeks | Duration | Purpose |
|---|---|---|---|
| **Pre-period** | 1–71 | ~17 months | Feature engineering, baseline estimation, stratification |
| **Post-period** | 72–102 | ~7 months | Metric validation, variance calibration proxy |

The 71-week cutoff is chosen to leave a sufficiently long post-period for rolling window variance estimation while keeping the pre-period long enough to compute stable behavioral averages and recency features.

---

## Step 1: Transaction Enrichment

Each transaction record contains discount fields that distinguish between different types of price reductions:

- `RETAIL_DISC` — standard shelf discount (loyalty card price reduction)
- `COUPON_DISC` — manufacturer or store coupon discount
- `COUPON_MATCH_DISC` — additional store match on top of manufacturer coupon

Transactions are joined with the product master (`product.csv`) on `PRODUCT_ID` to attach `DEPARTMENT`, `COMMODITY_DESC`, and `BRAND` to each line item. This enables category-level aggregations and promotion responsiveness features.

---

## Step 2: Household-Level Feature Engineering (Pre-Period)

All features are computed from pre-period transactions (weeks 1–71) and aggregated to the household level. The resulting table has one row per household.

### Spend Features

| Feature | Definition |
|---|---|
| `total_spend` | Sum of `SALES_VALUE` across all pre-period transactions |
| `avg_weekly_spend` | `total_spend` ÷ number of active weeks in pre-period |
| `avg_basket_size` | `total_spend` ÷ number of distinct baskets |

### Frequency Features

| Feature | Definition |
|---|---|
| `total_trips` | Count of distinct basket IDs in pre-period |
| `avg_trips_per_week` | `total_trips` ÷ number of pre-period weeks |
| `total_items` | Sum of quantities purchased |
| `items_per_trip` | `total_items` ÷ `total_trips` |

### Recency Feature

| Feature | Definition |
|---|---|
| `recency_days` | Days elapsed between the household's last pre-period transaction and the end of week 71 |

### Promotion Responsiveness Features

| Feature | Definition |
|---|---|
| `coupon_usage_rate` | Fraction of baskets containing at least one coupon redemption |
| `loyalty_usage_rate` | Fraction of baskets with a loyalty card discount applied |
| `discount_per_trip` | Average total discount amount (`RETAIL_DISC` + `COUPON_DISC` + `COUPON_MATCH_DISC`) per trip |

### Category Features

| Feature | Definition |
|---|---|
| `n_departments` | Count of distinct departments purchased from |
| `top_department` | Department accounting for the largest share of spend |

---

## Step 3: Enriching with External Tables

### Demographics (`hh_demographic`)

Demographics are available for ~800 of the 2,498 households. Fields joined to the feature table:

| Field | Description |
|---|---|
| `AGE_DESC` | Age group bucket |
| `MARITAL_STATUS_CODE` | Marital status |
| `INCOME_DESC` | Household income range |
| `HOMEOWNER_DESC` | Homeowner / renter status |
| `HH_COMP_DESC` | Household composition (size) |
| `KID_CATEGORY_DESC` | Presence and count of children |

Households without demographic records have `NaN` in these columns; they remain in the analytical population and are not excluded from the experiment.

### Campaign History (`campaign_table` + `campaign_desc`)

The campaign table is joined with campaign descriptions to compute:

- `n_campaigns_received` — number of distinct campaigns the household was targeted in during the pre-period

This field is used as an eligibility criterion (see Notebook 2) and as a proxy for contactability via direct mail.

### Coupon Redemption (`coupon_redempt` + `coupon`)

Redemption events from the pre-period are joined to the feature table to compute:

- `n_coupons_redeemed` — total coupons redeemed in the pre-period
- Used to derive `coupon_usage_rate` at the trip level

---

## Step 4: Post-Period Outcome Variables

Post-period transactions (weeks 72–102) are used exclusively as a proxy for realistic experiment outcomes during the design phase — no treatment is applied. The following variables are computed for each household:

| Variable | Definition |
|---|---|
| `post_total_spend` | Total spend in the post-period |
| `post_4wk_spend` | Total spend in a representative 4-week rolling window |
| `post_conversion` | Binary indicator: made ≥1 purchase in the 4-week window |

The 4-week window is chosen to match the planned experiment duration and coupon validity period.

---

## Step 5: Stratification Variables

Three categorical variables are constructed for use in stratification and EDA:

### Spend Tier (4 levels — quartiles of `avg_weekly_spend`)

| Tier | Population Quartile |
|---|---|
| Low | Bottom 25% |
| Medium-Low | 25th–50th percentile |
| Medium-High | 50th–75th percentile |
| High | Top 25% |

### Recency Band (4 levels — based on `recency_days`)

| Band | Days Since Last Purchase |
|---|---|
| 0–7d | Active |
| 8–30d | Recent |
| 31–90d | Lapsing |
| 90d+ | Churned |

### Promo Tier (3 levels — based on `coupon_usage_rate`)

| Tier | Coupon Usage Level |
|---|---|
| No_Promo | Zero coupon usage |
| Low_Promo | Below-median usage |
| High_Promo | Above-median usage |

---

## Output

The feature engineering pipeline produces a single household-level table:

**File:** `data/raw/hh_features.csv`
**Rows:** 2,498 (one per household)
**Columns:** ~50 (spend, frequency, recency, promo, category, demographic, and stratification features)

This table is the primary input to all downstream experiment design steps in Notebook 2.
