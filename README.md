# Artifact Evaluation -- PermiOSAn: Mapping and Measuring iOS and Android Permissions Across Space and Time

This repository contains the code and data to reproduce the results presented in our paper "PermiOSAn: Mapping and Measuring iOS and Android Permissions Across Space and Time".



## Prerequisites

Before running any scripts, ensure you have Python 3 and [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

The scripts use uv's hashbang execution and should install dependencies automatically.


## Reproducing Tables and Figures

To verify the statistics and measurements presented in the paper's tables and figures,
run the following scripts **in order** from the `permission-mapping/permission_analysis/` directory:

```bash
cd permission-mapping/permission_analysis
./permission_analysis.py
./process_json.py
./filter_permission_diffs.py
./permission_analysis_statistics.py
```

> **Note:** Scripts must be run sequentially, as each step depends on the output of the previous one.



## Verifying the Jaccard Similarity

To reproduce the Jaccard Similarity scores measuring the degree of overlap between
XPPCs with shared entities, run the following from the `permission-mapping/jaccard_similarity/` directory:

```bash
cd permission-mapping/jaccard_similarity
./main.py
```



## Verifying Cohen's Kappa

To reproduce the Cohen's Kappa inter-rater reliability score for our codebook-based
permission mapping approach, run the following from the `permission_analysis/` directory:

```bash
cd permission-analysis
./calculate_cohens_kappa.py
```

