# Sensitivity and Robustness Analyses

This stage evaluates how sensitive the synthetic target-trial findings are to alternative weighting choices, overlap restrictions, and an alternative exposure-window definition.

## Analyses implemented

### 1. Primary IPTW
Original causal contrast:
- Late discontinuation: 0–60 days before conception
- Early discontinuation: 61–180 days before conception

Adjusted result:
- Early risk: 14.29%
- Late risk: 19.88%
- Risk difference: 5.58 percentage points
- Risk ratio: 1.39

### 2. Stabilized IPTW
Stabilized weights use the marginal treatment probability in the numerator.

Result:
- Risk difference: 5.58 percentage points
- Risk ratio: 1.39
- Effective sample size increased from 1846.7 to 1882.5
- Maximum weight decreased from 5.89 to 2.60

This supports the stability of the primary estimate under a numerically more stable weighting scheme.

### 3. Weight truncation

1st–99th percentile truncation:
- Risk difference: 5.77 percentage points
- Risk ratio: 1.41
- Maximum absolute weighted SMD: 0.014

5th–95th percentile truncation:
- Risk difference: 6.27 percentage points
- Risk ratio: 1.46
- Maximum absolute weighted SMD: 0.041

The treatment-effect estimate remains in the same direction across truncation strategies, although stronger truncation changes the magnitude somewhat.

### 4. Common-support restriction

Observed propensity-score common support:
- Lower bound: 0.340
- Upper bound: 0.830

Only 4 of 2,000 patients were excluded.

Result after common-support restriction:
- Risk difference: 5.49 percentage points
- Risk ratio: 1.38
- Maximum absolute weighted SMD: 0.015

This indicates strong overlap in the synthetic cohort.

### 5. Alternative exposure window

Sensitivity definition:
- Late discontinuation: 0–30 days before conception
- Early discontinuation: 31–180 days before conception

The propensity-score model was re-estimated for this new treatment definition.

Result:
- Early risk: 16.67%
- Late risk: 20.08%
- Risk difference: 3.41 percentage points
- Risk ratio: 1.20
- Maximum absolute weighted SMD: 0.010

This analysis changes the treatment definition and therefore changes the causal contrast. It should not be interpreted as a direct re-estimation of the exact primary estimand.

## Interpretation

Across stabilized weighting, percentile truncation, and common-support restriction, the primary synthetic finding remains directionally consistent.

The alternative 30-day exposure definition yields a smaller effect estimate, illustrating an important pharmacoepidemiologic point: conclusions can depend on how exposure windows are defined.

## Scope limitation

These are methodological sensitivity analyses performed on synthetic data. They demonstrate robustness workflows and causal-design reasoning, not clinical evidence about GLP-1RA safety in pregnancy.
