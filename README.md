# Bacterial DNA Repair as a Cybersecurity Resilience Model

Connecting bacterial antibiotic resistance to cybersecurity.

## About This Project

This project studies how *Bacillus subtilis* (a Gram-positive bacterium) uses DNA
repair machinery — specifically the **homologous recombination (HR)** pathway — to
survive DNA double-strand breaks (DSBs) caused by fluoroquinolone antibiotics
(norfloxacin and ciprofloxacin). The biological findings are framed here as a model
for **resilience in systems under attack**: just as a cell without functioning repair
genes cannot recover from damage and dies, a system without redundancy or self-repair
mechanisms cannot recover from a compromise.

Originally conducted as a senior research project (SMB481 Project in Microbiology,
Department of Microbiology, Faculty of Science, Srinakharinwirot University), the
repository repackages the wet-lab data and analysis for anyone interested in the
biology-to-resilience analogy.

## Background

Double-strand breaks (DSBs) are the most severe form of DNA damage a cell can
experience. In Gram-negative bacteria like *E. coli*, the RecBCD complex processes
broken DNA ends before RecA can perform strand exchange and repair. Gram-positive
bacteria such as *B. subtilis* lack RecBCD, and instead rely on the **AddAB**
complex to perform the same end-resection role, loading RecA onto the exposed
single strand to initiate repair.

This project tests what happens to *B. subtilis* when the genes for these two
"repair" components — `recA` and `addA` — are knocked out, and the cell is then
attacked with DNA-damaging antibiotics.

**Strains used:**
| Strain | Genotype |
|---|---|
| PY012 | Wild-type |
| PY001 | *recA⁻* (RecA knockout) |
| MA012 | *addA⁻* (AddA knockout) |

**Antibiotics tested:** norfloxacin and ciprofloxacin (both fluoroquinolones that
inhibit DNA gyrase / topoisomerase IV, inducing DSBs), each at 7.8 µg/L.

## Methods (Summary)

1. **Growth curve measurement** — OD600 tracked over 0–360 minutes for all three
   strains under normal conditions.
2. **Norfloxacin sensitivity** — strains grown ± norfloxacin, then plated at 10⁻³
   and 10⁻⁴ dilutions; colonies counted (CFU/mL) after 24–48 h.
3. **Ciprofloxacin sensitivity** — same protocol as above, using ciprofloxacin.

Full step-by-step protocols and media recipes (LB agar/broth composition) are in the
appendix of the report.

## Results

- **Growth curves:** Both knockout strains (PY001 *recA⁻* and MA012 *addA⁻*) grew
  measurably slower than wild-type PY012, with MA012 showing the most pronounced
  delay — see `growth_curve.csv` for the raw OD600 time-series data.
- **Norfloxacin sensitivity:** Both knockouts showed significantly reduced CFU/mL
  counts relative to wild-type when exposed to norfloxacin, indicating impaired
  ability to survive DSB damage.
- **Ciprofloxacin sensitivity:** Same pattern held — knockout strains, especially
  MA012, were markedly more sensitive than wild-type.
- **Interpretation:** Both `recA` and `addA` are required for effective homologous
  recombination repair of antibiotic-induced DSBs in *B. subtilis*. Loss of either
  gene compromises growth and survival under DNA-damaging stress.

Raw counts, plate images, and CFU calculations are available in the full report.
Growth curve and colony-count data used to generate the figures live in
`growth_curve.csv` and `data.csv`; the analysis pipeline is in `analysis.py`.

## Repository Structure

```
.
├── analysis.py          # Growth curve / CFU analysis scripts
├── data.csv             # Raw experimental data
├── growth_curve.csv      # OD600 time-series data
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```


## Why This Matters for Cybersecurity

Antibiotic resistance is one of the most studied defense mechanisms in nature. Understanding *why* some systems survive attacks and others do not — whether bacterial or digital — is the foundation of resilience engineering. This project is the start of my journey applying biological thinking to cybersecurity problems, particularly in healthcare and biotech environments where both domains intersect.

## Background

- **Degree:** BSc Microbiology
- **Research focus:** DNA repair mechanisms in Gram-positive bacteria
- **Google Cybersecurity Certificate** (2026)
- **Goal:** MSc Cybersecurity 


## Citation / Source

Adapted from: *"A study of cellular DNA repair mechanisms that enable Gram positive
bacteria to resist certain antibiotics"* — SMB481 Project in Microbiology, B.Sc.
Microbiology, Faculty of Science, Srinakharinwirot University, Academic Year 2024
(2567 BE).

## License

Released under the [MIT License](LICENSE).
