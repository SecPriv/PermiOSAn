# Artifact Appendix (Required for all badges)

Paper title: **Mapping Android and iOS Permissions Across Space and Time**

Requested Badge(s):
  - [x] **Available**
  - [x] **Functional**
  - [x] **Reproduced**

## Description (Required for all badges)

This codebase is the artifact related to the paper **Mapping Android and iOS Permissions Across Space and Time** (PETS 2027) 
Authors: Magdalena Steinböck, Jakob Bleier, Florian Draschbacher, Christine Utz, Tobias Urban, Martina Lindorfer

The artifact contains the relevant data and scripts to reproduce the Figures and Tables provided in the paper.

### Security/Privacy Issues and Ethical Concerns (Required for all badges)

The artifact raises no ethical concerns or security/privacy issues.

## Basic Requirements (Required for Functional and Reproduced badges)

### Hardware Requirements (Required for Functional and Reproduced badges)

1. Can run on a laptop (No special hardware requirements)
2. The experiments were conducted using a MacBook Pro M1, 16GM RAM, 500GB storage, and verified on a Linux machine with similar specs.

### Software Requirements (Required for Functional and Reproduced badges)

Replace this with the software required to run your artifact and its versions,
as follows.

1. We tested the artifact on macOS Sequoia 15.7.4 as well as on Ubuntu 24.04.
2. The artifact was tested using Python 3.12.4. The required python packages are provided in
   the script files themselves through the `uv` tool.
3. Datasets required to run our artifact are provided in `permission_mapping/permission_analysis/data`.

### Estimated Time and Storage Consumption (Required for Functional and Reproduced badges)

- The overall human and compute times required to run the artifact are about 10 minutes.
- The overall disk space consumed by the artifact is below 1GB.

## Environment (Required for all badges)

In the following, describe how to access your artifact and all related and
necessary data and software components. Afterward, describe how to set up
everything and how to verify that everything is set up correctly.

### Accessibility (Required for all badges)

Our Artifact is available at GitHub under `https://github.com/SecPriv/PermiOSAn/`.

### Set Up the Environment (Required for Functional and Reproduced badges)

To set up our artifact, first clone it from GitHub:

```bash
git clone git@github.com:SecPriv/PermiOSAn.git
```

[Install uv](https://docs.astral.sh/uv/getting-started/installation/), which will manage python and python dependencies for our scripts.

### Testing the Environment (Required for Functional and Reproduced badges)

All scripts are stand-alone, the easiest way to check it works is by running the following commands:

```sh
cd permission-mapping
./calculate_cohens_kappa.py
```

This will run `/usr/bin/env -S uv run --script` as interpreter for the file install dependencies declared in the script block at the top of the file. The expected output is:

```
344
344
0.8630337465564738
```

## Artifact Evaluation (Required for Functional and Reproduced badges)

### Main Results and Claims

List all your paper's results and claims that are supported by your submitted
artifacts.

#### Main Result 1: Reproducing Tables and Figures

By executing Experiment 1, our Figures 2, 3, 4, and 5, as well as our Tables 
2, 3, and 6. The respective functions in the script each describe a Figure or 
Table.

#### Main Result 2: Verifying the Jaccard Similarity

Our paper claims that, across all XPPCs, we observe an average Jaccard
similarity of 0.59 (median: 0.50), indicating a moderate degree of
similarity between the two platforms’ permission-granting entities.
This claim is reproducible by executing our Experiment 2. In this 
Experiment we calculate the Jaccard similarity of all XPPCs based on 
our mapping results (from Table 11).

#### Main Result 3: Verifying Cohen's Kappa

Our paper claims that In 306 (88.4%) cases, the two researchers 
assigned the same group to permissions accross Android and iOS and we 
measured an inter-rater reliability using Cohen’s Kappa (𝜅 = 0.86).
This claim is reproducible by executing our Experiment 3. In this
Experiment we calculate the Cohen's Kappa based on the provided 
group assignments of both coders.


### Experiments
List each experiment to execute to reproduce your results. Describe:
 - How to execute it in detailed steps.
 - What the expected result is.
 - How long it takes to execute in human and compute times (approximately).
 - How much space it consumes on disk (approximately) (omit if <10GB).
 - Which claim and results does it support, and how.

#### Experiment 1: Reproducing Tables and Figures
- Time: < 10m
- Storage: <10GB

To verify the numbers and measurements presented in the paper's tables and figures,
run the following scripts **in order** from the `permission_mapping_test/` directory:

```bash
cd permission_mapping_test
python permission_analysis.py
python process_json.py
python filter_permission_diffs.py
python permission_analysis_statistics.py
```

> **Note:** Scripts must be run sequentially, as each step depends on the output of the previous one.

This generates all tables and figures that were used in the paper. 
The expected result is that the generated figures match the figures from the paper provided in `permission_mapping/permission_analysis/plots_28_07_2026`.

#### Experiment 2: Verifying the Jaccard Similarity

- Time: < 5m
- Storage: <10GB

To reproduce the Jaccard Similarity scores measuring the degree of overlap between
XPPCs with shared entities, run the following from the `jaccard_similarity/` directory:

```bash
cd jaccard_similarity
python main.py
```

This generates the value of the Jaccard Similarity we provide in Chapter 3.3 `Underlying Permission-Granting Mechanisms`.

#### Experiment 3: Verifying Cohen's Kappa
- Time: < 5m
- Storage: <10GB

To reproduce the Cohen's Kappa inter-rater reliability score for our codebook-based
permission mapping approach, run the following from the `permission_analysis/` directory:

```bash
cd permission_analysis
python calculate_cohens_kappa.py
```

This generates the value of the Cohen's Kappa we provide in Chapter 3.2.


## Limitations (Required for Functional and Reproduced badges)

We provide all extracted data and code to reproduce the figures and numbers in the paper. 
The app packages are not public, but can be shared on request together with their static analysis scripts.

## Notes on Reusability (Encouraged for all badges)

Our main contribution that can be reused by other researchers is our permission mapping of 
permissions on Android and iOS, which we provide in a machine-readable json format in
`permission_mapping/permission_analysis/data/permission_mapping.json`.
