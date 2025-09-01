from itertools import combinations
from collections import Counter
from typing import Callable, TypeVar

from pymongo.collection import Collection

from xpa.database.db_connector import get_collection
from xpa.database.analysis_results.preprocessing_result.android_preprocessing_result.android_preprocessing_result import AndroidPreprocessingResult

_T = TypeVar("_T")
collection = get_collection("analysis_results_android")

def _fetch_all(coll: Collection[_T], constructor: Callable[[], _T]) -> list[_T]:
    cursor = coll.find()
    targets: list[_T] = []
    for doc in cursor:
        targets.append(constructor(**doc))
    return targets

# Fetch data and generate pairs
feature_pairs = Counter()
apps = _fetch_all(collection, AndroidPreprocessingResult)
len_apps = len(apps)
counter = 1
for app in apps:
    #print(f"Analysing app {app.app_id} ({counter}/{len_apps})...")
    permissions_list = app.apk_info.get("uses_permissions", [])
    permissions = [item[0] for item in permissions_list]
    permissions = set(permissions)
    # Generate all combinations of two features
    pairs = combinations(sorted(permissions), 2)
    feature_pairs.update(pairs)
    counter += 1

# Print top co-occurring pairs
with open("./permission_analysis/top_100_pairs_android.csv", "w") as fp:
    fp.write("permission1\tpermission2\tcount\n")
    for pair, count in feature_pairs.most_common(100):
        fp.write(f"{pair[0]}\t{pair[1]}\t{count}\n")

with open("./permission_analysis/all_pairs_android.csv", "w") as fp:
    fp.write("permission1\tpermission2\tcount\n")
    for pair, count in feature_pairs.most_common():
        fp.write(f"{pair[0]}\t{pair[1]}\t{count}\n")
