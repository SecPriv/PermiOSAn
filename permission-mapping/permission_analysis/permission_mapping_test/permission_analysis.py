import json
import pandas as pd
import matplotlib.pyplot as plt
import copy

DATE = "28-07-2026"
YEARS = ["2023", "2024", "2025"]

with open("./data/permission_mapping.json") as fp:
    permission_mapping = json.load(fp)

for YEAR in YEARS:
    with open(f"./data/matches_w_permissions_{YEAR}_bind_({DATE}).json") as fp:
        apps = json.load(fp)

    # iterate over permission mapping to convert lists to sets for better comparison
    blank_dict = {}
    for obj in permission_mapping:
        obj["android_permissions"] = set(obj.get("android_permissions", None))
        obj["ios_permissions"] = set(obj.get("ios_permissions", None))
        blank_dict[obj.get("permission_category")] = { "android": set(), "ios": set() }

    apps_w_diffs = {}
    app_permissions = {}
    i = 1
    for app_pair in apps:
        
        ios_permissions = set([obj.get("name", None) for obj in app_pair.get("ios_entitlements", [])] + [obj.get("permission", None) for obj in app_pair.get("ios_permissions", [])])
        android_permissions = set([obj[0].replace("android.permission.", "") if obj != [] else None for obj in app_pair.get("android_permissions", [])])
  
        if app_pair.get("ios_id") == "LiveScore":
            print(app_pair)


        permissions_intersections = copy.deepcopy(blank_dict)
        for obj in permission_mapping:
            permissions_intersections[obj.get("permission_category")]["android"] = (obj.get("android_permissions").intersection(android_permissions))
            permissions_intersections[obj.get("permission_category")]["ios"] = (obj.get("ios_permissions").intersection(ios_permissions))
        
        app_permissions[app_pair["_id"]] = permissions_intersections

        differences = {
            perm_type: perms
            for perm_type, perms in permissions_intersections.items()
            if (not perms["android"] and perms["ios"]) or (perms["android"] and not perms["ios"])
        }
        commons = {
            perm_type: perms
            for perm_type, perms in permissions_intersections.items()
            if (perms["android"] and perms["ios"])
        }
        totals = {
            "total_ios":  len(ios_permissions),
            "total_android": len(android_permissions),
            "total_android_custom": len([perm for perm in android_permissions if "." in perm]),
            "total_common_permissions": len(commons),
            "common_permissions": commons
        }
        perm_analysis = {
            "permission_diffs": differences
        } | totals

        apps_w_diffs[app_pair["_id"]] = perm_analysis


    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError
        #print(apps_w_diffs)
    with open(f'./apps_w_diffs_{YEAR}_{DATE}.json', "w") as fp:
        json.dump(apps_w_diffs, fp, default=set_default)
    with open(f'./apps_permission_mapping_stats_{YEAR}_{DATE}.json', "w") as fp:
        json.dump(app_permissions, fp, default=set_default)
