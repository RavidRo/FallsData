import random


def create_raw_data(data, entities, properties):
    # Taking out rows with unnamed properties
    properties_ids = properties["Variable ID"].to_list()
    cleaned_data = data[data["TemporalPropertyID"].isin(properties_ids)]

    # Choosing 'target' entities
    entities_ids = entities["id"].drop_duplicates().to_list()
    chosen_data = cleaned_data[cleaned_data["EntityID"].isin(entities_ids)]

    int_columns = ["TimeStamp"]
    chosen_data[int_columns] = chosen_data[int_columns].astype(int)

    # Reordering columns
    chosen_data = chosen_data[
        ["EntityID", "TemporalPropertyID", "TimeStamp", "TemporalPropertyValue"]
    ]

    print(f"Created raw data")

    return chosen_data
