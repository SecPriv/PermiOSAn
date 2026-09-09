import pandas as pd


def analyze_permission_file(csv_file):
    df = pd.read_csv(csv_file)
    df = df.rename(columns={
        "granted by": "ios_granted_by",
        "granted by.1": "android_granted_by",
        "iOS": "ios_permission",
        "Android": "android_permission",
        "Category": "category"
    })

    df["category"] = (
        df["category"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Normalize text
    for col in ["category", "ios_granted_by", "android_granted_by"]:
        df[col] = df[col].fillna("").astype(str).str.strip().str.lower()

    results = []

    for category, group in df.groupby("category"):
        ios_grants = set(group.loc[group["ios_granted_by"] != "", "ios_granted_by"])
        android_grants = set(group.loc[group["android_granted_by"] != "", "android_granted_by"])

        intersection = ios_grants & android_grants
        union = ios_grants | android_grants

        if len(union) == 0:
            jaccard = 1.0
        else:
            jaccard = len(intersection) / len(union)

        results.append({
            "category": category,
            "total_granting_categories": len(union),
            "same": len(intersection),
            "different": len(union - intersection),
            "ios_count": len(ios_grants),
            "android_count": len(android_grants),
            "ios_granted_by": ", ".join(sorted(ios_grants)),
            "android_granted_by": ", ".join(sorted(android_grants)),
            "jaccard_similarity": jaccard
        })
    summary = pd.DataFrame(results)

    print(summary)
    summary.to_csv("granting_comparison_by_category.csv", index=False)
    return summary


def analyze_granted_by(summary):
    """
    summary is the DataFrame produced by the previous comparison script.
    """

    total_categories = len(summary)

    same_categories = (summary["different"] == 0).sum()
    different_categories = (summary["different"] > 0).sum()

    android_more = (summary["android_count"] > summary["ios_count"]).sum()
    ios_more = (summary["ios_count"] > summary["android_count"]).sum()
    equal_number = (summary["ios_count"] == summary["android_count"]).sum()

    # ----------------------------------------------------
    # Jaccard statistics
    # ----------------------------------------------------
    avg_jaccard = summary["jaccard_similarity"].mean()
    median_jaccard = summary["jaccard_similarity"].median()

    identical = (summary["jaccard_similarity"] == 1.0).sum()
    completely_different = (summary["jaccard_similarity"] == 0.0).sum()
    partial_overlap = (
            (summary["jaccard_similarity"] > 0.0)
            & (summary["jaccard_similarity"] < 1.0)
    ).sum()

    # ----------------------------------------------------
    # Most similar / divergent categories
    # ----------------------------------------------------
    most_similar = summary.sort_values(
        "jaccard_similarity",
        ascending=False
    )

    most_divergent = summary.sort_values(
        "jaccard_similarity",
        ascending=True
    )

    print("=" * 60)
    print("Granting Mechanism Analysis")
    print("=" * 60)

    print(f"Total categories: {total_categories}")
    print()

    print(f"Identical granting model: {same_categories}")
    print(f"Different granting model: {different_categories}")
    print()

    print(f"Android uses more granting types: {android_more}")
    print(f"iOS uses more granting types: {ios_more}")
    print(f"Equal number of granting types: {equal_number}")
    print()

    print(f"Average Jaccard similarity: {avg_jaccard: .3f}")
    print(f"Median Jaccard similarity: {median_jaccard: .3f}")
    print()

    print(f"Identical categories (J=1.0): {identical}")
    print(f"Partial overlap: {partial_overlap}")
    print(f"Completely different (J=0): {completely_different}")
    print()

    print("=" * 60)
    print("10 Most Similar Categories")
    print("=" * 60)
    print(
        most_similar[
            [
                "category",
                "jaccard_similarity",
                "ios_granted_by",
                "android_granted_by",
            ]
        ].head(10)
    )

    print()

    print("=" * 60)
    print("10 Most Divergent Categories")
    print("=" * 60)
    print(
        most_divergent[
            [
                "category",
                "jaccard_similarity",
                "ios_granted_by",
                "android_granted_by",
            ]
        ].head(10)
    )

    # Save for later inspection
    most_similar.to_csv("most_similar_categories.csv", index=False)
    most_divergent.to_csv("most_divergent_categories.csv", index=False)


if __name__ == '__main__':
    my_csv_file = "Permission_Mapping.csv"
    differences = analyze_permission_file(csv_file=my_csv_file)
    analyze_granted_by(differences)
