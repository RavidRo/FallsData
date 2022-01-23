import random


def create_raw_data(data, target, properties):
    # Removing unnamed columns
    data = data.loc[:, ~data.columns.str.contains("^Unnamed")]

    # Taking our rows with unnamed properties
    properties_ids = properties["Variable ID"].to_list()
    cleaned_data = data[data["TemporalPropertyID"].isin(properties_ids)]

    # Choosing 'target' entities
    entities_ids = cleaned_data["EntityID"].drop_duplicates().to_list()
    chosen_entities_ids = random.sample(entities_ids, target)
    chosen_data = cleaned_data[cleaned_data["EntityID"].isin(chosen_entities_ids)]

    int_columns = ["TimeStamp"]
    chosen_data[int_columns] = chosen_data[int_columns].astype(int)

    print(f"Created raw data")

    return chosen_data
