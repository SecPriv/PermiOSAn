#!/usr/bin/env python3

import openpyxl
import json

def main():
    workbook = openpyxl.load_workbook("Permission Mapping.xlsx")
    sheet = workbook['Mapping Results Corrected']
    rows = list(sheet.iter_rows(values_only=True))

    
    lastrow = None
    category_started = False

    mapping_to_add = { "permission_category": None,
            "android_permissions": [],
            "ios_permissions": []}
    mappings = []

    for row in rows:

        android, ios, _, _, _, _ = row

        if android == "Android" and ios == "iOS":
            # line signifies a new category mapping
            mapping_to_add["permission_category"] = lastrow[0]
            category_started = True
        elif android == None and ios == None:
            # line signifies ending of a category mapping 
            if mapping_to_add["permission_category"] is not None:
                mappings.append(mapping_to_add)
                mapping_to_add = { "permission_category": None,
                        "android_permissions": [],
                        "ios_permissions": []}
                category_started = False
        elif category_started:
            if android is not None:
                mapping_to_add["android_permissions"].append(android)
            if ios is not None:
                mapping_to_add["ios_permissions"].append(ios)

        #print(row)
        lastrow = row

    #print(json.dumps(mappings, indent=2))
    if len(mappings) > 0:
        with open("mapping.json", "w") as f:
            f.write(json.dumps(mappings, indent=2))
    else:
        print("Warning: no data found, no json written!")

if __name__ == "__main__":
    main()
