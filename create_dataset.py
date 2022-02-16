import pandas as pd

from src.balance_entities import balance_entities
from src.to_entities import create_entities
from src.to_raw_data import create_raw_data
from src.to_vmap import create_vmap

falls = {
    "ids": [78, 79, 80, 81, 82],
    "names": [
        "fall_no_injury",
        "fall_monitored_injury",
        "fall_minor_injury",
        "fall_major_injury",
        "fall_no_data",
    ],
}
group_falls = True
balance = True
selected_falls = [80, 81]
target_entities = 200
dataset_directory = "Falls"
data_directory = "data"


def import_data():
    entities_imported = pd.read_csv(data_directory + "/entity_info_mapping_with_score.csv")
    raw_data_imported = pd.read_csv(data_directory + "/FallPrediction_data.csv")
    properties = pd.read_excel(data_directory + "/fall_properties.xlsx")

    return raw_data_imported, properties, entities_imported


def export_data(raw_data, vmap, entities):
    raw_data.to_csv(index=False, path_or_buf=f"{dataset_directory}/raw_data.csv")
    vmap.to_csv(index=False, path_or_buf=f"{dataset_directory}/vmap.csv")
    entities.to_csv(index=False, path_or_buf=f"{dataset_directory}/entities.csv")


if __name__ == "__main__":
    print("Creating Falls dataset ------------")

    raw_data, properties, entities = import_data()

    vmap = create_vmap(properties, falls, group_falls, selected_falls)
    print("Created vmap")
    new_entities = create_entities(raw_data, entities, selected_falls)
    print("Created entities")
    balanced_entities = balance_entities(new_entities, target_entities, balance)

    new_raw_data = create_raw_data(
        balanced_entities, raw_data, selected_falls, falls["ids"], group_falls
    )

    export_data(new_raw_data, vmap, balanced_entities)
    print("Exported successfully dataset")
