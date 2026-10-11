"""
External Control Arm (ECA) demonstration for the synthetic GLP-1 pregnancy project.

Design
------
Index treated arm:
    Late preconception discontinuation (0-60 days) from the original
    synthetic target-trial cohort.

External control arm:
    A separately generated synthetic external database containing early
    discontinuation (61-180 days) patients.

The demonstration aligns eligibility, estimates the probability of belonging
to the index treated arm versus the external source, and uses ATT-style
weighting so that external controls are reweighted toward the baseline
characteristics of the treated index cohort.

This is a methodological demonstration only. It is not clinical evidence and
does not represent a validated external control for GLP-1RA pregnancy safety.

Inputs
------
data/synthetic_glp1_pregnancy.csv
data/synthetic_external_control.csv

Outputs
-------
results/eca_results.csv
results/eca_balance.csv
results/eca_diagnostics.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "synthetic_glp1_pregnancy.csv"
EXTERNAL_PATH = ROOT / "data" / "synthetic_external_control.csv"
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


def sigmoid(z):
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1 / (1 + np.exp(-z[pos]))
    exp_z = np.exp(z[~pos])
    out[~pos] = exp_z / (1 + exp_z)
    return out


def fit_ridge_logistic(X, y, l2=1.0, max_iter=100, tol=1e-9):
    """
    Small Newton-Raphson logistic model with L2 penalty on non-intercept terms.

    This is used here to keep the ECA demonstration self-contained and
    reproducible.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)

    X_design = np.column_stack([np.ones(len(X)), X])
    beta = np.zeros(X_design.shape[1])

    for _ in range(max_iter):
        p = sigmoid(X_design @ beta)
        w = np.clip(p * (1 - p), 1e-9, None)

        gradient = X_design.T @ (y - p)
        hessian = X_design.T @ (X_design * w[:, None])

        penalty = np.zeros_like(beta)
        penalty[1:] = l2 * beta[1:]
        gradient -= penalty

        penalty_matrix = np.zeros_like(hessian)
        penalty_matrix[1:, 1:] = np.eye(len(beta) - 1) * l2
        hessian += penalty_matrix

        delta = np.linalg.solve(hessian, gradient)
        beta += delta

        if np.max(np.abs(delta)) < tol:
            break

    p = sigmoid(X_design @ beta)
    return beta, np.clip(p, 0.01, 0.99)


def weighted_mean(x, w):
    return np.average(np.asarray(x, dtype=float), weights=np.asarray(w, dtype=float))


def weighted_variance(x, w):
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    mean = weighted_mean(x, w)
    return np.average((x - mean) ** 2, weights=w)


def standardized_mean_difference(treated, control, variable, weighted=False):
    if weighted:
        wt = treated["att_weight"]
        wc = control["att_weight"]
    else:
        wt = np.ones(len(treated))
        wc = np.ones(len(control))

    mean_t = weighted_mean(treated[variable], wt)
    mean_c = weighted_mean(control[variable], wc)

    var_t = weighted_variance(treated[variable], wt)
    var_c = weighted_variance(control[variable], wc)

    pooled_sd = np.sqrt((var_t + var_c) / 2)
    return (mean_t - mean_c) / pooled_sd


def effective_sample_size(weights):
    weights = np.asarray(weights, dtype=float)
    return (weights.sum() ** 2) / np.sum(weights ** 2)


def eca_estimate(data):
    treated = data[data["index_treated"] == 1]
    external = data[data["index_treated"] == 0]

    treated_risk = treated["preterm_birth"].mean()
    external_risk = weighted_mean(
        external["preterm_birth"],
        external["att_weight"],
    )

    rd = treated_risk - external_risk
    rr = treated_risk / external_risk

    return treated_risk, external_risk, rd, rr


# ---------------------------------------------------------------------
# 1. Build aligned index treated and external control cohorts
# ---------------------------------------------------------------------
index = pd.read_csv(INDEX_PATH)
external = pd.read_csv(EXTERNAL_PATH)

# Align to the target-trial age eligibility criterion.
index = index[
    index["age"].between(18, 45, inclusive="both")
].copy()

# Index treated arm = late discontinuation from original target-trial data.
index = index[index["late_discontinuation"] == 1].copy()

# External controls are generated to satisfy the early-discontinuation window.
external = external[
    external["age"].between(18, 45, inclusive="both")
    & external["days_before_conception"].between(61, 180, inclusive="both")
].copy()

index["index_treated"] = 1
index["source"] = "Index treated cohort"

external["index_treated"] = 0
external["source"] = "Synthetic external database"

index_keep = index[
    BASELINE_VARS + ["preterm_birth", "index_treated", "source"]
].copy()

external_keep = external[
    BASELINE_VARS + ["preterm_birth", "index_treated", "source"]
].copy()

combined = pd.concat(
    [index_keep, external_keep],
    ignore_index=True,
)

# ---------------------------------------------------------------------
# 2. Estimate source/treatment membership propensity
# ---------------------------------------------------------------------
beta, membership_ps = fit_ridge_logistic(
    combined[BASELINE_VARS].to_numpy(),
    combined["index_treated"].to_numpy(),
    l2=1.0,
)

combined["membership_ps"] = membership_ps

# ATT-style weights:
# treated index patients retain weight 1;
# external controls receive odds of index membership.
combined["att_weight"] = np.where(
    combined["index_treated"] == 1,
    1.0,
    combined["membership_ps"] / (1 - combined["membership_ps"]),
)

treated = combined[combined["index_treated"] == 1].copy()
external_control = combined[combined["index_treated"] == 0].copy()

# ---------------------------------------------------------------------
# 3. Balance diagnostics
# ---------------------------------------------------------------------
balance_rows = []

for variable in BASELINE_VARS:
    balance_rows.append({
        "Variable": variable,
        "SMD before weighting": standardized_mean_difference(
            treated,
            external_control,
            variable,
            weighted=False,
        ),
        "SMD after ATT weighting": standardized_mean_difference(
            treated,
            external_control,
            variable,
            weighted=True,
        ),
    })

balance = pd.DataFrame(balance_rows)
balance.to_csv(
    RESULTS_DIR / "eca_balance.csv",
    index=False,
)

# ---------------------------------------------------------------------
# 4. Main ATT estimate
# ---------------------------------------------------------------------
treated_risk, external_risk, rd, rr = eca_estimate(combined)

# ---------------------------------------------------------------------
# 5. Common-support restriction
# ---------------------------------------------------------------------
treated_ps = treated["membership_ps"]
external_ps = external_control["membership_ps"]

common_lower = max(treated_ps.min(), external_ps.min())
common_upper = min(treated_ps.max(), external_ps.max())

common = combined[
    combined["membership_ps"].between(
        common_lower,
        common_upper,
        inclusive="both",
    )
].copy()

cs_treated_risk, cs_external_risk, cs_rd, cs_rr = eca_estimate(common)

# ---------------------------------------------------------------------
# 6. Stratified bootstrap uncertainty
# ---------------------------------------------------------------------
rng = np.random.default_rng(20261012)
bootstrap_rd = []
bootstrap_rr = []

treated_raw = treated[BASELINE_VARS + ["preterm_birth"]].copy()
external_raw = external_control[BASELINE_VARS + ["preterm_birth"]].copy()

n_boot = 300

for _ in range(n_boot):
    boot_treated = treated_raw.iloc[
        rng.integers(0, len(treated_raw), len(treated_raw))
    ].copy()

    boot_external = external_raw.iloc[
        rng.integers(0, len(external_raw), len(external_raw))
    ].copy()

    boot_treated["index_treated"] = 1
    boot_external["index_treated"] = 0

    boot = pd.concat(
        [boot_treated, boot_external],
        ignore_index=True,
    )

    _, boot_ps = fit_ridge_logistic(
        boot[BASELINE_VARS].to_numpy(),
        boot["index_treated"].to_numpy(),
        l2=1.0,
    )

    boot["membership_ps"] = boot_ps
    boot["att_weight"] = np.where(
        boot["index_treated"] == 1,
        1.0,
        boot["membership_ps"] / (1 - boot["membership_ps"]),
    )

    _, _, boot_rd_value, boot_rr_value = eca_estimate(boot)
    bootstrap_rd.append(boot_rd_value)
    bootstrap_rr.append(boot_rr_value)

rd_ci = np.percentile(bootstrap_rd, [2.5, 97.5])
rr_ci = np.percentile(bootstrap_rr, [2.5, 97.5])

# ---------------------------------------------------------------------
# 7. Write results and diagnostics
# ---------------------------------------------------------------------
results = pd.DataFrame([
    {
        "Analysis": "External control ATT-weighted",
        "Index treated N": len(treated),
        "External control N": len(external_control),
        "Index treated risk (%)": treated_risk * 100,
        "Weighted external control risk (%)": external_risk * 100,
        "Risk difference (percentage points)": rd * 100,
        "RD 95% CI": f"{rd_ci[0] * 100:.2f} to {rd_ci[1] * 100:.2f}",
        "Risk ratio": rr,
        "RR 95% CI": f"{rr_ci[0]:.2f} to {rr_ci[1]:.2f}",
        "Estimand": (
            "ATT-style contrast in the baseline characteristics of the "
            "index treated cohort"
        ),
    },
    {
        "Analysis": "Common-support restricted ECA",
        "Index treated N": int((common["index_treated"] == 1).sum()),
        "External control N": int((common["index_treated"] == 0).sum()),
        "Index treated risk (%)": cs_treated_risk * 100,
        "Weighted external control risk (%)": cs_external_risk * 100,
        "Risk difference (percentage points)": cs_rd * 100,
        "RD 95% CI": "Not bootstrapped separately",
        "Risk ratio": cs_rr,
        "RR 95% CI": "Not bootstrapped separately",
        "Estimand": "ATT-style contrast after common-support restriction",
    },
])

results.to_csv(
    RESULTS_DIR / "eca_results.csv",
    index=False,
)

diagnostics = pd.DataFrame({
    "Diagnostic": [
        "Index treated N after eligibility alignment",
        "External control N after eligibility alignment",
        "Index membership PS minimum - treated",
        "Index membership PS maximum - treated",
        "Index membership PS minimum - external",
        "Index membership PS maximum - external",
        "Common-support lower bound",
        "Common-support upper bound",
        "Index treated excluded by common-support restriction",
        "External controls excluded by common-support restriction",
        "External-control effective sample size after ATT weighting",
        "Maximum absolute SMD before weighting",
        "Maximum absolute SMD after ATT weighting",
        "Bootstrap repetitions",
    ],
    "Value": [
        len(treated),
        len(external_control),
        treated_ps.min(),
        treated_ps.max(),
        external_ps.min(),
        external_ps.max(),
        common_lower,
        common_upper,
        len(treated) - int((common["index_treated"] == 1).sum()),
        len(external_control) - int((common["index_treated"] == 0).sum()),
        effective_sample_size(external_control["att_weight"]),
        balance["SMD before weighting"].abs().max(),
        balance["SMD after ATT weighting"].abs().max(),
        n_boot,
    ],
})

diagnostics.to_csv(
    RESULTS_DIR / "eca_diagnostics.csv",
    index=False,
)

print(results)
print()
print(balance.round(4))
print()
print(diagnostics.round(4))
