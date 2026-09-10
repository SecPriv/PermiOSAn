import json

with open("./data/permission_mapping.json", "r") as fp:
    mapping = json.load(fp)

with open("./data/ios_protected_resources.json", "r") as fp:
    protected_resources = set(json.load(fp))

with open("./data/ios_entitlements.json", "r") as fp:
    entitlements = set(json.load(fp))

with open("./data/ios_unmapped_permissions.json", "r") as fp:
    ios_unmapped_table = set(json.load(fp))

with open("./data/android_unmapped_permissions.json", "r") as fp:
    android_unmapped = set(json.load(fp))

ios_mapped = set()
android_mapped = set()
for xppc in mapping:
    ios_mapped |= set(xppc.get("ios_permissions"))
    android_mapped |= set(xppc.get("android_permissions"))
    print(f'{xppc.get("permission_category")} -- Android: {len(set(xppc.get("android_permissions")))} -- iOS: {len(set(xppc.get("ios_permissions")))}')


ios_full_permissions = protected_resources | entitlements

unmapped_ios = ios_full_permissions.difference(ios_mapped)

print(f"iOS Total: {len(ios_full_permissions)}; iOS prot. resources: {len(protected_resources)}; iOS entitlements: {len(entitlements)}")
print(f"iOS Mapped: {len(ios_mapped)}")
print(f"iOS Unmapped: {len(unmapped_ios)}; iOS unmapped Table: {len(ios_unmapped_table)}")
print(sorted(unmapped_ios.difference(ios_unmapped_table)))
print(ios_mapped.difference(ios_full_permissions))
print(f"Android Total: {len(android_mapped | android_unmapped)}; Android Mapped: {len(android_mapped)}; Android Unmapped: {len(android_unmapped)}")
print(sorted(android_unmapped))