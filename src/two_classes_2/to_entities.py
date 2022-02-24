from math import ceil, floor
import random


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
