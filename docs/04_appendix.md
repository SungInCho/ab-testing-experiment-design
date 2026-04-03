# Appendix

**Notebook:** `notebooks/03_appendix.ipynb`

Supporting analyses and reference materials for the experiment design.

---

## Appendix A: Baseline Summary by Stratification Cell

### Purpose
Verify that the stratification variables (spend tier × recency band) capture meaningful behavioral variation. If strata are internally homogeneous but differ across cells, stratified randomization will be most effective.

### Structure
The table shows the mean and standard deviation of key covariates within each of the 16 cells (4 spend tiers × 4 recency bands):
- `avg_weekly_spend`
- `total_trips`
- `coupon_usage_rate`
- `days_since_last_purchase`

### Key Finding
Strata differ substantially across spend levels. The Low tier spends ~1/4 as much per week as the High tier. Within-stratum variance is lower than overall variance, confirming that stratification reduces imbalance risk.

---

## Appendix B: Sample Size Calculation Sheet — Multiple MDE Scenarios

### Purpose
Provide a sensitivity analysis showing how required sample size changes across different assumptions, enabling the experimenter to understand the full feasibility landscape.

### Formula

For a two-sample t-test (equal allocation, two-sided):

$$n_{\text{per arm}} = \frac{2\sigma^2 (z_{1-\alpha/2} + z_{1-\beta})^2}{\delta^2}$$

For CUPED-adjusted variance:

$$n_{\text{per arm}}^{\text{CUPED}} = \frac{2\sigma_{\text{CUPED}}^2 (z_{1-\alpha/2} + z_{1-\beta})^2}{\delta^2}$$

where $\sigma_{\text{CUPED}} = \sigma \cdot \sqrt{1 - \rho^2}$ and $\rho \approx 0.81$.

### Scenarios Evaluated

**MDE range:** $8, $14, $20 (4-week total)
**Sigma scenarios:**
- Raw σ (full ITT, no winsorization)
- Winsorized σ (1st–99th percentile clip)
- Conservative σ (max of pre-scaled and post-rolling)
- CUPED-adjusted σ (conservative × √(1 − ρ²))

**Power levels:** 80%, 90%

### Key Takeaways
- At MDE = $14 (moderate), CUPED reduces required n per arm by ~35–45% vs. raw σ
- CUPED adjustment is the most impactful design choice for improving feasibility
- If eligible N is insufficient at the primary MDE, consider: (1) relaxing MDE to $20, or (2) accepting 80% power with CUPED

---

## Appendix C: Pre-Registered Analysis Plan Template

This is the formal registration document that would be filed before any treatment is delivered. Once locked, no modifications are permitted.

### Document Contents

**Hypothesis:**
- H₀: The coupon campaign does not change 4-week total household spend
- H₁: The coupon campaign changes 4-week total spend (two-sided)

**Primary metric:** 4-week total spend (ITT, zeros included)
**Test:** Welch's two-sample t-test
**Significance level:** α = 0.05
**Power:** 80%
**MDE:** $14 per 4-week window
**Sample size:** Pre-specified per arm from power analysis
**Randomization:** Stratified by spend tier × recency band, seed = 42
**Pre-processing:** Winsorization at 1st/99th percentile
**Adjustment:** CUPED using pre-period avg weekly spend × 4 as covariate

**Launch decision gates:**
1. p < 0.05 (two-sided)
2. Point estimate ≥ $14 AND CI lower > $0
3. Guardrails: discount cost ≤ $3/HH, non-target spend decline < 5%

---

## Appendix D: Subgroup Analysis Preview (Exploratory)

### Purpose
Understand whether the treatment effect (if any) varies across important segments. These are declared exploratory — they will NOT influence the launch decision but will inform future targeting strategy.

### Pre-Declared Subgroups

| Subgroup | Variable | Levels |
|---|---|---|
| Spend tier | `spend_tier` | Low / Medium-Low / Medium-High / High |
| Recency | `recency_band` | 0–7d / 8–30d / 31–90d |
| Age group | `AGE_DESC` | 25–34 / 35–44 / 45–54 / 55–64 / 65+ |
| Income | `INCOME_DESC` | Under $35K / $35–75K / $75K+ |
| Household size | `HOUSEHOLD_SIZE_DESC` | 1 / 2 / 3–4 / 5+ |

### Analysis
Within each subgroup, simulate the baseline difference in 4-week spend (pre-period, no treatment). This preview shows the expected direction of heterogeneity — higher-spend and more-active households may have lower percentage lift but higher absolute lift.

### Important Caveat
Subgroup analyses are underpowered relative to the primary test. Results should be interpreted as directional hypotheses for future experiments, not as definitive findings.

---

## Appendix E: Binary Outcome Power Analysis — Conversion Rate

### Purpose
Compute required sample size for the secondary metric: conversion rate (proportion of households making ≥1 purchase in the 4-week window).

### Formula (Two-Proportion Z-Test)

$$n_{\text{per arm}} = \frac{(z_{1-\alpha/2} + z_{1-\beta})^2 [p_C(1-p_C) + p_T(1-p_T)]}{(p_T - p_C)^2}$$

### Key Parameters

| Parameter | Value | Source |
|---|---|---|
| Baseline conversion rate ($p_C$) | ~92% | Observed post-period (1 – zero-spend rate of 8%) |
| Minimum detectable lift | +3 to +5 pp | Business assumption |
| α | 0.05 | Primary test standard |
| Power | 0.80 | Standard |

### Key Finding
For a binary outcome at ~92% baseline conversion, even a 3–5 percentage point lift requires very large sample sizes — because variance of a Bernoulli variable at p = 0.92 is p(1−p) = 0.07, which is small, but detecting small absolute changes at high baseline rates is inherently difficult. The continuous spend metric (primary) is the more sensitive outcome for this experiment.

---

## Appendix F: A/A Simulation Detail

### Purpose
Validate that the Welch's t-test has the correct type I error rate when applied to the 4-week total spend metric on the actual data.

### Method
1. Select a representative 4-week post-period window
2. Run 1,000 random 50/50 splits of the eligible population
3. Apply Welch's t-test to each split
4. Record p-values and mean differences

### Expected Results
- FPR ≈ 5% (consistent with α = 0.05)
- p-value distribution: approximately uniform on [0, 1]
- Distribution of mean differences: centered at zero, normally distributed by CLT

### MDE Feasibility
The 95th percentile of |mean differences| defines the noise floor. A target MDE above this level is realistically detectable.

---

## Appendix G: Stratification Balance Verification

### Purpose
Confirm that stratified randomization produces better covariate balance than simple random assignment.

### Method
Compare the maximum standardized mean difference (SMD) across covariates between:
1. **Stratified randomization** (spend tier × recency band)
2. **Simple random assignment** (benchmark)

### Expected Result
Stratified randomization should produce lower SMD for spend-related variables. The improvement is most pronounced for `avg_weekly_spend` (the stratification variable itself) and moderately effective for correlated variables (trips, recency).
