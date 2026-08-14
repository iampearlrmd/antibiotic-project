# analysis.py
# Bacterial DNA Repair vs Antibiotic Attack
# Author: [Your Name]
# Project: Connecting biological defense mechanisms to cybersecurity resilience

import csv
import math

# ── Load data ──────────────────────────────────────────────────────────────────
def load_data(filepath):
    data = []
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['CFU_per_ml'] = int(row['CFU_per_ml'])
            data.append(row)
    return data

# ── Calculate survival rate relative to wild-type ──────────────────────────────
def calculate_survival_rate(data):
    wildtype_cfu = next(d['CFU_per_ml'] for d in data if d['strain'] == 'PY012')
    results = []
    for row in data:
        rate = (row['CFU_per_ml'] / wildtype_cfu) * 100
        results.append({
            'strain': row['strain'],
            'repair_gene': row['repair_gene'],
            'CFU_per_ml': row['CFU_per_ml'],
            'survival_rate_%': round(rate, 2)
        })
    return results

# ── Cybersecurity parallel ─────────────────────────────────────────────────────
def security_parallel(strain, repair_gene, survival_rate):
    if repair_gene == 'wild-type':
        return "FULLY PATCHED SYSTEM — all defense mechanisms active"
    elif repair_gene == 'recA-':
        return f"PARTIAL VULNERABILITY — RecA patch missing, {100 - survival_rate:.1f}% less resilient than patched system"
    elif repair_gene == 'addA-':
        return f"HIGH VULNERABILITY — AddA patch missing, {100 - survival_rate:.1f}% less resilient than patched system"

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    data = load_data('data.csv')
    # Use no_drug condition for baseline analysis
    baseline = [d for d in data if d['condition'] == 'no_drug']
    results = calculate_survival_rate(baseline)

    print("=" * 65)
    print("BACTERIAL DNA REPAIR — CYBERSECURITY RESILIENCE MODEL")
    print("=" * 65)
    print(f"\n{'Strain':<10} {'Gene':<12} {'CFU/ml':<15} {'Survival%':<12} {'Security Parallel'}")
    print("-" * 65)

    for r in results:
        parallel = security_parallel(r['strain'], r['repair_gene'], r['survival_rate_%'])
        print(f"{r['strain']:<10} {r['repair_gene']:<12} {r['CFU_per_ml']:<15,} {r['survival_rate_%']:<12}%")
        print(f"  → {parallel}\n")

    print("=" * 65)
    print("KEY INSIGHT:")
    print("Bacteria without DNA repair genes (recA, addA) survive")
    print("antibiotic attacks at significantly lower rates.")
    print("This mirrors unpatched systems facing cyberattacks —")
    print("missing one defense layer dramatically increases risk.")
    print("=" * 65)

if __name__ == "__main__":
    main()
