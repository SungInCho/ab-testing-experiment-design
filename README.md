# A/B Test Experiment Design — dunnhumby The Complete Journey

A rigorous, pre-registered A/B test experiment design for a household-level coupon campaign, built on the [dunnhumby "The Complete Journey"](https://www.dunnhumby.com/source-files/) dataset. This project follows a structured 14-step experiment design framework and demonstrates best practices in causal inference, power analysis, variance reduction (CUPED), and statistical testing.

---

## Business Question

> *"Will sending household-level promotional coupons to eligible frequent shoppers increase their 4-week total spend by at least $14 — enough to justify full-scale campaign rollout?"*

---

## Repository Structure

```
ab-testing-experiment-design/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md                    # Data dictionary and field descriptions
│   └── raw/                         # Raw CSV files (not tracked in Git)
│
├── docs/                            # Written documentation
│   ├── 01_data_preparation.md       # Data loading, joining, and feature engineering
│   ├── 02_exploratory_data_analysis.md  # EDA findings and distribution analysis
│   ├── 03_ab_test_experiment_design.md  # Full 14-step experiment design
│   ├── 04_appendix.md               # Supporting analyses (power tables, subgroups, binary outcomes)
│   ├── final_summary.md             # End-to-end project summary with key results
│   └── Data Description.pdf         # Original dataset documentation
│
├── notebooks/                       # Jupyter notebooks (main deliverables)
│   ├── 01_data_preparation_and_eda.ipynb
│   ├── 02_experiment_design.ipynb
│   └── 03_appendix.ipynb
│
├── src/                             # Reusable Python modules
│   ├── preprocessing.py             # Data loading and joining
│   ├── eligibility.py               # Eligibility filter logic
│   ├── metrics.py                   # Outcome metric construction
│   ├── variance.py                  # Variance estimation and winsorization
│   ├── aa_simulation.py             # A/A simulation framework
│   ├── power.py                     # Sample size and power calculations
│   ├── cuped.py                     # CUPED variance reduction
│   └── randomization.py             # Stratified randomization
│
└── outputs/
    ├── figures/                     # Saved plots
    ├── tables/                      # Saved summary tables
    └── intermediate/                # Cached intermediate datasets
```

---

## Dataset

**Source:** dunnhumby — The Complete Journey
**Scale:** ~2,500 households × 102 weeks (~2 years) of grocery transactions, ~2.6M line-item records

| File | Description |
|---|---|
| `transaction_data.csv` | Line-item receipts (household × basket × product) |
| `hh_demographic.csv` | Demographics for a subset of households |
| `campaign_table.csv` | Household campaign participation history |
| `campaign_desc.csv` | Campaign type and week range metadata |
| `coupon.csv` | Coupon-to-product mappings |
| `coupon_redempt.csv` | Coupon redemption events |
| `product.csv` | Product master with department and brand |
| `causal_data.csv` | Weekly display and mailer flags by product/store |
| `hh_features.csv` | Engineered household-level feature table (output of Notebook 1) |

> Raw data files are not tracked in Git. Place them in `data/raw/` before running notebooks.

---

## Notebooks

| Notebook | Description |
|---|---|
| `01_data_preparation_and_eda.ipynb` | Load and join 8 raw tables; engineer household-level features; EDA of spend, frequency, recency, and promotion behavior |
| `02_experiment_design.ipynb` | Full 14-step experiment design: eligibility, baselines, variance estimation, power analysis, randomization, pre-launch checks, pre-registered analysis plan |
| `03_appendix.ipynb` | Stratum-level baseline summary, sample size sensitivity table, pre-registration template, subgroup preview, binary outcome power analysis |

---

## 14-Step Design Summary

| Step | Decision |
|---|---|
| 1. Business decision | Coupon campaign ROI test — requires ≥$14 incremental spend per HH per 4 weeks |
| 2. Eligible population | ≥2 pre-period trips, recency ≤90 days, ≥1 campaign contact → **1,288 households** |
| 3. Treatment / Control | Category coupons (direct mail) vs. business-as-usual; 4-week window |
| 4. Metrics | **Primary:** 4-week total spend (ITT). **Secondary:** conversion, basket size, trips |
| 5a. Baselines | Right-skewed spend, low coupon usage; spend tier and recency band validated as stratifiers |
| 5b. Variance | σ_raw=$188.81, σ_win=$183.18, σ_CUPED=$138.01; ρ=0.682 pre-post correlation |
| 5c. MDE realism | A/A noise floor ~$6–8 < $14 MDE → metric is sufficiently sensitive |
| 6. MDE | **$14.00 per 4 weeks** ($3.50/week) — cost-justified break-even threshold |
| 7. Alpha / Power | α = 0.05, Power = 0.80, two-sided Welch's t-test |
| 8. Sample size | MDE=$14 requires ~3,052 households with CUPED (1,288 available); min feasible MDE ≈ $24 |
| 9. Allocation | 50% Treatment / 50% Control (644 per arm) |
| 10. Randomization | Stratified: spend tier (4) × recency band (4) = 16 cells; seed = 42 |
| 11. Duration | 4 weeks fixed horizon; no early stopping |
| 12. Quality checks | SRM ✓, covariate balance ✓, A/A FPR≈5% ✓, no duplicates ✓ |
| 13. Analysis plan | Welch's t-test (primary), CUPED adjustment, ITT, Bonferroni for secondary |
| 14. Decision rule | Launch: p < 0.05 AND effect ≥ $14 AND guardrails pass |

---

## Key Results

### Eligible Population

- **Total households:** 2,498
- **Eligible (ITT population):** 1,288 (3 eligibility criteria applied)
- **Treatment / Control:** 644 / 644 (stratified 50/50 split)

### Variance and CUPED

| Scenario | σ (4-week) | Notes |
|---|---|---|
| Raw ITT | $188.81 | Full distribution, zeros included |
| Winsorized (1–99%) | $183.18 | Outliers clipped |
| CUPED-adjusted | $138.01 | ρ = 0.682; 53.5% variance reduction |

### Power Analysis (MDE = $14, Power = 80%)

| Variance Scenario | n per arm | n total | Feasible? |
|---|---|---|---|
| Raw | ~2,856 | ~5,712 | No |
| Winsorized | ~2,684 | ~5,368 | No |
| CUPED | ~1,526 | ~3,052 | **No** |

**Minimum feasible MDE at 80% power (CUPED):** ~$24 per 4-week window (n_total ≈ 1,040)

### Pre-Launch Quality Checks

| Check | Result |
|---|---|
| Sample ratio mismatch | PASS (p > 0.01) |
| Baseline covariate balance | PASS (no significant imbalances) |
| A/A simulation FPR | PASS (~5%, matches α) |
| Duplicate households | PASS (0 duplicates) |

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Download data

Download the dunnhumby "The Complete Journey" dataset and place all CSV files in `data/raw/`:
- [Kaggle](https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey)
- [dunnhumby Source Files](https://www.dunnhumby.com/source-files/)

### 3. Run notebooks in order

```bash
jupyter notebook
```

Run `01` → `02` → `03`. Notebook 1 outputs `hh_features.csv`, which is required by Notebooks 2 and 3.

### 4. Using `src/` modules directly

```python
from src.power import sample_size_two_sample_ttest
from src.cuped import apply_cuped
from src.randomization import stratified_randomize

# Required sample size per arm
n = sample_size_two_sample_ttest(sigma=138.01, delta=14.0, alpha=0.05, power=0.80)
print(f"n per arm (CUPED): {n}")  # ~1,526

# Apply CUPED adjustment
cuped_outcomes = apply_cuped(y_post, x_pre)

# Stratified randomization
assignments = stratified_randomize(df, strata_cols=['spend_tier', 'recency_band'], seed=42)
```

---

## Statistical Methods

| Method | Purpose |
|---|---|
| **Welch's t-test** | Primary hypothesis test; handles unequal variance; robust at n > 100 by CLT |
| **CUPED** | Variance reduction using correlated pre-period covariate; reduces σ by ~27%, sample size by ~46% |
| **Stratified randomization** | Ensures balance on spend tier and recency — the two strongest confounders |
| **ITT framework** | All eligible households included regardless of coupon redemption; prevents selection bias |
| **Winsorization** | Clips 1st/99th percentile outliers; reduces influence of extreme spenders on variance |

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
| jupyter | ≥ 1.0 |

---

## License

This project uses the dunnhumby "The Complete Journey" dataset for educational and research purposes under dunnhumby's terms of use.

---

*Portfolio project demonstrating A/B test experiment design and causal inference methodology.*
