# A/B Test Experiment Design — dunnhumby The Complete Journey

A rigorous, pre-registered A/B test experiment design for a household-level coupon campaign, built on the [dunnhumby "The Complete Journey"](https://www.dunnhumby.com/source-files/) dataset. This project follows a structured 14-step experiment design framework and demonstrates best practices in causal inference, power analysis, variance reduction (CUPED), and statistical testing.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Dataset](#dataset)
3. [Repository Structure](#repository-structure)
4. [Experiment Design Summary](#experiment-design-summary)
5. [Key Results](#key-results)
6. [Methodology](#methodology)
7. [How to Run](#how-to-run)
8. [Requirements](#requirements)

---

## Project Overview

**Business Question:** Will sending household-level promotional coupons to eligible frequent shoppers increase their 4-week total spend by at least $14 — enough to justify the campaign rollout cost?

**Approach:**
- Designed a complete pre-registered A/B test using historical grocery transaction data as a proxy for a future experiment
- Applied the **Intent-to-Treat (ITT)** framework — all eligible households, including zero-spenders, are included in the primary analysis
- Used **4-week total spend** as the primary outcome metric, matching the planned coupon validity window
- Applied **CUPED** (Controlled-experiment Using Pre-Experiment Data) for variance reduction
- Validated the design with SRM checks, baseline balance tests, and A/A simulations

---

## Dataset

**Source:** dunnhumby — The Complete Journey
**Scale:** ~2,500 households × 2 years (~102 weeks) of grocery transactions, ~2.6M line-item records

| File | Description |
|---|---|
| `transaction_data.csv` | Line-item purchases (receipt level) |
| `hh_demographic.csv` | Demographics for a subset of households |
| `campaign_table.csv` | Household campaign participation history |
| `campaign_desc.csv` | Campaign type descriptions |
| `coupon.csv` | Coupon-to-product mapping |
| `coupon_redempt.csv` | Coupon redemption events |
| `product.csv` | Product master with department/brand |
| `causal_data.csv` | Display and mailer flags by product/week |
| `hh_features.csv` | Engineered household-level feature table (pre + post) |

> **Note:** Raw data files are not tracked in Git due to file size. Place them in `data/raw/` before running notebooks.

---

## Repository Structure

```
ab-testing-experiment-design-complete-journey/
│
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── .gitignore
│
├── data/
│   ├── README.md                    # Data dictionary & field descriptions
│   └── raw/                         # Raw CSV files (not tracked in Git)
│       └── .gitkeep
│
├── docs/                            # Written documentation for each stage
│   ├── 01_data_preparation.md
│   ├── 02_exploratory_data_analysis.md
│   ├── 03_ab_test_experiment_design.md
│   ├── 04_appendix.md
│   ├── final_summary.md             # Complete design summary (all 14 steps)
│   ├── Data Description.pdf         # Original dataset documentation
│   └── Experiment Design Plan.pdf   # Original design plan
│
├── notebooks/                       # Jupyter notebooks (main deliverables)
│   ├── 01_data_preparation_and_eda.ipynb
│   ├── 02_experiment_design.ipynb
│   └── 03_appendix.ipynb
│
├── src/                             # Reusable Python modules
│   ├── __init__.py
│   ├── preprocessing.py             # Data loading & joining
│   ├── eligibility.py               # Eligibility filter logic
│   ├── metrics.py                   # Outcome metric construction
│   ├── variance.py                  # Variance estimation & winsorization
│   ├── aa_simulation.py             # A/A simulation framework
│   ├── power.py                     # Sample size & power calculations
│   ├── cuped.py                     # CUPED variance reduction
│   └── randomization.py             # Stratified randomization
│
├── outputs/
│   ├── figures/                     # Saved plots
│   ├── tables/                      # Saved summary tables
│   └── intermediate/                # Cached intermediate datasets
│
└── presentations/
    └── experiment_design_summary.md # Presentation-ready summary
```

---

## Experiment Design Summary

| Step | Decision |
|---|---|
| **1. Business Decision** | Will a coupon increase incremental spend enough to justify rollout? |
| **2. Eligible Population** | Active HHs with ≥2 trips, recency ≤90 days, ≥1 prior campaign contact |
| **3. Treatment / Control** | Category-specific coupon (direct mail) vs. business-as-usual; 4-week window |
| **4. Metrics** | **Primary:** 4-week total spend. **Secondary:** conversion rate, basket size, trips |
| **5a. Pre-Period Baselines** | Spend, frequency, promo responsiveness computed per household |
| **5b. Variance Validation** | 4-week rolling window σ; pre vs. post distribution confirmed stable |
| **5c. MDE Realism** | A/A simulation noise floor < MDE → experiment is feasible |
| **6. MDE** | **$14 per 4 weeks** ($3.50/week) — cost-justified break-even threshold |
| **7. Alpha / Power** | α = 0.05, Power = 0.80, two-sided Welch's t-test |
| **8. Sample Size** | Computed per arm using 4-week ITT σ; reduced ~35–45% via CUPED |
| **9. Allocation** | 50 / 50 treatment-control split |
| **10. Randomization** | Stratified by spend tier (4 levels) × recency band (4 levels), seed = 42 |
| **11. Duration** | 4 weeks, fixed horizon, no early stopping |
| **12. Quality Checks** | SRM, baseline balance (Welch's t, χ²), A/A simulation, duplicate check |
| **13. Analysis Plan** | Welch's t-test (primary), CUPED, ITT framework; Bonferroni for secondary |
| **14. Decision Rule** | Launch if p < 0.05 AND effect ≥ $14/4wk AND guardrails pass |

---

## Key Results

### Eligible Population
- **2,498 total households** in the dataset
- **Eligibility criteria applied:** ≥2 pre-period trips, recency ≤90 days, ≥1 campaign contact
- Eligible pool serves as the ITT analysis population (zero-spenders included as Y = 0)

### Pre-Period Baseline (Eligible Households)
| Metric | Value |
|---|---|
| Median avg weekly spend | ~$17–20 |
| Spend distribution | Right-skewed (skewness ≈ 1.4), heavy-tailed |
| Zero-spend rate in 4-week windows | ~8% |
| Pre-to-post spend correlation | r ≈ 0.81 (supports CUPED) |

### Power Analysis (4-Week Total Spend)
| Scenario | σ (4-wk) | MDE | n per arm | Feasible? |
|---|---|---|---|---|
| Raw | Full ITT σ | $14 | Computed | Check curves |
| Winsorized (1–99%) | Reduced σ | $14 | Reduced | More feasible |
| CUPED-adjusted | σ × √(1−ρ²) | $14 | ~35–45% lower | Most feasible |

### CUPED Variance Reduction
- Pre-to-post correlation: **ρ ≈ 0.81**
- Variance reduction: **~35% (1 − ρ²)**
- CUPED aligns granularity: Y = 4-week total spend, X = avg weekly spend × 4

### Quality Checks (Simulated)
| Check | Result |
|---|---|
| SRM test | p > 0.01 — ratio consistent with 50/50 |
| Baseline balance (Welch's t) | No significant covariate imbalance |
| A/A simulation FPR | ≈ 5% (correct type I error rate) |
| Duplicate households | None detected |

### Decision Rule
The campaign is recommended for **LAUNCH** if and only if:
1. Primary metric p-value < 0.05 (two-sided)
2. Point estimate ≥ $14/4wk AND lower 95% CI > $0
3. Guardrails pass: discount cost ≤ $3/HH, non-target spend decline < 5%

---

## Methodology

### 14-Step Experiment Design Framework

**Step 1 — Business Decision**
Define the economic question and the decision that depends on the experiment outcome. The coupon campaign must generate at least $14 incremental spend per household per 4-week window to break even.

**Step 2 — Eligibility Definition**
Filter households to those that are contactable and engaged: ≥2 pre-period trips, recency ≤90 days from end of pre-period, ≥1 historical campaign contact.

**Step 3 — Treatment & Control**
Treatment: category-specific coupons sent by direct mail. Control: business-as-usual (no mailing). Experiment window: 4 weeks.

**Step 4 — Metrics**
- **Primary:** 4-week total household spend (continuous, Welch's t-test)
- **Secondary:** conversion rate (binary), basket size ($/trip), total trips

**Steps 5a–5c — Baseline, Variance, Feasibility**
- 5a: Pre-period behavioral summary by spend tier and recency band
- 5b: 4-week rolling window variance estimation; confirmed σ stability and pre–post consistency
- 5c: Metric feasibility check (sparsity, skewness, Q-Q) + A/A simulation MDE realism

**Step 6 — MDE**
MDE = $14 / 4-week window (cost-based: 5 coupons × $1 × 20% redemption + $0.50 mailing = $1.50 break-even, moderate scenario = $14).

**Step 7 — Alpha & Power**
α = 0.05, Power = 0.80, two-sided (detect both positive and negative effects).

**Step 8 — Sample Size**
Using `n = 2σ²(z_{α/2} + z_β)² / δ²` with ITT σ from 4-week rolling windows. Power curves shown for raw σ, winsorized σ, and CUPED-adjusted σ.

**Step 9 — Allocation**
50/50 split — maximizes power for given total N at low treatment cost.

**Step 10 — Randomization**
Stratified randomization within spend tier × recency band strata (4×4 = 16 cells), ensuring balance on the strongest predictors of the outcome.

**Step 11 — Duration & Stopping Rules**
4-week fixed horizon. No interim analysis. No early stopping. Coupon validity = experiment window.

**Step 12 — Pre-Launch Quality Checks**
SRM test, baseline balance (Welch's t + χ² for categorical), A/A simulation, duplicate check.

**Step 13 — Analysis Plan (Pre-Registered)**
Welch's t-test on 4-week total spend (ITT). Optional CUPED adjustment. Winsorization at 1st/99th percentile. Zero-spend households included. Bonferroni correction for secondary metrics.

**Step 14 — Decision Rule**
Three-gate decision: statistical significance + practical significance (effect ≥ MDE + CI lower > 0) + guardrails.

### Statistical Methods
- **Welch's t-test:** Handles unequal variance between groups; robust for skewed distributions at n > 100
- **CUPED:** Reduces variance using correlated pre-period covariate; equivalent to OLS with pre-period covariate
- **Stratified randomization:** Ensures balance on spend tier and recency — the two strongest confounders
- **ITT framework:** All eligible households included regardless of actual coupon redemption; prevents selection bias
- **Winsorization:** Clips outliers at 1st/99th percentile; reduces influence of extreme spenders on variance

---

## How to Run

### Prerequisites
```bash
# Clone the repository
git clone https://github.com/<your-username>/ab-testing-experiment-design-complete-journey.git
cd ab-testing-experiment-design-complete-journey

# Install dependencies
pip install -r requirements.txt
```

### Data Setup
Download the dunnhumby "The Complete Journey" dataset and place all CSV files in `data/raw/`:
- [Download from Kaggle](https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey)
- Or from [dunnhumby Source Files](https://www.dunnhumby.com/source-files/)

### Run Notebooks (in order)
```bash
jupyter notebook
```

| Notebook | Description |
|---|---|
| `notebooks/01_data_preparation_and_eda.ipynb` | Data loading, feature engineering, EDA |
| `notebooks/02_experiment_design.ipynb` | Full 14-step experiment design |
| `notebooks/03_appendix.ipynb` | Supporting analyses (sample size tables, A/A simulation, subgroup preview, binary power) |

### Using the `src/` Modules
```python
from src.eligibility import filter_eligible_households
from src.power import sample_size_two_sample_ttest
from src.cuped import apply_cuped
from src.randomization import stratified_randomize

# Example: compute required sample size
n = sample_size_two_sample_ttest(sigma=85.0, delta=14.0, alpha=0.05, power=0.80)
print(f"Required n per arm: {n}")
```

---

## Requirements

| Package | Version |
|---|---|
| Python | ≥ 3.9 |
| pandas | ≥ 2.0 |
| numpy | ≥ 1.24 |
| scipy | ≥ 1.10 |
| statsmodels | ≥ 0.14 |
| matplotlib | ≥ 3.7 |
| seaborn | ≥ 0.12 |

Install all: `pip install -r requirements.txt`

---

## License

This project uses the dunnhumby "The Complete Journey" dataset for educational and research purposes. The dataset is provided by dunnhumby under their terms of use.

---

*Project developed as a portfolio exercise in A/B test experiment design and causal inference methodology.*
