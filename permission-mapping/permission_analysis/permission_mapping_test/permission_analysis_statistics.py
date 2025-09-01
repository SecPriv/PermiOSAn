import os
import pymongo as mongo
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter
import statistics

DATE = "25-08-2025"
PLOT_FOLDER_PATH = "ENTER FOLDER PATH HERE"

MONGO_URL: str = os.getenv(
     "MONGO_URL", "mongodb://localadmin:localadmin@localhost/"
)
MONGO_DB: str = os.getenv("MONGO_DB", "permissions_paper")
_client = mongo.MongoClient(MONGO_URL)

_db = _client[MONGO_DB]

collection_2023 = _db[f"permission_diffs_2023-filtered-({DATE})"]
collection_2024 = _db[f"permission_diffs_2024-filtered-({DATE})"]
collection_2025 = _db[f"permission_diffs_2025-filtered-({DATE})"]


def _independent_distribution_diffs_year(year: int):
    return [
        {
            '$project': {
                'ios_id': 1, 
                'permission_diffs': 1, 
                'total_android': 1, 
                'total_android_custom': 1, 
                'total_ios': 1, 
                'total_common_permissions': 1, 
                'common_permissions': 1, 
                'diffs': {
                    '$size': {
                        '$objectToArray': '$permission_diffs'
                    }
                }
            }
        }, {
            '$group': {
                '_id': '$diffs', 
                'number': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                '_id': 1
            }
        }
    ]

def get_permission_distribution_of_differences_per_year():
    res_indep_dist_diffs_2023 = collection_2023.aggregate(_independent_distribution_diffs_year(2023))
    res_indep_dist_diffs_2024 = collection_2024.aggregate(_independent_distribution_diffs_year(2024))
    res_indep_dist_diffs_2025 = collection_2025.aggregate(_independent_distribution_diffs_year(2025))

    print("Distribution permission diffs in 2023:")
    sum_2023 = 0
    for doc in res_indep_dist_diffs_2023:
        print(doc)
        sum_2023 += doc["number"]
    print(f"Total diffs in 2023: {sum_2023}")
    print("----------------------------------")
    print("Distribution permission diffs in 2024:")
    sum_2024 = 0
    for doc in res_indep_dist_diffs_2024:
        print(doc)
        sum_2024 += doc["number"]
    print(f"Total diffs in 2024: {sum_2024}")
    print("----------------------------------")
    print("Distribution permission diffs in 2024:")
    sum_2025 = 0
    for doc in res_indep_dist_diffs_2025:
        print(doc)
        sum_2025 += doc["number"]
    print(f"Total diffs in 2025: {sum_2025}")
    print("__________________________________")
    print("Considering only pairs 2023 -> 2024 -> 2025")

def _distribution():
   return [
    {
        '$addFields': {
            'n_diffs': {
                '$size': {
                    '$objectToArray': '$permission_diffs'
                }
            }
        }
    }, {
        '$group': {
            '_id': '$n_diffs', 
            'number': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            '_id': 1
        }
    }
]

def get_permission_distribution_cdf():
    res_dist_diffs_2023 = collection_2023.aggregate(_distribution())
    res_dist_diffs_2024 = collection_2024.aggregate(_distribution())
    res_dist_diffs_2025 = collection_2025.aggregate(_distribution())

    print("Distribution 2023 -> 2024 of 2023:")
    sum_2023 = 0
    numbers_cdf_2023 = []
    for doc in res_dist_diffs_2023:
        print(doc)
        sum_2023 += doc["number"]
        numbers_cdf_2023.append(doc)
    print(f"Total: {sum_2023}")
    print("----------------------------------")
    print("Distribution 2023 -> 2024 of 2024:")
    sum_2024 = 0
    numbers_cdf_2024 = []
    for doc in res_dist_diffs_2024:
        print(doc)
        sum_2024 += doc["number"]
        numbers_cdf_2024.append(doc)
    print(f"Total: {sum_2024}")
    print("----------------------------------")
    print("Distribution 2024 -> 2025 of 2025:")
    sum_2025 = 0
    numbers_cdf_2025 = []
    for doc in res_dist_diffs_2025:
        print(doc)
        sum_2025 += doc["number"]
        numbers_cdf_2025.append(doc)
    print(f"Total: {sum_2025}")
    df_cdf_2023 = pd.DataFrame(numbers_cdf_2023)
    df_cdf_2024 = pd.DataFrame(numbers_cdf_2024)
    df_cdf_2025 = pd.DataFrame(numbers_cdf_2025)
    #df_cdf_2025 = pd.DataFrame(numbers_cdf_2025)
    df_cdf_2023 = df_cdf_2023.sort_values(by='_id').reset_index(drop=True)
    df_cdf_2024 = df_cdf_2024.sort_values(by='_id').reset_index(drop=True)
    df_cdf_2025 = df_cdf_2025.sort_values(by='_id').reset_index(drop=True)

    stats_df = pd.concat([df_cdf_2023.rename(columns={"number": "f_2023"}).set_index('_id'), 
                          df_cdf_2024.rename(columns={"number": "f_2024"}).set_index('_id'), 
                          df_cdf_2025.rename(columns={"number": "f_2025"}).set_index('_id')], 
                          axis=1)
    stats_df = stats_df.fillna(0)
    # PDF
    stats_df['pdf_2023'] = stats_df['f_2023'] / sum(stats_df['f_2023'])
    stats_df['pdf_2024'] = stats_df['f_2024'] / sum(stats_df['f_2024'])
    stats_df['pdf_2025'] = stats_df['f_2025'] / sum(stats_df['f_2025'])
    # CDF
    stats_df['cdf_2023'] = stats_df['pdf_2023'].cumsum()
    stats_df['cdf_2024'] = stats_df['pdf_2024'].cumsum()
    stats_df['cdf_2025'] = stats_df['pdf_2025'].cumsum()
    print(stats_df)
    
    fig, ax = plt.subplots(figsize=(15, 7))
    colors = sns.color_palette("colorblind", 3)
    ax.plot(stats_df.index.to_list(), stats_df['cdf_2023'], drawstyle='steps-post', label="2023", color=colors[0], linestyle='-.', linewidth=5)
    ax.plot(stats_df.index.to_list(), stats_df['cdf_2024'], drawstyle='steps-post', label="2024", color=colors[1], linestyle='--', linewidth=5)
    ax.plot(stats_df.index.to_list(), stats_df['cdf_2025'], drawstyle='steps-post', label="2025", color=colors[2], linestyle=':', linewidth=5)
    plt.xticks(range(0,13), fontsize=22)
    plt.yticks(np.arange(0,1.1,0.1), fontsize=22)
    plt.xlabel('# of Differences', fontsize=22)
    plt.ylabel('CDF', fontsize=22)
    #plt.title('CDF of Difference Distribution')
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.25, zorder=0)
    plt.legend(fontsize=22)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"get_permission_distribution_cdf-({DATE})-updated.pdf"), format="pdf")  
    #plt.show()

    print("__________________________________")

def _apps_where_number_diffs_not_change(frm: int, to: int):
    return [
    {
        '$addFields': {
            'n_diffs': {
                '$size': {
                    '$objectToArray': '$permission_diffs'
                }
            }, 
            f'n_diffs_{to}': {
                '$size': {
                    '$objectToArray': f'${to}.permission_diffs'
                }
            }
        }
    }, {
        '$addFields': {
            'is_different': {
                '$ne': [
                    '$n_diffs', f'$n_diffs_{to}'
                ]
            }, 
            'difference': {
                '$subtract': [
                    '$n_diffs', f'$n_diffs_{to}'
                ]
            }
        }
    }, {
        '$match': {
            'is_different': False
        }
    }, {
        '$addFields': {
            'y_fields': {
                '$map': {
                    'input': {
                        '$objectToArray': '$permission_diffs'
                    }, 
                    'as': 'field', 
                    'in': '$$field.k'
                }
            }, 
            f'{to}_fields': {
                '$map': {
                    'input': {
                        '$objectToArray': f'${to}.permission_diffs'
                    }, 
                    'as': 'field', 
                    'in': '$$field.k'
                }
            }
        }
    }, {
        '$addFields': {
            'sameKeys': {
                '$setEquals': [
                    f'${to}_fields', '$y_fields'
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$sameKeys', 
            'number': {
                '$sum': 1
            }
        }
    }
]

def _apps_where_number_diff_changed(year: int):
    return [
    {
        '$addFields': {
            'other.diffs': {
                '$size': {
                    '$objectToArray': f'${year}.permission_diffs'
                }
            }, 
            'diffs': {
                '$size': {
                    '$objectToArray': '$permission_diffs'
                }
            }
        }
    }, {
        '$addFields': {
            'is_different': {
                '$ne': [
                    '$diffs', '$other.diffs'
                ]
            }, 
            'number_diffs': {
                '$subtract': [
                    '$diffs', '$other.diffs'
                ]
            }
        }
    }, {
        '$match': {
            'is_different': True
        }
    }, {
        '$group': {
            '_id': '$number_diffs', 
            'number': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            '_id': 1
        }
    }
]

def get_changes_of_permission_diffs():
    print("Apps with diff change between 2023-2024:")
    res_diff_2023_2024 = collection_2023.aggregate(_apps_where_number_diff_changed(2024))
    sum = 0
    sum_neg = 0
    for doc in res_diff_2023_2024:
        print(doc)
        if int(doc["_id"]) < 0:
            sum_neg += doc["number"]
        sum += doc["number"]
    print(f"Total apps with diffs: {sum}")
    print(f"Apps with MORE (2024) diffs than in 2023: {sum-sum_neg}")
    print(f"Apps with LESS (2024) diffs than in 2023: {sum_neg}")
    print("----------------------------------")
    res_diff_2024_2025 = collection_2024.aggregate(_apps_where_number_diff_changed(2025))
    sum = 0
    sum_neg = 0
    for doc in res_diff_2024_2025:
        print(doc)
        if int(doc["_id"]) < 0:
            sum_neg += doc["number"]
        sum += doc["number"]
    print(f"Total apps with diffs: {sum}")
    print(f"Apps with MORE (2025) diffs than in 2024: {sum-sum_neg}")
    print(f"Apps with LESS (2025) diffs than in 2024: {sum_neg}")
    print("----------------------------------")
    print("Apps with no diff change between 2023-2024:")
    res_no_diff_2023_2024 = collection_2023.aggregate(_apps_where_number_diffs_not_change(2023,2024))
    sum = 0
    for doc in res_no_diff_2023_2024:
        if doc["_id"] == "True":
            print(f"Apps with the same diffs: {doc['number']}")
        else:
            print(f"Apps with different diffs: {doc['number']}")
        sum += doc["number"]
    print(f"Total apps with no diffs: {sum}")
    print("----------------------------------")
    print("Apps with no diff change between 2024-2025:")
    res_no_diff_2024_2025 = collection_2024.aggregate(_apps_where_number_diffs_not_change(2024,2025))
    sum = 0
    for doc in res_no_diff_2024_2025:
        if doc["_id"] == "True":
            print(f"Apps with the same diffs: {doc['number']}")
        else:
            print(f"Apps with different diffs: {doc['number']}")
        sum += doc["number"]
    print(f"Total apps with no diffs: {sum}")

    print("__________________________________")

def _distribution_of_diffs_among_permission_categories():
    return [
    {
        '$match': {
            'permission_diffs': {
                '$ne': {}
            }
        }
    }, {
        '$project': {
            'permission_diffs_array': {
                '$objectToArray': '$permission_diffs'
            }
        }
    }, {
        '$unwind': {
            'path': '$permission_diffs_array', 
            'includeArrayIndex': 'string', 
            'preserveNullAndEmptyArrays': True
        }
    }, {
        '$addFields': {
            'category': '$permission_diffs_array.k', 
            'android': '$permission_diffs_array.v.android', 
            'ios': '$permission_diffs_array.v.ios'
        }
    }, {
        '$group': {
            '_id': '$category', 
            'docCount': {
                '$sum': 1
            }, 
            'android_non_empty': {
                '$sum': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$android'
                                }, 0
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'ios_non_empty': {
                '$sum': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$ios'
                                }, 0
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }, {
        '$sort': {
            'docCount': -1
        }
    }
]

def get_differences_among_categories():
    print("Distribution of differences among permission categories in 2023:")
    res_diff_categories_2023 = collection_2023.aggregate(_distribution_of_diffs_among_permission_categories())
    for doc in res_diff_categories_2023:
        print(doc)

    print("----------------------------------")
    print("Distribution of differences among permission categories in 2024:")
    res_diff_categories_2024 = collection_2024.aggregate(_distribution_of_diffs_among_permission_categories())
    for doc in res_diff_categories_2024:
        print(doc)

    print("----------------------------------")
    print("Distribution of differences among permission categories in 2025:")
    res_diff_categories_2025 = collection_2025.aggregate(_distribution_of_diffs_among_permission_categories())
    for doc in res_diff_categories_2025:
        print(doc)

    print("__________________________________")

def _distribution_of_categories_per_year():
    return [
    {
        '$addFields': {
            'merged': {
                '$mergeObjects': [
                    '$common_permissions', '$permission_diffs'
                ]
            }
        }
    }, {
        '$addFields': {
            'mergedArray': {
                '$objectToArray': '$merged'
            }
        }
    }, {
        '$unwind': {
            'path': '$mergedArray', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$project': {
            'category': '$mergedArray.k', 
            'year': 1, 
            'docId': '$ios_id'
        }
    }, {
        '$group': {
            '_id': '$category', 
            'app_ids': {
                '$addToSet': '$docId'
            }
        }
    }, {
        '$sort': {
            'category': 1
        }
    }
]

def plot_differences_added_removed_across_categories():
    print("Distribution of differences among permission categories between 2023 - 2024:")
    res_diff_categories_2023 = [doc for doc in collection_2023.aggregate(_distribution_of_categories_per_year())]
    res_diff_categories_2024 = [doc for doc in collection_2024.aggregate(_distribution_of_categories_per_year())]
    res_diff_categories_2025 = [doc for doc in collection_2025.aggregate(_distribution_of_categories_per_year())]
    ###
    added_data_2023_2024 = {}
    removed_data_2023_2024 = {}
    for doc_2023 in res_diff_categories_2023:
        for doc_2024 in res_diff_categories_2024:
            if doc_2023["_id"] == doc_2024["_id"]:
                added_data_2023_2024[doc_2023["_id"]] = len([x for x in doc_2024["app_ids"] if x not in doc_2023["app_ids"]])
                removed_data_2023_2024[doc_2023["_id"]] = -1 * len([x for x in doc_2023["app_ids"] if x not in doc_2024["app_ids"]])
    ###
    added_data_2024_2025 = {}
    removed_data_2024_2025 = {}
    for doc_2024 in res_diff_categories_2024:
        for doc_2025 in res_diff_categories_2025:
            if doc_2024["_id"] == doc_2025["_id"]:
                added_data_2024_2025[doc_2024["_id"]] = len([x for x in doc_2025["app_ids"] if x not in doc_2024["app_ids"]])
                removed_data_2024_2025[doc_2024["_id"]] = -1* len([x for x in doc_2024["app_ids"] if x not in doc_2025["app_ids"]])
    ###
    added_data_2023_2025 = {}
    removed_data_2023_2025 = {}
    for doc_2023 in res_diff_categories_2023:
        for doc_2025 in res_diff_categories_2025:
            if doc_2023["_id"] == doc_2025["_id"]:
                added_data_2023_2025[doc_2025["_id"]] = len([x for x in doc_2025["app_ids"] if x not in doc_2023["app_ids"]])
                removed_data_2023_2025[doc_2025["_id"]] = -1* len([x for x in doc_2023["app_ids"] if x not in doc_2025["app_ids"]])
    ###
    categories = set([doc["_id"] for doc in res_diff_categories_2023])
    added_val_23_24, added_val_24_25, removed_val_23_24, removed_val_24_25, cats, both_23 = [], [], [], [], [], []
    for category in categories:
        cats.append(category)
        added_val_23_24.append(added_data_2023_2024[category])
        added_val_24_25.append(added_data_2024_2025[category])
        removed_val_23_24.append(removed_data_2023_2024[category])
        removed_val_24_25.append(removed_data_2024_2025[category])
        both_23.append(added_data_2023_2024[category] - removed_data_2023_2024[category])

    df_1 = pd.DataFrame({
        'categories': cats,
        'added_val_23_24': added_val_23_24,
        'removed_val_23_24': removed_val_23_24, 
        'added_val_24_25': added_val_24_25, 
        'removed_val_24_25': removed_val_24_25,
        'both_23': both_23
        })
    df_1 = df_1.sort_values('both_23', ascending=False).reset_index(drop=True)

    net_23_24  = [(df_1['added_val_23_24'][i] + df_1['removed_val_23_24'][i]) for i in range(0, len(added_val_23_24))]
    net_24_25 = [(df_1['added_val_24_25'][i] + df_1['removed_val_24_25'][i]) for i in range(0, len(added_val_24_25))]
    
    #print(f"{len(added_data_2023_2024)} -- {len(removed_data_2023_2024)} -- {len(net_23_24)}")

    x = range(len(categories))
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.45
    # Offset positions for 2023 and 2024
    x_2023 = [i - bar_width/2 for i in x]
    x_2024 = [i + bar_width/2 for i in x]
    # color combis: 19535F + 4ECDC4 ; D30C7B + 4ECDC4 ; D1437C + 25C4B9
    plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
    #ax.bar(x, added_data_2023_2024, width=bar_width, color="#6C6C6C", edgecolor="black", linewidth=0.5, label="added", zorder=2)
    #ax.bar(x, removed_data_2023_2024, width=bar_width, color="#C6C6C6", edgecolor="black", linewidth=0.5, label="removed", zorder=2)
    # Plot 2023 bars
    ax.bar(x_2023, df_1['added_val_23_24'], width=bar_width, color="#6C6C6C",
        edgecolor="black", linewidth=0.5, label="added 2024", zorder=2)
    ax.bar(x_2023, df_1['removed_val_23_24'], width=bar_width, color="#C6C6C6",
        edgecolor="black", linewidth=0.5, label="removed 2024", zorder=2)

    # Plot 2024 bars
    ax.bar(x_2024, df_1['added_val_24_25'], width=bar_width, color="#6C6C6C",
        edgecolor="black", linewidth=0.5, label="added 2025", zorder=2, hatch="//")
    ax.bar(x_2024, df_1['removed_val_24_25'], width=bar_width, color="#C6C6C6",
        edgecolor="black", linewidth=0.5, label="removed 2025", zorder=2, hatch="//")

    plt.subplots_adjust(bottom=0.29)
    plt.axhline(0, color='black')
    plt.xticks(x, fontsize=16)
    plt.yticks(fontsize=14)
    ax.set_xticklabels(df_1['categories'], rotation=45, ha='right')
    #ax.set_xlim(-bar_width / 2, len(categories) - 1 + bar_width / 2)
    for i in range(0, len(net_23_24)):
        plt.text(x_2023[i], df_1['added_val_23_24'][i] + 2, f'{net_23_24[i]:+}', 
                va='center', ha='center', fontsize=9, zorder=3)
        plt.text(x_2024[i], df_1['added_val_24_25'][i] + 2, f'{net_24_25[i]:+}', 
                va='center', ha='center', fontsize=9, zorder=3)
        #print(net[i])
        #plt.text(i, added_data_2023_2024[i] + 20, f'{net[i]:+}', va='center', ha='center', fontsize=8, zorder=3)
    plt.legend(fontsize=16)
    #plt.tight_layout()
    plt.margins(x=0.01)
    plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"differences_added_removed_23_24_25-({DATE}).pdf"), format="pdf")  
    #plt.tight_layout()
    #plt.show()
    added_val_23_25, removed_val_23_25, cats, both = [], [], [], []
    for category in categories:
            cats.append(category)
            added_val_23_25 .append(added_data_2023_2025[category])
            removed_val_23_25.append(removed_data_2023_2025[category])
            both.append(added_data_2023_2025[category] - removed_data_2023_2025[category])

    df_2 = pd.DataFrame({'categories': cats, 'added_val_23_25': added_val_23_25, 'removed_val_23_25': removed_val_23_25, 'both': both})
    df_2 = df_2.sort_values('both', ascending=False).reset_index(drop=True)
    net_23_25 = [(df_2['added_val_23_25'][i] + df_2['removed_val_23_25'][i]) for i in range(0, len(added_val_23_25))]

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7, zorder=0)
    plt.subplots_adjust(bottom=0.28)
    bar_width = 0.9
    x_2025 = [i for i in x]
    ax.bar(x_2025, df_2['added_val_23_25'], width=bar_width, color="#6C6C6C",
        edgecolor="black", linewidth=0.5, label="added 2025", zorder=2)
    ax.bar(x_2025, df_2['removed_val_23_25'], width=bar_width, color="#C6C6C6",
        edgecolor="black", linewidth=0.5, label="removed 2025", zorder=2)
    plt.axhline(0, color='black')
    plt.xticks(x)
    plt.yticks(fontsize=14)
    ax.set_xticklabels(df_2['categories'], rotation=45, ha='right', fontsize=16)
    #ax.set_xlim(-bar_width / 2, len(categories) - 1 + bar_width / 2)
    for i in range(0, len(net_23_25)):
        plt.text(x_2025[i], df_2['added_val_23_25'][i] + 5, f'{net_23_25[i]:+}', 
                va='center', ha='center', fontsize=12, zorder=3)
    plt.legend(fontsize=16)
    plt.margins(x=0.001)
    plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"differences_added_removed_23_25-({DATE}).pdf"), format="pdf")  


def _app_permissions_per_mapping_category():
    return [
    {
        '$project': {
            'ios_id': 1, 
            'categories_diff': {
                '$objectToArray': '$permission_diffs'
            }, 
            'categories_common': {
                '$objectToArray': '$common_permissions'
            }
        }
    }, {
        '$project': {
            'ios_id': 1, 
            'categories': {
                '$concatArrays': [
                    '$categories_diff', '$categories_common'
                ]
            }
        }
    }, {
        '$unwind': '$categories'
    }, {
        '$project': {
            'ios_id': 1, 
            'category': '$categories.k', 
            'android': '$categories.v.android', 
            'ios': '$categories.v.ios'
        }
    }, {
        '$group': {
            '_id': '$category', 
            'android_non_empty': {
                '$addToSet': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$android'
                                }, 0
                            ]
                        }, '$ios_id', '$$REMOVE'
                    ]
                }
            }, 
            'ios_non_empty': {
                '$addToSet': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$ios'
                                }, 0
                            ]
                        }, '$ios_id', '$$REMOVE'
                    ]
                }
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'category': '$_id', 
            'android_non_empty': 1, 
            'ios_non_empty': 1
        }
    }, {
        '$sort': {
            'category': 1
        }
    }
]
    
def _jitter_plot_data_aggregation():
    return [
    {
        '$project': {
            'merged': {
                '$mergeObjects': [
                    '$common_permissions', '$permission_diffs'
                ]
            }
        }
    }, {
        '$project': {
            'entries': {
                '$objectToArray': '$merged'
            }
        }
    }, {
        '$project': {
            'androidCount': {
                '$size': {
                    '$filter': {
                        'input': '$entries', 
                        'as': 'e', 
                        'cond': {
                            '$gt': [
                                {
                                    '$size': '$$e.v.android'
                                }, 0
                            ]
                        }
                    }
                }
            }, 
            'iosCount': {
                '$size': {
                    '$filter': {
                        'input': '$entries', 
                        'as': 'e', 
                        'cond': {
                            '$gt': [
                                {
                                    '$size': '$$e.v.ios'
                                }, 0
                            ]
                        }
                    }
                }
            }
        }
    }
]

def jitter_plot_about_permission_occurrences():
    def _jitter_plot(cursor, year: int):
        jitter_df = pd.DataFrame(list(cursor))

        # Add jitter
        jitter_strength = 0.3
        jitter_df['android_jitter'] = jitter_df['androidCount'] + np.random.uniform(-jitter_strength, jitter_strength, size=len(jitter_df))
        jitter_df['ios_jitter'] = jitter_df['iosCount'] + np.random.uniform(-jitter_strength, jitter_strength, size=len(jitter_df))

        # Plot
        plt.figure(figsize=(5, 5))
        plt.axline((0, 0), slope=1, color="grey", linestyle="--", linewidth=1)
        plt.grid(True, linestyle='--', alpha=0.5, zorder=-1)
        plt.scatter(jitter_df['ios_jitter'], jitter_df['android_jitter'], alpha=0.6, edgecolor='black', zorder=2)
        plt.xlabel("iOS Categories with Permissions", fontsize=14)
        plt.ylabel("Android Categories with Permissions", fontsize=14)
        #plt.title(f"Android vs iOS Permission Category Usage {year}", fontsize=10)
        plt.xticks(range(0,17), fontsize=12)
        plt.yticks(range(0,17), fontsize=12)
        plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"jitter_plot_permission_occurrences_{year}-({DATE}).pdf"), format="pdf")  
        #plt.show()
 
    cursor = collection_2023.aggregate(_jitter_plot_data_aggregation())
    _jitter_plot(cursor, 2023)
    cursor = collection_2024.aggregate(_jitter_plot_data_aggregation())
    _jitter_plot(cursor, 2024)
    cursor = collection_2025.aggregate(_jitter_plot_data_aggregation())
    _jitter_plot(cursor, 2025)

def cdf_permission_usage_android_ios():
    def _cdf_plot(cursor, year):
        android = []
        ios = []
        for item in cursor:
            android.append(item['androidCount'])
            ios.append(item['iosCount'])

        android_c = Counter(android)
        ios_c = Counter(ios)

        print(android_c)
        
        df_android = pd.DataFrame({"_id": android_c.keys(), "android": android_c.values()}).sort_values('_id').reset_index(drop=True)
        df_ios = pd.DataFrame({"_id": ios_c.keys(), "ios": ios_c.values()}).sort_values('_id').reset_index(drop=True)
        

        stats_df = pd.concat([df_android.set_index('_id'), df_ios.set_index('_id')], axis=1)
        stats_df = stats_df.fillna(0)
        # PDF
        stats_df['pdf_android'] = stats_df['android'] / sum(stats_df['android'])
        stats_df['pdf_ios'] = stats_df['ios'] / sum(stats_df['ios'])
        # CDF
        stats_df['cdf_android'] = stats_df['pdf_android'].cumsum()
        stats_df['cdf_ios'] = stats_df['pdf_ios'].cumsum()
        print(stats_df)
        
        fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
        colors = sns.color_palette("colorblind", 3)
        ax.plot(stats_df.index.to_list(), stats_df['cdf_android'], drawstyle='steps-post', label="Android", color=colors[0])
        ax.plot(stats_df.index.to_list(), stats_df['cdf_ios'], drawstyle='steps-post', label="iOS", color=colors[1])
        plt.axvline(stats_df[stats_df['cdf_android'] >= 0.99].index.values[0], color=colors[0], linestyle='--', label='99th percentile Android')
        plt.axvline(stats_df[stats_df['cdf_ios'] >= 0.99].index.values[0], color=colors[1], linestyle='--', label='99th percentile iOS')
        plt.axvline(stats_df[stats_df['cdf_android'] >= 0.10].index.values[0], color=colors[0], linestyle=':', label='10th percentile Android')
        plt.axvline(stats_df[stats_df['cdf_ios'] >= 0.10].index.values[0], color=colors[1], linestyle=':', label='10th percentile iOS')
        plt.xticks(range(0,16), fontsize=14)
        plt.yticks(np.arange(0,1.1,0.1), fontsize=14)
        plt.xlabel('# of Permission Categories', fontsize=14)
        plt.ylabel('CDF', fontsize=14)
        #plt.title(f'CDF of Permission Distribution ({year})', fontsize=9)
        plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.25, zorder=0)
        plt.legend(loc="lower right", fontsize=14, framealpha=1, markerscale=1)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"get_permission_cdf_ios_android_{year}-({DATE}).pdf"), format="pdf")  
        #plt.show()



    cursor = collection_2023.aggregate(_jitter_plot_data_aggregation())
    _cdf_plot(cursor, 2023)
    cursor = collection_2024.aggregate(_jitter_plot_data_aggregation())
    _cdf_plot(cursor, 2024)
    cursor = collection_2025.aggregate(_jitter_plot_data_aggregation())
    _cdf_plot(cursor, 2025)

def _get_top_most_differences():
    return [
    {
        '$project': {
            'different': {
                '$objectToArray': '$permission_diffs'
            }
        }
    }, {
        '$unwind': '$different'
    }, {
        '$addFields': {
            'category': '$different.k', 
            'android': '$different.v.android', 
            'ios': '$different.v.ios'
        }
    }, {
        '$group': {
            '_id': '$different.k', 
            'android_count': {
                '$sum': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$android'
                                }, 0
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'ios_count': {
                '$sum': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$ios'
                                }, 0
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    }, {
        '$limit': 5
    }
]

def plot_top_5_different_categories_per_year():
    def _plot_top_differences(results, year):
        categories = {}
        for doc in results:
            categories[doc['_id']] = {
                'counts': doc['count'],
                'android': doc['android_count'],
                'ios': doc['ios_count']
            }

        df = pd.DataFrame().from_dict(categories, orient="index")
        
        fig, ax = plt.subplots(figsize=(5, 4))
        p = ax.bar(df.index, df['counts'], color="#6C6C6C", edgecolor="black")
        plt.title(f"Top 5 Permission Categories with Most Differences ({year})", fontsize=10)
        plt.ylabel("Number of Apps with Differences",fontsize=9)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        ax.bar_label(p)
        #plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"top_5_different_categories_{year}-({DATE}).pdf"), format="pdf")  
        #plt.show()
        return df

    years = {
        "2023": collection_2023,
        "2024": collection_2024,
        "2025": collection_2025,
    }

    global_df = pd.DataFrame()

    for year, col in years.items():
        top = col.aggregate(_get_top_most_differences())
        df = _plot_top_differences(top, year)
        global_df = pd.concat([global_df, df.rename(columns={"counts": f"counts_{year}", "ios": f"ios_{year}", "android": f"android_{year}"})], axis=1)
        global_df[f'android_{year}_%'] = global_df[f'android_{year}'] / global_df[f'counts_{year}'] * 100
        global_df[f'android_{year}_%'] = global_df[f'android_{year}_%'].round(1)
        global_df[f'ios_{year}_%'] = global_df[f'ios_{year}'] / global_df[f'counts_{year}'] * 100
        global_df[f'ios_{year}_%'] = global_df[f'ios_{year}_%'].round(1)
        global_df

    print(global_df.iloc[:, [0, 1, 3, 2, 4, 5, 6, 8, 7, 9, 10, 11, 13, 12, 14]].to_latex(index=True))


def plot_permissions_per_category_and_ios_android_per_year():
    def _bar_plot(results, year):
        categories = []
        ios = []
        android = []
        both = []
        for doc in results:
            categories.append(doc['category'])
            both_set = set()
            both_set = set(doc['ios_non_empty']) & set(doc['android_non_empty'])
            both.append(len(both_set))
            ios_only = set(doc['ios_non_empty']).difference(both_set)
            ios.append(len(ios_only))
            android_only = set(doc['android_non_empty']).difference(both_set)
            android.append(len(android_only))
            #print(f"both: {len(both)}; ios only: {len(ios_only)}; ios total: {len(doc['ios_non_empty'])};android only: {len(android_only)}; android total: {len(doc['android_non_empty'])}")

        df = pd.DataFrame(
            {'categories': categories,
            'ios': ios,
            'android': android,
            'both': both
            })
        
        df = df.sort_values(by=['both'], ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 4.5))
        plt.subplots_adjust(bottom=0.25)
        w = 0.45
        x_1 = [i - w/2 for i in range(len(categories))]
        x_2 = [i + w/2 for i in range(len(categories))]
        
        ax.bar(x_1, df['both'], width=w, color="#202020", edgecolor="black", label="Both")
        ax.bar(x_1, df['android'], bottom = df['both'], width=w, color="#727272", edgecolor="black", label="Android")
        ax.bar(x_2, df['both'], width=w, color="#202020", edgecolor="black")
        ax.bar(x_2, df['ios'], bottom = df['both'], width=w, color="#CACACA", edgecolor="black", label="iOS")

        # df["sum_android"] = df['android'] + df['both']
        # df["sum_ios"] = df["ios"] + df["both"]
        # df["android_%"] = df["sum_android"] / 2964 *100
        # df["ios_%"] = df["sum_ios"] / 2964 *100
        # print(df)
        # return

        #plt.title(f"Permissions per Category ({year})")
        plt.ylabel("Number of Apps", fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        ax.set_xticks(range(len(categories)))
        ax.set_yticks(np.arange(0, 3500, 500))
        plt.yticks(fontsize=14)
        ax.set_xticklabels(df['categories'], rotation=45, ha='right', fontsize=14)
        ax.legend(fontsize=14)
        plt.tight_layout()
        plt.margins(x=0.01)
        plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"permissions_per_category_{year}-({DATE})-updated.pdf"), format="pdf")  
        #plt.show()
    
    years = {
        "2023": collection_2023,
        "2024": collection_2024,
        "2025": collection_2025,
    }

    for year, col in years.items():
        top = col.aggregate(_app_permissions_per_mapping_category())
        _bar_plot(top, year)
#get_permission_distribution_of_differences_per_year()


def _get_permission_cat_number_and_app_store_category_per_app_for():
    return [
    {
        '$lookup': {
            'from': 'ios_metadata_2023', 
            'localField': 'ios_id', 
            'foreignField': 'app_id', 
            'as': 'metadata_result'
        }
    }, {
        '$match': {
            'metadata_result.0': {
                '$exists': True
            }
        }
    }, {
        '$addFields': {
            'metadata_result': {
                '$first': '$metadata_result'
            }
        }
    }, {
        '$addFields': {
            'genre': '$metadata_result.attributes.genreDisplayName'
        }
    }, {
        '$addFields': {
            'permission_diffs_array': {
                '$objectToArray': '$permission_diffs'
            }, 
            'permission_common_array': {
                '$objectToArray': '$common_permissions'
            }
        }
    }, {
        '$addFields': {
            'permissions_array': {
                '$concatArrays': [
                    '$permission_diffs_array', '$permission_common_array'
                ]
            }
        }
    }, {
        '$project': {
            'permission_diffs_array': 0, 
            'permission_common_array': 0
        }
    }, {
        '$unwind': {
            'path': '$permissions_array', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$addFields': {
            'category': '$permissions_array.k', 
            'android': '$permissions_array.v.android', 
            'ios': '$permissions_array.v.ios'
        }
    }, {
        '$group': {
            '_id': '$ios_id', 
            'docCount': {
                '$sum': 1
            }, 
            'android_non_empty': {
                '$sum': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$android'
                                }, 0
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'ios_non_empty': {
                '$sum': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$ios'
                                }, 0
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'genre': {
                '$first': '$genre'
            }
        }
    }
]

def plot_permission_cats_per_app_store_category():
    def _bar_plot(cursor, year):
        store_category_dict = {}
        for app in cursor:
            ios_value = (app['ios_non_empty'] if app['ios_non_empty'] is not None else 0)
            android_value = (app['android_non_empty'] if app['android_non_empty'] is not None else 0)
            genre = app['genre']
            if genre not in store_category_dict.keys():
                store_category_dict[genre] = {
                    "ios": [ios_value],
                    "android": [android_value]
                }
            else:
                store_category_dict[genre]['ios'].append(ios_value)
                store_category_dict[genre]['android'].append(android_value)

        for key, value in store_category_dict.items():
            store_category_dict[key]['ios_avg'] = statistics.mean(value['ios'])
            store_category_dict[key]['android_avg'] = statistics.mean(value['android'])

        df = pd.DataFrame().from_dict(store_category_dict, orient="index")
        df = df.sort_values('android_avg', ascending=False)

        bar_width = 0.4
        fig, ax = plt.subplots(figsize=(8,4))
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        x_1 = [i - bar_width/2 for i in range(df.index.size)]
        x_2 = [i + bar_width/2 for i in range(df.index.size)]
        ax.bar(x_1, df['android_avg'], width=bar_width, label="Android", color="#494949")
        ax.bar(x_2, df['ios_avg'], width=bar_width, label="iOS", color="#b5b5b5")
        ax.set_yticks(np.arange(0,8,1))
        ax.set_xticks(range(df.index.size))
        ax.set_xticklabels(df.index, rotation=45, ha='right')
        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_FOLDER_PATH, f"permissions_avg_app_store_category_{year}-({DATE}).pdf"), format="pdf")

        return df
        

    years = {
        "2023": collection_2023,
        "2024": collection_2024,
        "2025": collection_2025,
    }
    global_df = pd.DataFrame()
    for year, col in years.items():
        cursor = col.aggregate(_get_permission_cat_number_and_app_store_category_per_app_for())
        df = _bar_plot(cursor, year)
        global_df = pd.concat([global_df, df[['android_avg','ios_avg']].rename(columns={"ios_avg": f"ios_avg_{year}", "android_avg": f"android_avg_{year}"})], axis=1)

    #print(global_df)
    print(global_df.round(decimals=2).iloc[:, [0, 2, 4, 1, 3, 5]].to_latex(index=True))
    print(global_df.round(decimals=2).to_latex(index=True))

    print(global_df['ios_avg_2023'] - global_df['android_avg_2023'])
    print(global_df['ios_avg_2025'] - global_df['android_avg_2025'])


def _get_permission_distribution_android_ios():
    return [
    {
        '$addFields': {
            'merged': {
                '$mergeObjects': [
                    '$common_permissions', '$permission_diffs'
                ]
            }
        }
    }, {
        '$addFields': {
            'mergedArray': {
                '$objectToArray': '$merged'
            }
        }
    }, {
        '$unwind': {
            'path': '$mergedArray', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$addFields': {
            'category': '$mergedArray.k', 
            'android': '$mergedArray.v.android', 
            'ios': '$mergedArray.v.ios'
        }
    }, {
        '$group': {
            '_id': '$mergedArray.k', 
            'android_non_empty': {
                '$addToSet': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$android'
                                }, 0
                            ]
                        }, '$ios_id', '$$REMOVE'
                    ]
                }
            }, 
            'ios_non_empty': {
                '$addToSet': {
                    '$cond': [
                        {
                            '$gt': [
                                {
                                    '$size': '$ios'
                                }, 0
                            ]
                        }, '$ios_id', '$$REMOVE'
                    ]
                }
            }, 
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    }
]

def get_growth_rate_of_permission_categories_android_vs_ios():
    years = {
        "2023": collection_2023,
        "2025": collection_2025,
    }
    global_df = pd.DataFrame()
    for year, col in years.items():
        cursor = col.aggregate(_get_permission_distribution_android_ios())
        
        cat_dict = {}
        for item in cursor:
            cat_dict[item['_id']] = {
                f'android_{year}': len(item['android_non_empty']),
                f'ios_{year}': len(item['ios_non_empty']),
                #f'total_{year}': item['count']
            }

        df = pd.DataFrame().from_dict(cat_dict, orient="index")
        global_df = pd.concat([global_df, df], axis=1)
    
    global_df['android_growth_total'] = (global_df['android_2025'] - global_df['android_2023'])
    global_df['android_growth_%'] = ( ((global_df['android_2025'] - global_df['android_2023']) / global_df['android_2023']) * 100).round(1)
    global_df['ios_growth_total'] = (global_df['ios_2025'] - global_df['ios_2023'])
    global_df['ios_growth_%'] =  (((global_df['ios_2025'] - global_df['ios_2023']) / global_df['ios_2023']) * 100).round(1)
    global_df['android_ios_diff'] = global_df['android_growth_total'] - global_df['ios_growth_total']
    #print(global_df.fillna(0).apply(pd.to_numeric, downcast='integer').sort_values('android_ios_diff', ascending=False).to_latex())
    #print(global_df['android_growth_%'].sort_values())
    print(global_df["ios_growth_%"].sort_values())
    #print(global_df)

def get_avg_permissions_per_app():
    apps_2023 = collection_2023.find({})
    apps_2024 = collection_2024.find({})
    apps_2025 = collection_2025.find({})

    years = {
        "2023": apps_2023,
        "2024": apps_2024,
        "2025": apps_2025
    }

    for year, apps in years.items():
        android_permissions = []
        ios_permissions = []
        for app in apps:
            android = app.get("total_common_permissions")
            ios = app.get("total_common_permissions")
            permission_diffs = app.get("permission_diffs")
            for category in permission_diffs:
                diff = permission_diffs.get(category)
                if len(diff.get("android")) > 0: android += 1
                if len(diff.get("ios")) > 0: ios += 1
            android_permissions.append(android)
            ios_permissions.append(ios)
        print("---------------------------------------------------------")
        print(f"{year}:")
        print(f"iOS total permissions: {len(ios_permissions)} AVG: {statistics.mean(ios_permissions)}")
        print(f"Android total permissions: {len(android_permissions)} AVG: {statistics.mean(android_permissions)}")
        print("---------------------------------------------------------")



#get_growth_rate_of_permission_categories_android_vs_ios()
#get_permission_distribution_of_differences_per_year()
#get_permission_distribution_cdf()
#get_changes_of_permission_diffs()
#get_differences_among_categories()
#plot_differences_added_removed_across_categories()
#jitter_plot_about_permission_occurrences()
#cdf_permission_usage_android_ios()
#plot_top_5_different_categories_per_year()
#plot_permissions_per_category_and_ios_android_per_year()
#plot_permission_cats_per_app_store_category()
get_avg_permissions_per_app()