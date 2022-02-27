import os
import pandas as pd

from src.two_classes_2.to_entities import create_entities, create_entities_most_data
from src.two_classes_2.to_raw_data import create_raw_data
from src.two_classes_2.to_vmap import create_vmap, filter_vmap

target_entities = 10000
balance_classes = True
dataset_directory = "Falls"
two_classes_directory = "time_window_data"
data_directory = "data"


def import_data():
    path = os.path.join(data_directory, two_classes_directory)
    entities_imported = pd.read_csv(path + "/entities_info_windows.csv")
    raw_data_imported = pd.read_csv(path + "/hogo_data_windows.csv")
    properties = pd.read_csv(path + "/fall_properties.csv")

    return raw_data_imported, properties, entities_imported


def export_data(raw_data, vmap, entities):
    raw_data.to_csv(index=False, path_or_buf=f"{dataset_directory}/raw_data.csv")
    vmap.to_csv(index=False, path_or_buf=f"{dataset_directory}/vmap.csv")
    entities.to_csv(index=False, path_or_buf=f"{dataset_directory}/entities.csv")


if __name__ == "__main__":
    print("Creating Falls dataset ------------")

    raw_data, properties, entities = import_data()

    vmap = create_vmap(properties)
    print("Created vmap")

    classification_rows = raw_data[raw_data["TemporalPropertyID"] == -1]

    new_entities = create_entities_most_data(entities, raw_data, target_entities, balance_classes)
    print("Created entities")

    new_raw_data = create_raw_data(raw_data, new_entities, vmap)

    vmap = filter_vmap(vmap, new_raw_data)

    export_data(new_raw_data, vmap, new_entities)
    print("Exported successfully dataset")
