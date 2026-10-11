# GLP-1 Target Trial Emulation

A reproducible real-world evidence project demonstrating how a hypothetical target trial can be emulated using synthetic longitudinal healthcare data.

The project focuses on causal inference, propensity-score weighting, cohort comparability, and HTA-oriented evidence generation, with methodological links to External Control Arms and OMOP/EHDS-compatible real-world data workflows.

---

## Research Question

Among individuals exposed to GLP-1 receptor agonists before pregnancy, what is the effect of early versus late preconception discontinuation on the risk of preterm birth?

---

## Target Trial Framework

The hypothetical target trial defines:

- Population: pregnancies with preconception GLP-1RA exposure
- Eligibility: age 18–45 years, documented pregnancy, GLP-1RA exposure within 180 days before conception
- Strategy A: early discontinuation, 61–180 days before conception
- Strategy B: late discontinuation, 0–60 days before conception
- Time zero: estimated date of conception
- Primary outcome: preterm birth
- Follow-up: conception to end of pregnancy
- Primary estimands: risk difference and risk ratio

The complete protocol is available in:

protocol/target_trial_protocol.md

---

## Data

This project uses a synthetic cohort of 2,000 patients.

Baseline variables include:

- Age
- BMI
- Diabetes
- Hypertension
- Smoking
- Prior preterm birth

Treatment assignment and outcomes were generated with deliberate confounding so that causal-adjustment methods could be demonstrated.

No real patient data are used.

The synthetic dataset is available in:

data/synthetic_glp1_pregnancy.csv

---

## Causal Inference Workflow

The analysis follows this sequence:

1. Define the hypothetical target trial
2. Generate synthetic longitudinal real-world data
3. Define treatment strategies
4. Assess baseline imbalance
5. Estimate propensity scores
6. Calculate inverse probability of treatment weights (IPTW)
7. Reassess covariate balance
8. Estimate weighted treatment effects
9. Quantify uncertainty using bootstrap confidence intervals
10. Present results in an HTA-oriented format

---

## Propensity Score and IPTW

A logistic regression model estimates each patient's probability of late discontinuation based on baseline characteristics.

Inverse probability of treatment weighting is then used to construct a weighted pseudo-population in which measured baseline characteristics are more comparable between treatment groups.

Covariate balance is assessed using standardized mean differences (SMD).

A commonly used balance threshold is:

|SMD| < 0.10

---

## Balance Results

Before IPTW, important baseline imbalances were present.

Examples:

- Diabetes: SMD = 0.403
- BMI: SMD = 0.157
- Hypertension: SMD = 0.125
- Prior preterm birth: SMD = 0.147

After IPTW, all measured baseline covariates had absolute SMD values well below 0.10.

This demonstrates successful balance of the measured confounders in the synthetic cohort.

---

## Treatment Effect Results

### Crude Analysis

- Early discontinuation risk: 12.68%
- Late discontinuation risk: 21.22%
- Risk difference: 8.53 percentage points
- Risk ratio: 1.67

### IPTW-Adjusted Analysis

- Early discontinuation risk: 14.29%
- Late discontinuation risk: 19.88%
- Risk difference: 5.58 percentage points
- 95% CI: 2.5 to 9.0 percentage points
- Risk ratio: 1.39
- 95% CI: 1.15 to 1.71

The reduction from the crude RR of 1.67 to the IPTW-adjusted RR of 1.39 illustrates how baseline confounding can exaggerate an observational association.

These results are generated from synthetic data and must not be interpreted as clinical evidence regarding GLP-1 receptor agonists.

---

## External Control Arm Relevance

Although this project is not itself a clinical-trial external control arm, it demonstrates several principles directly relevant to ECA development:
- Explicit eligibility criteria
- Alignment of time zero
- Transparent cohort construction
- Baseline comparability
- Propensity-score adjustment
- Balance diagnostics
- Treatment-effect estimation
- Sensitivity to residual confounding

These principles are important when constructing real-world comparison cohorts for single-arm or externally controlled clinical studies.

---

## OMOP and EHDS Relevance

An OMOP-inspired transformation layer is now included in the repository.

The transformation decomposes the flat synthetic cohort into domain-specific tables representing:

- PERSON
- OBSERVATION_PERIOD
- DRUG_EXPOSURE
- CONDITION_OCCURRENCE
- MEASUREMENT
- OBSERVATION

Study-specific derived variables such as treatment strategy, propensity score, and IPTW remain in a separate analysis cohort table.

The transformation is implemented in:

`scripts/02_omop_transformation.py`

The source-to-domain mapping and scope limitations are documented in:

`docs/omop_mapping.md`

This is an **OMOP-inspired educational transformation**, not a validated production OMOP CDM ETL. Standard OHDSI vocabulary mapping has not yet been performed, and concept IDs remain placeholders.

The EHDS connection remains methodological rather than an implemented data source: the project demonstrates transparent, interoperable RWE design principles that could support cross-database European evidence generation.

---

## HTA Evidence Generation

The project emphasizes outputs that are useful in comparative-effectiveness and Health Technology Assessment workflows, including:

- Absolute risks
- Risk differences
- Risk ratios
- Confidence intervals
- Covariate balance diagnostics
- Explicit causal estimands
- Transparent assumptions
- Reproducible cohort definitions
- Sensitivity analyses

The broader objective is to demonstrate how real-world data can be transformed into structured evidence suitable for downstream evidence synthesis and HTA-oriented decision support.

---

## Repository Structure

```text
GLP1-Target-Trial-Emulation/
│
├── README.md
├── protocol/
│   └── target_trial_protocol.md
│
├── data/
│   └── synthetic_glp1_pregnancy.csv
│
├── notebooks/
│   └── 01_generate_synthetic_data.ipynb
│
├── results/
│   └── hta_results_summary.csv
├── docs/
│   └── omop_mapping.md
├── scripts/
│   └── 02_omop_transformation.py
└── figures/
    ├── love_plot.svg
    ├── propensity_overlap.svg
    ├── iptw_distribution.svg
    └── effect_estimates.svg
```

---

## Current Status

### Completed

- Target trial protocol
- Synthetic cohort generation
- Confounding simulation
- Propensity-score estimation
- Inverse probability of treatment weighting (IPTW)
- Covariate balance assessment
- Crude and adjusted treatment-effect estimation
- Bootstrap confidence intervals
- HTA-style results summary
- OMOP-inspired source-to-domain mapping
- Reproducible OMOP-inspired transformation script
- Covariate-balance Love plot
- Propensity-score overlap figure
- IPTW weight-distribution figure
- Crude vs IPTW-adjusted effect-estimate figure

### Planned Extensions

- External Control Arm demonstration
- Sensitivity and robustness analyses
- Additional pregnancy outcomes
- Expanded HTA-oriented evidence outputs
- Optional validated OHDSI vocabulary mapping

---

## Disclaimer

This repository is an educational and methodological demonstration.

All patient-level data are synthetic.

The numerical results are not intended to provide clinical guidance or make claims about the safety or effectiveness of GLP-1 receptor agonists in pregnancy.
