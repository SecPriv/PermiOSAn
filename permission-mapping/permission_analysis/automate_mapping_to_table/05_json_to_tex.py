#!/usr/bin/env python3

import openpyxl
import json


def get_longest(mapping_data):
    maxios, maxcat, maxand = 0, 0, 0
    for c in mapping_data:
        maxcat = max(len(c["permission_category"]), maxcat)
        for i in c["ios_permissions"]:
            maxios = max(len(i), maxios)
        for a in c["android_permissions"]:
            maxand = max(len(a), maxand)
    return maxios, maxcat, maxand

def main():
    with open("mapping.json") as f:
        mapping_data = json.loads(f.read())

    maxios, maxcat, maxand = get_longest(mapping_data)
    
    cell_defs = []
    table_rows = []
    #table_rows.append("\\textbf{Apple Category} & \\textbf{iOS} & \\textbf{Our Category} & \\textbf{Android} & \\textbf{Permission Group} \\\\")
    table_rows.append("\\textbf{iOS} & \\textbf{Our Category} & \\textbf{Android} \\\\")

    for category_data in mapping_data:
        current_category = category_data["permission_category"]
        android_permissions = category_data["android_permissions"]
        ios_permissions = category_data["ios_permissions"]

        len_android = len(android_permissions)
        len_ios = len(ios_permissions)
        longest = max(len_android, len_ios)

        # TODO first prep ios category mapping
        # TODO then prep android perm group mapping

        # then iterate over longest
        for i in range(longest):
            current_android_permission = android_permissions[i] if i < len_android else " "
            current_android_permission = current_android_permission.replace("_", "\_")
            current_ios_permission = ios_permissions[i] if i < len_ios else " "
            if i == 0:
                if longest > 1:
                    #cell_defs.append(f"cell{{{len(table_rows)+1}}}{{3}} = {{r={longest}}}{{valign=m}}, %{current_category}")
                    cell_defs.append(f"cell{{{len(table_rows)+1}}}{{2}} = {{r={longest}}}{{valign=m}}, %{current_category}")
            else:
                current_category = " "

            #table_rows.append(f"  & {current_ios_permission:{maxios}} & {current_category:{maxcat}} & {current_android_permission:{maxand}} &  \\\\")
            table_rows.append(f" {current_ios_permission:{maxios}} & {current_category:{maxcat}} & {current_android_permission:{maxand}}  \\\\")

    
    print("""
\\begin{table*}[t]
\\centering
\\begin{tblr}{
    colspec={|l|l|l|},
    hlines,
    hline{2} = {2pt},""")
    for cell_def in cell_defs:
        print(f"    {cell_def}")
    print("}")
    for table_row in table_rows:
        print(f"    {table_row}")
    print("""\end{tblr}
\\vspace{1ex}
\\caption{Mapping - This is just an example not the actual mapping that we have.}
\\end{table*}""")

#    colspec={|l|l||l||l|l|},

    return

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

        alen_androidndroid, ios, _, _, _, _ = row

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
