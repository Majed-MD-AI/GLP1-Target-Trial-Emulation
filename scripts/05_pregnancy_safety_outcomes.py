"""
Pregnancy medication-safety outcome expansion for the synthetic target-trial project.

This stage adds synthetic secondary pregnancy outcomes already prespecified in
the protocol:
- preeclampsia
- small for gestational age (SGA)
- large for gestational age (LGA)
- congenital malformations

The source outcome file is synthetic and generated only for methodological
demonstration. The analysis enforces the protocol age eligibility criterion
(18-45 years), re-estimates the propensity score in the eligible cohort, applies
IPTW, and estimates outcome-specific risk differences and risk ratios.

Inputs
------
data/synthetic_glp1_pregnancy.csv
data/synthetic_pregnancy_safety_outcomes.csv

Output
------
results/pregnancy_safety_outcomes.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "data" / "synthetic_glp1_pregnancy.csv"
OUTCOME_PATH = ROOT / "data" / "synthetic_pregnancy_safety_outcomes.csv"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

BASELINE_VARS = [
    "age",
    "bmi",
    "diabetes",
    "hypertension",
    "smoking",
    "prior_preterm_birth",
]

OUTCOMES = {
    "preeclampsia": "Preeclampsia",
    "small_for_gestational_age": "Small for gestational age",
    "large_for_gestational_age": "Large for gestational age",
    "congenital_malformation": "Congenital malformation",
}

base = pd.read_csv(BASE_PATH)
secondary = pd.read_csv(OUTCOME_PATH)

data = base.merge(
    secondary,
    on="patient_id",
    how="inner",
)

data = data[
    data["age"].between(18, 45, inclusive="both")
].copy()

# ---------------------------------------------------------------------
# Re-estimate propensity score in the eligible analysis cohort
# ---------------------------------------------------------------------
ps_model = LogisticRegression(max_iter=1000)
ps_model.fit(
    data[BASELINE_VARS],
    data["late_discontinuation"],
)

data["ps_secondary"] = ps_model.predict_proba(
    data[BASELINE_VARS]
)[:, 1].clip(0.01, 0.99)

data["iptw_secondary"] = np.where(
    data["late_discontinuation"] == 1,
    1 / data["ps_secondary"],
    1 / (1 - data["ps_secondary"]),
)


def weighted_risk(frame, outcome):
    return np.average(
        frame[outcome],
        weights=frame["iptw_secondary"],
    )


def estimate(frame, outcome):
    early = frame[frame["late_discontinuation"] == 0]
    late = frame[frame["late_discontinuation"] == 1]

    crude_early = early[outcome].mean()
    crude_late = late[outcome].mean()

    adjusted_early = weighted_risk(early, outcome)
    adjusted_late = weighted_risk(late, outcome)

    return {
        "Early N": len(early),
        "Late N": len(late),
        "Crude early risk (%)": crude_early * 100,
        "Crude late risk (%)": crude_late * 100,
        "Crude RD (percentage points)": (crude_late - crude_early) * 100,
        "Crude RR": crude_late / crude_early,
        "Adjusted early risk (%)": adjusted_early * 100,
        "Adjusted late risk (%)": adjusted_late * 100,
        "Adjusted RD (percentage points)": (
            adjusted_late - adjusted_early
        ) * 100,
        "Adjusted RR": adjusted_late / adjusted_early,
    }


# ---------------------------------------------------------------------
# Bootstrap uncertainty with PS re-estimation
# ---------------------------------------------------------------------
rng = np.random.default_rng(20261014)
n_boot = 300

bootstrap = {
    outcome: {"rd": [], "rr": []}
    for outcome in OUTCOMES
}

for _ in range(n_boot):
    idx = rng.choice(
        len(data),
        size=len(data),
        replace=True,
    )

    boot = data.iloc[idx].copy()

    model = LogisticRegression(max_iter=1000)
    model.fit(
        boot[BASELINE_VARS],
        boot["late_discontinuation"],
    )

    ps = model.predict_proba(
        boot[BASELINE_VARS]
    )[:, 1].clip(0.01, 0.99)

    boot["w_boot"] = np.where(
        boot["late_discontinuation"] == 1,
        1 / ps,
        1 / (1 - ps),
    )

    early = boot[boot["late_discontinuation"] == 0]
    late = boot[boot["late_discontinuation"] == 1]

    for outcome in OUTCOMES:
        early_risk = np.average(
            early[outcome],
            weights=early["w_boot"],
        )
        late_risk = np.average(
            late[outcome],
            weights=late["w_boot"],
        )

        bootstrap[outcome]["rd"].append(
            late_risk - early_risk
        )
        bootstrap[outcome]["rr"].append(
            late_risk / early_risk
        )

rows = []

for outcome, label in OUTCOMES.items():
    result = estimate(data, outcome)

    rd_ci = np.percentile(
        bootstrap[outcome]["rd"],
        [2.5, 97.5],
    )
    rr_ci = np.percentile(
        bootstrap[outcome]["rr"],
        [2.5, 97.5],
    )

    rows.append({
        "Outcome": label,
        "Eligible N": len(data),
        **result,
        "Adjusted RD 95% CI": (
            f"{rd_ci[0] * 100:.2f} to {rd_ci[1] * 100:.2f}"
        ),
        "Adjusted RR 95% CI": (
            f"{rr_ci[0]:.2f} to {rr_ci[1]:.2f}"
        ),
        "Bootstrap repetitions": n_boot,
    })

results = pd.DataFrame(rows)

results.to_csv(
    RESULTS_DIR / "pregnancy_safety_outcomes.csv",
    index=False,
)

print(results.round(3))
