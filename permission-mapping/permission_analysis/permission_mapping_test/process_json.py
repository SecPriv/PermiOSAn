import json

DATE = "25-08-2025"
YEAR = "2023"
FILE = "apps_w_diffs"

with open(f"{FILE}_{YEAR}_{DATE}.json", "r") as fp:
    js = json.load(fp)

mongdb_compatible = []

for item in js:
    mongdb_compatible.append({
        "ios_id": item,
    }| js[item]) 

with open(f"{FILE}_{YEAR}_mongodb_{DATE}.json", "w") as fp:
    json.dump(mongdb_compatible, fp)