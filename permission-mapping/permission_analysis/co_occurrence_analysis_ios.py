from itertools import combinations
from collections import Counter
from typing import Callable, TypeVar

from pymongo.collection import Collection

from xpa.database.db_connector import get_collection
from xpa.database.analysis_results.preprocessing_result.ios_preprocessing_result.ios_preprocessing_result import iOSPreprocessingResult

_T = TypeVar("_T")
collection = get_collection("analysis_results_ios")

def _fetch_all(coll: Collection[_T], constructor: Callable[[], _T]) -> list[_T]:
    cursor = coll.find()
    targets: list[_T] = []
    for doc in cursor:
        targets.append(constructor(**doc))
    return targets

# Fetch data and generate pairs
feature_pairs = Counter()
apps = _fetch_all(collection, iOSPreprocessingResult)
len_apps = len(apps)
counter = 1
for app in apps:
    #print(f"Analysing app {app.app_id} ({counter}/{len_apps})...")
    permissions_list = app.plist.get("permissions", [])
    entitlements_list = app.entitlements.get("entitlements", [])
    permissions = [item.get("permission") for item in permissions_list]
    entitlements = [item.get("name") for item in entitlements_list]
    permissions = set(permissions)
    entitlements = set(entitlements)
    entitlements.discard("application-identifier")
    entitlements.discard("com.apple.developer.ubiquity-container-identifiers")
    entitlements.discard("com.apple.developer.team-identifier")
    both = permissions.union(entitlements)
    # Generate all combinations of two features
    pairs = combinations(sorted(both), 2)
    feature_pairs.update(pairs)
    counter += 1

# Print top co-occurring pairs
with open("./permission_analysis/top_1000_e+p_pairs_ios.csv", "w") as fp:
    fp.write("permission1\tpermission2\tcount\n")
    for pair, count in feature_pairs.most_common(1000):
        fp.write(f"{pair[0]}\t{pair[1]}\t{count}\n")

with open("./permission_analysis/all_e+p_pairs_ios.csv", "w") as fp:
    fp.write("permission1\tpermission2\tcount\n")
    for pair, count in feature_pairs.most_common():
        fp.write(f"{pair[0]}\t{pair[1]}\t{count}\n")
