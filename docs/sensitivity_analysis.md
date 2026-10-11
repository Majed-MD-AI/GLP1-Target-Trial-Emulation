# Sensitivity and Robustness Analyses

This stage evaluates how sensitive the **eligibility-aligned** synthetic target-trial findings are to alternative weighting choices, overlap restrictions, and an alternative exposure-window definition.

The canonical analysis cohort applies the protocol age criterion of 18–45 years:

- Source records: 2,000
- Eligible records: 1,987
- Early discontinuation: 876
- Late discontinuation: 1,111

## Analyses implemented

### 1. Primary IPTW

Primary causal contrast:
- Late discontinuation: 0–60 days before conception
- Early discontinuation: 61–180 days before conception

Adjusted result:
- Early risk: 14.34%
- Late risk: 19.83%
- Risk difference: 5.49 percentage points
- Risk ratio: 1.38

### 2. Stabilized IPTW

Stabilized weights use the marginal treatment probability in the numerator.

Result:
- Risk difference: 5.49 percentage points
- Risk ratio: 1.38
- Effective sample size increased from 1,832.0 to 1,868.7
- Maximum weight decreased from 6.12 to 2.70

This supports stability of the primary estimate under a numerically more stable weighting scheme.

### 3. Weight truncation

1st–99th percentile truncation:
- Risk difference: 5.68 percentage points
- Risk ratio: 1.40
- Maximum absolute weighted SMD: 0.015

5th–95th percentile truncation:
- Risk difference: 6.21 percentage points
- Risk ratio: 1.45
- Maximum absolute weighted SMD: 0.043

The treatment-effect estimate remains in the same direction across truncation strategies, although stronger truncation changes the magnitude.

### 4. Common-support restriction

Observed propensity-score common support:
- Lower bound: 0.340
- Upper bound: 0.837

Only 4 of 1,987 eligible patients were excluded.

Result after common-support restriction:
- Risk difference: 5.39 percentage points
- Risk ratio: 1.38
- Maximum absolute weighted SMD: 0.016

This indicates strong measured overlap in the synthetic cohort.

### 5. Alternative exposure window

Sensitivity definition:
- Late discontinuation: 0–30 days before conception
- Early discontinuation: 31–180 days before conception

The propensity-score model was re-estimated for this changed treatment definition.

Result:
- Early risk: 16.66%
- Late risk: 19.99%
- Risk difference: 3.33 percentage points
- Risk ratio: 1.20
- Maximum absolute weighted SMD: 0.010

This changes the treatment definition and therefore changes the causal contrast. It is a design sensitivity analysis rather than a re-estimation of the exact primary estimand.

## Interpretation

Across stabilized weighting, percentile truncation, and common-support restriction, the primary synthetic finding remains directionally consistent.

The alternative 30-day exposure definition yields a smaller effect estimate, illustrating a central pharmacoepidemiologic issue: estimates can depend on how exposure windows are defined.

## Scope limitation

These are methodological sensitivity analyses performed on synthetic data. They demonstrate robustness workflows and causal-design reasoning, not clinical evidence about GLP-1RA safety in pregnancy.
