# Exploratory Data Analysis

**Notebook:** `notebooks/01_data_preparation_and_eda.ipynb` (Section 4–5)

---

## Overview

Exploratory Data Analysis (EDA) characterizes the household population to:
1. Understand the spend distribution and identify variance challenges for power analysis
2. Examine engagement patterns (trips, recency) to inform eligibility criteria
3. Analyze promotion responsiveness to motivate the coupon experiment
4. Explore demographic distributions in the available subset
5. Identify weekly spend trends and seasonality
6. Define spend tiers and recency bands for stratified randomization

---

## 4a. Spend Distribution

**Key findings:**
- Spend distribution is **right-skewed** — most households spend modestly, but a small fraction of high-spend outliers inflates variance
- Skewness ≈ 1.4 (post-period 4-week windows)
- **Implication:** Raw variance will overestimate the noise in a well-run experiment; winsorization (1st–99th percentile) is recommended before power analysis

**Distribution characteristics:**
| Statistic | Pre-period avg weekly spend |
|---|---|
| Median | ~$17–20/week |
| Mean | Higher (pulled right by outliers) |
| Distribution shape | Right-skewed, heavy upper tail |

**Action taken:**
- Both raw and winsorized σ are computed for power scenarios
- CUPED further reduces effective variance by exploiting pre-post correlation

---

## 4b. Trip Frequency & Recency

**Key findings:**
- Most households shop 1–3 times per week on average
- Recency distribution is concentrated in the 0–30 day range, with a tail of lapsed/churned households
- **Implication for eligibility:** Households with recency > 90 days are likely churned and unlikely to respond to a coupon campaign; they are excluded from the eligible population

---

## 4c. Promotion Responsiveness

**Key findings:**
- Overall coupon usage rate is relatively low across the full population (~17–20% redemption rate on received campaigns)
- Loyalty card discount rate is higher, indicating that most households do use loyalty pricing
- **Implication:** Coupon response will be concentrated among price-sensitive segments; this experiment tests whether targeted coupons increase overall spend, not just channel-specific discounts

---

## 4d. Demographic Breakdown

Only ~800 of 2,498 households have demographic data. Among those:
- Age distribution spans 25–65+, with concentration in 35–54
- Income range: broad distribution from under $25K to over $125K
- Household size: mix of 1-person to 5+ person households

**Note:** Demographic data is not required for eligibility and will not be used in the primary analysis. It is available for subgroup analysis only (Appendix D).

---

## 4e. Weekly Spend Trends

**Key findings:**
- Weekly aggregate spend is relatively stable over 102 weeks with no strong upward or downward trend
- Minor seasonality is visible (holiday period spikes) but does not undermine a 4-week experiment window
- No structural break between pre-period (weeks 1–71) and post-period (weeks 72–102), supporting the use of post-period data as a variance estimation proxy

---

## 4f. Spend Segmentation for Stratification

Spend tiers are defined using quartiles of `avg_weekly_spend`:

| Tier | Weekly Spend Range | Share |
|---|---|---|
| Low | Bottom 25% | 25% |
| Medium-Low | 25th–50th pct | 25% |
| Medium-High | 50th–75th pct | 25% |
| High | Top 25% | 25% |

Recency bands are defined using days since last purchase:

| Band | Days Since Last Purchase |
|---|---|
| 0–7d | Active (shopped within last week) |
| 8–30d | Recent |
| 31–90d | Lapsing |
| 90d+ | Churned (excluded from eligibility) |

These two variables define the **16-cell stratification grid** used in randomization (Step 10 of the experiment design).

---

## 5. Post-Period Outcome Variables

Post-period outcomes (weeks 72–102) are computed per household as validation:
- They confirm that spending patterns in the post-period are consistent with the pre-period
- They provide the empirical σ estimates used in power analysis (Steps 5b–5c)
- The pre-post correlation (r ≈ 0.81) justifies CUPED as a powerful variance reduction technique

**Summary Statistics:**

| Metric | Value |
|---|---|
| Total households | 2,498 |
| Post-period conversion rate | ~92% (households with ≥1 post-period purchase) |
| Pre-post spend correlation | r ≈ 0.81 |
| Zero-spend rate in 4-week windows | ~8% |
