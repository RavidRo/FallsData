
def get_informative_entities(entities_imported, raw_data, target):
    entities = entities_imported.rename(columns={"entity_id": "id"})
    entities = entities[["id", "Gender", "AgeRange", "Score"]]
    entities = entities.dropna().drop_duplicates()
    informative_entities = get_most_informative_entities(raw_data, target)
    entities = entities[entities["id"].isin(informative_entities)]
    int_columns = ["AgeRange", "Score"]
    entities[int_columns] = entities[int_columns].astype(int)
    return entities


def get_most_informative_entities(raw_data, count_entities):
    # returning windows with most data rows by different residents
    raw_data_grouped_by = raw_data['EntityID'].value_counts(dropna=True, sort=True).reset_index()
    raw_data_grouped_by.columns = ['EntityID', 'counts']
    entities_chosen = []
    for _, row in raw_data_grouped_by.iterrows():
        if len(entities_chosen) < count_entities:
            entityID = row['EntityID']
            if entityID not in entities_chosen:
                entities_chosen.append(entityID)
        else:
            break
    return entities_chosen
