"""
OMOP-inspired transformation for the synthetic GLP-1 pregnancy cohort.

This script decomposes the flat analytical dataset into domain-specific tables
that resemble core OMOP CDM domains. It is intentionally educational and does
not claim full OMOP conformance or validated OHDSI vocabulary mapping.

Input:
    data/synthetic_glp1_pregnancy.csv

Outputs:
    omop_output/person.csv
    omop_output/observation_period.csv
    omop_output/drug_exposure.csv
    omop_output/condition_occurrence.csv
    omop_output/measurement.csv
    omop_output/observation.csv
    omop_output/analysis_cohort.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "synthetic_glp1_pregnancy.csv"
OUTPUT_DIR = ROOT / "omop_output"
OUTPUT_DIR.mkdir(exist_ok=True)

patients = pd.read_csv(INPUT)

# ---------------------------------------------------------------------
# Synthetic calendar dates
# ---------------------------------------------------------------------
# The source cohort stores relative timing, not real calendar dates.
# We create deterministic synthetic conception dates only to demonstrate
# longitudinal domain structure.
base_date = pd.Timestamp("2025-01-01")
patients["conception_date"] = [
    base_date + pd.Timedelta(days=i % 365)
    for i in range(len(patients))
]

patients["baseline_date"] = patients["conception_date"] - pd.Timedelta(days=30)
patients["history_date"] = patients["conception_date"] - pd.Timedelta(days=180)
patients["outcome_date"] = patients["conception_date"] + pd.Timedelta(days=245)
patients["last_glp1_exposure_date"] = (
    patients["conception_date"]
    - pd.to_timedelta(patients["days_before_conception"], unit="D")
)

# ---------------------------------------------------------------------
# PERSON
# ---------------------------------------------------------------------
person = pd.DataFrame({
    "person_id": patients["patient_id"],
    "gender_concept_id": 0,
    "year_of_birth": (
        patients["conception_date"].dt.year
        - np.floor(patients["age"]).astype(int)
    ),
    "month_of_birth": pd.NA,
    "day_of_birth": pd.NA,
    "birth_datetime": pd.NA,
    "race_concept_id": 0,
    "ethnicity_concept_id": 0,
    "location_id": pd.NA,
    "provider_id": pd.NA,
    "care_site_id": pd.NA,
    "person_source_value": "SYNTH-" + patients["patient_id"].astype(str),
    "gender_source_value": "Not simulated",
    "gender_source_concept_id": 0,
    "race_source_value": "Not simulated",
    "race_source_concept_id": 0,
    "ethnicity_source_value": "Not simulated",
    "ethnicity_source_concept_id": 0,
})

# ---------------------------------------------------------------------
# OBSERVATION_PERIOD
# ---------------------------------------------------------------------
observation_period = pd.DataFrame({
    "observation_period_id": patients["patient_id"],
    "person_id": patients["patient_id"],
    "observation_period_start_date": (
        patients["conception_date"] - pd.Timedelta(days=365)
    ).dt.date,
    "observation_period_end_date": (
        patients["conception_date"] + pd.Timedelta(days=300)
    ).dt.date,
    "period_type_concept_id": 0,
})

# ---------------------------------------------------------------------
# DRUG_EXPOSURE
# ---------------------------------------------------------------------
drug_exposure = pd.DataFrame({
    "drug_exposure_id": patients["patient_id"],
    "person_id": patients["patient_id"],
    "drug_concept_id": 0,
    "drug_exposure_start_date": patients["last_glp1_exposure_date"].dt.date,
    "drug_exposure_start_datetime": pd.NA,
    "drug_exposure_end_date": patients["last_glp1_exposure_date"].dt.date,
    "drug_exposure_end_datetime": pd.NA,
    "verbatim_end_date": patients["last_glp1_exposure_date"].dt.date,
    "drug_type_concept_id": 0,
    "stop_reason": patients["treatment_strategy"],
    "refills": pd.NA,
    "quantity": pd.NA,
    "days_supply": pd.NA,
    "sig": pd.NA,
    "route_concept_id": 0,
    "lot_number": pd.NA,
    "provider_id": pd.NA,
    "visit_occurrence_id": pd.NA,
    "visit_detail_id": pd.NA,
    "drug_source_value": "GLP-1 receptor agonist - synthetic last exposure event",
    "drug_source_concept_id": 0,
    "route_source_value": pd.NA,
    "dose_unit_source_value": pd.NA,
})

# ---------------------------------------------------------------------
# CONDITION_OCCURRENCE
# ---------------------------------------------------------------------
condition_rows = []
condition_id = 1

def add_condition(mask, label, date_series, role):
    global condition_id
    for idx in patients.index[mask]:
        condition_rows.append({
            "condition_occurrence_id": condition_id,
            "person_id": patients.at[idx, "patient_id"],
            "condition_concept_id": 0,
            "condition_start_date": date_series.at[idx].date(),
            "condition_start_datetime": pd.NA,
            "condition_end_date": pd.NA,
            "condition_end_datetime": pd.NA,
            "condition_type_concept_id": 0,
            "condition_status_concept_id": 0,
            "stop_reason": pd.NA,
            "provider_id": pd.NA,
            "visit_occurrence_id": pd.NA,
            "visit_detail_id": pd.NA,
            "condition_source_value": label,
            "condition_source_concept_id": 0,
            "condition_status_source_value": role,
        })
        condition_id += 1

add_condition(
    patients["diabetes"].eq(1),
    "Diabetes mellitus",
    patients["baseline_date"],
    "baseline confounder",
)
add_condition(
    patients["hypertension"].eq(1),
    "Hypertension",
    patients["baseline_date"],
    "baseline confounder",
)
add_condition(
    patients["prior_preterm_birth"].eq(1),
    "History of preterm birth",
    patients["history_date"],
    "baseline history",
)
add_condition(
    patients["preterm_birth"].eq(1),
    "Preterm birth",
    patients["outcome_date"],
    "study outcome",
)

condition_occurrence = pd.DataFrame(condition_rows)

# ---------------------------------------------------------------------
# MEASUREMENT
# ---------------------------------------------------------------------
measurement = pd.DataFrame({
    "measurement_id": np.arange(1, len(patients) + 1),
    "person_id": patients["patient_id"],
    "measurement_concept_id": 0,
    "measurement_date": patients["baseline_date"].dt.date,
    "measurement_datetime": pd.NA,
    "measurement_time": pd.NA,
    "measurement_type_concept_id": 0,
    "operator_concept_id": 0,
    "value_as_number": patients["bmi"],
    "value_as_concept_id": 0,
    "unit_concept_id": 0,
    "range_low": pd.NA,
    "range_high": pd.NA,
    "provider_id": pd.NA,
    "visit_occurrence_id": pd.NA,
    "visit_detail_id": pd.NA,
    "measurement_source_value": "Body mass index",
    "measurement_source_concept_id": 0,
    "unit_source_value": "kg/m2",
    "unit_source_concept_id": 0,
    "value_source_value": patients["bmi"].astype(str),
    "measurement_event_id": pd.NA,
    "meas_event_field_concept_id": 0,
})

# ---------------------------------------------------------------------
# OBSERVATION
# ---------------------------------------------------------------------
observation = pd.DataFrame({
    "observation_id": np.arange(1, len(patients) + 1),
    "person_id": patients["patient_id"],
    "observation_concept_id": 0,
    "observation_date": patients["baseline_date"].dt.date,
    "observation_datetime": pd.NA,
    "observation_type_concept_id": 0,
    "value_as_number": pd.NA,
    "value_as_string": np.where(
        patients["smoking"].eq(1),
        "Current smoker",
        "Not current smoker",
    ),
    "value_as_concept_id": 0,
    "qualifier_concept_id": 0,
    "unit_concept_id": 0,
    "provider_id": pd.NA,
    "visit_occurrence_id": pd.NA,
    "visit_detail_id": pd.NA,
    "observation_source_value": "Smoking status",
    "observation_source_concept_id": 0,
    "unit_source_value": pd.NA,
    "qualifier_source_value": pd.NA,
    "value_source_value": patients["smoking"].astype(str),
    "observation_event_id": pd.NA,
    "obs_event_field_concept_id": 0,
})

# ---------------------------------------------------------------------
# Analysis-specific cohort table
# ---------------------------------------------------------------------
analysis_cohort = patients[[
    "patient_id",
    "conception_date",
    "treatment_strategy",
    "late_discontinuation",
    "days_before_conception",
    "preterm_birth",
    "propensity_score",
    "iptw",
]].rename(columns={"patient_id": "person_id"})

analysis_cohort["conception_date"] = analysis_cohort["conception_date"].dt.date

# ---------------------------------------------------------------------
# Write outputs
# ---------------------------------------------------------------------
tables = {
    "person": person,
    "observation_period": observation_period,
    "drug_exposure": drug_exposure,
    "condition_occurrence": condition_occurrence,
    "measurement": measurement,
    "observation": observation,
    "analysis_cohort": analysis_cohort,
}

for name, table in tables.items():
    table.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)

print("OMOP-inspired transformation complete.")
for name, table in tables.items():
    print(f"{name}: {len(table):,} rows")
