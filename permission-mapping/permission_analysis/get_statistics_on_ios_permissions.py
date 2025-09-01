from typing import Callable, TypeVar

from pymongo.collection import Collection
import numpy as np

from xpa.android_preprocessing import util
from xpa.database.db_connector import get_collection
from xpa.database.analysis_results.preprocessing_result.ios_preprocessing_result.ios_preprocessing_result import iOSPreprocessingResult
from xpa.database.permissions.ios_permission.ios_permission import iOSPermission

_T = TypeVar("_T")


ios_collection = "analysis_results_ios"

ios_analysis_results = get_collection(ios_collection)

def _fetch_all(coll: Collection[_T], constructor: Callable[[], _T]) -> list[_T]:
    cursor = coll.find()
    targets: list[_T] = []
    for doc in cursor:
        targets.append(constructor(**doc))
    return targets

ios_apps = _fetch_all(ios_analysis_results, iOSPreprocessingResult)
for app in ios_apps:
    # for each app get the list of permissions it uses
    permissions = app.plist.get("permissions")
    entitlements = app.entitlements.get("entitlements")
    if permissions is None:
        continue
    for permission in permissions:
        # for each permission
        if permission is None:
            continue
        name = str(permission.get("permission"))
        value = str(permission.get("value"))

        # see if there is already an entry for this permission in the database
        perm_entries = iOSPermission.find(filter={"permission_id": name})
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
            run_id = util.create_pipeline_run(tool_name="ios_permission_statistics", arguments=None).run_id
            doc = iOSPermission(
                os="iOS",
                run_id=run_id,
                permission_id=name,
                values={f"{value}": 1},
                used_by=[app.app_id],
                type="plist"
            )
            #print(doc)
            doc.insert()
        
    if entitlements is None:
        continue
    for entitlement in entitlements:
        name = entitlement.get("name")
        values = entitlement.get("value")
        # see if there is already an entry for this entitlement in the database
        ent_entries = iOSPermission.find(filter={"permission_id": name})
        if len(ent_entries) > 0:
            # permission already exists in the database
            if len(ent_entries) != 1:
                # there should only be one entry per permission
                print(f"Something went wrong here. {permission}, {ent_entries}")
                quit()
            # update the permission entry
            ent_entry = ent_entries[0]
            ent_values = ent_entry.values
            if app.app_id in ent_entry.used_by:
                    continue
            if np.isscalar(values):
                v = str(values)
                if ent_values.get(values) is not None and app.app_id not in perm_entry.used_by:
                # if the value already exist just update the counter
                    ent_values[v] = ent_values.get(v) + 1
                else:
                # otherwise add the value to the dict
                    ent_values[v] = 1
            else:
                for v in values:
                    v = str(v)
                    if ent_values.get(v) is not None:
                        ent_values[v] = ent_values.get(v) + 1
                    else:
                        ent_values[v] = 1
            
            ent_entry.values = ent_values # TODO: is this necessary or already a side effect?
            ent_entry.used_by.append(app.app_id)
            ent_entry.update()

        else:
            run_id = util.create_pipeline_run(tool_name="ios_permission_statistics", arguments=None).run_id
            vl = {}
            if np.isscalar(values):
                vl[str(values)] = 1
            else:
                for val in values:
                    vl[str(val)] = 1
            doc = iOSPermission(
                os="iOS",
                run_id=run_id,
                permission_id=name,
                values=vl,
                used_by=[app.app_id],
                type="entitlement"
            )
            doc.insert()