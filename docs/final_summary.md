# Final Design Summary

**Project:** Household-Level Coupon A/B Test — dunnhumby Complete Journey
**Framework:** 14-Step Pre-Registered Experiment Design

---

## Business Question

> *"Will sending category-specific promotional coupons to eligible frequent shoppers increase their 4-week total spend by at least $14 — enough to justify full-scale campaign rollout?"*

---

## Project Flow

```
Raw Data (8 tables)
        │
        ▼
[Notebook 1] Data Preparation & EDA
  • Load & join 8 raw tables
  • Engineer household-level features (spend, frequency, recency, promo)
  • Explore distributions, trends, and stratification structure
  • Output: hh_features.csv (2,498 HH × 50 features)
        │
        ▼
[Notebook 2] Experiment Design (14 Steps)
  • Steps 1–4:  Business question, eligibility, treatment/control, metrics
  • Steps 5a–5c: Baselines, variance estimation, A/A simulation
  • Steps 6–7:  MDE justification, α and power settings
  • Step 8:     Power analysis and sample size calculation
  • Steps 9–11: Allocation, randomization, duration/stopping rules
  • Step 12:    Pre-launch quality checks
  • Steps 13–14: Pre-registered analysis plan and decision rule
        │
        ▼
[Notebook 3] Appendix
  • Appendix A: Stratum-level baseline summary
  • Appendix B: Sample size sensitivity table (MDE × σ × power)
  • Appendix C: Formal pre-registration template
  • Appendix D: Exploratory subgroup analysis preview
  • Appendix E: Binary outcome (conversion rate) power analysis
```

---

## Complete Design Decisions

| Step | Topic | Decision |
|---|---|---|
| 1 | Business decision | Coupon campaign ROI test — requires ≥$14 incremental spend per HH per 4 weeks to justify rollout |
| 2 | Eligible population | ≥2 pre-period trips + recency ≤90 days + ≥1 campaign contact → **1,288 households** |
| 3 | Treatment / Control | Category coupons via direct mail vs. business-as-usual; 4-week window |
| 4 | Metrics | **Primary:** 4-week total spend (ITT). **Secondary:** conversion, basket size, trips, category penetration |
| 5a | Baselines | Right-skewed spend, low coupon usage, high recency concentration in Active band |
| 5b | Variance estimation | 4-week rolling window ITT σ; ρ = 0.682 pre-post; σ_raw=$188.81, σ_CUPED=$138.01 |
| 5c | MDE realism | A/A noise floor ~$6–8 < $14 MDE → metric is sensitive enough |
| 6 | MDE | **$14.00 per 4 weeks** ($3.50/week) — cost-based break-even with margin |
| 7 | Alpha / Power | α = 0.05, Power = 0.80, two-sided Welch's t-test |
| 8 | Sample size | Requires ~3,052 total even with CUPED at MDE=$14 → underpowered; min feasible MDE ≈ $24 |
| 9 | Allocation | 50% Treatment / 50% Control (644 per arm) |
| 10 | Randomization | Stratified: spend tier (4) × recency band (4) = 16 cells; seed = 42 |
| 11 | Duration | 4 weeks fixed horizon; no early stopping; 1-week mail delivery buffer |
| 12 | Quality checks | SRM ✓ — Balance ✓ — A/A FPR≈5% ✓ — No duplicates ✓ |
| 13 | Analysis plan | Welch's t-test (primary); CUPED adjustment; ITT + Bonferroni correction for secondary |
| 14 | Decision rule | Launch: p < 0.05 AND effect ≥ $14 AND guardrails pass |

---

## Key Parameters

| Parameter | Value |
|---|---|
| Dataset | dunnhumby Complete Journey |
| Total households | 2,498 |
| Eligible households (ITT population) | 1,288 |
| Pre-period | Weeks 1–71 (~17 months) |
| Post-period (proxy for design) | Weeks 72–102 (~7 months) |
| Experiment window | 4 weeks (28 days) |
| Primary metric | 4-week total household spend (ITT) |
| MDE | $14.00 per 4 weeks |
| Significance level | α = 0.05 (two-sided) |
| Power | 80% |
| Treatment allocation | 50 / 50 (644 per arm) |
| Stratification | spend_tier × recency_band (16 cells) |
| Randomization seed | 42 |

---

## Statistical Results

### Eligible Population Breakdown

| Filter | Households Remaining |
|---|---|
| Total in dataset | 2,498 |
| After ≥2 trips filter | — |
| After recency ≤90d filter | — |
| After ≥1 campaign contact filter | **1,288** |

### Pre-Period Baseline (Eligible, n=1,288)

| Metric | Value |
|---|---|
| Spend distribution | Right-skewed, skewness ≈ 1.4 |
| Zero-spend rate (4-week windows) | ~8% |
| Pre-to-post spend correlation | ρ = 0.682 |
| Coupon usage rate | ~1–2% (low; most households near zero) |
| Dominant recency band | 0–7d Active (n=942, 73% of eligible) |

### Variance Estimates (4-Week Total Spend, ITT)

| Scenario | σ | Notes |
|---|---|---|
| Raw | $188.81 | Full distribution, zeros included |
| Winsorized (1–99%) | $183.18 | Clips extreme upper values |
| CUPED-adjusted | $138.01 | 53.5% variance reduction via ρ=0.682 |

### Power Analysis Results

| MDE (4-week) | n/arm (CUPED) | n total | Feasible? |
|---|---|---|---|
| $8 | ~6,104 | ~12,208 | No |
| $14 | ~1,526 | ~3,052 | **No** |
| $20 | ~760 | ~1,520 | No |
| $24 | ~520 | ~1,040 | **Yes** |
| $32 | ~292 | ~584 | Yes |

**Critical finding:** The business-justified MDE of $14 requires approximately 3,052 eligible households with CUPED — more than 2× the available 1,288. The minimum feasible MDE at 80% power with the current eligible pool is approximately **$24 per 4-week window**.

### CUPED Efficiency

| Metric | Value |
|---|---|
| Pre-post correlation (ρ) | 0.682 |
| Variance reduction (1 − ρ²) | 53.5% |
| σ reduction | $188.81 → $138.01 (−27%) |
| Sample size reduction at same power | ~46% |

Despite CUPED's substantial variance reduction, the experiment remains underpowered for the $14 MDE given the available eligible population. CUPED remains essential — without it, the gap would be even larger.

### Pre-Launch Quality Check Results

| Check | Method | Result |
|---|---|---|
| Sample ratio mismatch | Binomial test, H₀: p=0.5 | PASS (p > 0.01) |
| Baseline covariate balance | Welch's t-test + χ² | PASS (no significant imbalances) |
| A/A simulation FPR | 1,000 random splits | PASS (FPR ≈ 5%) |
| Duplicate households | Row-level check | PASS (0 duplicates) |

### Binary Outcome Feasibility (Conversion Rate)

| MDE | Baseline Conversion | n/arm (80% power) | Feasible? |
|---|---|---|---|
| 2 pp | 92.2% → 94.2% | ~2,498 | No |
| 5 pp | 92.2% → 97.2% | ~314 | Yes |
| 10 pp | 92.2% → 100% | ~40 | Yes (ceiling) |

The high baseline conversion rate (92.2%) and ceiling effect make conversion rate a poor primary metric. 4-week total spend is the appropriate primary outcome.

---

## Analysis Plan Summary (Pre-Registered)

### Primary Analysis

| Component | Specification |
|---|---|
| Estimand | ITT: E[Y(1) − Y(0) \| Eligible] |
| Test | Welch's t-test (unequal variance, two-sided) |
| Outcome | 4-week total household spend (zeros included) |
| Variance reduction | CUPED (θ = Cov(Y_post, X_pre) / Var(X_pre)) |
| Outlier handling | Winsorize at 1st/99th percentile |
| Significance | α = 0.05 |

### Decision Rule (Three-Gate Framework)

| Gate | Criterion | Ensures |
|---|---|---|
| Statistical significance | p < 0.05 (two-sided) | Effect is unlikely due to chance |
| Practical significance | Estimate ≥ $14 AND lower 95% CI > $0 | Effect is economically meaningful |
| Guardrails | Discount cost ≤ $3/HH AND non-target spend decline < 5% | No harmful side effects |

All three gates must pass for a **LAUNCH** recommendation.

---

## Summary of Key Design Features

1. **Cost-justified MDE:** $14 derived from campaign economics ($1.50/HH cost, moderate ROI scenario) — not an arbitrary effect size
2. **ITT framework:** All 1,288 eligible households included in analysis regardless of coupon redemption; prevents selection bias
3. **4-week metric alignment:** Primary metric matches experiment window and coupon validity period exactly
4. **Empirical variance estimation:** 4-week rolling window variance from post-period data, not scaled 71-week average
5. **CUPED variance reduction:** ρ = 0.682 enables ~46% sample size reduction at the same power — the critical technique enabling feasibility
6. **Stratified randomization:** 16-cell stratification grid (spend tier × recency) ensures balance on the two strongest confounders
7. **Pre-registered analysis plan:** Locked before treatment delivery; eliminates researcher degrees of freedom and p-hacking risk
8. **Four pre-launch QA checks:** SRM, covariate balance, A/A simulation, and duplicate check — all must pass before coupon delivery
9. **Three-gate decision rule:** Combines statistical, practical, and guardrail criteria — prevents launching campaigns with statistically real but economically insufficient effects
10. **Honest power gap acknowledgment:** The design rigorously quantifies that MDE=$14 is not achievable with 1,288 households; minimum feasible MDE ≈ $24 with CUPED

---

## Conclusion

This project delivers a complete, pre-registered A/B experiment design for a household-level grocery coupon campaign. The design follows a rigorous 14-step framework grounded in causal inference best practices.

**The central power analysis finding** is that the business-justified MDE of $14 per 4-week window cannot be detected with statistical power of 80% given the available 1,288 eligible households — even after applying CUPED variance reduction. The minimum detectable effect with the current sample is approximately **$24 per 4-week window** (at 80% power, α = 0.05).

**Practical implications for a real experiment:**
- If the campaign budget is fixed, lower power must be accepted or the MDE threshold relaxed
- If detecting $14 is essential, the eligible pool must be expanded (relaxed criteria) or sample size increased through broader recruitment
- CUPED is non-negotiable — it reduces required sample size by ~46% and is the single biggest lever available
- The pre-registered design is execution-ready the moment a sufficient eligible population is assembled and coupons can be deployed

The design is complete, transparent about its limitations, and structured to prevent both false discoveries and missed opportunities.
