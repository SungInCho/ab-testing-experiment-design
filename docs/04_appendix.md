# Appendix

**Notebook:** `notebooks/03_appendix.ipynb`

Supporting analyses and reference materials for the experiment design documented in `03_ab_test_experiment_design.md`.

---

## Appendix A: Baseline Summary by Stratification Cell

### Purpose

Demonstrate that the 16 stratification cells (4 spend tiers × 4 recency bands) capture meaningful behavioral variation and that stratified randomization is warranted.

### Spend Tier Summary (Eligible Population, n = 1,288)

| Spend Tier | n | Pre-Period 4-wk Spend (Mean) | Pre-Period 4-wk Spend (SD) |
|---|---|---|---|
| High | 573 | $332.90 | $145.57 |
| Medium-High | 458 | $133.38 | $27.28 |
| Medium-Low | 234 | $67.64 | $15.29 |
| Low | 23 | $28.90 | $5.78 |

### Recency Band Summary (Eligible Population)

| Recency Band | n | Mean Spend | Engagement Level |
|---|---|---|---|
| 0–7d (Active) | 942 | High | Highest |
| 8–30d (Recent) | 287 | Moderate | Moderate |
| 31–90d (Lapsing) | 59 | Low | Lowest |

### Interpretation

- Spend varies by a factor of ~11× across tiers (Low vs. High)
- Within-tier standard deviations are much smaller than across-tier differences — stratifying eliminates this as a confounder
- Recency captures a complementary dimension: Active and Lapsing households differ in coupon responsiveness even within the same spend tier
- A heatmap of household counts by stratum cell shows concentration in the High × Active cell — stratification ensures the small Low-tier and Lapsing-band cells are still balanced 50/50

---

## Appendix B: Sample Size Calculation Sheet

### Purpose

Sensitivity analysis across MDE values, variance assumptions, and power levels to inform feasibility and identify the minimum detectable effect achievable with the available sample.

### Variance Inputs (4-Week Total Spend, ITT, Eligible Population)

| Estimate | σ | Notes |
|---|---|---|
| `σ_raw` | $188.81 | Full ITT distribution, zeros included |
| `σ_win` | $183.18 | Winsorized at 1st–99th percentile |
| `σ_CUPED` | $138.01 | CUPED-adjusted: σ_raw × √(1 − 0.682²) |
| Pre-post correlation | ρ = 0.682 | Pre-period avg weekly spend × 4 vs. post 4-week total spend |

### Sample Size Formula

$$n_{\text{per arm}} = \frac{2\sigma^2 (z_{1-\alpha/2} + z_{1-\beta})^2}{\delta^2}$$

With CUPED: replace σ with σ_CUPED = σ × √(1 − ρ²)

### Feasibility Table (Power = 80%, α = 0.05)

| MDE (4-week) | n/arm — Raw | n/arm — Winsorized | n/arm — CUPED | Total (CUPED) | Feasible? |
|---|---|---|---|---|---|
| $8 | ~11,425 | ~10,738 | ~6,104 | ~12,208 | No |
| $12 | ~5,078 | ~4,772 | ~2,713 | ~5,426 | No |
| $14 | ~2,856 | ~2,684 | ~1,526 | ~3,052 | No |
| $20 | ~1,461 | ~1,373 | ~760 | ~1,520 | No |
| $24 | ~663 | ~623 | ~520 | ~1,040 | **Yes** |
| $32 | ~445 | ~418 | ~292 | ~584 | **Yes** |
| $40 | ~365 | ~343 | ~239 | ~478 | **Yes** |

**Available eligible households: 1,288 (644 per arm)**

### Key Takeaways

- **MDE = $14 is not achievable** with 1,288 eligible households, even with CUPED variance reduction
- **Minimum feasible MDE** at 80% power with CUPED: approximately **$24** (total n ≈ 1,040)
- At MDE = $24, CUPED is the enabling technique — without it, the same scenario requires ~2× more subjects
- The experiment is underpowered for the business-justified $14 threshold with the current eligible pool

### Power Curve Visualization

Two plots are generated:
- **(a) n per arm vs. MDE** for raw, winsorized, and CUPED variance estimates — with reference lines at MDE = $14 and max n/arm = 644
- **(b) Power vs. true effect size** at fixed n = 644 per arm — shows achievable power at different effect sizes under each variance scenario

---

## Appendix C: Pre-Registered Analysis Plan Template

A formal pre-registration document to be filed before treatment delivery and randomization output are released to any analyst.

### Experiment Details

| Field | Value |
|---|---|
| **Experiment name** | Household Coupon Re-engagement Campaign |
| **Owner** | Data Science Team |
| **Status** | Pre-registered (locked) |
| **Registration date** | Filed before Day 0 (randomization) |

### 1. Hypothesis

- **H₀:** μ_T − μ_C = 0 (no effect on 4-week household spend)
- **H₁:** μ_T − μ_C ≠ 0 (two-sided alternative)

### 2. Primary Outcome

| Field | Specification |
|---|---|
| Metric | 4-week total household spend ($) |
| Unit | Household |
| Window | 4 weeks post-coupon delivery (Days 3–31) |
| Inclusion | All eligible households, ITT (including $0 spend) |

### 3. Statistical Test

| Parameter | Value |
|---|---|
| Test | Welch's t-test (unequal variance) |
| α | 0.05 (two-sided) |
| Power | 0.80 |
| MDE | $14.00 (4-week total) |
| Variance source | Post-period 4-week rolling window (σ = $188.81 raw, $138.01 CUPED) |
| Variance reduction | CUPED using pre-period avg weekly spend × 4 |

### 4. Outlier Handling

- Winsorize outcome at 1st and 99th percentiles
- Report both raw and winsorized results
- Primary decision based on winsorized estimate

### 5. Secondary Analyses (Exploratory — Bonferroni α/4 = 0.0125)

- Conversion rate (binary: made ≥1 purchase in 4-week window)
- Basket size (avg spend per trip in 4-week window)
- Trip frequency (number of trips in 4-week window)
- Category penetration (purchased in target category, binary)

### 6. Subgroup Analyses (Exploratory only — no impact on launch decision)

- By spend tier: Low / Medium-Low / Medium-High / High
- By recency band: 0–7d / 8–30d / 31–90d
- By demographics: Age group, income level, household size (where available)

### 7. Decision Rule

Roll out if **all** of:
1. Primary metric p-value < 0.05 (two-sided)
2. Point estimate ≥ $14.00 AND lower 95% CI bound > $0
3. All guardrail metrics within tolerance

### 8. Experiment Timeline

| Milestone | Timing |
|---|---|
| Pre-registration filed | Before Day 0 |
| Randomization + assignment | Day 0 |
| Coupons delivered | Day 0–3 |
| Post-treatment window | Day 3–31 |
| Data freeze | Day 35 |
| Analysis | Day 36–38 |
| Decision meeting | Day 40 |

---

## Appendix D: Subgroup Analysis Preview (Exploratory)

### Purpose

Pre-declared exploratory analyses examining whether the treatment effect (if real) varies meaningfully across segments. These analyses are hypothesis-generating and will not affect the launch decision.

### By Spend Tier

For each spend tier, the following are reported:

- n_T, n_C (group sizes)
- Mean 4-week spend per group
- Observed difference (no treatment applied — used for pre-experiment baseline comparison)
- p-value of Welch's t-test

**Visualization:** Bar plots of 4-week total spend by spend tier and group (Treatment vs. Control)

### By Recency Band

- Bar plots of 4-week total spend by recency band (0–7d, 8–30d, 31–90d) and group
- Active households are expected to show higher baseline spend in both groups

### By Demographics

- Subgroup analyses stratified by age group, income level, and household size
- Limited to households with demographic data (~800 of 1,288 eligible)
- Results interpreted with caution given smaller subgroup sizes and multiple comparisons

**Important Note:** Since no treatment has actually been applied (this is a design exercise using historical data), all subgroup differences reflect pre-existing behavioral variation rather than true treatment effects.

---

## Appendix E: Binary Outcome Power Analysis (Conversion Rate)

### Purpose

Complement the continuous spend power analysis with a binary outcome analysis for **conversion rate** (proportion of households making ≥1 purchase in the 4-week window).

### Baseline

- **Baseline 4-week conversion rate (control):** 0.922 (92.2%)
- **N eligible:** 1,288 (644 per arm)

### Formula (Two-Proportion z-Test)

$$n_{\text{per arm}} = \frac{(z_{1-\alpha/2} + z_{1-\beta})^2 [p_C(1-p_C) + p_T(1-p_T)]}{(p_T - p_C)^2}$$

### Sample Size Requirements

| MDE (percentage points) | p_T | n/arm (Power=80%) | n/arm (Power=90%) | Feasible (≤644)? |
|---|---|---|---|---|
| 2 pp | 0.942 | ~2,498 | ~3,347 | No |
| 3 pp | 0.952 | ~1,080 | ~1,446 | No |
| 5 pp | 0.972 | ~314 | ~421 | **Yes** |
| 7 pp | 0.992 | ~130 | ~174 | **Yes** |
| 10 pp | 1.000 | ~40 | ~53 | **Yes** (ceiling effect) |

### Interpretation

- The high baseline conversion rate (92.2%) creates a **ceiling effect** — very little room to increase conversion
- Detecting a 2–3 percentage point increase is statistically infeasible with the available sample
- A 5 pp increase is feasible but would mean nearly all households (97.2%) are converting — practically implausible
- **Conversion rate is not a sensitive metric** for this experiment; 4-week total spend is the appropriate primary outcome
- Binary outcome analysis confirms that the continuous spend metric is the right choice for primary inference
