import random


def create_entities(entities_imported, target):
    # Renaming columns
    entities = entities_imported.rename(columns={"EntityID": "id"})
    entities = entities[["id", "Gender", "AgeRange", "Score"]]

    entities = entities.dropna().drop_duplicates()

    # Choosing 'target' entities
    entities_ids = entities["id"].drop_duplicates().to_list()
    chosen_entities_ids = random.sample(entities_ids, target)
    chosen_data = cleaned_data[cleaned_data["EntityID"].isin(chosen_entities_ids)]

    int_columns = ["AgeRange", "Score"]
    entities[int_columns] = entities[int_columns].astype(int)

    return entities


def choose_entities():
    # Selecting chosen entities
    entities_ids = list(raw_data_imported["EntityID"].unique())
    entities = entities[entities["id"].isin(entities_ids)]

    return entities
