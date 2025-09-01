from typing import Callable, TypeVar

from pymongo.collection import Collection
from xpa.android_preprocessing import util
from xpa.database.db_connector import get_collection
from xpa.database.analysis_results.preprocessing_result.android_preprocessing_result.android_preprocessing_result import AndroidPreprocessingResult
from xpa.database.permissions.android_permission.android_permission import AndroidPermission

_T = TypeVar("_T")


android_collection = "analysis_results_android"

android_analysis_results = get_collection(android_collection)

def _fetch_all(coll: Collection[_T], constructor: Callable[[], _T]) -> list[_T]:
    cursor = coll.find()
    targets: list[_T] = []
    for doc in cursor:
        targets.append(constructor(**doc))
    return targets

android_apps = _fetch_all(android_analysis_results, AndroidPreprocessingResult)
for app in android_apps:
    # for each app get the list of permissions it uses
    permissions = app.apk_info.get("uses_permissions")
    if permissions is None:
        continue
    for permission in permissions:
        # for each permission
        if permission is None:
            continue
        name = permission[0]
        value = str(permission[1])
        # see if there is already an entry for this permission in the database
        perm_entries = AndroidPermission.find(filter={"permission_id": permission[0]})
        if len(perm_entries) > 0:
            # permission already exists in the database
            if len(perm_entries) != 1:
                # there should only be one entry per permission
                print(f"Something went wrong here. {permission}, {perm_entries}")
                quit()
            # update the permission entry
            perm_entry = perm_entries[0]
            if app.app_id in perm_entry.used_by:
                continue
            values = perm_entry.values
            if values.get(value) is not None:
                # if the value already exist just update the counter
                values[value] = values.get(value) + 1
            else:
                # otherwise add the value to the dict
                values[value] = 1
            perm_entry.values = values # TODO: is this necessary or already a side effect?
            perm_entry.used_by.append(app.app_id)
            perm_entry.update()

        else:
            # permission does not exist in the database
            run_id = util.create_pipeline_run(tool_name="android_permission_statistics", arguments=None).run_id
            doc = AndroidPermission(
                os="Android",
                run_id=run_id,
                permission_id=name,
                values={f"{value}": 1},
                used_by=[app.app_id],
                type="manifest"
            )
            #print(doc)
            doc.insert()
        