# Target Trial Protocol

## Research Question

Among individuals exposed to GLP-1 receptor agonists before pregnancy, what is the effect of different preconception discontinuation strategies on pregnancy outcomes?

## Why a Target Trial?

Randomized trials of medication exposure around pregnancy are often difficult or unethical to conduct.

Target trial emulation provides a framework for using observational longitudinal healthcare data to mimic the design principles of a randomized controlled trial.

The goal is not to reproduce randomization, but to explicitly define:

- Eligibility criteria
- Treatment strategies
- Time zero
- Follow-up
- Outcomes
- Causal estimand
- Analysis plan

## Eligibility Criteria

Participants must:

- Have a recorded pregnancy
- Be aged 18–45 years at conception
- Have evidence of GLP-1 receptor agonist exposure within 180 days before conception
- Have sufficient baseline medical history before conception to measure relevant confounders

## Treatment Strategies

The primary analysis will compare two preconception GLP-1RA discontinuation strategies:

### Strategy A: Early Discontinuation

Last documented GLP-1RA exposure occurred 61–180 days before conception.

### Strategy B: Late Discontinuation

Last documented GLP-1RA exposure occurred 0–60 days before conception.

Additional discontinuation windows may be evaluated in sensitivity analyses.

## Time Zero

Time zero is the estimated date of conception.

Eligibility and treatment strategy classification are determined using information available before or at time zero.

Follow-up begins at conception and continues until the end of pregnancy or occurrence of the outcome of interest.

## Follow-up

Follow-up begins at the estimated date of conception and continues until the end of pregnancy.

Participants will be followed until:

- Delivery
- Pregnancy loss
- End of available observation

## Outcomes

### Primary Outcome

Preterm birth, defined as delivery before 37 completed weeks of gestation.

### Secondary Outcomes

Potential secondary outcomes include:

- Preeclampsia
- Small for gestational age
- Large for gestational age
- Congenital malformations

## Causal Estimand

The primary estimand is the effect of early versus late preconception GLP-1RA discontinuation on the risk of preterm birth among eligible pregnancies.

Treatment effects will primarily be expressed using:

- Risk difference
- Risk ratio

## Baseline Confounders

Potential baseline confounders will be measured before or at time zero.

These may include:

- Maternal age
- Body mass index
- Diabetes status and severity
- Hypertension
- Prior pregnancy history
- Smoking status
- Indication for GLP-1 receptor agonist treatment
- Concomitant medications
- Baseline comorbidity burden

These variables are selected because they may influence both treatment strategy selection and pregnancy outcomes.

## Confounding Control

The primary analysis will use propensity-score methods to improve comparability between treatment strategy groups.

The planned approach is:

1. Estimate the probability of receiving the observed treatment strategy using baseline covariates
2. Calculate inverse probability of treatment weights
3. Assess covariate balance after weighting
4. Estimate weighted risks of the primary outcome
5. Calculate risk differences and risk ratios

Sensitivity analyses may use alternative adjustment strategies such as regression adjustment or propensity-score matching.

## Analysis Principle

The analysis follows a causal-inference framework.

Only variables measured before or at time zero are considered for baseline confounding adjustment.

Post-treatment variables are not adjusted for unless explicitly required by the estimand.

This preserves the temporal ordering of eligibility, treatment assignment, confounder measurement, and outcome assessment defined by the target trial.

## Relevance to External Control Arms

The principles used in this target trial emulation are directly relevant to external control arm design.

An external control arm uses real-world data to construct a comparison group for a treated population, often when a randomized concurrent control group is unavailable or limited.

Key principles shared with target trial emulation include:

- Clear eligibility criteria
- Alignment of time zero
- Comparable baseline characteristics
- Control of confounding
- Transparent cohort construction
- Sensitivity analyses for residual bias

## OMOP and EHDS Relevance

The project will use an OMOP-inspired structure for key clinical variables and cohort definitions.

This supports the broader goal of reproducible and interoperable real-world evidence generation across healthcare databases.

In a real European data environment, standardized data models such as OMOP may facilitate multi-database analyses and evidence generation within the broader European Health Data Space ecosystem.

## HTA Evidence Generation

The final outputs will focus on treatment-effect measures that are relevant to health technology assessment.

These include:

- Absolute risks
- Risk differences
- Risk ratios
- Confidence intervals
- Covariate balance diagnostics
- Sensitivity analyses
- Transparent reporting of assumptions and limitations

The goal is to demonstrate how real-world data can be transformed into structured causal evidence that may support comparative-effectiveness and HTA decision-making.
