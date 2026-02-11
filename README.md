# AllerScope

**A structural landscape of allergens with epitope-level resolution.**

AllerScope is a structural manifold framework for organizing allergen space.
By integrating protein structure prediction, epitope mapping, and geometry-based comparison, AllerScope enables systematic exploration of structural relationships across allergens — within and across kingdoms.

> **Preprint** KT Kim. _A Structural Landscape of Fungal Allergens with Epitope-Level Resolution Reveals Cross-Kingdom Structural Similarity._ bioRxiv (2026). [doi:10.64898/2026.01.24.701546](https://doi.org/10.64898/2026.01.24.701546)

---

## Overview

<img width="6807" height="3730" alt="GH1" src="https://github.com/user-attachments/assets/9a7f94fa-ca20-4d11-9cd7-967ca7ed7b53" />

AllerScope provides a modular pipeline for:

1. Structure Generation
High-confidence allergen models via ColabFold (AlphaFold2)

2. Epitope-Level Abstraction
B-cell epitope prediction using BepiPred-3.0 and DiscoTope-3.0
Extraction of epitope-restricted structural models

3. Geometric Manifold Construction
Pairwise structural comparison (TM-score)
Distance matrix construction
Low-dimensional embedding at both whole-protein and epitope levels

The current implementation maps fungal allergens as a first charted region of allergen structural space.
The framework itself is organism-agnostic and designed for extension toward a universal allergen atlas.
---

## Repository Structure

```
AllerScope/
├── data/
│   ├── raw/                        # Source sequences and structures
│   │   ├── fungal_allergen/
│   │   ├── fungal_protein/
│   │   └── non-fungal_allergen/
│   └── processed/
│       ├── epitope/                # Epitope predictions (BepiPred, DiscoTope)
│       ├── fungal_allergen_pdb/    # Predicted structures (fungal)
│       ├── non-fungal_allergen_pdb/
│       └── manifold/               # Distance/score matrices
│
└── src/
    ├── structure/                  # Structure prediction & selection
    │   ├── run_colabfold.sh
    │   └── select_best_pdb.py
    ├── epitope/                    # Epitope prediction & PDB extraction
    │   ├── run_bepipred.sh
    │   ├── run_discotope.sh
    │   └── build_epitope_pdb.py
    └── manifold/                   # Manifold construction & clustering
        ├── construct_protein_manifold.py
        ├── construct_epitope_manifold.py
        ├── cluster_protein_manifold.ipynb
        └── cluster_epitope_manifold.ipynb
```
Key outputs defining the structural space:
 - protein_tm_distance_matrix.npy
 - epitope_tm_distance_matrix.npy
 - corresponding TM-score matrices

These matrices represent the geometric foundation of AllerScope.

---

## Getting Started

### Prerequisites

- Python 3.9+
- [ColabFold](https://github.com/sokrypton/ColabFold)
- [BepiPred-3.0](https://services.healthtech.dtu.dk/services/BepiPred-3.0/)
- [DiscoTope-3.0](https://services.healthtech.dtu.dk/services/DiscoTope-3.0/)
- [TM-align](https://zhanggroup.org/TM-align/)

### Installation

```bash
git clone https://github.com/<username>/AllerScope.git
cd AllerScope
pip install -r requirements.txt  # (coming soon)
```

### Usage

```bash
# 1. Predict structures
bash src/structure/run_colabfold.sh
python src/structure/select_best_pdb.py

# 2. Predict epitopes
bash src/epitope/run_bepipred.sh
bash src/epitope/run_discotope.sh
python src/epitope/build_epitope_pdb.py

# 3. Build manifolds
python src/manifold/construct_protein_manifold.py
python src/manifold/construct_epitope_manifold.py
```

---

## Citation

Please cite the associated preprint if this framework contributes to your work.

> KT Kim. "A Structural Landscape of Fungal Allergens with Epitope-Level Resolution Reveals Cross-Kingdom Structural Similarity." _bioRxiv_ (2026). [https://doi.org/10.64898/2026.01.24.701546](https://doi.org/10.64898/2026.01.24.701546)
---
