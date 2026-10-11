"""
Canonical primary analysis for the synthetic GLP-1 target-trial emulation.

The source dataset contains 2,000 synthetic records. The target-trial protocol
specifies eligibility age 18-45 years, so this script explicitly applies that
criterion before estimating propensity scores or treatment effects.

This keeps a realistic distinction between:
1. source data, which may contain ineligible records, and
2. the analysis cohort, which must satisfy the emulated trial eligibility rules.

Inputs
------
data/synthetic_glp1_pregnancy.csv

Outputs
-------
results/hta_results_summary.csv
results/eligibility_audit.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "synthetic_glp1_pregnancy.csv"
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


def weighted_mean(values, weights):
    return np.average(values, weights=weights)


def weighted_mean_var(values, weights):
    mean = weighted_mean(values, weights)
    var = np.average((values - mean) ** 2, weights=weights)
    return mean, var


def smd_unweighted(data, var):
    early = data[data["late_discontinuation"] == 0][var]
    late = data[data["late_discontinuation"] == 1][var]

    mean_early = early.mean()
    mean_late = late.mean()

    var_early = early.var()
    var_late = late.var()

    pooled_sd = np.sqrt((var_early + var_late) / 2)
    return (mean_late - mean_early) / pooled_sd


def smd_weighted(data, var):
    early = data[data["late_discontinuation"] == 0]
    late = data[data["late_discontinuation"] == 1]

    mean_early, var_early = weighted_mean_var(
        early[var],
        early["iptw"],
    )
    mean_late, var_late = weighted_mean_var(
        late[var],
        late["iptw"],
    )

    pooled_sd = np.sqrt((var_early + var_late) / 2)
    return (mean_late - mean_early) / pooled_sd


# ---------------------------------------------------------------------
# 1. Load source data and enforce target-trial eligibility
# ---------------------------------------------------------------------
source = pd.read_csv(INPUT)

eligible = source[
    source["age"].between(18, 45, inclusive="both")
].copy()

eligibility_audit = pd.DataFrame({
    "Metric": [
        "Source records",
        "Eligible analysis records",
        "Excluded for age <18",
        "Excluded for age >45",
        "Total age-ineligible records",
    ],
    "Value": [
        len(source),
        len(eligible),
        int((source["age"] < 18).sum()),
        int((source["age"] > 45).sum()),
        int((~source["age"].between(18, 45, inclusive="both")).sum()),
    ],
})

eligibility_audit.to_csv(
    RESULTS_DIR / "eligibility_audit.csv",
    index=False,
)

# ---------------------------------------------------------------------
# 2. Re-estimate propensity scores in the eligible cohort
# ---------------------------------------------------------------------
X = eligible[BASELINE_VARS]
y = eligible["late_discontinuation"]

ps_model = LogisticRegression(max_iter=1000)
ps_model.fit(X, y)

eligible["propensity_score_reestimated"] = ps_model.predict_proba(X)[:, 1]

eligible["iptw_reestimated"] = np.where(
    eligible["late_discontinuation"] == 1,
    1 / eligible["propensity_score_reestimated"],
    1 / (1 - eligible["propensity_score_reestimated"]),
)

# Use canonical names inside this analysis.
eligible["propensity_score"] = eligible["propensity_score_reestimated"]
eligible["iptw"] = eligible["iptw_reestimated"]

# ---------------------------------------------------------------------
# 3. Crude and IPTW-adjusted estimates
# ---------------------------------------------------------------------
early = eligible[eligible["late_discontinuation"] == 0]
late = eligible[eligible["late_discontinuation"] == 1]

risk_early = early["preterm_birth"].mean()
risk_late = late["preterm_birth"].mean()

risk_difference = risk_late - risk_early
risk_ratio = risk_late / risk_early

weighted_risk_early = weighted_mean(
    early["preterm_birth"],
    early["iptw"],
)
weighted_risk_late = weighted_mean(
    late["preterm_birth"],
    late["iptw"],
)

weighted_risk_difference = (
    weighted_risk_late - weighted_risk_early
)
weighted_risk_ratio = (
    weighted_risk_late / weighted_risk_early
)

# ---------------------------------------------------------------------
# 4. Bootstrap uncertainty with PS re-estimation
# ---------------------------------------------------------------------
rng = np.random.default_rng(42)
bootstrap_rd = []
bootstrap_rr = []

n_boot = 500

for _ in range(n_boot):
    idx = rng.choice(
        len(eligible),
        size=len(eligible),
        replace=True,
    )

    boot = eligible.iloc[idx].copy()

    X_boot = boot[BASELINE_VARS]
    y_boot = boot["late_discontinuation"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X_boot, y_boot)

    ps = model.predict_proba(X_boot)[:, 1]
    ps = np.clip(ps, 0.01, 0.99)

    boot["iptw_boot"] = np.where(
        boot["late_discontinuation"] == 1,
        1 / ps,
        1 / (1 - ps),
    )

    early_boot = boot[boot["late_discontinuation"] == 0]
    late_boot = boot[boot["late_discontinuation"] == 1]

    risk_early_boot = weighted_mean(
        early_boot["preterm_birth"],
        early_boot["iptw_boot"],
    )
    risk_late_boot = weighted_mean(
        late_boot["preterm_birth"],
        late_boot["iptw_boot"],
    )

    bootstrap_rd.append(
        risk_late_boot - risk_early_boot
    )
    bootstrap_rr.append(
        risk_late_boot / risk_early_boot
    )

rd_ci = np.percentile(bootstrap_rd, [2.5, 97.5])
rr_ci = np.percentile(bootstrap_rr, [2.5, 97.5])

# ---------------------------------------------------------------------
# 5. HTA-oriented summary
# ---------------------------------------------------------------------
results_table = pd.DataFrame({
    "Analysis": [
        "Crude",
        "IPTW-adjusted",
    ],
    "Eligible N": [
        len(eligible),
        len(eligible),
    ],
    "Early N": [
        len(early),
        len(early),
    ],
    "Late N": [
        len(late),
        len(late),
    ],
    "Early risk (%)": [
        risk_early * 100,
        weighted_risk_early * 100,
    ],
    "Late risk (%)": [
        risk_late * 100,
        weighted_risk_late * 100,
    ],
    "Risk difference (percentage points)": [
        risk_difference * 100,
        weighted_risk_difference * 100,
    ],
    "RD 95% CI": [
        "Not calculated",
        f"{rd_ci[0] * 100:.1f} to {rd_ci[1] * 100:.1f}",
    ],
    "Risk ratio": [
        risk_ratio,
        weighted_risk_ratio,
    ],
    "RR 95% CI": [
        "Not calculated",
        f"{rr_ci[0]:.2f} to {rr_ci[1]:.2f}",
    ],
})

results_table.to_csv(
    RESULTS_DIR / "hta_results_summary.csv",
    index=False,
)

print(eligibility_audit)
print()
print(results_table.round(3))
print()
print("Balance after IPTW:")
for var in BASELINE_VARS:
    print(
        var,
        "before=",
        round(smd_unweighted(eligible, var), 3),
        "after=",
        round(smd_weighted(eligible, var), 3),
    )
