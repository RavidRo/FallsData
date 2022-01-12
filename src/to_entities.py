import pandas as pd


def __rename_raw_data(raw_data):
    return raw_data[["EntityID", "TimeStamp"]].rename(columns={"EntityID": "id"})


def __create_frequency(raw_data):
    raw_data = raw_data.groupby("id")
    raw_data_max = raw_data.max().rename(columns={"TimeStamp": "max_time"})
    raw_data_min = raw_data.min().rename(columns={"TimeStamp": "min_time"})
    raw_data_count = raw_data.count().rename(columns={"TimeStamp": "count"})
    raw_data = raw_data_max.join(raw_data_min).join(raw_data_count)

    frequency = raw_data.apply(
        lambda row: pd.Series(
            [row[2] / (row[0] - row[1])],
            index=["Frequency"],
        ),
        axis=1,
    )

    # Splitting the frequencies to categories
    std = frequency["Frequency"].std()
    mean = frequency["Frequency"].mean()

    verLow = mean - std * 2
    low = mean - std
    heigh = mean + std
    veryHeigh = mean + std * 2

    bins = [0, verLow, low, heigh, veryHeigh, 100]
    labels = ["Very_Low", "Low", "Average", "High", "Very_High"]
    frequency["Frequency"] = pd.cut(frequency["Frequency"], bins, labels=labels)

    return frequency


def __reformat_entities(entities):
    entities = entities[["entity_id", "Gender", "AgeRange", "Score"]]
    entities = entities.rename(columns={"entity_id": "id", "AgeRange": "Age_Range"})
    entities = entities.drop_duplicates()
    return entities


def __get_selected_falls_entities(entities, raw_data, selected_falls):
    fell = raw_data[raw_data["TemporalPropertyID"].isin(selected_falls)][
        ["EntityID"]
    ].drop_duplicates()
    return entities[entities["id"].isin(fell["EntityID"].to_list())]


def create_entities(raw_data_imported, entities_imported, selected_falls):
    renamed_raw_data = __rename_raw_data(raw_data_imported)
    frequenced_data = __create_frequency(renamed_raw_data)

    reformated_entities = __reformat_entities(entities_imported)
    entities_with_frequency = reformated_entities.join(frequenced_data, on="id")

    # Removed rows with null
    entities_with_frequency = entities_with_frequency.dropna()

    entities_only_selected = __get_selected_falls_entities(
        entities_with_frequency, raw_data_imported, selected_falls
    )

    # Puts the data in the right order and sets numerical columns to integers
    entities_only_selected["Score"] = entities_only_selected.apply(
        lambda row: int(row["Score"]), axis=1
    )
    entities_only_selected["Age_Range"] = entities_only_selected.apply(
        lambda row: int(row["Age_Range"]), axis=1
    )
    entities_only_selected["id"] = entities_only_selected.apply(lambda row: int(row["id"]), axis=1)
    entities = entities_only_selected[["id", "Gender", "Age_Range", "Score", "Frequency"]]

    return entities
