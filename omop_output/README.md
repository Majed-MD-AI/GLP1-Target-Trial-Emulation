# OMOP-inspired generated outputs

These files are generated from the synthetic analytical cohort using the transformation logic in:

`scripts/02_omop_transformation.py`

## Tables

| File | Rows | Purpose |
| --- | ---: | --- |
| `person.csv` | 2,000 | Synthetic person-level demographic shell |
| `observation_period.csv` | 2,000 | Synthetic data-availability windows |
| `drug_exposure.csv` | 2,000 | Last synthetic preconception GLP-1RA exposure event |
| `condition_occurrence.csv` | 1,794 | Baseline conditions, obstetric history, and preterm-birth outcomes |
| `measurement.csv` | 2,000 | Baseline BMI measurements |
| `observation.csv` | 2,000 | Baseline smoking-status observations |
| `analysis_cohort.csv` | 2,000 | Study-specific treatment, outcome, propensity-score, and IPTW variables |
| `validation_summary.csv` | — | Row-count and source-to-output validation checks |

## Important scope note

These outputs are **OMOP-inspired**, not a production OMOP CDM instance.

- Standard OHDSI vocabulary mapping has not been performed.
- OMOP concept IDs are placeholders (`0`) where a validated standard concept is not assigned.
- Calendar dates are deterministic synthetic scaffolding derived from the original relative timing.
- Study-specific derived variables remain outside the clinical-domain tables.

See `docs/omop_mapping.md` for the detailed source-to-domain mapping.
