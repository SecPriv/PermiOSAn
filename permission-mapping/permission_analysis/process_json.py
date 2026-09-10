#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# ///

import json

DATE = "28-07-2026"
YEARS = ["2023", "2024", "2025"]
FILE = "apps_w_diffs"


for YEAR in YEARS:
    with open(f"{FILE}_{YEAR}_{DATE}.json", "r") as fp:
        js = json.load(fp)

    mongdb_compatible = []

    for item in js:
        mongdb_compatible.append({
            "ios_id": item,
        }| js[item]) 

    with open(f"{FILE}_{YEAR}_bind_{DATE}.json", "w") as fp:
        json.dump(mongdb_compatible, fp)
