# Contributing to Antibiotic-Cyber Model

Thanks for your interest in this project! It started as a senior research project on
bacterial DNA repair (*B. subtilis* `recA`/`addA` knockouts and antibiotic
sensitivity), reframed here as an open resource on biological resilience models.
Contributions are welcome, especially from people working at the intersection of biology and cybersecurity.

## Who Should Contribute

- Microbiologist interested in cybersecurity
- Anyone working on healthcare or lab infrastructure security


## How to Contribute

1. **Fork** the repository and create a new branch for your change:
   ```bash
   git checkout -b your-feature-name
   ```
2. **Make your changes.** This could include:
   - Improvements to `analysis.py` (plotting, statistics, additional CFU/OD600
     calculations)
   - Corrections or additions to `data.csv` / `growth_curve.csv`
   - Documentation fixes or clarifications in `README.md`
   - Extending the resilience-model analogy with new material
3. **Test your changes** before submitting — if you modify `analysis.py`, make sure
   it still runs cleanly against `data.csv` and `growth_curve.csv` and reproduces the
   existing figures.
4. **Commit with a clear message:**
   ```bash
   git commit -m "Fix CFU calculation for 10^-4 dilution"
   ```
5. **Open a pull request** describing what you changed and why.

## Reporting Issues

If you spot an error in the data, analysis, or documentation, please open an issue
with:
- A short description of the problem
- The relevant file(s) and line/section
- Suggested fix, if you have one

## Code Style

- Python code should be readable and commented, especially around unit conversions
  (CFU/mL, dilution factors, OD600 timepoints).
- Keep raw experimental data (`data.csv`, `growth_curve.csv`) unmodified — if you
  need to correct an entry, note the change and reasoning in your PR description.

## Code of Conduct

Be respectful and constructive. This project touches on academic research data —
please handle corrections and disagreements collegially.
