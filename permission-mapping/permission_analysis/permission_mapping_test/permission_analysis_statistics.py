import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import statistics
import json

DATE = "28-07-2026"
PLOT_FOLDER_PATH = "./plots_28_07_2026_no_mongo"
os.makedirs(PLOT_FOLDER_PATH, exist_ok=True)


with open(f"./data/permissions_paper.permission_diffs_2023-filtered-({DATE}).json") as fp:
    collection_2023 = json.load(fp)

with open(f"./data/permissions_paper.permission_diffs_2024-filtered-({DATE}).json") as fp:
    collection_2024 = json.load(fp)

with open(f"./data/permissions_paper.permission_diffs_2025-filtered-({DATE}).json") as fp:
    collection_2025 = json.load(fp)



# Groups app pairs by the number of keys in permission_diffs, counts each group
def _agg_independent_distribution_diffs_year(collection):
    counter = Counter()
    for doc in collection:
        n_diffs = len(doc.get("permission_diffs", {}))
        counter[n_diffs] += 1
    return sorted([{"_id": k, "number": v} for k, v in counter.items()], key=lambda x: x["_id"])


def get_permission_distribution_of_differences_per_year():
    res_indep_dist_diffs_2023 = _agg_independent_distribution_diffs_year(collection_2023)
    res_indep_dist_diffs_2024 = _agg_independent_distribution_diffs_year(collection_2024)
    res_indep_dist_diffs_2025 = _agg_independent_distribution_diffs_year(collection_2025)

    print("Distribution permission diffs in 2023:")
    sum_2023 = 0
    for doc in res_indep_dist_diffs_2023:
        print(doc)
        sum_2023 += doc["number"]
    print(f"Total diffs in 2023: {sum_2023}")
    print("----------------------------------")
    print("Distribution permission diffs in 2024:")
    sum_2024 = 0
    for doc in res_indep_dist_diffs_2024:
        print(doc)
        sum_2024 += doc["number"]
    print(f"Total diffs in 2024: {sum_2024}")
    print("----------------------------------")
    print("Distribution permission diffs in 2024:")
    sum_2025 = 0
    for doc in res_indep_dist_diffs_2025:
        print(doc)
        sum_2025 += doc["number"]
    print(f"Total diffs in 2025: {sum_2025}")
    print("__________________________________")
    print("Considering only pairs 2023 -> 2024 -> 2025")



def get_permission_distribution_cdf():
    res_dist_diffs_2023 = _agg_independent_distribution_diffs_year(collection_2023)
    res_dist_diffs_2024 = _agg_independent_distribution_diffs_year(collection_2024)
    res_dist_diffs_2025 = _agg_independent_distribution_diffs_year(collection_2025)

    print("Distribution 2023 -> 2024 of 2023:")
    sum_2023 = 0
    numbers_cdf_2023 = []
    for doc in res_dist_diffs_2023:
        print(doc)
        sum_2023 += doc["number"]
        numbers_cdf_2023.append(doc)
    print(f"Total: {sum_2023}")
    print("----------------------------------")
    print("Distribution 2023 -> 2024 of 2024:")
    sum_2024 = 0
    numbers_cdf_2024 = []
    for doc in res_dist_diffs_2024:
        print(doc)
        sum_2024 += doc["number"]
        numbers_cdf_2024.append(doc)
    print(f"Total: {sum_2024}")
    print("----------------------------------")
    print("Distribution 2024 -> 2025 of 2025:")
    sum_2025 = 0
    numbers_cdf_2025 = []
    for doc in res_dist_diffs_2025:
        print(doc)
        sum_2025 += doc["number"]
        numbers_cdf_2025.append(doc)
    print(f"Total: {sum_2025}")
    df_cdf_2023 = pd.DataFrame(numbers_cdf_2023)
    df_cdf_2024 = pd.DataFrame(numbers_cdf_2024)
    df_cdf_2025 = pd.DataFrame(numbers_cdf_2025)
    df_cdf_2023 = df_cdf_2023.sort_values(by='_id').reset_index(drop=True)
    df_cdf_2024 = df_cdf_2024.sort_values(by='_id').reset_index(drop=True)
    df_cdf_2025 = df_cdf_2025.sort_values(by='_id').reset_index(drop=True)

    stats_df = pd.concat([df_cdf_2023.rename(columns={"number": "f_2023"}).set_index('_id'),
                          df_cdf_2024.rename(columns={"number": "f_2024"}).set_index('_id'),
                          df_cdf_2025.rename(columns={"number": "f_2025"}).set_index('_id')],
                          axis=1)
    stats_df = stats_df.fillna(0)
    # PDF
    stats_df['pdf_2023'] = stats_df['f_2023'] / sum(stats_df['f_2023'])
    stats_df['pdf_2024'] = stats_df['f_2024'] / sum(stats_df['f_2024'])
    stats_df['pdf_2025'] = stats_df['f_2025'] / sum(stats_df['f_2025'])
    # CDF
    stats_df['cdf_2023'] = stats_df['pdf_2023'].cumsum()
    stats_df['cdf_2024'] = stats_df['pdf_2024'].cumsum()
    stats_df['cdf_2025'] = stats_df['pdf_2025'].cumsum()
    print(stats_df)

    fig, ax = plt.subplots(figsize=(15, 7))
    colors = sns.color_palette("colorblind", 3)
    ax.plot(stats_df.index.to_list(), stats_df['cdf_2023'], drawstyle='steps-post', label="2023", color=colors[0], linestyle='-.', linewidth=5)
    ax.plot(stats_df.index.to_list(), stats_df['cdf_2024'], drawstyle='steps-post', label="2024", color=colors[1], linestyle='--', linewidth=5)
    ax.plot(stats_df.index.to_list(), stats_df['cdf_2025'], drawstyle='steps-post', label="2025", color=colors[2], linestyle=':', linewidth=5)
    plt.xticks(range(0,13), fontsize=22)
    plt.yticks(np.arange(0,1.1,0.1), fontsize=22)
    plt.xlabel('# of Differences', fontsize=22)
    plt.ylabel('CDF', fontsize=22)
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.25, zorder=0)
    plt.legend(fontsize=22)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"get_permission_distribution_cdf-({DATE})-updated.pdf"), format="pdf")

    print("__________________________________")


# Compares n_diffs of the base obj vs the nested sub-obj keyed by year, groups by (n_diffs_base - n_diffs_other), keeps only rows that differ
def _agg_apps_where_number_diff_changed(collection, year):
    counter = Counter()
    for doc in collection:
        n_diffs = len(doc.get("permission_diffs", {}))
        other = doc.get(str(year), {})
        n_diffs_other = len(other.get("permission_diffs", {}))
        if n_diffs != n_diffs_other:
            counter[n_diffs - n_diffs_other] += 1
    return sorted([{"_id": k, "number": v} for k, v in counter.items()], key=lambda x: x["_id"])


# Keeps only app pairs where n_diffs is equal between base and nested `to` obj, then checks whether the set of category keys is also the same and groups by that boolean
def _agg_apps_where_number_diffs_not_change(collection, frm, to):
    counter = Counter()
    for doc in collection:
        n_diffs = len(doc.get("permission_diffs", {}))
        other = doc.get(str(to), {})
        n_diffs_other = len(other.get("permission_diffs", {}))
        if n_diffs != n_diffs_other:
            continue  # only keep equal-count docs
        y_fields = set(doc.get("permission_diffs", {}).keys())
        to_fields = set(other.get("permission_diffs", {}).keys())
        same_keys = str(y_fields == to_fields)
        counter[same_keys] += 1
    return [{"_id": k, "number": v} for k, v in counter.items()]


def get_changes_of_permission_diffs():
    print("Apps with diff change between 2023-2024:")
    res_diff_2023_2024 = _agg_apps_where_number_diff_changed(collection_2023, 2024)
    sum = 0
    sum_neg = 0
    for doc in res_diff_2023_2024:
        print(doc)
        if int(doc["_id"]) < 0:
            sum_neg += doc["number"]
        sum += doc["number"]
    print(f"Total apps with diffs: {sum}")
    print(f"Apps with MORE (2024) diffs than in 2023: {sum-sum_neg}")
    print(f"Apps with LESS (2024) diffs than in 2023: {sum_neg}")
    print("----------------------------------")
    res_diff_2024_2025 = _agg_apps_where_number_diff_changed(collection_2024, 2025)
    sum = 0
    sum_neg = 0
    for doc in res_diff_2024_2025:
        print(doc)
        if int(doc["_id"]) < 0:
            sum_neg += doc["number"]
        sum += doc["number"]
    print(f"Total apps with diffs: {sum}")
    print(f"Apps with MORE (2025) diffs than in 2024: {sum-sum_neg}")
    print(f"Apps with LESS (2025) diffs than in 2024: {sum_neg}")
    print("----------------------------------")
    print("Apps with no diff change between 2023-2024:")
    res_no_diff_2023_2024 = _agg_apps_where_number_diffs_not_change(collection_2023, 2023, 2024)
    sum = 0
    for doc in res_no_diff_2023_2024:
        if doc["_id"] == "True":
            print(f"Apps with the same diffs: {doc['number']}")
        else:
            print(f"Apps with different diffs: {doc['number']}")
        sum += doc["number"]
    print(f"Total apps with no diffs: {sum}")
    print("----------------------------------")
    print("Apps with no diff change between 2024-2025:")
    res_no_diff_2024_2025 = _agg_apps_where_number_diffs_not_change(collection_2024, 2024, 2025)
    sum = 0
    for doc in res_no_diff_2024_2025:
        if doc["_id"] == "True":
            print(f"Apps with the same diffs: {doc['number']}")
        else:
            print(f"Apps with different diffs: {doc['number']}")
        sum += doc["number"]
    print(f"Total apps with no diffs: {sum}")

    print("__________________________________")


# Filters app pairs with non-empty permission_diffs, then for each category entry counts: total occurrences, android non-empty, ios non-empty
def _agg_distribution_of_diffs_among_permission_categories(collection):
    agg = defaultdict(lambda: {"docCount": 0, "android_non_empty": 0, "ios_non_empty": 0})
    for doc in collection:
        perm_diffs = doc.get("permission_diffs", {})
        if not perm_diffs:
            continue
        for category, v in perm_diffs.items():
            agg[category]["docCount"] += 1
            if len(v.get("android", [])) > 0:
                agg[category]["android_non_empty"] += 1
            if len(v.get("ios", [])) > 0:
                agg[category]["ios_non_empty"] += 1
    return sorted(
        [{"_id": cat, **counts} for cat, counts in agg.items()],
        key=lambda x: -x["docCount"]
    )


def get_differences_among_categories():
    print("Distribution of differences among permission categories in 2023:")
    for doc in _agg_distribution_of_diffs_among_permission_categories(collection_2023):
        print(doc)

    print("----------------------------------")
    print("Distribution of differences among permission categories in 2024:")
    for doc in _agg_distribution_of_diffs_among_permission_categories(collection_2024):
        print(doc)

    print("----------------------------------")
    print("Distribution of differences among permission categories in 2025:")
    for doc in _agg_distribution_of_diffs_among_permission_categories(collection_2025):
        print(doc)

    print("__________________________________")


# Merges common_permissions + permission_diffs per app pair, then for each category, collects the set of ios_ids that have that category
def _agg_distribution_of_categories_per_year(collection):
    agg = defaultdict(set)
    for doc in collection:
        ios_id = doc.get("ios_id")
        merged = {**doc.get("common_permissions", {}), **doc.get("permission_diffs", {})}
        for category in merged:
            agg[category].add(ios_id)
    return sorted(
        [{"_id": cat, "app_ids": list(ids)} for cat, ids in agg.items()],
        key=lambda x: x["_id"]
    )


def plot_differences_added_removed_across_categories():
    print("Distribution of differences among permission categories between 2023 - 2025:")
    res_diff_categories_2023 = _agg_distribution_of_categories_per_year(collection_2023)
    res_diff_categories_2024 = _agg_distribution_of_categories_per_year(collection_2024)
    res_diff_categories_2025 = _agg_distribution_of_categories_per_year(collection_2025)


    # Build lookup dicts for O(1) access
    dict_2023 = {d["_id"]: set(d["app_ids"]) for d in res_diff_categories_2023}
    dict_2024 = {d["_id"]: set(d["app_ids"]) for d in res_diff_categories_2024}
    dict_2025 = {d["_id"]: set(d["app_ids"]) for d in res_diff_categories_2025}

    # 2023-2024
    added_data_2023_2024 = {}
    removed_data_2023_2024 = {}
    for cat in dict_2023:
        if cat in dict_2024:
            added_data_2023_2024[cat] = len(dict_2024[cat] - dict_2023[cat])
            removed_data_2023_2024[cat] = -1 * len(dict_2023[cat] - dict_2024[cat])
    print("---------------------------------------------")
    print("2023-2024:")
    print("ADDED")
    print(added_data_2023_2024)
    print("REMOVED")
    print(removed_data_2023_2024)

    # 2024-2025
    added_data_2024_2025 = {}
    removed_data_2024_2025 = {}
    for cat in dict_2024:
        if cat in dict_2025:
            added_data_2024_2025[cat] = len(dict_2025[cat] - dict_2024[cat])
            removed_data_2024_2025[cat] = -1 * len(dict_2024[cat] - dict_2025[cat])
    print("---------------------------------------------")
    print("2024-2025:")
    print("ADDED")
    print(added_data_2024_2025)
    print("REMOVED")
    print(removed_data_2024_2025)

    # 2023-2025
    added_data_2023_2025 = {}
    removed_data_2023_2025 = {}
    for cat in dict_2023:
        if cat in dict_2025:
            added_data_2023_2025[cat] = len(dict_2025[cat] - dict_2023[cat])
            removed_data_2023_2025[cat] = -1 * len(dict_2023[cat] - dict_2025[cat])
    print("---------------------------------------------")
    print("2023-2024:")
    print("ADDED")
    print(added_data_2023_2025)
    print("REMOVED")
    print(removed_data_2023_2025)
    print("---------------------------------------------")

    categories = set(dict_2023.keys())
    added_val_23_24, added_val_24_25, removed_val_23_24, removed_val_24_25, cats, both_23 = [], [], [], [], [], []
    for category in categories:
        cats.append(category)
        added_val_23_24.append(added_data_2023_2024[category])
        added_val_24_25.append(added_data_2024_2025[category])
        removed_val_23_24.append(removed_data_2023_2024[category])
        removed_val_24_25.append(removed_data_2024_2025[category])
        both_23.append(added_data_2023_2024[category] - removed_data_2023_2024[category])

    df_1 = pd.DataFrame({
        'categories': cats,
        'added_val_23_24': added_val_23_24,
        'removed_val_23_24': removed_val_23_24,
        'added_val_24_25': added_val_24_25,
        'removed_val_24_25': removed_val_24_25,
        'both_23': both_23
        })
    df_1 = df_1.sort_values('both_23', ascending=False).reset_index(drop=True)

    net_23_24  = [(df_1['added_val_23_24'][i] + df_1['removed_val_23_24'][i]) for i in range(0, len(added_val_23_24))]
    net_24_25 = [(df_1['added_val_24_25'][i] + df_1['removed_val_24_25'][i]) for i in range(0, len(added_val_24_25))]

    x = range(len(categories))
    fig, ax = plt.subplots(figsize=(12, 5))
    bar_width = 0.45
    # Offset positions for 2023 and 2024
    x_2023 = [i - bar_width/2 for i in x]
    x_2024 = [i + bar_width/2 for i in x]
    plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
    # Plot 2023 bars
    ax.bar(x_2023, df_1['added_val_23_24'], width=bar_width, color="#6C6C6C",
        edgecolor="black", linewidth=0.5, label="added 2024", zorder=2)
    ax.bar(x_2023, df_1['removed_val_23_24'], width=bar_width, color="#C6C6C6",
        edgecolor="black", linewidth=0.5, label="removed 2024", zorder=2)
    
    # Plot 2024 bars
    ax.bar(x_2024, df_1['added_val_24_25'], width=bar_width, color="#6C6C6C",
        edgecolor="black", linewidth=0.5, label="added 2025", zorder=2, hatch="//")
    ax.bar(x_2024, df_1['removed_val_24_25'], width=bar_width, color="#C6C6C6",
        edgecolor="black", linewidth=0.5, label="removed 2025", zorder=2, hatch="//")
    
    plt.subplots_adjust(bottom=0.29)
    plt.axhline(0, color='black')
    plt.xticks(x, fontsize=16)
    plt.yticks(fontsize=14)
    ax.set_xticklabels(df_1['categories'], rotation=45, ha='right')
    for i in range(0, len(net_23_24)):
        plt.text(x_2023[i], df_1['added_val_23_24'][i] + 2, f'{net_23_24[i]:+}',
                va='center', ha='center', fontsize=9, zorder=3)
        plt.text(x_2024[i], df_1['added_val_24_25'][i] + 2, f'{net_24_25[i]:+}',
                va='center', ha='center', fontsize=9, zorder=3)
    plt.legend(fontsize=16)
    plt.margins(x=0.01)
    plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"differences_added_removed_23_24_25-({DATE}).pdf"), format="pdf")

    added_val_23_25, removed_val_23_25, cats, both = [], [], [], []
    for category in categories:
            if category == "Telephony Services":
                cats.append("Tel. Services")
            elif category == "Accessory Setup":
                cats.append("Acc. Setup")
            elif category == "Device Management":
                cats.append("Device Mgmt.")
            else:
                cats.append(category)
            added_val_23_25.append(added_data_2023_2025[category])
            removed_val_23_25.append(removed_data_2023_2025[category])
            both.append(added_data_2023_2025[category] - removed_data_2023_2025[category])

    df_2 = pd.DataFrame({'categories': cats, 'added_val_23_25': added_val_23_25, 'removed_val_23_25': removed_val_23_25, 'both': both})
    df_2 = df_2.sort_values('both', ascending=False).reset_index(drop=True)
    net_23_25 = [(df_2['added_val_23_25'][i] + df_2['removed_val_23_25'][i]) for i in range(0, len(added_val_23_25))]

    fig, ax = plt.subplots(figsize=(12, 5))
    plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
    plt.subplots_adjust(bottom=0.28)
    bar_width = 0.9
    x_2025 = [i for i in x]
    ax.bar(x_2025, df_2['added_val_23_25'], width=bar_width, color="#6C6C6C",
        edgecolor="black", linewidth=0.5, label="added 2025", zorder=2)
    ax.bar(x_2025, df_2['removed_val_23_25'], width=bar_width, color="#C6C6C6",
        edgecolor="black", linewidth=0.5, label="removed 2025", zorder=2)
    plt.axhline(0, color='black')
    plt.xticks(x)
    plt.yticks(fontsize=14)
    ax.set_xticklabels(df_2['categories'], rotation=45, ha='right', fontsize=16)
    for i in range(0, len(net_23_25)):
        plt.text(x_2025[i], df_2['added_val_23_25'][i] + 5, f'{net_23_25[i]:+}',
                va='center', ha='center', fontsize=12, zorder=3)
    plt.legend(fontsize=16)
    ax.tick_params(axis='x', pad=0)
    plt.margins(x=0.001)
    plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"differences_added_removed_23_25-({DATE}).pdf"), format="pdf")


# Merges common_permissions + permission_diffs, then for each category collects, the sets of ios_ids that have a non-empty android/ios list
def _agg_app_permissions_per_mapping_category(collection):
    android_sets = defaultdict(set)
    ios_sets = defaultdict(set)
    for doc in collection:
        ios_id = doc.get("ios_id")
        merged = {**doc.get("permission_diffs", {}), **doc.get("common_permissions", {})}
        for category, v in merged.items():
            if len(v.get("android", [])) > 0:
                android_sets[category].add(ios_id)
            if len(v.get("ios", [])) > 0:
                ios_sets[category].add(ios_id)
    all_cats = set(android_sets.keys()) | set(ios_sets.keys())
    return sorted(
        [{"category": cat,
          "android_non_empty": list(android_sets[cat]),
          "ios_non_empty": list(ios_sets[cat])}
         for cat in all_cats],
        key=lambda x: x["category"]
    )


# For each app pair, counts how many categories have a non-empty android/ios list, across the merged (common_permissions + permission_diffs) object
def _agg_jitter_plot_data(collection):
    results = []
    for doc in collection:
        merged = {**doc.get("common_permissions", {}), **doc.get("permission_diffs", {})}
        android_count = sum(1 for v in merged.values() if len(v.get("android", [])) > 0)
        ios_count = sum(1 for v in merged.values() if len(v.get("ios", [])) > 0)
        results.append({"androidCount": android_count, "iosCount": ios_count})
    return results


def jitter_plot_about_permission_occurrences():
    def _jitter_plot(cursor, year: int):
        jitter_df = pd.DataFrame(list(cursor))

        # Add jitter
        jitter_strength = 0.3
        jitter_df['android_jitter'] = jitter_df['androidCount'] + np.random.uniform(-jitter_strength, jitter_strength, size=len(jitter_df))
        jitter_df['ios_jitter'] = jitter_df['iosCount'] + np.random.uniform(-jitter_strength, jitter_strength, size=len(jitter_df))

        # Plot
        plt.figure(figsize=(5, 5))
        plt.axline((0, 0), slope=1, color="grey", linestyle="--", linewidth=1)
        plt.grid(True, linestyle='--', alpha=0.5, zorder=-1)
        plt.scatter(jitter_df['ios_jitter'], jitter_df['android_jitter'], alpha=0.6, edgecolor='black', zorder=2, color="#006172")
        plt.xlabel("iOS", fontsize=14)
        plt.ylabel("Android", fontsize=14)
        plt.ylim(-1, 16)
        plt.xticks(range(0,17), fontsize=12)
        plt.yticks(range(0,17), fontsize=12)
        plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"jitter_plot_permission_occurrences_{year}-({DATE}).pdf"), format="pdf")

    _jitter_plot(_agg_jitter_plot_data(collection_2023), 2023)
    _jitter_plot(_agg_jitter_plot_data(collection_2024), 2024)
    _jitter_plot(_agg_jitter_plot_data(collection_2025), 2025)


def cdf_permission_usage_android_ios():
    def _cdf_plot(cursor, year):
        android = []
        ios = []
        for item in cursor:
            android.append(item['androidCount'])
            ios.append(item['iosCount'])

        android_c = Counter(android)
        ios_c = Counter(ios)

        print(android_c)

        df_android = pd.DataFrame({"_id": android_c.keys(), "android": android_c.values()}).sort_values('_id').reset_index(drop=True)
        df_ios = pd.DataFrame({"_id": ios_c.keys(), "ios": ios_c.values()}).sort_values('_id').reset_index(drop=True)

        stats_df = pd.concat([df_android.set_index('_id'), df_ios.set_index('_id')], axis=1)
        stats_df = stats_df.fillna(0)
        # PDF
        stats_df['pdf_android'] = stats_df['android'] / sum(stats_df['android'])
        stats_df['pdf_ios'] = stats_df['ios'] / sum(stats_df['ios'])
        # CDF
        stats_df['cdf_android'] = stats_df['pdf_android'].cumsum()
        stats_df['cdf_ios'] = stats_df['pdf_ios'].cumsum()
        print(stats_df)

        fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
        colors = sns.color_palette("colorblind", 3)
        ax.plot(stats_df.index.to_list(), stats_df['cdf_android'], drawstyle='steps-post', label="Android", color=colors[0])
        ax.plot(stats_df.index.to_list(), stats_df['cdf_ios'], drawstyle='steps-post', label="iOS", color=colors[1])
        plt.axvline(stats_df[stats_df['cdf_android'] >= 0.99].index.values[0], color=colors[0], linestyle='--', label='99th percentile Android')
        plt.axvline(stats_df[stats_df['cdf_ios'] >= 0.99].index.values[0], color=colors[1], linestyle='--', label='99th percentile iOS')
        plt.axvline(stats_df[stats_df['cdf_android'] >= 0.10].index.values[0], color=colors[0], linestyle=':', label='10th percentile Android')
        plt.axvline(stats_df[stats_df['cdf_ios'] >= 0.10].index.values[0], color=colors[1], linestyle=':', label='10th percentile iOS')
        plt.xticks(range(0,16), fontsize=14)
        plt.yticks(np.arange(0,1.1,0.1), fontsize=14)
        plt.xlabel('# of Permission Categories', fontsize=14)
        plt.ylabel('CDF', fontsize=14)
        plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.25, zorder=0)
        plt.legend(loc="lower right", fontsize=14, framealpha=1, markerscale=1)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"get_permission_cdf_ios_android_{year}-({DATE}).pdf"), format="pdf")

    _cdf_plot(_agg_jitter_plot_data(collection_2023), 2023)
    _cdf_plot(_agg_jitter_plot_data(collection_2024), 2024)
    _cdf_plot(_agg_jitter_plot_data(collection_2025), 2025)


# Iterates over permission_diffs per app pair, counts total occurrences and, how many have non-empty android/ios lists per category, returns top 5
def _agg_get_top_most_differences(collection):
    agg = defaultdict(lambda: {"android_count": 0, "ios_count": 0, "count": 0})
    for doc in collection:
        for category, v in doc.get("permission_diffs", {}).items():
            agg[category]["count"] += 1
            if len(v.get("android", [])) > 0:
                agg[category]["android_count"] += 1
            if len(v.get("ios", [])) > 0:
                agg[category]["ios_count"] += 1
    results = sorted(
        [{"_id": cat, **counts} for cat, counts in agg.items()],
        key=lambda x: -x["count"]
    )
    return results[:5]


def plot_top_5_different_categories_per_year():
    def _plot_top_differences(results, year):
        categories = {}
        for doc in results:
            categories[doc['_id']] = {
                'counts': doc['count'],
                'android': doc['android_count'],
                'ios': doc['ios_count']
            }
        df = pd.DataFrame().from_dict(categories, orient="index")

        print(df)

        fig, ax = plt.subplots(figsize=(5, 4))
        p = ax.bar(df.index, df['counts'], color="#6C6C6C", edgecolor="black")
        plt.title(f"Top 5 Permission Categories with Most Differences ({year})", fontsize=10)
        plt.ylabel("Number of Apps with Differences", fontsize=9)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        ax.bar_label(p)
        #plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"top_5_different_categories_{year}-({DATE}).pdf"), format="pdf")
        return df

    years = {
        "2023": collection_2023,
        "2024": collection_2024,
        "2025": collection_2025,
    }

    global_df = pd.DataFrame()

    for year, col in years.items():
        top = _agg_get_top_most_differences(col)
        df = _plot_top_differences(top, year)
        global_df = pd.concat([global_df, df.rename(columns={"counts": f"counts_{year}", "ios": f"ios_{year}", "android": f"android_{year}"})], axis=1)
        global_df[f'android_{year}_%'] = global_df[f'android_{year}'] / global_df[f'counts_{year}'] * 100
        global_df[f'android_{year}_%'] = global_df[f'android_{year}_%'].round(1)
        global_df[f'ios_{year}_%'] = global_df[f'ios_{year}'] / global_df[f'counts_{year}'] * 100
        global_df[f'ios_{year}_%'] = global_df[f'ios_{year}_%'].round(1)
        global_df

    print(global_df.iloc[:, [0, 1, 3, 2, 4, 5, 6, 8, 7, 9, 10, 11, 13, 12, 14]].to_latex(index=True))


def plot_permissions_per_category_and_ios_android_per_year():
    def _bar_plot(results, year):
        categories = []
        ios = []
        android = []
        both = []
        for doc in results:
            categories.append(doc['category'])
            both_set = set(doc['ios_non_empty']) & set(doc['android_non_empty'])
            both.append(len(both_set))
            ios_only = set(doc['ios_non_empty']).difference(both_set)
            ios.append(len(ios_only))
            android_only = set(doc['android_non_empty']).difference(both_set)
            android.append(len(android_only))

        categories_shortened = []
        for category in categories:
            if category == "Telephony Services":
                categories_shortened.append("Tel. Services")
            elif category == "Accessory Setup":
                categories_shortened.append("Acc. Setup")
            elif category == "Device Management":
                categories_shortened.append("Device Mgmt.")
            else:
                categories_shortened.append(category)

        df = pd.DataFrame(
            {'categories': categories_shortened,
            'ios': ios,
            'android': android,
            'both': both
            })
        df = df.sort_values(by=['both'], ascending=False)

        fig, ax = plt.subplots(figsize=(8, 3.5))
        plt.subplots_adjust(bottom=0.25)
        w = 0.45
        x_1 = [i - w/2 for i in range(len(categories))]
        x_2 = [i + w/2 for i in range(len(categories))]

        ax.bar(x_1, df['both'], width=w, color="#202020", edgecolor="black", label="Both")
        ax.bar(x_1, df['android'], bottom=df['both'], width=w, color="#727272", edgecolor="black", label="Android")
        ax.bar(x_2, df['both'], width=w, color="#202020", edgecolor="black")
        ax.bar(x_2, df['ios'], bottom=df['both'], width=w, color="#CACACA", edgecolor="black", label="iOS")
        ax.tick_params(axis='x', pad=0)

        print(df)

        plt.ylabel("Number of Apps", fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        ax.set_xticks(range(len(categories)))
        ax.set_yticks(np.arange(0, 3500, 500))
        plt.yticks(fontsize=14)
        ax.set_xticklabels(df['categories'], rotation=45, ha='right', fontsize=14)
        ax.legend(fontsize=14)
        plt.tight_layout()
        plt.margins(x=0.01)
        plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"permissions_per_category_{year}-({DATE})-updated.pdf"), format="pdf")

    years = {
        "2023": collection_2023,
        "2024": collection_2024,
        "2025": collection_2025,
    }
    for year, col in years.items():
        top = _agg_app_permissions_per_mapping_category(col)
        _bar_plot(top, year)


def _load_metadata_lookup(path):
    try:
        with open(path) as fp:
            metadata = json.load(fp)
        return {doc["app_id"]: doc.get("app_store_category") for doc in metadata}
    except FileNotFoundError:
        print(f"WARNING: Metadata file not found at {path}. plot_permission_cats_per_app_store_category will be skipped.")
        return None


def _agg_get_permission_cat_number_and_app_store_category_per_app(collection, metadata_lookup):
    results = []
    for doc in collection:
        ios_id = doc.get("ios_id")
        # only skip apps that have no entry in the metadata json at all
        if ios_id not in metadata_lookup:
            print(f'iOS ID is not in metdata: {ios_id}')
            continue
        genre = metadata_lookup[ios_id]
        merged = {**doc.get("permission_diffs", {}), **doc.get("common_permissions", {})}
        android_count = sum(1 for v in merged.values() if len(v.get("android", [])) > 0)
        ios_count = sum(1 for v in merged.values() if len(v.get("ios", [])) > 0)
        results.append({
            "_id": ios_id,
            "docCount": len(merged),
            "android_non_empty": android_count,
            "ios_non_empty": ios_count,
            "genre": genre,
        })
    return results


def  plot_permission_cats_per_app_store_category():
    metadata_lookup = _load_metadata_lookup(f"./data/permissions_paper.ios_metadata_2023.json")
    if metadata_lookup is None:
        return

    def _bar_plot(cursor, year):
        store_category_dict = {}
        for app in cursor:
            ios_value = (app['ios_non_empty'] if app['ios_non_empty'] is not None else 0)
            android_value = (app['android_non_empty'] if app['android_non_empty'] is not None else 0)
            genre = app['genre']
            if genre not in store_category_dict.keys():
                store_category_dict[genre] = {
                    "ios": [ios_value],
                    "android": [android_value]
                }
            else:
                store_category_dict[genre]['ios'].append(ios_value)
                store_category_dict[genre]['android'].append(android_value)

        for key, value in store_category_dict.items():
            store_category_dict[key]['ios_avg'] = statistics.mean(value['ios'])
            store_category_dict[key]['android_avg'] = statistics.mean(value['android'])

        df = pd.DataFrame().from_dict(store_category_dict, orient="index")
        df = df.sort_values('android_avg', ascending=False)

        bar_width = 0.4
        fig, ax = plt.subplots(figsize=(8,4))
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        x_1 = [i - bar_width/2 for i in range(df.index.size)]
        x_2 = [i + bar_width/2 for i in range(df.index.size)]
        ax.bar(x_1, df['android_avg'], width=bar_width, label="Android", color="#494949")
        ax.bar(x_2, df['ios_avg'], width=bar_width, label="iOS", color="#b5b5b5")
        ax.set_yticks(np.arange(0,8,1))
        ax.set_xticks(range(df.index.size))
        ax.set_xticklabels(df.index, rotation=45, ha='right')
        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"permissions_avg_app_store_category_{year}-({DATE}).pdf"), format="pdf")
        return df

    years = {
        "2023": collection_2023,
        "2024": collection_2024,
        "2025": collection_2025,
    }
    global_df = pd.DataFrame()
    for year, col in years.items():
        cursor = _agg_get_permission_cat_number_and_app_store_category_per_app(col, metadata_lookup)
        df = _bar_plot(cursor, year)
        global_df = pd.concat([global_df, df[['android_avg','ios_avg']].rename(columns={"ios_avg": f"ios_avg_{year}", "android_avg": f"android_avg_{year}"})], axis=1)

    print(global_df.round(decimals=2).iloc[:, [0, 2, 4, 1, 3, 5]].to_latex(index=True))
    print(global_df.round(decimals=2).to_latex(index=True))
    print(global_df['ios_avg_2023'] - global_df['android_avg_2023'])
    print(global_df['ios_avg_2025'] - global_df['android_avg_2025'])


# Merges common_permissions + permission_diffs, then for each category collects the set of ios_ids that have a non-empty android/ios list, plus total count
def _agg_get_permission_distribution_android_ios(collection):
    android_sets = defaultdict(set)
    ios_sets = defaultdict(set)
    counts = defaultdict(int)
    for doc in collection:
        ios_id = doc.get("ios_id")
        merged = {**doc.get("common_permissions", {}), **doc.get("permission_diffs", {})}
        for category, v in merged.items():
            counts[category] += 1
            if len(v.get("android", [])) > 0:
                android_sets[category].add(ios_id)
            if len(v.get("ios", [])) > 0:
                ios_sets[category].add(ios_id)
    all_cats = set(counts.keys())
    return sorted(
        [{"_id": cat,
          "android_non_empty": list(android_sets[cat]),
          "ios_non_empty": list(ios_sets[cat]),
          "count": counts[cat]}
         for cat in all_cats],
        key=lambda x: -x["count"]
    )


def get_growth_rate_of_permission_categories_android_vs_ios():
    years = {
        "2023": collection_2023,
        "2025": collection_2025,
    }
    global_df = pd.DataFrame()
    for year, col in years.items():
        cursor = _agg_get_permission_distribution_android_ios(col)
        cat_dict = {}
        for item in cursor:
            cat_dict[item['_id']] = {
                f'android_{year}': len(item['android_non_empty']),
                f'ios_{year}': len(item['ios_non_empty']),
            }
        df = pd.DataFrame().from_dict(cat_dict, orient="index")
        global_df = pd.concat([global_df, df], axis=1)

    global_df['android_growth_total'] = (global_df['android_2025'] - global_df['android_2023'])
    global_df['android_growth_%'] = (((global_df['android_2025'] - global_df['android_2023']) / global_df['android_2023']) * 100).round(1)
    global_df['ios_growth_total'] = (global_df['ios_2025'] - global_df['ios_2023'])
    global_df['ios_growth_%'] = (((global_df['ios_2025'] - global_df['ios_2023']) / global_df['ios_2023']) * 100).round(1)
    global_df['android_ios_diff'] = global_df['android_growth_total'] - global_df['ios_growth_total']
    print(global_df.fillna(0).apply(pd.to_numeric, downcast='integer').sort_values('android_ios_diff', ascending=False).to_latex())


def get_avg_permissions_per_app():
    years = {
        "2023": collection_2023,
        "2024": collection_2024,
        "2025": collection_2025
    }
    
    for year, apps in years.items():
        android_permissions = []
        ios_permissions = []
        for app in apps:
            android = app.get("total_common_permissions")
            ios = app.get("total_common_permissions")
            permission_diffs = app.get("permission_diffs")
            for category in permission_diffs:
                diff = permission_diffs.get(category)
                if len(diff.get("android")) > 0: android += 1
                if len(diff.get("ios")) > 0: ios += 1
            android_permissions.append(android)
            ios_permissions.append(ios)
        print("---------------------------------------------------------")
        print(f"{year}:")
        print(f"iOS total permissions: {len(ios_permissions)} AVG: {statistics.mean(ios_permissions)}")
        print(f"Android total permissions: {len(android_permissions)} AVG: {statistics.mean(android_permissions)}")
        print("---------------------------------------------------------")


get_growth_rate_of_permission_categories_android_vs_ios()
get_permission_distribution_of_differences_per_year()
get_permission_distribution_cdf()
get_changes_of_permission_diffs()
get_differences_among_categories()
plot_differences_added_removed_across_categories()
jitter_plot_about_permission_occurrences()
cdf_permission_usage_android_ios()
plot_top_5_different_categories_per_year()
plot_permissions_per_category_and_ios_android_per_year()
plot_permission_cats_per_app_store_category()
get_avg_permissions_per_app()