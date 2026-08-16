"""
analysis.py
===========
Analysis pipeline for the "antibiotic-project" senior thesis:

    "A study of cellular DNA repair mechanisms that enable Gram positive
    bacteria to resist certain antibiotics"
    (B. subtilis PY012 wild-type vs. PY001 (recA-) vs. MA012 (addA-),
    sensitivity to norfloxacin & ciprofloxacin)

Reads two input files (matching the repo layout):
    growth_curve.csv  -> OD600 growth-curve data   (Figures 5, 6, 7)
    data.csv          -> CFU / colony-count data    (Figure 8)

Writes plots to ./figures/:
    fig5_growth_curve_control.png
    fig6_growth_curve_norfloxacin.png
    fig7_growth_curve_ciprofloxacin.png
    fig8_cfu_barchart.png

--------------------------------------------------------------------------
EXPECTED CSV SCHEMA
--------------------------------------------------------------------------
growth_curve.csv (long format, one row per reading):
    time_min, strain, experiment, group, replicate, od600

    strain      : PY012 | PY001 | MA012
    experiment  : baseline | norfloxacin | ciprofloxacin
                  (baseline = Figure 5, no antibiotic at all;
                   norfloxacin/ciprofloxacin = Figures 6/7, each of which
                   plots BOTH a treated and a control line per strain)
    group       : control | treated
                  (for experiment="baseline", group is always "control")
    replicate   : 1..n (biological replicate number)
    od600       : float

data.csv (long format, one row per plate):
    strain, antibiotic, group, dilution, colonies, cfu_per_ml

    antibiotic  : norfloxacin | ciprofloxacin
    group       : treated | control
    dilution    : e.g. 0.001, 0.0001   (i.e. 10^-3, 10^-4)
    colonies    : raw colony count (only 30-300 range is valid per the
                  thesis's plate-count methodology)
    cfu_per_ml  : optional pre-calculated CFU/mL. If missing/blank, it is
                  computed from colonies / (dilution * plated_volume_ml)

If your real CSV files use different column names, edit COLUMN_MAP below
-- the rest of the script only ever refers to the standardized names on
the right-hand side, so you only need to change one spot.
--------------------------------------------------------------------------
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# CONFIG - adjust here if your real CSVs use different column names/paths
# --------------------------------------------------------------------------

GROWTH_CURVE_CSV = Path("growth_curve.csv")
CFU_CSV = Path("data.csv")
OUTPUT_DIR = Path("figures")

# Volume (mL) plated during the standard plate count (adjust if different)
PLATED_VOLUME_ML = 0.1

# Rename columns from your actual file -> the standardized names used below.
# Left = name in your CSV, Right = name analysis.py expects.
# Leave as identity mappings if your columns already match.
GROWTH_COLUMN_MAP = {
    "time_min": "time_min",
    "strain": "strain",
    "experiment": "experiment",
    "group": "group",
    "replicate": "replicate",
    "od600": "od600",
}

CFU_COLUMN_MAP = {
    "strain": "strain",
    "antibiotic": "antibiotic",
    "group": "group",
    "dilution": "dilution",
    "colonies": "colonies",
    "cfu_per_ml": "cfu_per_ml",
}

# Consistent color/style scheme across all figures, echoing the thesis plots
STRAIN_COLORS = {
    "PY012": "#e2761b",  # wild-type - orange
    "PY001": "#2b7fc9",  # recA-      - blue
    "MA012": "#3f9e4d",  # addA-      - green
}
STRAIN_LABELS = {
    "PY012": "PY012 (wild-type)",
    "PY001": "PY001 (recA\u207b)",
    "MA012": "MA012 (addA\u207b)",
}


# --------------------------------------------------------------------------
# DATA LOADING
# --------------------------------------------------------------------------

def _load_csv(path: Path, column_map: dict, required: list) -> pd.DataFrame:
    if not path.exists():
        sys.exit(
            f"ERROR: could not find '{path}'.\n"
            f"Place it next to analysis.py, or update the path in the "
            f"CONFIG section at the top of this script."
        )
    df = pd.read_csv(path)
    df = df.rename(columns=column_map)
    missing = [c for c in required if c not in df.columns]
    if missing:
        sys.exit(
            f"ERROR: '{path}' is missing expected column(s): {missing}\n"
            f"Update the COLUMN_MAP at the top of analysis.py to match "
            f"your actual CSV headers."
        )
    return df


def load_growth_curve(path: Path = GROWTH_CURVE_CSV) -> pd.DataFrame:
    df = _load_csv(
        path,
        GROWTH_COLUMN_MAP,
        required=["time_min", "strain", "experiment", "group", "od600"],
    )
    df["time_min"] = pd.to_numeric(df["time_min"], errors="coerce")
    df["od600"] = pd.to_numeric(df["od600"], errors="coerce")
    return df.dropna(subset=["time_min", "od600"])


def load_cfu_data(path: Path = CFU_CSV) -> pd.DataFrame:
    df = _load_csv(
        path,
        CFU_COLUMN_MAP,
        required=["strain", "antibiotic", "group", "dilution", "colonies"],
    )
    df["dilution"] = pd.to_numeric(df["dilution"], errors="coerce")
    df["colonies"] = pd.to_numeric(df["colonies"], errors="coerce")

    if "cfu_per_ml" not in df.columns:
        df["cfu_per_ml"] = pd.NA
    df["cfu_per_ml"] = pd.to_numeric(df["cfu_per_ml"], errors="coerce")

    # Fill in missing CFU/mL values: colonies / (dilution * plated volume)
    needs_calc = df["cfu_per_ml"].isna()
    df.loc[needs_calc, "cfu_per_ml"] = (
        df.loc[needs_calc, "colonies"]
        / (df.loc[needs_calc, "dilution"] * PLATED_VOLUME_ML)
    )

    # Per thesis methodology, only 30-300 colony plates are valid counts
    dropped = df[(df["colonies"] < 30) | (df["colonies"] > 300)]
    if not dropped.empty:
        print(
            f"Note: dropping {len(dropped)} plate(s) outside the "
            f"30-300 colony countable range (methodology in thesis section 3.2.2)."
        )
    df = df[(df["colonies"] >= 30) & (df["colonies"] <= 300)]
    return df


# --------------------------------------------------------------------------
# PLOTTING - growth curves (Figures 5, 6, 7)
# --------------------------------------------------------------------------

def plot_growth_curve(df: pd.DataFrame, experiment: str, title: str, out_path: Path):
    """
    Plots mean OD600 vs. time for each strain under a given experiment.

    For "baseline" (Figure 5) this draws one line per strain (no drug).
    For "norfloxacin"/"ciprofloxacin" (Figures 6/7) this draws BOTH the
    treated and control line per strain (solid = control/no-drug,
    dashed = treated), matching the six-line layout in the report.

    Error bars (SD across replicates) are drawn automatically whenever
    more than one replicate exists for a given time point.
    """
    subset = df[df["experiment"] == experiment]
    if subset.empty:
        print(f"Skipping '{title}': no rows found for experiment='{experiment}'.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    groups_present = [g for g in ["control", "treated"] if g in subset["group"].unique()]

    for strain in ["PY012", "PY001", "MA012"]:
        for group in groups_present:
            line_df = subset[(subset["strain"] == strain) & (subset["group"] == group)]
            if line_df.empty:
                continue
            grouped = line_df.groupby("time_min")["od600"].agg(["mean", "std"]).reset_index()
            grouped["std"] = grouped["std"].fillna(0)

            # Only append a (treated)/(control) qualifier when both groups
            # are present on the same chart (i.e. not for the baseline plot)
            label = STRAIN_LABELS[strain]
            if len(groups_present) > 1:
                label += " - control" if group == "control" else " - treated"

            ax.errorbar(
                grouped["time_min"],
                grouped["mean"],
                yerr=grouped["std"],
                marker="o",
                capsize=3,
                linestyle="-" if group == "control" else "--",
                alpha=1.0 if group == "control" else 0.75,
                label=label,
                color=STRAIN_COLORS[strain],
            )

    ax.set_title(title)
    ax.set_xlabel("Time (minute)")
    ax.set_ylabel("OD600")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"Saved {out_path}")


# --------------------------------------------------------------------------
# PLOTTING - CFU bar chart (Figure 8)
# --------------------------------------------------------------------------

def plot_cfu_barchart(df: pd.DataFrame, out_path: Path):
    """
    Grouped bar chart of CFU/mL by strain, split by antibiotic + treated/control,
    mirroring Figure 8 in the report.
    """
    if df.empty:
        print("Skipping CFU bar chart: no valid CFU data.")
        return

    summary = (
        df.groupby(["antibiotic", "group", "strain"])["cfu_per_ml"]
        .mean()
        .reset_index()
    )

    # Build the four x-axis categories: Norf., Norf.(control), Ciprof., Ciprof.(control)
    categories = []
    for antibiotic in ["norfloxacin", "ciprofloxacin"]:
        for group in ["treated", "control"]:
            label = f"{antibiotic.capitalize()[:5]}." + (" (control)" if group == "control" else "")
            categories.append((antibiotic, group, label))

    strains = ["PY012", "PY001", "MA012"]
    x = range(len(categories))
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for i, strain in enumerate(strains):
        values = []
        for antibiotic, group, _ in categories:
            match = summary[
                (summary["antibiotic"] == antibiotic)
                & (summary["group"] == group)
                & (summary["strain"] == strain)
            ]
            values.append(match["cfu_per_ml"].iloc[0] if not match.empty else 0)
        offset = (i - 1) * width
        ax.bar(
            [xi + offset for xi in x],
            values,
            width=width,
            label=STRAIN_LABELS[strain],
            color=STRAIN_COLORS[strain],
        )

    ax.set_xticks(list(x))
    ax.set_xticklabels([c[2] for c in categories])
    ax.set_ylabel("CFU/mL")
    ax.set_title("CFU/mL after norfloxacin and ciprofloxacin treatment")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"Saved {out_path}")


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    growth_df = load_growth_curve()
    plot_growth_curve(
        growth_df, "baseline",
        "Growth curves of PY012, PY001, and MA012 strains (no antibiotic)",
        OUTPUT_DIR / "fig5_growth_curve_control.png",
    )
    plot_growth_curve(
        growth_df, "norfloxacin",
        "Growth curve of bacterial strains treated with norfloxacin",
        OUTPUT_DIR / "fig6_growth_curve_norfloxacin.png",
    )
    plot_growth_curve(
        growth_df, "ciprofloxacin",
        "Growth curve of bacterial strains treated with ciprofloxacin",
        OUTPUT_DIR / "fig7_growth_curve_ciprofloxacin.png",
    )

    cfu_df = load_cfu_data()
    plot_cfu_barchart(cfu_df, OUTPUT_DIR / "fig8_cfu_barchart.png")

    print("\nDone. Figures written to:", OUTPUT_DIR.resolve())


if __name__ == "__main__":
    main()
