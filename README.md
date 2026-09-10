# Artifact Evaluation -- PermiOSAn: Mapping and Measuring iOS and Android Permissions Across Space and Time

This repository contains the code and data to reproduce the results presented in our paper "PermiOSAn: Mapping and Measuring iOS and Android Permissions Across Space and Time".



## Prerequisites

Before running any scripts, ensure you have Python 3 and [Poetry](https://python-poetry.org/docs/#installation) installed, then install the dependencies:

```bash
poetry install
```

Then activate the virtual environment with `poetry shell` before running any of the scripts below, or prefix each command with `poetry run` if you prefer not to activate the shell.


## Reproducing Tables and Figures

To verify the statistics and measurements presented in the paper's tables and figures,
run the following scripts **in order** from the `permission_mapping_test/` directory:

```bash
cd permission_mapping_test
python permission_analysis.py
python process_json.py
python filter_permission_diffs.py
python permission_analysis_statistics.py
```

> **Note:** Scripts must be run sequentially, as each step depends on the output of the previous one.



## Verifying the Jaccard Similarity

To reproduce the Jaccard Similarity scores measuring the degree of overlap between
XPPCs with shared entities, run the following from the `jaccard_similarity/` directory:

```bash
cd jaccard_similarity
python main.py
```



## Verifying Cohen's Kappa

To reproduce the Cohen's Kappa inter-rater reliability score for our codebook-based
permission mapping approach, run the following from the `permission_analysis/` directory:

```bash
cd permission_analysis
python calculate_cohens_kappa.py
```



## Repository Structure

```
.
├── permission_mapping_test/
│   ├── permission_analysis.py
│   ├── process_json.py
│   ├── filter_permission_diffs.py
│   └── permission_analysis_statistics.py
├── jaccard_similarity/
│   └── main.py
└── permission_analysis/
    └── calculate_cohens_kappa.py
```