"""
Sensitivity and robustness analyses for the synthetic GLP-1 target-trial emulation.

This script evaluates whether the primary IPTW result is materially altered by:
1. Stabilized IPTW.
2. 1st-99th percentile weight truncation.
3. 5th-95th percentile weight truncation.
4. Restriction to propensity-score common support.
5. An alternative exposure-window definition (0-30 vs 31-180 days).

The alternative 30-day analysis changes the treatment definition and therefore
changes the causal contrast. It is included as a design sensitivity analysis,
not as a direct re-estimation of the exact primary estimand.

Input:
    data/synthetic_glp1_pregnancy.csv

Outputs:
    results/sensitivity_analysis.csv
    results/sensitivity_diagnostics.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "synthetic_glp1_pregnancy.csv"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT)

BASELINE_VARS = [
    "age",
    "bmi",
    "diabetes",
    "hypertension",
    "smoking",
    "prior_preterm_birth",
]


def effective_sample_size(weights):
    weights = np.asarray(weights, dtype=float)
    return (weights.sum() ** 2) / np.sum(weights ** 2)


def weighted_mean(values, weights):
    return np.average(values, weights=weights)


def weighted_variance(values, weights):
    mean = weighted_mean(values, weights)
    return np.average((values - mean) ** 2, weights=weights)


def max_abs_weighted_smd(data, treatment_col, weight_col):
    treated = data[data[treatment_col] == 1]
    control = data[data[treatment_col] == 0]

    smds = []

    for var in BASELINE_VARS:
        mean_t = weighted_mean(treated[var], treated[weight_col])
        mean_c = weighted_mean(control[var], control[weight_col])

        var_t = weighted_variance(treated[var], treated[weight_col])
        var_c = weighted_variance(control[var], control[weight_col])

        pooled_sd = np.sqrt((var_t + var_c) / 2)
        smd = (mean_t - mean_c) / pooled_sd
        smds.append(abs(smd))

    return max(smds)


def summarize_weighted_analysis(
    data,
    treatment_col,
    weight_col,
    label,
    notes,
):
    early = data[data[treatment_col] == 0]
    late = data[data[treatment_col] == 1]

    early_risk = weighted_mean(
        early["preterm_birth"],
        early[weight_col],
    )
    late_risk = weighted_mean(
        late["preterm_birth"],
        late[weight_col],
    )

    rd = late_risk - early_risk
    rr = late_risk / early_risk

    weights = data[weight_col].to_numpy()

    return {
        "Analysis": label,
        "N": len(data),
        "Early N": len(early),
        "Late N": len(late),
        "Early risk (%)": early_risk * 100,
        "Late risk (%)": late_risk * 100,
        "Risk difference (percentage points)": rd * 100,
        "Risk ratio": rr,
        "Weight min": weights.min(),
        "Weight max": weights.max(),
        "Effective sample size": effective_sample_size(weights),
        "Max absolute weighted SMD": max_abs_weighted_smd(
            data,
            treatment_col,
            weight_col,
        ),
        "Notes": notes,
    }


results = []

# ---------------------------------------------------------------------
# 1. Primary IPTW
# ---------------------------------------------------------------------
results.append(
    summarize_weighted_analysis(
        df,
        treatment_col="late_discontinuation",
        weight_col="iptw",
        label="Primary IPTW",
        notes="Primary 0-60 vs 61-180 day treatment contrast.",
    )
)

# ---------------------------------------------------------------------
# 2. Stabilized IPTW
# ---------------------------------------------------------------------
p_late = df["late_discontinuation"].mean()

df["stabilized_iptw"] = np.where(
    df["late_discontinuation"] == 1,
    p_late / df["propensity_score"],
    (1 - p_late) / (1 - df["propensity_score"]),
)

results.append(
    summarize_weighted_analysis(
        df,
        treatment_col="late_discontinuation",
        weight_col="stabilized_iptw",
        label="Stabilized IPTW",
        notes=(
            "Same primary estimand; numerator uses the marginal treatment "
            "probability."
        ),
    )
)

# ---------------------------------------------------------------------
# 3. Percentile-truncated weights
# ---------------------------------------------------------------------
for lower_q, upper_q, label in [
    (0.01, 0.99, "IPTW truncated 1st-99th pct"),
    (0.05, 0.95, "IPTW truncated 5th-95th pct"),
]:
    lower = df["iptw"].quantile(lower_q)
    upper = df["iptw"].quantile(upper_q)

    col = f"iptw_truncated_{int(lower_q*100):02d}_{int(upper_q*100):02d}"
    df[col] = df["iptw"].clip(lower=lower, upper=upper)

    results.append(
        summarize_weighted_analysis(
            df,
            treatment_col="late_discontinuation",
            weight_col=col,
            label=label,
            notes=f"Weights clipped to [{lower:.3f}, {upper:.3f}].",
        )
    )

# ---------------------------------------------------------------------
# 4. Common-support restriction
# ---------------------------------------------------------------------
early_ps = df.loc[
    df["late_discontinuation"] == 0,
    "propensity_score",
]
late_ps = df.loc[
    df["late_discontinuation"] == 1,
    "propensity_score",
]

common_lower = max(early_ps.min(), late_ps.min())
common_upper = min(early_ps.max(), late_ps.max())

common = df[
    df["propensity_score"].between(
        common_lower,
        common_upper,
        inclusive="both",
    )
].copy()

results.append(
    summarize_weighted_analysis(
        common,
        treatment_col="late_discontinuation",
        weight_col="iptw",
        label="Common-support trimmed IPTW",
        notes=(
            f"Restricted to overlapping PS range "
            f"[{common_lower:.3f}, {common_upper:.3f}]."
        ),
    )
)

# ---------------------------------------------------------------------
# 5. Alternative exposure-window definition
# ---------------------------------------------------------------------
# Sensitivity contrast:
#   Late = 0-30 days before conception
#   Early = 31-180 days before conception
#
# This is a different treatment definition from the primary target trial.
df["late_discontinuation_30d"] = (
    df["days_before_conception"] <= 30
).astype(int)

X_alt = df[BASELINE_VARS]
y_alt = df["late_discontinuation_30d"]

alt_ps_model = LogisticRegression(max_iter=1000)
alt_ps_model.fit(X_alt, y_alt)

df["propensity_score_30d"] = alt_ps_model.predict_proba(X_alt)[:, 1]

# Protect against numerical instability in a general implementation.
df["propensity_score_30d"] = df["propensity_score_30d"].clip(0.01, 0.99)

df["iptw_30d"] = np.where(
    df["late_discontinuation_30d"] == 1,
    1 / df["propensity_score_30d"],
    1 / (1 - df["propensity_score_30d"]),
)

results.append(
    summarize_weighted_analysis(
        df,
        treatment_col="late_discontinuation_30d",
        weight_col="iptw_30d",
        label="Alternative window: 0-30 vs 31-180 days",
        notes=(
            "Different treatment definition; propensity-score model "
            "re-estimated for the 30-day contrast."
        ),
    )
)

results_table = pd.DataFrame(results)
results_table.to_csv(
    RESULTS_DIR / "sensitivity_analysis.csv",
    index=False,
)

# ---------------------------------------------------------------------
# Diagnostics summary
# ---------------------------------------------------------------------
q01 = df["iptw"].quantile(0.01)
q99 = df["iptw"].quantile(0.99)
q05 = df["iptw"].quantile(0.05)
q95 = df["iptw"].quantile(0.95)

diagnostics = pd.DataFrame({
    "Diagnostic": [
        "Primary treatment prevalence (late)",
        "Early-group PS minimum",
        "Early-group PS maximum",
        "Late-group PS minimum",
        "Late-group PS maximum",
        "Common-support lower bound",
        "Common-support upper bound",
        "Patients excluded by common-support trimming",
        "Primary IPTW 1st percentile",
        "Primary IPTW 99th percentile",
        "Primary IPTW 5th percentile",
        "Primary IPTW 95th percentile",
    ],
    "Value": [
        p_late,
        early_ps.min(),
        early_ps.max(),
        late_ps.min(),
        late_ps.max(),
        common_lower,
        common_upper,
        len(df) - len(common),
        q01,
        q99,
        q05,
        q95,
    ],
})

diagnostics.to_csv(
    RESULTS_DIR / "sensitivity_diagnostics.csv",
    index=False,
)

print(results_table.round(4))
print()
print(diagnostics.round(4))
