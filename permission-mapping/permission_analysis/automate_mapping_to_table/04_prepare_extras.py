#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def extract_permissions(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    mapping = {}
    for perm in root.findall(".//permission"):
        name = perm.attrib.get("{http://schemas.android.com/apk/res/android}name")
        group = perm.attrib.get("{http://schemas.android.com/apk/res/android}permissionGroup")
        if name and group: # and "UNDEFINED" not in group:
            mapping[name] = group
    return mapping


if __name__ == "__main__":
    # Example usage
    xml_file = "res/AndroidManifest.xml"
    mapping = extract_permissions(xml_file)

    for name, group in mapping.items():
        print(name, group)

