# Pregnancy Medication-Safety Outcome Expansion

This stage extends the original target-trial analysis to additional pregnancy outcomes already prespecified in the protocol.

The original primary outcome remains **preterm birth**. The project goal has not changed.

## Secondary outcomes added

- Preeclampsia
- Small for gestational age (SGA)
- Large for gestational age (LGA)
- Congenital malformation

These outcomes are generated synthetically and are included only to demonstrate a broader pregnancy pharmacoepidemiology workflow.

## Analysis design

The analysis:

1. merges the synthetic secondary-outcome file with the original cohort
2. enforces the protocol age eligibility criterion of 18–45 years
3. re-estimates the propensity score in the eligible cohort
4. applies IPTW
5. reports crude and adjusted absolute risks
6. reports adjusted risk differences and risk ratios
7. estimates 95% confidence intervals using 300 bootstrap repetitions with propensity-score re-estimation

Eligible analysis cohort:

- Total: 1,987
- Early discontinuation: 876
- Late discontinuation: 1,111

## Results

### Preeclampsia

Adjusted:
- Early risk: 10.54%
- Late risk: 13.30%
- Risk difference: 2.76 percentage points
- 95% CI: -0.18 to 5.74
- Risk ratio: 1.26
- 95% CI: 0.99 to 1.62

### Small for gestational age

Adjusted:
- Early risk: 10.11%
- Late risk: 9.25%
- Risk difference: -0.86 percentage points
- 95% CI: -3.11 to 2.31
- Risk ratio: 0.91
- 95% CI: 0.74 to 1.28

### Large for gestational age

Adjusted:
- Early risk: 11.54%
- Late risk: 12.30%
- Risk difference: 0.75 percentage points
- 95% CI: -2.17 to 3.57
- Risk ratio: 1.07
- 95% CI: 0.83 to 1.37

### Congenital malformation

Adjusted:
- Early risk: 3.42%
- Late risk: 2.97%
- Risk difference: -0.45 percentage points
- 95% CI: -2.16 to 1.30
- Risk ratio: 0.87
- 95% CI: 0.52 to 1.48

## Interpretation

The purpose of this stage is methodological.

It shows how the same target-trial and causal-adjustment framework can be extended to multiple maternal and fetal outcomes without changing the primary study question.

It also illustrates that different pregnancy outcomes can show different effect patterns and different levels of statistical uncertainty.

## Important limitation

All secondary outcomes are synthetic.

These numerical results are not clinical evidence and must not be interpreted as claims about GLP-1RA safety in pregnancy.
