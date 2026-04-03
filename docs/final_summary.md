# Final Design Summary

**Project:** Household-Level Coupon A/B Test — dunnhumby Complete Journey
**Date:** April 2026
**Framework:** 14-Step Pre-Registered Experiment Design

---

## Business Question

> *"Will sending category-specific promotional coupons to eligible frequent shoppers increase their 4-week total spend by at least $14?"*

---

## Complete Design Decisions

| Step | Topic | Decision |
|---|---|---|
| 1 | Business Decision | Coupon campaign ROI test — requires ≥$14 incremental spend per HH per 4 weeks |
| 2 | Eligible Population | Active HHs: ≥2 pre-period trips, recency ≤90 days, ≥1 campaign contact |
| 3 | Treatment / Control | Category coupons (direct mail) vs. no mailing; 4-week window |
| 4 | Metrics | Primary: 4-week total spend (ITT). Secondary: conversion, basket size, trips |
| 5a | Baselines | Pre-period: right-skewed spend, low coupon rate, stratification validated |
| 5b | Variance Estimation | 4-week rolling ITT σ; pre-post stable (r ≈ 0.81); post σ used for power |
| 5c | MDE Realism | A/A noise floor < $14 MDE → experiment is feasible |
| 6 | MDE | **$14 per 4 weeks** ($3.50/week) — cost-justified |
| 7 | Alpha / Power | α = 0.05, Power = 0.80, two-sided Welch's t-test |
| 8 | Sample Size | n/arm from 4-week ITT σ; CUPED reduces by ~35% (ρ ≈ 0.81) |
| 9 | Allocation | 50% Treatment / 50% Control |
| 10 | Randomization | Stratified: spend tier (4) × recency band (4) = 16 cells; seed = 42 |
| 11 | Duration | 4 weeks fixed horizon; no early stopping; 1-week washout buffer |
| 12 | Quality Checks | SRM ✓, balance ✓, A/A FPR ≈ 5% ✓, no duplicates ✓ |
| 13 | Analysis Plan | Welch's t-test (primary), CUPED adjustment, ITT + Bonferroni (secondary) |
| 14 | Decision Rule | Launch: p < 0.05 AND effect ≥ $14 AND guardrails pass |

---

## Key Parameters at a Glance

| Parameter | Value |
|---|---|
| Dataset | dunnhumby Complete Journey |
| Total households | 2,498 |
| Pre-period | Weeks 1–71 (~17 months) |
| Post-period (proxy) | Weeks 72–102 (~7 months) |
| Experiment window | 4 weeks |
| Primary metric | 4-week total spend (ITT) |
| MDE | $14.00 per 4 weeks |
| Significance level | α = 0.05 |
| Power | 80% |
| Test | Two-sided Welch's t-test |
| Allocation | 50/50 |
| Randomization | Stratified (spend tier × recency band) |
| Pre-post correlation | r ≈ 0.81 |
| CUPED variance reduction | ~35% |
| Zero-spend rate (4-wk) | ~8% |

---

## Statistical Design Summary

### Power Analysis

For the primary metric (4-week total spend), the required sample size per arm is computed as:

$$n = \frac{2\sigma^2 (z_{1-\alpha/2} + z_{1-\beta})^2}{\delta^2}$$

Key σ scenarios:

| σ Scenario | Value | n/arm at MDE=$14 |
|---|---|---|
| Raw (full ITT) | Estimated from data | Highest |
| Winsorized (1–99%) | Reduced | Moderate |
| Conservative (max pre/post) | Max of two estimates | Used for planning |
| CUPED-adjusted | Conservative × √(1−ρ²) | ~35% lower |

### CUPED Variance Reduction

$$\hat{Y}_i^{\text{CUPED}} = Y_i^{\text{post}} - \theta(X_i^{\text{pre}} - \bar{X}^{\text{pre}})$$

- $Y^{\text{post}}$: 4-week total spend (experiment metric)
- $X^{\text{pre}}$: pre-period avg weekly spend × 4 (aligned to 4-week unit)
- $\theta = \text{Cov}(Y,X) / \text{Var}(X)$
- Variance reduction ≈ $1 - \rho^2 \approx 34\%$ at $\rho = 0.81$

---

## Quality Checks (Pre-Launch)

| Check | Method | Criterion | Status |
|---|---|---|---|
| SRM | Binomial test on group counts | p > 0.01 | ✓ Pass |
| Baseline balance | Welch's t (continuous), χ² (categorical) | All p > 0.05 | ✓ Pass |
| A/A simulation | 1000 random splits, FPR check | FPR ≈ 5% | ✓ Pass |
| Duplicate check | Count unique household keys | 0 duplicates | ✓ Pass |

---

## Decision Framework

The campaign is recommended for **LAUNCH** if and only if:

1. **Statistical significance:** p < 0.05 (two-sided Welch's t-test)
2. **Practical significance:** Effect estimate ≥ $14/4wk AND CI lower bound > $0
3. **Guardrails:** Discount cost ≤ $3/HH AND non-target category spend decline < 5%

### Decision Matrix

| p < 0.05 | Effect ≥ $14 | Guardrails OK | Action |
|---|---|---|---|
| ✓ | ✓ | ✓ | **LAUNCH** — Full rollout |
| ✓ | ✗ | ✓ | **ITERATE** — Effect exists but below break-even |
| ✓ | ✓ | ✗ | **HOLD** — Investigate guardrail violations |
| ✗ | — | — | **NO LAUNCH** — Insufficient evidence |

---

## Appendix Reference

| Appendix | Content |
|---|---|
| A | Baseline summary by stratification cell (16 cells) |
| B | Sample size sensitivity table (MDE × σ × power scenarios) |
| C | Pre-registered analysis plan template |
| D | Subgroup analysis preview (spend tier, demographics) |
| E | Binary power analysis for conversion rate |
| F | A/A simulation detailed results |
| G | Stratification balance verification |

---

## Notebooks

| Notebook | Description |
|---|---|
| `01_data_preparation_and_eda.ipynb` | Data loading, feature engineering, EDA (Steps pre-1) |
| `02_experiment_design.ipynb` | Full 14-step experiment design |
| `03_appendix.ipynb` | Supporting analyses (Appendices A–G) |
