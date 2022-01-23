import pandas as pd


def create_entities(raw_data_imported, entities_imported):
    # Renaming columns
    entities = entities_imported.rename(columns={"EntityID": "id"})
    entities = entities[["id", "Gender", "Age", "Height", "Owner_Score"]]

    # Selecting chosen entities
    entities_ids = list(raw_data_imported["EntityID"].unique())
    entities = entities[entities["id"].isin(entities_ids)]

    int_columns = ["Age", "Owner_Score"]
    entities[int_columns] = entities[int_columns].astype(int)

    return entities
