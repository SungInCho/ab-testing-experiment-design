# Exploratory Data Analysis

**Notebook:** `notebooks/01_data_preparation_and_eda.ipynb` (Steps 4–6)

---

## Overview

The EDA section explores household-level behavioral patterns derived from 71 weeks of pre-period transactions. The goals are to (1) understand the distribution and structure of the data before designing the experiment, (2) identify key predictors of spend and engagement, and (3) validate the stratification variables used in randomization.

---

## Spend Distribution

### Total Pre-Period Spend

Pre-period total spend (`total_spend`) is heavily right-skewed, driven by a small fraction of high-frequency, high-basket households:

- **Median** is substantially lower than the mean
- The distribution has a long upper tail with no natural ceiling
- Log-transformation reveals an approximately log-normal shape

### Average Weekly Spend

`avg_weekly_spend` is the primary stratification variable and the covariate used in CUPED variance reduction:

- Right-skewed distribution with skewness ≈ 1.4
- Household spending ranges from near-zero to several hundred dollars per week
- Spend tier quartiles reflect meaningful behavioral segments (see table below)

| Tier | Households (Eligible) | Mean Avg Weekly Spend |
|---|---|---|
| Low | 23 | ~$7 |
| Medium-Low | 234 | ~$17 |
| Medium-High | 458 | ~$33 |
| High | 573 | ~$83 |

### Spend per Trip

`avg_basket_size` (spend per trip) varies considerably across households and is correlated with but distinct from weekly spend:

- Some households shop frequently with small baskets; others shop infrequently with large baskets
- This distinction is captured in the `spend_tier` vs. `total_trips` axes

---

## Trip Frequency and Recency

### Total Trips

`total_trips` in the pre-period ranges from just a few visits to hundreds across 71 weeks. The distribution is right-skewed but less extreme than spend.

`avg_trips_per_week` shows that most active households visit roughly 1–3 times per week.

### Recency

`recency_days` measures how recently a household transacted before the end of week 71:

| Band | Days Since Last Purchase | Eligible Households |
|---|---|---|
| 0–7d (Active) | 0–7 | 942 |
| 8–30d (Recent) | 8–30 | 287 |
| 31–90d (Lapsing) | 31–90 | 59 |
| 90d+ (Churned) | > 90 | Excluded |

The vast majority of eligible households (73%) are in the 0–7d band, indicating high recent engagement. Lapsing households (31–90d) represent a small fraction with meaningfully lower spend levels.

---

## Promotion Responsiveness

### Coupon Usage Rate

`coupon_usage_rate` — the fraction of trips involving a coupon redemption — is very low on average:

- Most households have a coupon usage rate near zero
- A small segment of "coupon enthusiasts" shows consistently high usage
- The distribution is zero-inflated with a long right tail

This low baseline usage is relevant for experiment design: the treatment (coupon delivery) will introduce a new redemption opportunity, and the ITT framework captures the average effect across all eligible households regardless of redemption.

### Loyalty Card Usage

`loyalty_usage_rate` is substantially higher than coupon usage — most transactions involve a loyalty discount. This reflects the retailer's broad loyalty program penetration.

### Discount per Trip

`discount_per_trip` captures the average dollar amount saved per visit. Higher-spending households tend to receive larger absolute discounts in part because they purchase more items.

---

## Demographic Breakdown

Demographics are available for approximately 800 of 2,498 households. Among households with demographic information:

- **Age groups** span a wide range; middle-aged adults are most represented
- **Income levels** cover a broad spectrum, with the modal range in the middle tiers
- **Household size** ranges from single-person to large family units
- **Children:** Households with children tend to have higher spending and more frequent trips
- **Homeowners** slightly outnumber renters in the demographic-matched subset

Demographic fields are used only in exploratory subgroup analyses (Appendix D) and do not affect the primary eligibility criteria or randomization.

---

## Weekly Spend Trends

Plotting mean weekly spend across all 102 weeks reveals:

- **Stable baseline spending** throughout weeks 1–71 with no strong trend
- **Seasonal patterns** consistent with typical grocery retail (slight increases around holidays)
- **Continuity across the pre/post boundary** — the week-71 cutoff does not coincide with any visible structural break

The stability of spend across the pre/post boundary supports using the pre-period as a reliable baseline for CUPED adjustment and variance estimation.

---

## Pre-Period vs. Post-Period Consistency

A scatter plot of pre-period average weekly spend (scaled to 4 weeks) versus post-period 4-week total spend for the eligible population shows:

- Strong linear relationship with positive slope
- Pre-to-post Pearson correlation: **ρ = 0.682**
- This correlation is the foundation for CUPED variance reduction — higher ρ means greater potential sample size savings

The strong pre-post consistency confirms that pre-period spending is a reliable covariate for the CUPED adjustment in the analysis plan.

---

## Spend Tier × Recency Band Cross-Tabulation

Analyzing spend behavior across the 16 stratification cells (4 spend tiers × 4 recency bands) reveals meaningful heterogeneity:

| Spend Tier | Pre-Period 4-wk Spend (Mean ± SD) |
|---|---|
| High | $332.90 ± $145.57 |
| Medium-High | $133.38 ± $27.28 |
| Medium-Low | $67.64 ± $15.29 |
| Low | $28.90 ± $5.78 |

- Higher spend tiers show higher variance in absolute terms — this motivates stratified randomization
- The High tier (n=573) dominates the eligible pool numerically
- The Low tier (n=23) is very small; within-cell balance is ensured by stratified assignment

Recency bands show expected patterns: Active households (0–7d) have higher mean spend and more consistent shopping behavior than Lapsing households.

---

## Distribution Diagnostics

### Zero-Spend Rate

In 4-week rolling windows on post-period data (used as a proxy for the experiment outcome):

- **Zero-spend rate ≈ 8%** — low but non-negligible
- This confirms that zero-spend households must be included in the ITT analysis (Y = 0 for non-purchasers)
- The low sparsity supports using a standard continuous-outcome t-test rather than a two-part model

### Heavy Tails (Skewness Check)

- 4-week total spend has skewness ≈ 1.2–1.4 in post-period rolling windows
- Q-Q plot shows deviation from normality in the upper tail
- With n > 600 per arm, the Central Limit Theorem supports asymptotic validity of the Welch's t-test
- Winsorization at the 1st and 99th percentiles is pre-registered as a robustness check

### A/A Simulation Preview

To verify that the 4-week metric is well-behaved under the null hypothesis, 1,000 random 50/50 splits of the post-period population are analyzed:

- False positive rate ≈ 5% — confirms correct type I error rate
- p-value distribution is approximately uniform on [0, 1]
- The 95th percentile of observed absolute mean differences is approximately $6–8 — well below the $14 MDE, confirming that random noise will not produce false apparent effects of the target magnitude

---

## Key EDA Takeaways

| Finding | Implication for Experiment Design |
|---|---|
| Right-skewed spend with heavy upper tail | Use Welch's t-test; pre-register winsorization |
| ρ = 0.682 pre-post correlation | CUPED reduces required sample size by ~46% |
| Zero-spend rate ≈ 8% | Include zeros in ITT analysis; no exclusion of non-purchasers |
| Spend tier explains most variance | Use spend tier as primary stratification variable |
| Recency captures engagement level | Include recency band as secondary stratification dimension |
| Demographic data incomplete (~32% coverage) | Demographics used for exploratory subgroups only |
| Spending stable across pre/post boundary | Pre-period is a reliable baseline covariate |
