# A/B Test Experiment Design

**Notebook:** `notebooks/02_experiment_design.ipynb`

This document details the complete 14-step experiment design for a household-level coupon campaign A/B test, using the dunnhumby Complete Journey dataset.

---

## Step 1: Define the Business Decision

### Context
A national grocery retailer is considering launching a **targeted coupon campaign** to increase household spending. The campaign sends category-specific coupons via direct mail to selected households, targeting their top-purchased department.

### Decision Statement
> *"Will sending a household-level promotional coupon to eligible frequent shoppers increase their 4-week total spend by at least $14 — enough to justify the mailing and redemption costs?"*

### Why This Matters
Without an experiment, it is unclear whether coupons cause incremental spend or simply reward purchases that would have happened anyway. The A/B test provides a causal estimate of the lift.

---

## Step 2: Select the Eligible Population

### Eligibility Criteria

| Rule | Rationale |
|---|---|
| Active in pre-period (weeks 1–71) | Must have purchase history for baseline estimation |
| ≥2 trips in pre-period | Minimum engagement to be a viable coupon target |
| Recency ≤ 90 days | Exclude churned households unlikely to respond |
| ≥1 historical campaign received | Confirms contactability via direct mail |

### Why ITT Framework
All eligible households are included in the analysis, regardless of whether they actually redeem the coupon. This is the **Intent-to-Treat (ITT)** approach:
- Prevents selection bias from non-compliers
- Gives a conservative estimate of the campaign's average effect
- Is consistent with how the business would actually deploy the campaign

---

## Step 3: Treatment, Control, and Exposure Window

| Aspect | Description |
|---|---|
| **Treatment** | Category-specific coupons via direct mail (targeted to top department) |
| **Control** | Business-as-usual — no mailing |
| **Coupon value** | ~$1.00 average face value (consistent with observed COUPON_DISC in data) |
| **Coupons per household** | 5 coupons |
| **Mailing cost** | ~$0.50 per household |
| **Exposure window** | 4 weeks (28 days) |
| **Coupon validity** | 28 days from delivery (matches exposure window) |

---

## Step 4: Define Success Metrics

### Primary Metric
**4-week total household spend** during the post-treatment window.

$$\tau_{\text{ITT}} = \bar{Y}_T - \bar{Y}_C$$

where $Y_i$ = sum of all SALES_VALUE for household $i$ during the 4-week experiment window, and households with zero purchases contribute $Y_i = 0$.

### Secondary Metrics (Exploratory)

| Metric | Definition | Test |
|---|---|---|
| Conversion rate | Proportion with ≥1 purchase in 4-week window | Two-proportion z-test |
| Basket size ($/trip) | Spend / trips (0 if no trips) | Welch's t-test |
| Total trips | Count of distinct shopping visits | Welch's t-test |

Secondary metrics are not used for the launch decision. Results reported with Bonferroni-corrected thresholds.

---

## Step 5: Build Pre-Period Baselines

### 5a: Baseline Summary Statistics

Pre-period (weeks 1–71) behavioral summary by spend tier:

- **Spend distribution:** Right-skewed — winsorization necessary for power analysis
- **Stratification effectiveness:** Baseline characteristics differ significantly across spend tiers, confirming stratification adds value
- **Coupon responsiveness:** Low overall but varies by tier — treatment effect may be heterogeneous

### 5b: Variance Estimation & Post-Period Validation

We estimate σ using **4-week rolling windows** over the post-period (weeks 72–102):

- Rolling windows avoid the smoothing effect of long-horizon averages
- ITT population (zeros included) gives an honest σ estimate for power analysis
- Key check: pre-period σ (scaled) and post-period σ are compared — we take the maximum (conservative)

**Variance estimation approach:**
```
Pre σ scaled = weekly_σ × √4
Post σ (ITT) = median std_spend_all from rolling 4-week windows
sigma_for_power = max(pre σ scaled, post σ)
```

**Pre-post correlation:** r ≈ 0.81 — confirms CUPED will be effective.

### 5c: Metric Feasibility & MDE Realism

**Feasibility checks:**
- Zero-spend rate in 4-week windows: ~8% — low enough for ITT analysis without special handling
- Distribution: Right-skewed, heavy upper tail (Q-Q deviation) — winsorization recommended
- Standard t-test remains valid at n > 100 by CLT

**MDE Realism (A/A Simulation):**
- 1000 random 50/50 splits of the post-period population (no treatment)
- The 95th percentile of |mean differences| defines the **noise floor**
- MDE ($14) > noise floor → experiment is feasible; the signal is above the noise

---

## Step 6: Minimum Detectable Effect (MDE)

### Cost-Based Justification

| Component | Value |
|---|---|
| Coupons per household | 5 |
| Average coupon face value | $1.00 |
| Expected redemption rate | ~20% |
| Coupon redemption cost | 5 × $1.00 × 20% = $1.00 |
| Mailing cost | $0.50 |
| **Total cost per treated HH** | **$1.50** |

Break-even over 4 weeks: $1.50 in incremental spend minimum.

### MDE Scenarios

| Scenario | MDE (4-week) | Description |
|---|---|---|
| Conservative | $8 | Low bar — catches even small effects |
| **Moderate (primary)** | **$14** | Cost-justified with margin; business base case |
| Ambitious | $20 | Strong ROI scenario |

**Primary MDE: $14 per 4-week window (~$3.50/week).**

---

## Step 7: Alpha, Power, and Test Type

| Parameter | Value | Rationale |
|---|---|---|
| Significance level (α) | 0.05 | Industry standard; 5% false positive rate |
| Power (1 − β) | 0.80 | 80% probability of detecting true effect ≥ MDE |
| Test type | Two-sided | Detect both positive and negative effects |
| Test statistic | Welch's t-test | Handles unequal variance; robust for skewed outcomes |

**Why two-sided:** Although we expect the coupon to increase spend, a two-sided test is more conservative and scientifically honest. An unexpectedly negative effect (coupon substitution) should also be detectable.

---

## Step 8: Required Sample Size

Using the formula for a two-sample t-test with equal allocation:

$$n_{\text{per arm}} = \frac{2\sigma^2 (z_{1-\alpha/2} + z_{1-\beta})^2}{\delta^2}$$

With CUPED-adjusted variance:
$$n_{\text{per arm}}^{\text{CUPED}} = \frac{2\sigma_{\text{CUPED}}^2 (z_{1-\alpha/2} + z_{1-\beta})^2}{\delta^2}$$

where $\sigma_{\text{CUPED}} = \sigma \cdot \sqrt{1 - \rho^2}$

**Key inputs:**
- σ (raw, 4-week ITT): estimated from rolling windows
- σ (winsorized, 4-week): after 1st/99th percentile clipping
- σ (CUPED): ~35% variance reduction with ρ ≈ 0.81

**Power curves** show n per arm vs. MDE for all three sigma scenarios, with the eligible N annotated to check feasibility.

---

## Step 9: Treatment Allocation

**Decision: 50/50 split**

| Consideration | Decision |
|---|---|
| Statistical efficiency | 50/50 maximizes power for given total N |
| Cost | Direct mail cost is low ($0.50/HH) — no reason to minimize treatment arm |
| Learning | Equal arms give symmetric confidence intervals |

---

## Step 10: Randomization Method

### Stratified Randomization

**Stratification grid:** spend tier (4 levels) × recency band (4 levels) = **16 cells**

Within each cell, households are shuffled and split 50/50 using `np.random.RandomState(seed=42)`.

**Why stratify:**
- Spend tier is the strongest predictor of future spend — balancing it removes the biggest confounder
- Recency band controls for engagement level — active vs. lapsing households differ in their coupon responsiveness
- Stratification guarantees balance even with smaller sample sizes

---

## Step 11: Experiment Duration & Stopping Rules

| Parameter | Value | Rationale |
|---|---|---|
| Post-treatment window | 4 weeks | Covers 2+ full shopping cycles |
| Coupon validity | 28 days | Matches measurement window |
| Washout buffer | 1 week | Accounts for mail delivery lag |
| Analysis type | Fixed horizon | No peeking, no early stopping |

### Why No Early Stopping
- Peeking inflates the false positive rate (multiple testing problem)
- Grocery behavior has weekly cycles — need full 4 weeks for stable estimates
- Coupon response may lag delivery by a few days

---

## Step 12: Pre-Launch Quality Checks

Four checks must pass before any treatment is delivered:

### 12a: Sample Ratio Mismatch (SRM)
Binomial test on group counts. Expected: 50/50 split.
- **Pass criterion:** p > 0.01

### 12b: Baseline Balance
Welch's t-test on continuous covariates; χ² on categorical covariates.
- **Pass criterion:** All p > 0.05 (with ~5% false flags expected by chance)

### 12c: A/A Simulation Sanity Check
1000 random A/A splits → false positive rate should ≈ α = 0.05.
- **Pass criterion:** FPR ∈ [0.03, 0.08]

### 12d: Duplicate Check
Each household must appear exactly once in the assignment table.
- **Pass criterion:** 0 duplicates

### Quality Check Summary

| Check | Expected Result |
|---|---|
| SRM test | p > 0.01 |
| Baseline balance | No significant covariate differences |
| A/A FPR | ≈ 5% |
| Duplicates | None |

---

## Step 13: Pre-Registered Analysis Plan

### Estimand (ITT)
$$\tau_{\text{ITT}} = E[Y_i(1) - Y_i(0) \mid \text{Eligible}]$$

### Primary Estimator: Welch's t-test

$$t = \frac{\bar{Y}_T - \bar{Y}_C}{\sqrt{\frac{s_T^2}{n_T} + \frac{s_C^2}{n_C}}}$$

95% confidence interval:
$$(\bar{Y}_T - \bar{Y}_C) \pm t_{1-\alpha/2,\nu} \cdot \sqrt{\frac{s_T^2}{n_T} + \frac{s_C^2}{n_C}}$$

### CUPED Adjustment (Planned)

$$\hat{Y}_i^{\text{CUPED}} = Y_i^{\text{post}} - \theta (X_i^{\text{pre}} - \bar{X}^{\text{pre}})$$

$$\theta = \frac{\text{Cov}(Y^{\text{post}}, X^{\text{pre}})}{\text{Var}(X^{\text{pre}})}$$

- $Y_i^{\text{post}}$ = 4-week total spend (post-period)
- $X_i^{\text{pre}}$ = pre-period avg weekly spend × 4 (scaled to same 4-week unit)
- Variance reduction ≈ (1 − ρ²) ≈ 35% at ρ = 0.81

### Other Analysis Rules
- **Outliers:** Winsorize at 1st/99th percentile; report both winsorized and raw
- **Missing values:** Zero-spend households included as Y = 0 (ITT)
- **Multiple comparisons:** Primary metric — single test, no adjustment. Secondary — Bonferroni correction

---

## Step 14: Decision Rule

### Launch Criteria (All Three Must Pass)

| Gate | Criterion |
|---|---|
| Statistical significance | p-value < 0.05 (two-sided) |
| Practical significance | Point estimate ≥ $14/4wk AND 95% CI lower bound > $0 |
| Guardrails | Discount cost ≤ $3/HH AND non-target spend decline < 5% |

### Decision Matrix

| p < 0.05 | Effect ≥ MDE | Guardrails OK | Decision |
|---|---|---|---|
| Yes | Yes | Yes | **LAUNCH** |
| Yes | No | Yes | **ITERATE** — Effect exists but below economic threshold |
| Yes | Yes | No | **HOLD** — Investigate guardrail violations |
| No | — | — | **NO LAUNCH** — Insufficient evidence |
