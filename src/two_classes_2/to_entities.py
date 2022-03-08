from math import ceil, floor
import random
import pandas as pd


def split_data_to_classes(entities, raw_data):
    fell_ids = entities[entities["Class"] == 1].drop_duplicates().dropna()["id"].to_list()
    did_not_fell_ids = (
        entities[entities["Class"] == 0].drop_duplicates().dropna()["id"].to_list()
    )
    fell_raw_data = raw_data[raw_data['EntityID'].isin(fell_ids)]
    not_fell_raw_data = raw_data[raw_data['EntityID'].isin(did_not_fell_ids)]
    return fell_raw_data, not_fell_raw_data


def get_most_informative_entities(raw_data, count_entities, entities_info):
    # returning windows with most data rows by different residents
    raw_data_grouped_by = raw_data['EntityID'].value_counts(dropna=True, sort=True).reset_index()
    raw_data_grouped_by.columns = ['EntityID', 'counts']
    windows_entities_mapping = {}
    for _, row in entities_info.iterrows():
        windows_entities_mapping[row['id']] = row['ConnectionID']
    entities_chosen = []
    windodws_chosen = []
    for _, row in raw_data_grouped_by.iterrows():
        if len(windodws_chosen) < count_entities:
            window_id = row['EntityID']
            entity_id = windows_entities_mapping[window_id]
            if entity_id not in entities_chosen:
                entities_chosen.append(entity_id)
                windodws_chosen.append(window_id)
        else:
            break
    return windodws_chosen


def create_entities_most_data(entities_imported, raw_data, target, balance_classes):
    entities = entities_imported.rename(columns={"EntityID": "id", "AgeRange_x": "AgeRange", "Score_x": "Score", "Gender_x": "Gender"})
    entities = entities[["id", "Gender", "AgeRange", "Score", "Class", "ConnectionID"]]
    entities = entities.dropna().drop_duplicates()
    fell_raw, not_fell_raw = split_data_to_classes(entities, raw_data)
    fell_informative_entities = get_most_informative_entities(fell_raw, int(target/2), entities)
    not_fell_informative_entities = get_most_informative_entities(not_fell_raw, int(target/2), entities)
    informative_entities = fell_informative_entities + not_fell_informative_entities
    entities = entities[entities["id"].isin(informative_entities)]
    entities = entities.drop(labels='ConnectionID', axis=1)
    int_columns = ["AgeRange", "Score"]
    entities[int_columns] = entities[int_columns].astype(int)
    return entities



def create_entities(entities_imported, target, balance_classes):
    # Renaming columns
    entities = entities_imported.rename(columns={"EntityID": "id"})
    entities = entities[["id", "Gender", "AgeRange", "Score", "Class"]]

    entities = entities.dropna().drop_duplicates()

    # Choosing 'target' entities
    if balance_classes:
        fell_ids = entities[entities["Class"] == 1].drop_duplicates().dropna()["id"].to_list()
        did_not_fell_ids = (
            entities[entities["Class"] == 0].drop_duplicates().dropna()["id"].to_list()
        )
        chosen_entities_ids_did_not_fell = random.sample(did_not_fell_ids, floor(target / 2))
        chosen_entities_ids_fell = random.sample(fell_ids, ceil(target / 2))
        chosen_entities_ids = chosen_entities_ids_did_not_fell + chosen_entities_ids_fell
    else:
        entities_ids = entities["id"].drop_duplicates().to_list()
        chosen_entities_ids = random.sample(entities_ids, target)
    entities = entities[entities["id"].isin(chosen_entities_ids)]

    int_columns = ["AgeRange", "Score"]
    entities[int_columns] = entities[int_columns].astype(int)

    return entities
