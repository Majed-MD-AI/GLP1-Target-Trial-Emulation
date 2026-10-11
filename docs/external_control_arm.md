# External Control Arm Demonstration

This extension demonstrates how the target-trial framework can be adapted to an **External Control Arm (ECA)** design using a separate synthetic external data source.

## Design

### Index treated arm
The treated index cohort is drawn from the original target-trial dataset and consists of patients with:

- age 18–45 years
- late GLP-1RA discontinuation, defined as 0–60 days before conception

### External control arm
A separate synthetic external database was generated with:

- age 18–45 years
- early GLP-1RA discontinuation, defined as 61–180 days before conception
- the same baseline covariates and outcome structure as the target-trial demonstration
- intentionally different baseline covariate distribution to create a realistic comparability problem

The external cohort is stored in:

`data/synthetic_external_control.csv`

## Eligibility alignment

The original protocol specified age 18–45 years. The original synthetic target-trial dataset contains 13 records outside this range because age was generated from an unconstrained normal distribution.

The ECA analysis therefore explicitly enforces the stated age eligibility criterion before constructing the index treated arm.

This is a methodological correction for the ECA extension and is documented rather than hidden.

## Comparability model

A logistic model estimates the probability of belonging to the **index treated cohort** versus the **external control source**, conditional on:

- age
- BMI
- diabetes
- hypertension
- smoking
- prior preterm birth

The external controls are then weighted using ATT-style odds weights:

- index treated patients: weight = 1
- external controls: weight = p(index treated) / (1 - p(index treated))

This reweights the external controls toward the baseline characteristics of the treated index cohort.

## Covariate balance

Maximum absolute SMD before weighting:

**0.347**

Maximum absolute SMD after ATT weighting:

**0.038**

All measured baseline covariates were below |SMD| = 0.10 after weighting.

The largest pre-weighting imbalance was diabetes:

- SMD before: 0.347
- SMD after: -0.038

## Main ECA estimate

After ATT weighting:

- Index treated N: 1,111
- External control N: 1,500
- Index treated preterm-birth risk: 21.15%
- Weighted external-control risk: 14.85%
- Risk difference: 6.30 percentage points
- 95% bootstrap CI for RD: 3.50 to 9.27 percentage points
- Risk ratio: 1.42
- 95% bootstrap CI for RR: 1.21 to 1.69

Bootstrap uncertainty was estimated using 300 stratified resamples, re-estimating the membership model within each bootstrap sample.

## Common-support restriction

Common propensity-score support:

- lower bound: 0.180
- upper bound: 0.760

Excluded:

- 3 treated index patients
- 12 external controls

Common-support result:

- Risk difference: 6.15 percentage points
- Risk ratio: 1.41

This is consistent with the main ATT-weighted ECA estimate.

## Interpretation

The purpose of this analysis is not to claim that the synthetic external cohort is a valid clinical comparator.

The purpose is to demonstrate the methodological workflow required for an ECA:

1. define the target population and treatment strategy
2. align eligibility criteria
3. define a separate external data source
4. assess baseline comparability
5. model source/treatment membership
6. reweight the external control arm
7. reassess covariate balance
8. estimate the comparative outcome effect
9. quantify uncertainty
10. assess common support

## Important limitations

This remains a synthetic methodological demonstration.

It does not address all real-world ECA challenges, including:

- unmeasured confounding
- differences in data provenance
- calendar-time bias
- outcome ascertainment differences
- immortal-time bias
- informative loss to follow-up
- missing-data mechanisms
- differences in healthcare systems or coding practices
- transportability beyond measured baseline covariates

Therefore the result must not be interpreted as clinical evidence regarding GLP-1RA safety in pregnancy.
