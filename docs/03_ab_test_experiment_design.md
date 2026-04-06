# A/B Test Experiment Design

**Notebook:** `notebooks/02_experiment_design.ipynb`

This document details the complete 14-step experiment design for a household-level coupon campaign A/B test, using the dunnhumby Complete Journey dataset as the data foundation.

---

## Step 1: Define the Business Decision

**Context:** A national grocery retailer is evaluating whether to run a targeted coupon campaign, delivering category-specific promotional coupons to eligible frequent-shopper households via direct mail.

**Business Question:**
> *"Will sending household-level promotional coupons to eligible frequent shoppers increase their 4-week total spend by at least $14 — enough to justify full-scale campaign rollout?"*

**Why this framing matters:**
- Ties the statistical test directly to a business action (launch vs. do not launch)
- Defines "meaningful" in dollar terms before the data is analyzed, preventing post-hoc rationalization
- Prevents reporting significance alone without economic context

---

## Step 2: Define the Eligible Population

Eligibility criteria reduce the 2,498 total households to a contactable, engaged population suitable for the experiment.

### Criteria

| Criterion | Rule | Rationale |
|---|---|---|
| Trip activity | ≥ 2 trips in pre-period | Minimum engagement; one-time visitors excluded |
| Recency | `recency_days` ≤ 90 | Excludes churned households unlikely to respond |
| Campaign contactability | ≥ 1 historical campaign contact | Confirms direct mail deliverability |

### Result

| Population | Households |
|---|---|
| Total in dataset | 2,498 |
| **Eligible (ITT population)** | **1,288** |

**Framework:** Intent-to-Treat (ITT) — all 1,288 eligible households are included in the primary analysis regardless of whether they actually redeem the coupon. This prevents selection bias and provides a conservative, deployment-realistic estimate of the campaign's average effect.

---

## Step 3: Treatment, Control, and Exposure Window

| Dimension | Specification |
|---|---|
| **Treatment** | Category-specific promotional coupons delivered via direct mail (5 coupons, ~$1.00 face value each) |
| **Control** | Business-as-usual — no mailing |
| **Coupon validity** | 28 days from delivery |
| **Post-treatment measurement window** | 4 weeks (Days 3–31) |
| **Data freeze** | Day 35 (buffer for late transaction processing) |

**Rationale for 4-week window:** Covers 2+ full grocery shopping cycles and exactly matches the coupon validity period, ensuring the measurement window captures the full intended treatment effect.

---

## Step 4: Define Success Metrics

### Primary Metric

**4-week total household spend** (post-treatment window, ITT)

$$\hat{\tau}_{\text{ITT}} = \bar{Y}_T - \bar{Y}_C$$

where households with zero purchases contribute $Y_i = 0$.

**Why this metric:**
- Directly maps to the business question (revenue impact)
- Continuous outcome enables Welch's t-test with well-understood power properties
- Aligns with the 4-week coupon validity and experiment window
- ITT inclusion of zero-spenders gives a realistic campaign-level average effect

### Secondary Metrics (Exploratory)

| Metric | Definition | Statistical Test |
|---|---|---|
| Conversion rate | Proportion with ≥1 purchase in 4-week window | Two-proportion z-test |
| Basket size | Average spend per trip in 4-week window | Welch's t-test |
| Trip frequency | Count of distinct shopping trips in 4-week window | Welch's t-test |
| Category penetration | Purchased in target category (binary) | Two-proportion z-test |

Secondary metrics are analyzed with **Bonferroni correction** (α / 4 = 0.0125 per test) and reported for directional insight only — they do not affect the launch decision.

---

## Step 5a: Build Pre-Period Baselines

Baseline statistics are computed on the eligible population (n = 1,288) from pre-period data.

### Key Baseline Metrics

| Metric | Description |
|---|---|
| `avg_weekly_spend` | Primary stratification and CUPED covariate |
| `spend_per_trip` | Basket size behavior |
| `total_trips` | Engagement frequency |
| `items_per_trip` | Purchase volume |
| `coupon_usage_rate` | Promotion responsiveness |
| `loyalty_usage_rate` | Loyalty program engagement |
| `discount_per_trip` | Total price reduction per visit |
| `n_departments` | Shopping breadth |
| `recency_days` | Days since last purchase |

### Baseline by Spend Tier

| Tier | n | Mean Pre-Period 4-wk Spend | SD |
|---|---|---|---|
| High | 573 | $332.90 | $145.57 |
| Medium-High | 458 | $133.38 | $27.28 |
| Medium-Low | 234 | $67.64 | $15.29 |
| Low | 23 | $28.90 | $5.78 |

### Baseline by Recency Band

| Band | n | Mean Spend | Mean Recency |
|---|---|---|---|
| 0–7d (Active) | 942 | High | ~3 days |
| 8–30d (Recent) | 287 | Moderate | ~18 days |
| 31–90d (Lapsing) | 59 | Low | ~55 days |

---

## Step 5b: Variance Estimation and Post-Period Metric Validation

### 4-Week Rolling Window Approach

Rather than scaling the 71-week average, variance is estimated using 4-week rolling windows on post-period data — providing estimates at the exact same granularity as the experiment outcome metric.

### Variance Estimates (4-Week Total Spend, ITT)

| Estimate | σ (4-week) | Notes |
|---|---|---|
| Raw ITT | **$188.81** | Full distribution, includes zeros |
| Winsorized (1st–99th pct) | **$183.18** | Clips extreme spenders |
| CUPED-adjusted | **$138.01** | Uses pre-post correlation ρ = 0.682 |

**Conservative estimate for power analysis:** `σ_for_power = max(σ_pre_scaled, median(σ_post_rolling))` = $188.81

### Pre-Post Consistency

- Pre-to-post Pearson correlation: **ρ = 0.682**
- Confirmed via scatter plot (pre-period avg weekly spend × 4 vs. post 4-week total spend)
- The stable pre-post relationship validates CUPED as a legitimate variance reduction technique

---

## Step 5c: Metric Feasibility and MDE Realism Check

### Sparsity Diagnostic

- Zero-spend rate in 4-week windows: **~8%**
- Low enough to proceed with a continuous-outcome model (no zero-inflated model needed)
- ITT inclusion of zeros is appropriate and straightforward

### Distribution Diagnostic

- Skewness ≈ 1.2–1.4 (right-skewed, heavy upper tail)
- Q-Q plot shows non-normality in tails, but CLT applies at n > 600 per arm
- Winsorization is pre-registered as a robustness check

### A/A Simulation

**Method:** 1,000 random 50/50 splits of the post-period eligible population with no treatment applied.

**Results:**
- False positive rate ≈ **5%** — correct under α = 0.05 null
- p-values approximately Uniform[0,1]
- 95th percentile of |Δmean| ≈ **$6–8** (noise floor)
- **$14 MDE > noise floor** → the metric is sensitive enough to detect the target effect if real

---

## Step 6: Minimum Detectable Effect (MDE)

The MDE is derived from campaign economics, not statistical convention.

### Cost-Based Justification

| Component | Value |
|---|---|
| Coupons per household | 5 |
| Average coupon face value | $1.00 |
| Expected redemption rate | ~20% |
| Coupon redemption cost | ~$1.00 / HH |
| Direct mail cost | ~$0.50 / HH |
| **Total campaign cost** | **~$1.50 / HH** |

The $1.50 break-even is the minimum needed to recoup costs. The $14 MDE represents a moderate scenario — approximately 9× the direct cost — providing meaningful margin above break-even.

### MDE Scenarios

| Scenario | MDE (4-week) | Rationale |
|---|---|---|
| Conservative | $8.00 | Low bar; detects smaller effects |
| **Moderate (primary)** | **$14.00** | Cost-justified with reasonable margin |
| Optimistic | $20.00 | Strong ROI scenario |

**Primary MDE: $14.00 per 4-week window ($3.50/week)**

---

## Step 7: Significance Level, Power, and Test Type

| Parameter | Value | Rationale |
|---|---|---|
| **Significance level (α)** | 0.05 | Industry standard; 5% false positive tolerance |
| **Power (1 − β)** | 0.80 | 80% probability of detecting a true effect ≥ MDE |
| **Test type** | Two-sided | Detects both increases and decreases in spend |
| **Test statistic** | Welch's t-test | Handles unequal variance; robust for skewed distributions at large n |

**Why two-sided:** Although the coupon is expected to increase spend, a two-sided test is more conservative and catches harmful effects (e.g., coupon substitution reducing other purchases).

---

## Step 8: Sample Size and Power Analysis

### Formula

$$n_{\text{per arm}} = \frac{2\sigma^2 \left(z_{1-\alpha/2} + z_{1-\beta}\right)^2}{\delta^2}$$

With CUPED variance reduction:

$$\sigma_{\text{CUPED}} = \sigma \cdot \sqrt{1 - \rho^2} = 188.81 \times \sqrt{1 - 0.682^2} = \$138.01$$

### Sample Size Requirements at MDE = $14, Power = 80%

| Variance Scenario | σ (4-week) | n per arm | n total | Feasible? (max 1,288) |
|---|---|---|---|---|
| Raw ITT | $188.81 | ~2,856 | ~5,712 | No |
| Winsorized (1–99%) | $183.18 | ~2,684 | ~5,368 | No |
| **CUPED-adjusted** | **$138.01** | **~1,526** | **~3,052** | **No** |

**Key Finding:** MDE = $14 is not achievable with the available 1,288 eligible households, even after CUPED adjustment.

### Feasible MDE Given Available Sample

With n = 644 per arm and CUPED (σ = $138.01), the minimum detectable effect at 80% power is:

$$\delta_{\min} = \sqrt{\frac{2\sigma^2(z_{1-\alpha/2}+z_{1-\beta})^2}{n}} \approx \$21.5$$

### Power Curves

Power curves are computed across MDE values of $4–$40 per 4-week window for all three variance scenarios (raw, winsorized, CUPED), showing:
- (a) Required sample size per arm vs. MDE
- (b) Achievable power vs. true effect size at fixed n = 644 per arm

---

## Step 9: Treatment Allocation

**Decision: 50/50 split**

| Consideration | Rationale |
|---|---|
| Statistical efficiency | Equal allocation maximizes power for a given total N |
| Cost | Direct mail cost (~$0.50/HH) is modest — no economic pressure to minimize the treatment arm |
| Symmetry | Provides symmetric confidence intervals and equal precision in both arms |

**Result:** 644 households assigned to Treatment, 644 to Control.

---

## Step 10: Randomization Method

### Stratified Randomization

**Strata:** `spend_tier` × `recency_band` = **4 × 4 = 16 cells**

```python
def stratified_randomize(df, strata_cols, seed=42):
    rng = np.random.RandomState(seed)
    assignments = pd.Series(index=df.index, dtype=str)
    for name, group in df.groupby(strata_cols):
        idx = group.index.values.copy()
        rng.shuffle(idx)
        mid = len(idx) // 2
        assignments.loc[idx[:mid]] = 'Treatment'
        assignments.loc[idx[mid:]] = 'Control'
    return assignments
```

**Why these strata:**

1. **Spend tier** is the strongest predictor of future spend — controlling it eliminates the largest source of variance between groups
2. **Recency band** captures engagement level — active vs. lapsing households differ in coupon responsiveness and baseline spending

**Result:** Near-perfect 50/50 split within each stratum (Treatment/Control ratio ≈ 1.0 in all 16 cells), with fixed random seed = 42 for reproducibility.

---

## Step 11: Experiment Duration and Stopping Rules

| Parameter | Value | Rationale |
|---|---|---|
| **Post-treatment window** | 4 weeks (28 days) | Covers 2+ full shopping cycles |
| **Coupon validity** | 28 days | Matches measurement window |
| **Washout buffer** | 1 week pre-measurement | Accounts for mail delivery lag |
| **Data freeze** | Day 35 | Buffer for late transaction processing |
| **Analysis type** | Fixed horizon | Prevents multiple-testing inflation from interim peeks |

**No early stopping rule:** Interim analysis inflates the false positive rate. Grocery behavior follows weekly cycles — four full weeks are needed for stable spend estimates.

---

## Step 12: Pre-Launch Quality Checks

Four mandatory quality checks are executed after randomization and before treatment delivery.

### 12a. Sample Ratio Mismatch (SRM) Test

Verify that the observed group sizes are consistent with a true 50/50 randomization.

- **Method:** Binomial test on group counts, H₀: p_T = 0.5
- **Pass criterion:** p-value > 0.01
- **Result:** PASS — observed ratio consistent with 50/50 randomization

### 12b. Baseline Covariate Balance

Compare pre-period covariates between Treatment and Control groups.

- **Method:** Welch's t-test for continuous variables; χ² for categorical variables
- **Variables tested:** `avg_weekly_spend`, `total_trips`, `spend_per_trip`, `items_per_trip`, `coupon_usage_rate`, `loyalty_usage_rate`, `recency_days`, `n_departments`
- **Pass criterion:** All p-values > 0.05 (expect ~5% to flag by chance)
- **Result:** PASS — no significant covariate imbalances detected

### 12c. A/A Simulation Sanity Check

Verify that the randomization produces a calibrated test statistic under the null hypothesis.

- **Method:** 1,000 random 50/50 splits of the eligible population (no treatment); apply Welch's t-test to each
- **Pass criterion:** False positive rate ∈ [0.03, 0.08]
- **Result:** PASS — FPR ≈ 5% (matches α = 0.05)

### 12d. Duplicate Check

Verify that each household appears exactly once in the assignment table.

- **Method:** Count rows per `household_key` in the assignment output
- **Pass criterion:** Zero duplicates, zero households in multiple groups
- **Result:** PASS — every household appears exactly once

---

## Step 13: Pre-Registered Analysis Plan

**This plan is locked before treatment delivery. No modifications are permitted after randomization.**

### 13a. Estimand

Average Treatment Effect under Intent-to-Treat (ITT):

$$\tau_{\text{ITT}} = \mathbb{E}[Y_i(1) - Y_i(0) \mid \text{Eligible}]$$

where:
- $Y_i(1)$ = 4-week total spend if household receives coupon
- $Y_i(0)$ = 4-week total spend if household receives no coupon
- Zero-spend households (non-purchasers) included with $Y_i = 0$

### 13b. Primary Estimator — Welch's t-test

$$t = \frac{\bar{Y}_T - \bar{Y}_C}{\sqrt{\dfrac{s_T^2}{n_T} + \dfrac{s_C^2}{n_C}}}$$

95% Confidence Interval:

$$(\bar{Y}_T - \bar{Y}_C) \pm t_{1-\alpha/2,\,\nu} \cdot \sqrt{\frac{s_T^2}{n_T} + \frac{s_C^2}{n_C}}$$

where $\nu$ is the Welch-Satterthwaite degrees of freedom.

### 13c. CUPED Variance Reduction (Optional)

$$\hat{Y}_i^{\text{CUPED}} = Y_i^{\text{post}} - \theta\left(X_i^{\text{pre}} - \bar{X}^{\text{pre}}\right)$$

where:
- $Y_i^{\text{post}}$ = 4-week total spend (experiment outcome)
- $X_i^{\text{pre}}$ = pre-period avg weekly spend × 4 (scaled to same unit)
- $\theta = \text{Cov}(Y^{\text{post}}, X^{\text{pre}}) / \text{Var}(X^{\text{pre}})$
- Expected variance reduction: $1 - \rho^2 = 1 - 0.682^2 \approx 53.5\%$

CUPED reduces the required sample size by ~53% at the same power level.

### 13d. Outlier Handling

- Winsorize the outcome variable at the 1st and 99th percentiles
- Report both raw and winsorized results; primary decision based on winsorized

### 13e. Secondary Analyses

| Metric | Test | Adjusted α |
|---|---|---|
| Conversion rate | Two-proportion z-test | 0.0125 (Bonferroni) |
| Basket size | Welch's t-test | 0.0125 |
| Trip frequency | Welch's t-test | 0.0125 |
| Category penetration | Two-proportion z-test | 0.0125 |

Secondary analyses are exploratory and do not affect the launch decision.

---

## Step 14: Decision Rule

**The campaign is recommended for launch if and only if all three conditions are met:**

| Gate | Criterion |
|---|---|
| 1. Statistical significance | Primary metric p-value < 0.05 (two-sided) |
| 2. Practical significance | Point estimate ≥ $14/4wk AND lower 95% CI bound > $0 |
| 3. Guardrail metrics | Discount cost ≤ $3/HH AND non-target spend decline < 5% |

### Decision Matrix

| p < 0.05 | Effect ≥ MDE | Guardrails OK | Recommended Action |
|---|---|---|---|
| ✓ | ✓ | ✓ | **LAUNCH** — Proceed to full rollout |
| ✓ | ✗ | ✓ | **ITERATE** — Effect exists but below break-even |
| ✓ | ✓ | ✗ | **HOLD** — Investigate guardrail violations before deciding |
| ✗ | — | — | **NO LAUNCH** — Insufficient evidence of meaningful effect |

The three-gate structure prevents launching a campaign that is statistically detectable but economically insufficient, and ensures guardrail violations (e.g., excessive discount costs) are investigated before rollout.
