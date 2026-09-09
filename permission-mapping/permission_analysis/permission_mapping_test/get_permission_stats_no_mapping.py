import numpy as np
import json


def get_app_json(year: str):
    return f"./data/matches_w_permissions_{year}.json"

filtered_apps = {}
with open("./data/filtered_app_ids-(08-08-2025).json", "r") as fp:
    filtered_apps = json.load(fp)
filtered_app_ids = [item.get("_id") for item in filtered_apps]

permission_mapping = {}
permission_mapping_ios, permission_mapping_android = [], []
with open("./data/permission_mapping.json", "r") as fp:
    permission_mapping = json.load(fp)
for mapping in permission_mapping:
    permission_mapping_ios += mapping.get("ios_permissions")
    permission_mapping_android += mapping.get("android_permissions")

years = ["2023", "2024", "2025"]

stats_dict = {"2023": {"android": {}, "ios": {}}, "2024": {"android": {}, "ios": {}}, "2025": {"android": {}, "ios": {}}}

for year in years:
    data = {}
    with open(get_app_json(year), "r") as fp:
        data = json.load(fp)

    total_apps = 0

    for app_pair in data:
        if app_pair.get("_id") not in filtered_app_ids:
            continue
        total_apps += 1
        entitlements = app_pair.get("ios_entitlements", [])
        for entitlement in entitlements:
            if entitlement.get("name") in permission_mapping_ios:
                continue
            if stats_dict.get(year, {}).get('ios', {}).get(entitlement.get("name"), None) is None:
                stats_dict[year]['ios'][entitlement.get("name")] = 1
            else:
                stats_dict[year]['ios'][entitlement.get("name")] += 1
        ios_permissions = app_pair.get("ios_permissions", [])
        for ios_permission in ios_permissions:
            if ios_permission.get("permission") in permission_mapping_ios:
                continue
            if stats_dict.get(year, {}).get('ios', {}).get(ios_permission.get("permission"), None) is None:
                stats_dict[year]['ios'][ios_permission.get("permission")] = 1
            else:
                stats_dict[year]['ios'][ios_permission.get("permission")] += 1
        android_permissions = app_pair.get("android_permissions", [])
        for android_permission in android_permissions:
            if android_permission[0] in permission_mapping_android:
                continue
            if stats_dict.get(year, {}).get('android', {}).get(android_permission[0], None) is None:
                stats_dict[year]['android'][android_permission[0]] = 1
            else:
                stats_dict[year]['android'][android_permission[0]] += 1

    print(f"Total apps in {year} are {total_apps}")

for year in years:
    with open(f"./no_mapping_permission_stats_{year}.json", "w") as fp:
        json.dump(stats_dict[year], fp)
