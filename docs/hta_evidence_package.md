# HTA-Oriented Evidence Package

This document consolidates the project into a single evidence-generation summary.

The repository remains a **synthetic methodological demonstration**. It is intended to show how a target-trial question can be translated into a transparent causal RWE workflow with interoperability, robustness, and external-comparator extensions.

## 1. Primary target-trial analysis

Question:
Among pregnancies with preconception GLP-1RA exposure, what is the effect of early (61–180 days) versus late (0–60 days) discontinuation before conception on preterm birth?

Protocol eligibility:
- age 18–45 years
- documented pregnancy
- GLP-1RA exposure within 180 days before conception

Source cohort:
- 2,000 synthetic records

Eligibility-aligned analysis cohort:
- 1,987 records
- 876 early discontinuation
- 1,111 late discontinuation
- 13 records excluded for age outside 18–45

Primary IPTW-adjusted result:
- Early risk: 14.34%
- Late risk: 19.83%
- Risk difference: 5.49 percentage points
- RD 95% CI: 2.4 to 9.1 percentage points
- Risk ratio: 1.38
- RR 95% CI: 1.14 to 1.74

## 2. Confounding control and balance

Propensity-score covariates:
- age
- BMI
- diabetes
- hypertension
- smoking
- prior preterm birth

After IPTW, all measured baseline covariates had absolute SMD values well below 0.10.

This supports measured baseline comparability within the synthetic demonstration.

## 3. Sensitivity and robustness

Implemented checks:
- stabilized IPTW
- 1st–99th percentile weight truncation
- 5th–95th percentile weight truncation
- common-support restriction
- alternative exposure definition: 0–30 vs 31–180 days

Results remained directionally consistent under weighting and overlap checks.

The alternative exposure window yielded a smaller adjusted RR (~1.20), illustrating sensitivity to exposure-window definition.

## 4. External Control Arm extension

A separate synthetic external control source was generated.

Index treated arm:
- late discontinuation from the original cohort
- age eligibility enforced

External comparator:
- early discontinuation from a distinct synthetic database

ATT-style weighting reduced maximum absolute SMD from 0.347 to 0.038.

Main ECA result:
- Index treated risk: 21.15%
- Weighted external-control risk: 14.85%
- Risk difference: 6.30 percentage points
- RD 95% CI: 3.50 to 9.27
- Risk ratio: 1.42
- RR 95% CI: 1.21 to 1.69

## 5. Pregnancy medication-safety expansion

Additional synthetic pregnancy outcomes were added without changing the original primary question:

- preeclampsia
- small for gestational age
- large for gestational age
- congenital malformation

Each outcome was analyzed using the same eligibility-aligned propensity-score/IPTW framework with 300 bootstrap repetitions.

This broadens the project from a single-outcome demonstration into a pregnancy pharmacoepidemiology workflow.

## 6. OMOP-inspired interoperability layer

The project includes:
- PERSON
- OBSERVATION_PERIOD
- DRUG_EXPOSURE
- CONDITION_OCCURRENCE
- MEASUREMENT
- OBSERVATION

Study-specific derived variables remain outside the clinical-domain tables.

This layer is explicitly described as **OMOP-inspired**, not as a validated production OMOP CDM ETL.

Standard OHDSI vocabulary mapping has not been performed.

## 7. EHDS relevance

EHDS is not used as a data source in this repository.

The connection is methodological:
- transparent cohort definition
- standardized domain separation
- reproducible causal analysis
- cross-database interoperability concepts
- reusable evidence-generation logic

## 8. HTA relevance

The project now produces:
- explicit target-trial protocol
- eligibility audit
- absolute risks
- risk differences
- risk ratios
- confidence intervals
- balance diagnostics
- overlap diagnostics
- weighting diagnostics
- sensitivity analyses
- ECA comparison
- multi-outcome pregnancy-safety results
- standardized-data transformation
- documented assumptions and limitations

This is best described as **HTA-oriented evidence generation**, not regulatory-grade HTA submission evidence.

## 9. Key limitations

The project does not currently address:
- unmeasured confounding
- missing-data mechanisms
- outcome misclassification
- true longitudinal treatment adherence
- time-varying confounding
- calendar-time bias
- healthcare-system differences
- validated OMOP vocabulary mapping
- real registry/EHR data
- negative-control analyses
- quantitative bias analysis

## 10. Portfolio positioning

The project demonstrates practical experience with:

- target trial emulation
- pregnancy pharmacoepidemiology
- causal inference
- propensity scores
- IPTW
- covariate balance
- bootstrap uncertainty
- sensitivity analysis
- external control arms
- standardized RWE structure
- OMOP-inspired transformation
- HTA-oriented evidence generation

All numerical findings are synthetic and must not be interpreted as clinical evidence about GLP-1RA safety in pregnancy.
