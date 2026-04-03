# Data Directory

This directory contains all raw data files used in the experiment design project.

## Source

**dunnhumby — The Complete Journey**
- [Kaggle](https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey)
- [dunnhumby Source Files](https://www.dunnhumby.com/source-files/)

Place all CSV files in `data/raw/` before running the notebooks.

---

## File Descriptions

### `transaction_data.csv`
Line-item grocery purchase records at the household × basket × product level.

| Column | Type | Description |
|---|---|---|
| `household_key` | int | Unique household identifier |
| `BASKET_ID` | int | Unique shopping trip/basket identifier |
| `DAY` | int | Day number (1–711) |
| `PRODUCT_ID` | int | Product SKU |
| `QUANTITY` | int | Number of units purchased |
| `SALES_VALUE` | float | Dollar amount paid (after discounts) |
| `STORE_ID` | int | Store identifier |
| `RETAIL_DISC` | float | Retail/loyalty card discount applied |
| `TRANS_TIME` | int | Transaction time (HHMM) |
| `WEEK_NO` | int | Week number (1–102) |
| `COUPON_DISC` | float | Coupon discount applied |
| `COUPON_MATCH_DISC` | float | Coupon match discount applied |

### `hh_demographic.csv`
Demographic attributes for a subset (~800) of households.

| Column | Description |
|---|---|
| `household_key` | Household identifier |
| `AGE_DESC` | Age group (e.g., "25-34") |
| `MARITAL_STATUS_CODE` | Marital status |
| `INCOME_DESC` | Household income range |
| `HOMEOWNER_DESC` | Homeowner / renter / unknown |
| `HH_COMP_DESC` | Household composition |
| `HOUSEHOLD_SIZE_DESC` | Number of people in household |
| `KID_CATEGORY_DESC` | Presence and number of children |

### `campaign_table.csv`
Links households to campaign participation events.

| Column | Description |
|---|---|
| `household_key` | Household identifier |
| `CAMPAIGN` | Campaign number |
| `DESCRIPTION` | Campaign type (TypeA / TypeB / TypeC) |

### `campaign_desc.csv`
Campaign metadata with start and end week numbers.

| Column | Description |
|---|---|
| `CAMPAIGN` | Campaign number |
| `DESCRIPTION` | Campaign type |
| `START_DAY` | Campaign start day |
| `END_DAY` | Campaign end day |

### `coupon.csv`
Maps coupons to the products they apply to.

| Column | Description |
|---|---|
| `COUPON_UPC` | Unique coupon barcode |
| `PRODUCT_ID` | Product the coupon applies to |
| `CAMPAIGN` | Campaign the coupon belongs to |

### `coupon_redempt.csv`
Records of actual coupon redemptions by household.

| Column | Description |
|---|---|
| `household_key` | Household identifier |
| `DAY` | Day of redemption |
| `COUPON_UPC` | Coupon barcode redeemed |
| `CAMPAIGN` | Associated campaign |

### `product.csv`
Product master data with department and sub-department.

| Column | Description |
|---|---|
| `PRODUCT_ID` | Product SKU |
| `DEPARTMENT` | Product department |
| `COMMODITY_DESC` | Product category |
| `SUB_COMMODITY_DESC` | Product sub-category |
| `MANUFACTURER` | Manufacturer code |
| `BRAND` | National or Private Label |
| `CURR_SIZE_OF_PRODUCT` | Package size |

### `causal_data.csv`
Weekly display and mailer flags by product and store.

| Column | Description |
|---|---|
| `PRODUCT_ID` | Product SKU |
| `STORE_ID` | Store identifier |
| `WEEK_NO` | Week number |
| `DISPLAY` | Display flag (0–9) |
| `MAILER` | Mailer flag (0–9) |

### `hh_features.csv` *(Engineered)*
Household-level feature table created in Notebook 1. Aggregated from transaction data with pre-period and post-period metrics.

**Pre-period features (weeks 1–71):**
- Spend: `total_spend`, `avg_weekly_spend`, `avg_basket_size`
- Frequency: `total_trips`, `avg_weekly_trips`, `total_items`
- Recency: `last_purchase_day`, `weeks_since_last_purchase`
- Promotion: `coupon_usage_rate`, `loyalty_disc_rate`, `avg_discount_per_trip`
- Category: `top_department`, `n_departments`
- Demographics (joined): `AGE_DESC`, `INCOME_DESC`, `HOUSEHOLD_SIZE_DESC`, etc.
- Stratification: `spend_tier`, `recency_band`

**Post-period outcomes (weeks 72–102):**
- `post_total_spend`, `post_avg_weekly_spend`, `post_total_trips`, `post_conversion`

---

## Time Period Definitions

| Period | Weeks | Duration | Purpose |
|---|---|---|---|
| **Pre-period (baseline)** | 1–71 | ~17 months | Feature engineering, variance estimation |
| **Post-period (holdout)** | 72–102 | ~7 months | Metric validation, power calibration |
| **Experiment window** | 4 weeks | 28 days | Actual treatment measurement |

---

## Key Statistics

| Metric | Value |
|---|---|
| Total households | 2,498 |
| Total transaction records | ~2.6M |
| Weeks of data | 102 |
| Households with demographics | ~800 |
| Historical coupon redemption rate | ~17–20% |
