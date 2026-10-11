# Changelog

## v1.0.0 — Portfolio baseline

### Target-trial core
- Defined eligibility, treatment strategies, time zero, follow-up, outcomes, estimands, and baseline confounders.
- Added eligibility-aligned canonical analysis (18–45 years).
- Added propensity-score estimation, IPTW, balance diagnostics, RD/RR estimation, and bootstrap confidence intervals.

### Robustness
- Added stabilized IPTW.
- Added 1st–99th and 5th–95th percentile weight truncation.
- Added common-support restriction.
- Added alternative 0–30 vs 31–180 day exposure-window analysis.

### External Control Arm
- Added a separate synthetic external-control cohort.
- Added index-vs-external membership propensity modeling and ATT-style external-control weighting.
- Added ECA balance, overlap, effect estimates, bootstrap uncertainty, and common-support analysis.

### Pregnancy medication safety
- Added synthetic preeclampsia, SGA, LGA, and congenital-malformation outcomes.
- Added outcome-specific IPTW analyses and bootstrap uncertainty.

### Interoperability and evidence packaging
- Added OMOP-inspired PERSON, OBSERVATION_PERIOD, DRUG_EXPOSURE, CONDITION_OCCURRENCE, MEASUREMENT, and OBSERVATION outputs.
- Added source-to-domain mapping, validation checks, EHDS-relevant framing, and an HTA-oriented evidence package.
- Added portfolio/application handoff documentation and publication-style figures.

### Scope
All patient-level data and numerical findings are synthetic and methodological. This release is a portfolio baseline, not clinical or regulatory evidence.
