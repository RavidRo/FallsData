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


def get_most_informative_entities(raw_data, count_entities):
    raw_data_grouped_by = raw_data['EntityID'].value_counts(dropna=True, sort=True).reset_index()
    raw_data_grouped_by.columns = ['EntityID', 'counts']
    most_data_entities = raw_data_grouped_by.nlargest(count_entities, 'counts')
    entities = most_data_entities['EntityID'].to_list()
    return entities

def create_entities_most_data(entities_imported, raw_data, target, balance_classes):
    entities = entities_imported.rename(columns={"EntityID": "id"})
    entities = entities[["id", "Gender", "AgeRange", "Score", "Class"]]
    entities = entities.dropna().drop_duplicates()

    # raw_data = pd.concat([raw_data.head(100), raw_data.tail(100)])
    fell_raw, not_fell_raw = split_data_to_classes(entities, raw_data)
    fell_informative_entities = get_most_informative_entities(fell_raw, 1000)
    not_fell_informative_entities = get_most_informative_entities(not_fell_raw, 1000)
    informative_entities = fell_informative_entities + not_fell_informative_entities
    entities = entities[entities["id"].isin(informative_entities)]
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
