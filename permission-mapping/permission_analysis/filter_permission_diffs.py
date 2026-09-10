#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# ///


import json
from pathlib import Path

def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def build_index(collection: list[dict], field: str) -> dict[str, list[dict]]:
    # Build a dict mapping field value -> list of matching documents
    index: dict[str, list[dict]] = {}
    for doc in collection:
        key = doc.get(field)
        if key is not None:
            index.setdefault(key, []).append(doc)
    return index


def aggregate(
    filtered_app_ids: list[dict],
    apps: list[dict],
    perm_diffs_1: list[dict],
    perm_diffs_2: list[dict],
    YEAR_1: str,
    YEAR_2: str
) -> list[dict]:

    # filtered_app_ids on ios_id == _id
    filtered_index = build_index(filtered_app_ids, "_id")

    for doc in apps:
        ios_id = doc.get("ios_id")
        doc["filtered"] = filtered_index.get(ios_id, [])

    # keep only apps present in the filtered set
    pipeline = [doc for doc in apps if len(doc["filtered"]) > 0]

    # map permission_diffs_2024 on ios_id
    diffs_2024_index = build_index(perm_diffs_1, "ios_id")

    for doc in pipeline:
        ios_id = doc.get("ios_id")
        doc[YEAR_1] = diffs_2024_index.get(ios_id, [])

    # map permission_diffs_2025 on ios_id
    diffs_2025_index = build_index(perm_diffs_2, "ios_id")

    for doc in pipeline:
        ios_id = doc.get("ios_id")
        doc[YEAR_2] = diffs_2025_index.get(ios_id, [])

    # must appear in BOTH diff collections
    pipeline = [
        doc for doc in pipeline
        if len(doc[YEAR_1]) > 0 and len(doc[YEAR_2]) > 0
    ]

    # unwrap first element of 2024/2025 arrays
    for doc in pipeline:
        doc[YEAR_1] = doc[YEAR_1][0]
        doc[YEAR_2] = doc[YEAR_2][0]

    return pipeline


def main() -> None:
    DATE = "28-07-2026"

    filtered_apps = load(Path("./data/filtered_app_ids-(08-08-2025).json"))
    perm_diffs_2023  = load(Path(f"./apps_w_diffs_2023_bind_{DATE}.json"))
    perm_diffs_2024  = load(Path(f"./apps_w_diffs_2024_bind_{DATE}.json"))
    perm_diffs_2025  = load(Path(f"./apps_w_diffs_2025_bind_{DATE}.json"))

    results = aggregate(filtered_apps, perm_diffs_2023, perm_diffs_2024, perm_diffs_2025, "2024", "2025")
    with open("./permission_diffs_2023-filtered-(28-07-2026).json", "w") as fp:
        json.dump(results, indent=2, fp=fp)

    perm_diffs_2023  = load(Path(f"./apps_w_diffs_2023_bind_{DATE}.json"))
    perm_diffs_2024  = load(Path(f"./apps_w_diffs_2024_bind_{DATE}.json"))
    perm_diffs_2025  = load(Path(f"./apps_w_diffs_2025_bind_{DATE}.json"))
    
    results = aggregate(filtered_apps, perm_diffs_2024, perm_diffs_2023, perm_diffs_2025, "2023", "2025")
    with open("./permission_diffs_2024-filtered-(28-07-2026).json", "w") as fp:
        json.dump(results, indent=2, fp=fp)

    perm_diffs_2023  = load(Path(f"./apps_w_diffs_2023_bind_{DATE}.json"))
    perm_diffs_2024  = load(Path(f"./apps_w_diffs_2024_bind_{DATE}.json"))
    perm_diffs_2025  = load(Path(f"./apps_w_diffs_2025_bind_{DATE}.json"))

    results = aggregate(filtered_apps, perm_diffs_2025, perm_diffs_2023, perm_diffs_2024, "2024", "2025")
    with open("./permission_diffs_2025-filtered-(28-07-2026).json", "w") as fp:
        json.dump(results, indent=2, fp=fp)


if __name__ == "__main__":
    main()
