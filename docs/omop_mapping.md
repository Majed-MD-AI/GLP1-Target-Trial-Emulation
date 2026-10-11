# OMOP-Inspired Mapping

This project includes an **OMOP-inspired** transformation layer for the synthetic GLP-1 pregnancy cohort.

It is designed to demonstrate how a flat analytical dataset can be decomposed into domain-specific longitudinal healthcare tables. It is **not** a validated production OMOP CDM ETL, and it does not claim conformance to an OHDSI vocabulary release.

## Why this layer exists

The original synthetic dataset stores demographic, exposure, condition, measurement, behavioral, and analysis variables in one flat table. In interoperable RWE workflows, these concepts are usually separated by domain so that cohort definitions and analyses can be reproduced across databases.

## Source-to-domain mapping

| Source variable | OMOP-inspired destination | Rationale |
| --- | --- | --- |
| `patient_id` | `PERSON.person_id` | Stable patient identifier |
| `age` | approximate `PERSON.year_of_birth` | Age is converted to an approximate year of birth for the synthetic demonstration |
| `days_before_conception` + `treatment_strategy` | `DRUG_EXPOSURE` | Encodes the synthetic last GLP-1RA exposure event before conception |
| `diabetes` | `CONDITION_OCCURRENCE` | Baseline clinical condition |
| `hypertension` | `CONDITION_OCCURRENCE` | Baseline clinical condition |
| `prior_preterm_birth` | `CONDITION_OCCURRENCE` | Baseline obstetric history |
| `preterm_birth` | `CONDITION_OCCURRENCE` | Primary study outcome |
| `bmi` | `MEASUREMENT` | Numeric clinical measurement |
| `smoking` | `OBSERVATION` | Behavioral observation |
| synthetic observation window | `OBSERVATION_PERIOD` | Defines the period with assumed data availability |
| `propensity_score`, `iptw`, study arm | `analysis_cohort.csv` | Derived analytical variables are kept outside the OMOP clinical-domain tables |

## Synthetic dates

The original source dataset contains relative timing but not calendar dates.

For reproducibility, the transformation creates deterministic synthetic conception dates beginning on 2025-01-01 and cycling across one calendar year. Other event dates are derived relative to conception.

These dates are scaffolding for the interoperability demonstration only and must not be interpreted as real clinical dates.

## Concept IDs

All OMOP `*_concept_id` fields are currently set to `0`.

This is intentional. The project has not yet performed a validated mapping to standard OHDSI concepts. Human-readable source values are retained so that vocabulary mapping can be added as a later extension without implying a level of standardization that has not been completed.

## Output tables

The transformation script creates:

- `PERSON`
- `OBSERVATION_PERIOD`
- `DRUG_EXPOSURE`
- `CONDITION_OCCURRENCE`
- `MEASUREMENT`
- `OBSERVATION`
- `analysis_cohort.csv` for study-specific derived variables

## Relationship to EHDS

The European Health Data Space (EHDS) is not implemented as a data source in this repository.

The relevance is methodological: an OMOP-style separation of clinical domains and transparent cohort logic demonstrates the type of interoperable, reusable RWE workflow that can support cross-database European evidence generation.

## Scope limitation

This layer is an educational and portfolio demonstration of standardized data thinking. It should be described as **OMOP-inspired**, not as a fully compliant OMOP CDM database.
