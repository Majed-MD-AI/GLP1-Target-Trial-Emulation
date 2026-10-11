# Portfolio and Application Handoff

## Project

**GLP-1 Target Trial Emulation — Pregnancy Pharmacoepidemiology / Causal RWE**

Repository:
https://github.com/Majed-MD-AI/GLP1-Target-Trial-Emulation

## One-line description

A reproducible synthetic real-world evidence project that emulates a pregnancy medication-safety target trial, applies propensity-score/IPTW causal adjustment, evaluates robustness and overlap, demonstrates a synthetic External Control Arm workflow, and adds an OMOP-inspired interoperability layer with HTA-oriented evidence outputs.

## What is actually implemented

- Explicit target-trial protocol
- Eligibility-aligned analysis cohort
- Synthetic longitudinal pregnancy/RWE data
- Deliberately confounded treatment assignment and outcome generation
- Propensity-score estimation
- Inverse probability of treatment weighting (IPTW)
- Standardized mean difference balance assessment
- Crude and adjusted risk difference/risk ratio estimation
- Bootstrap confidence intervals with propensity-score re-estimation
- Stabilized and truncated-weight sensitivity analyses
- Common-support assessment
- Alternative exposure-window sensitivity analysis
- Synthetic External Control Arm with ATT-style weighting
- ECA balance and common-support diagnostics
- Synthetic secondary pregnancy outcomes
- OMOP-inspired source-to-domain transformation
- Generated domain tables plus validation checks
- HTA-oriented integrated evidence summary
- Publication-style causal diagnostic figures

## Canonical primary result

Eligibility:
- 2,000 source records
- 1,987 eligible after applying age 18–45 years
- 876 early discontinuation
- 1,111 late discontinuation

Primary IPTW-adjusted preterm-birth result:
- Early risk: 14.34%
- Late risk: 19.83%
- Risk difference: 5.49 percentage points
- 95% CI: 2.4 to 9.1 percentage points
- Risk ratio: 1.38
- 95% CI: 1.14 to 1.74

These are synthetic methodological results, not clinical evidence.

## Suggested CV wording

**GLP-1 Target Trial Emulation — Pregnancy Pharmacoepidemiology / Causal RWE | GitHub project**

- Designed and implemented a synthetic target-trial emulation of preconception GLP-1RA discontinuation and pregnancy outcomes using propensity scores, IPTW, covariate-balance diagnostics, and bootstrap uncertainty estimation.
- Extended the analysis with stabilized/truncated weighting, overlap diagnostics, alternative exposure windows, and a synthetic External Control Arm using ATT-style reweighting.
- Built an OMOP-inspired data transformation layer and HTA-oriented evidence package, with additional synthetic maternal/fetal outcomes for pregnancy medication-safety research.

## Short motivation-letter wording

To strengthen my preparation for causal pharmacoepidemiology, I developed a reproducible target-trial emulation project focused on medication exposure around pregnancy. I defined eligibility, treatment strategies, time zero and estimands; generated a deliberately confounded synthetic cohort; applied propensity-score weighting and balance diagnostics; quantified uncertainty with bootstrap resampling; and tested robustness using alternative weighting, overlap restrictions and exposure definitions. I then extended the pipeline to a synthetic External Control Arm and an OMOP-inspired data structure, while adding maternal and fetal outcomes relevant to medication-safety research. The project is explicitly methodological and uses no real patient data.

## Aarhus medication-safety relevance

The strongest alignment is methodological rather than topic-copying:

- pregnancy medication safety
- observational/registry-style research
- target-trial thinking
- confounding by indication and baseline risk
- causal inference
- propensity-score methods
- outcome-specific uncertainty
- reproducible cohort construction
- external comparator methodology
- standardized RWE workflows

The original GLP-1 question should remain unchanged. The project should be presented as evidence that the same methods can transfer to other medication-safety questions in pregnancy.

## Skills demonstrated

Python; pandas; NumPy; scikit-learn; causal inference; target trial emulation; pharmacoepidemiology; propensity scores; IPTW; SMD balance diagnostics; bootstrap confidence intervals; sensitivity analysis; overlap/common support; External Control Arms; ATT weighting; pregnancy medication safety; OMOP-inspired data modeling; RWE; HTA-oriented evidence generation.

## Important claims to avoid

Do not say:
- that the project used real Danish registry data
- that it is a validated OMOP CDM implementation
- that EHDS data were accessed
- that it is regulatory-grade HTA evidence
- that the synthetic GLP-1 estimates are clinical safety findings

Safe wording:
- synthetic RWE demonstration
- OMOP-inspired transformation
- EHDS-relevant interoperability framing
- HTA-oriented evidence generation
- ECA methodological demonstration
