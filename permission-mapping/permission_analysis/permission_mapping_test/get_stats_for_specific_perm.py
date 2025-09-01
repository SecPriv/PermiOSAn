import json

permission_target = ["READ_MEDIA_VISUAL_USER_SELECTED",
"FOREGROUND_SERVICE_MEDIA_PLAYBACK",
"FOREGROUND_SERVICE_MEDIA_PROJECTION"]
other_permissions_in_category = [
      "READ_MEDIA_IMAGES",
      "READ_MEDIA_VIDEO",
      "READ_EXTERNAL_STORAGE",
      "WRITE_EXTERNAL_STORAGE",
      "READ_MEDIA_AUDIO",
      "MODIFY_AUDIO_SETTINGS",
      "FOREGROUND_SERVICE_MEDIA_PROCESSING",
    ]
app_set_2023 = set()
app_set_2025 = set()
app_set_other_2023 = set()
app_set_other_2025 = set()

with open("./data/permissions_paper.matches_w_permissions_2023.json", "r") as fp:
    apps_2023 = json.load(fp)

with open("./data/permissions_paper.matches_w_permissions_2025.json", "r") as fp:
    apps_2025 = json.load(fp)


for app in apps_2023:
    android_permissions = app.get("android_permissions", [])
    for perm in android_permissions:
        #print(perm[0])
        for target in permission_target:
            if target in perm[0]:
                app_set_2023.add(app.get("_id"))
        for other in other_permissions_in_category:
            if other in perm[0] and app.get("_id"):
                app_set_other_2023.add(app.get("_id"))


for app in apps_2025:
    android_permissions = app.get("android_permissions", [])
    for perm in android_permissions:
        for target in permission_target:
            if target in perm[0]:
                app_set_2025.add(app.get("_id"))
        for other in other_permissions_in_category:
            if other in perm[0] and app.get("_id"):
                app_set_other_2025.add(app.get("_id"))


print(f"2023: {len(app_set_2023)}; 2025: {len(app_set_2025)}")
print(f"other 2023: {len(app_set_other_2023)}; 2025: {len(app_set_other_2025)}")
#print(app_set_2023)
#print(app_set_2025)
print(f"Total increase: {len(app_set_2025.difference(app_set_2023))}")
non_overlap_2023 = app_set_2023.difference(app_set_other_2023)
non_overlap_2025 = app_set_2025.difference(app_set_other_2025)
print(f"Non-overlapping 2023: {len(non_overlap_2023)}; 2025: {len(non_overlap_2025)}")
print(len(non_overlap_2025.difference(non_overlap_2023)))

print(len(app_set_other_2025.difference(app_set_other_2023)))