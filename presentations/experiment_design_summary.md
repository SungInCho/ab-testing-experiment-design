# A/B Test Experiment Design
## Household-Level Coupon Campaign — dunnhumby Complete Journey

---

## Slide 1: Business Question

> *"Will sending targeted promotional coupons to frequent shoppers increase their 4-week total grocery spend by at least $14?"*

**Why it matters:**
- Coupon campaigns are costly — mailing + redemption ≈ $1.50 per household
- Without an experiment, impossible to separate incremental lift from baseline behavior
- A rigorous A/B test provides a causal estimate of campaign ROI

---

## Slide 2: Dataset & Scale

| Dimension | Value |
|---|---|
| Dataset | dunnhumby "The Complete Journey" |
| Households | 2,498 frequent shoppers |
| Transactions | ~2.6M line items |
| Time span | 102 weeks (~2 years) |
| Pre-period | Weeks 1–71 (baseline) |
| Post-period | Weeks 72–102 (validation proxy) |

---

## Slide 3: Experiment Design Overview

```
ELIGIBLE POPULATION
(active HHs: ≥2 trips, recency ≤90d, ≥1 campaign)
            │
            ▼
    STRATIFIED RANDOMIZATION
    (spend tier × recency band, 16 cells)
            │
     ┌──────┴──────┐
     ▼             ▼
 TREATMENT      CONTROL
(coupons)    (no mailing)
     │             │
     └──────┬──────┘
            ▼
  MEASURE: 4-WEEK TOTAL SPEND
  (ITT: zeros included)
```

---

## Slide 4: Key Design Decisions

| Step | Decision |
|---|---|
| Primary metric | 4-week total spend (ITT) |
| MDE | **$14** per 4 weeks (~$3.50/week) |
| α / Power | 0.05 / 80% |
| Test | Two-sided Welch's t-test |
| Allocation | 50 / 50 |
| Randomization | Stratified (spend tier × recency) |
| Duration | 4 weeks, fixed horizon |
| Variance reduction | CUPED (~35% variance reduction) |

---

## Slide 5: Why $14 MDE?

**Cost-based justification:**

| Component | Value |
|---|---|
| Coupons per HH | 5 coupons |
| Face value | $1.00/coupon |
| Redemption rate | ~20% |
| Redemption cost | $1.00/HH |
| Mailing cost | $0.50/HH |
| **Total cost** | **$1.50/HH** |

Break-even = $1.50 incremental spend.
MDE set at **$14** for a meaningful ROI margin ($14 > $1.50 → ~9× ROI if effect achieved).

---

## Slide 6: Variance Estimation

**Pre-post correlation:** r ≈ 0.81 → strong CUPED opportunity

**σ estimates (4-week total spend):**

```
Raw σ (ITT)         → Highest (conservative planning bound)
Winsorized σ        → Moderate (1st–99th pct clip)
CUPED-adjusted σ    → ~35% lower than raw
```

**Key insight:** Using σ from 4-week rolling windows (not 71-week pre-period average) gives a realistic noise estimate that matches the actual experiment duration.

---

## Slide 7: Power Analysis

Required n per arm formula:

$$n = \frac{2\sigma^2 (z_{0.975} + z_{0.80})^2}{\delta^2}$$

At MDE = $14:
- **Raw σ:** Highest n/arm
- **CUPED σ:** ~35% fewer HHs needed per arm
- **CUPED makes the experiment substantially more feasible**

Power curves in `notebooks/02_experiment_design.ipynb` → Step 8.

---

## Slide 8: CUPED Variance Reduction

**Why CUPED works here:**
- Pre-post spend correlation: **r ≈ 0.81**
- Households that spent more in the pre-period will spend more in post-period regardless of treatment
- CUPED removes this predictable variation, isolating the treatment signal

**Implementation:**

$$\hat{Y}_i = Y_i^{\text{post}} - \theta(X_i^{\text{pre}} - \bar{X}^{\text{pre}})$$

- $Y^{\text{post}}$ = 4-week total spend *(experiment metric)*
- $X^{\text{pre}}$ = avg weekly spend × 4 *(same unit — key for alignment)*
- Variance reduction = $(1 - \rho^2) \approx 34\%$

---

## Slide 9: Pre-Launch Quality Checks

All four checks must pass **before** treatment delivery:

| Check | Method | Status |
|---|---|---|
| Sample Ratio Mismatch | Binomial test (p > 0.01) | ✓ |
| Baseline Balance | Welch's t / χ² (no significant differences) | ✓ |
| A/A Simulation | FPR ≈ 5% on 1,000 random splits | ✓ |
| Duplicate Check | 0 households appear twice | ✓ |

---

## Slide 10: Decision Rule

**Launch if and only if all three gates pass:**

| Gate | Criterion |
|---|---|
| Statistical | p < 0.05 (two-sided) |
| Practical | Effect ≥ $14/4wk AND CI lower > $0 |
| Guardrails | Discount cost ≤ $3/HH AND non-target spend decline < 5% |

**Decision matrix:**

| Stat. Sig. | Effect ≥ MDE | Guardrails | Decision |
|---|---|---|---|
| ✓ | ✓ | ✓ | **LAUNCH** |
| ✓ | ✗ | ✓ | **ITERATE** |
| ✓ | ✓ | ✗ | **HOLD** |
| ✗ | — | — | **NO LAUNCH** |

---

## Slide 11: Repository Structure

```
ab-testing-experiment-design-complete-journey/
├── notebooks/         ← Main analysis (3 notebooks)
├── src/               ← Reusable Python modules
├── docs/              ← Written documentation
├── data/raw/          ← dunnhumby CSV files
└── outputs/           ← Figures, tables, intermediate data
```

**Notebooks:**
- `01_data_preparation_and_eda.ipynb`
- `02_experiment_design.ipynb` ← Main deliverable
- `03_appendix.ipynb`

---

## Summary

This project demonstrates a **complete, pre-registered A/B test experiment design** that:
- Uses cost-based MDE justification ($14/4wk)
- Applies CUPED for ~35% variance reduction (ρ ≈ 0.81)
- Uses ITT analysis with zero-spend households included
- Validates the design with 4 pre-launch quality checks
- Provides a clear, binary launch decision rule

**The design is ready for execution if an actual coupon campaign were to be run.**
