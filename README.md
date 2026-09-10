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



## Repository Structure

After running the above scripts, the repository will look like this:

```txt
.
├── README.md
├── ARTIFACT-APPENDIX.md
└── permission-mapping
    ├── calculate_cohens_kappa.py
    ├── jaccard_similarity
    │   ├── granting_comparison_by_category.csv
    │   ├── main.py
    │   ├── most_divergent_categories.csv
    │   ├── most_similar_categories.csv
    │   └── Permission_Mapping.csv
    └── permission_analysis
        ├── apps_permission_mapping_stats_2023_28-07-2026.json
        ├── apps_permission_mapping_stats_2024_28-07-2026.json
        ├── apps_permission_mapping_stats_2025_28-07-2026.json
        ├── apps_w_diffs_2023_28-07-2026.json
        ├── apps_w_diffs_2023_bind_28-07-2026.json
        ├── apps_w_diffs_2024_28-07-2026.json
        ├── apps_w_diffs_2024_bind_28-07-2026.json
        ├── apps_w_diffs_2025_28-07-2026.json
        ├── apps_w_diffs_2025_bind_28-07-2026.json
        ├── data
        │   ├── android_intents_2025.json
        │   ├── android_unmapped_permissions.json
        │   ├── filtered_app_ids-(08-08-2025).json
        │   ├── ios_app_store_category_2023.json
        │   ├── ios_entitlements.json
        │   ├── ios_protected_resources.json
        │   ├── ios_unmapped_permissions.json
        │   ├── matches_w_permissions_2023_bind_(28-07-2026).json
        │   ├── matches_w_permissions_2024_bind_(28-07-2026).json
        │   ├── matches_w_permissions_2025_bind_(28-07-2026).json
        │   ├── permission_diffs_2023-filtered-(28-07-2026).json
        │   ├── permission_diffs_2024-filtered-(28-07-2026).json
        │   ├── permission_diffs_2025-filtered-(28-07-2026).json
        │   └── permission_mapping.json
        ├── filter_permission_diffs.py
        ├── get_mapped_unmapped_permissions.py
        ├── get_permission_stats_general.py
        ├── get_permission_stats_no_mapping.py
        ├── get_stats_for_specific_perm.py
        ├── permission_analysis.py
        ├── permission_analysis_statistics.py
        ├── permission_diffs_2023-filtered-(28-07-2026).json
        ├── permission_diffs_2024-filtered-(28-07-2026).json
        ├── permission_diffs_2025-filtered-(28-07-2026).json
        ├── plots_28_07_2026
        │   ├── differences_added_removed_23_24_25-(28-07-2026).pdf
        │   ├── differences_added_removed_23_25-(28-07-2026).pdf
        │   ├── get_permission_cdf_ios_android_2023-(28-07-2026).pdf
        │   ├── get_permission_cdf_ios_android_2024-(28-07-2026).pdf
        │   ├── get_permission_cdf_ios_android_2025-(28-07-2026).pdf
        │   ├── get_permission_distribution_cdf-(28-07-2026)-updated.pdf
        │   ├── jitter_plot_permission_occurrences_2023-(28-07-2026).pdf
        │   ├── jitter_plot_permission_occurrences_2024-(28-07-2026).pdf
        │   ├── jitter_plot_permission_occurrences_2025-(28-07-2026).pdf
        │   ├── permissions_avg_app_store_category_2023-(28-07-2026).pdf
        │   ├── permissions_avg_app_store_category_2024-(28-07-2026).pdf
        │   ├── permissions_avg_app_store_category_2025-(28-07-2026).pdf
        │   ├── permissions_per_category_2023-(28-07-2026)-updated.pdf
        │   ├── permissions_per_category_2024-(28-07-2026)-updated.pdf
        │   └── permissions_per_category_2025-(28-07-2026)-updated.pdf
        ├── plots_28_07_2026_compare
        │   ├── differences_added_removed_23_24_25-(28-07-2026).pdf
        │   ├── differences_added_removed_23_25-(28-07-2026).pdf
        │   ├── get_permission_cdf_ios_android_2023-(28-07-2026).pdf
        │   ├── get_permission_cdf_ios_android_2024-(28-07-2026).pdf
        │   ├── get_permission_cdf_ios_android_2025-(28-07-2026).pdf
        │   ├── get_permission_distribution_cdf-(28-07-2026)-updated.pdf
        │   ├── jitter_plot_permission_occurrences_2023-(28-07-2026).pdf
        │   ├── jitter_plot_permission_occurrences_2024-(28-07-2026).pdf
        │   ├── jitter_plot_permission_occurrences_2025-(28-07-2026).pdf
        │   ├── permissions_per_category_2023-(28-07-2026)-updated.pdf
        │   ├── permissions_per_category_2024-(28-07-2026)-updated.pdf
        │   └── permissions_per_category_2025-(28-07-2026)-updated.pdf
        └── process_json.py


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
