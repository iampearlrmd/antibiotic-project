# Bacterial DNA Repair as a Cybersecurity Resilience Model

## About This Project

This project bridges my microbiology project on bacterial antibiotic resistance with principles of cybersecurity resilience. I studied how Gram-positive bacteria use DNA repair mechanisms (RecA, AddA) to survive antibiotic attacks — and discovered that the underlying logic is identical to how digital systems use patch management to survive cyberattacks.

## The Core Parallel

| Biology | Cybersecurity |
|---|---|
| Antibiotic (norfloxacin) | Cyberattack / malware |
| DNA damage | System vulnerability |
| RecA / AddA repair genes | Security patches / IDS |
| Bacterial survival (CFU/ml) | System resilience score |
| Wild-type strain | Fully patched system |
| Repair-deficient mutant | Unpatched system |

## My Lab Data

Three bacterial strains tested under norfloxacin attack (7.8 µg/L):

| Strain | Repair Gene | CFU/ml (no drug) | Security Equivalent |
|---|---|---|---|
| PY012 | wild-type | 2,395,000 | Fully patched system |
| PY001 | recA⁻ | 720,000 | Missing one patch layer |
| MA012 | addA⁻ | 610,000 | Missing critical patch |

**Finding:** Strains without repair genes survived at only 30% the rate of wild-type — directly showing how missing a single defense layer collapses overall resilience.

## How to Run

```bash
# Install Python 3 (python.org)
python3 analysis.py
```

## Why This Matters for Cybersecurity

Antibiotic resistance is one of the most studied defense mechanisms in nature. Understanding *why* some systems survive attacks and others do not — whether bacterial or digital — is the foundation of resilience engineering. This project is the start of my journey applying biological thinking to cybersecurity problems, particularly in healthcare and biotech environments where both domains intersect.

## Background

- **Degree:** BSc Microbiology
- **Research focus:** DNA repair mechanisms in Gram-positive bacteria
- **Google Cybersecurity Certificate** (2026)
- **Goal:** MSc Cybersecurity 

## Next Steps

- [ ] Add growth curve data (OD600 over time)
- [ ] Add norfloxacin sensitivity comparison chart
- [ ] Extend model to network intrusion detection datasets
