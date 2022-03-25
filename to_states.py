import pandas as pd

falls_properties_ids = [78]
unused_falls_properties_ids = [79, 82]

output_directory = "Falls_one_class_100_balanced"
input_directory = "data"

entities_imported = pd.read_csv(output_directory + "/entities.csv")
raw_data_imported = pd.read_csv(output_directory + "/raw_data.csv")
vmap_imported = pd.read_csv(output_directory + "/vmap.csv")
states_imported = pd.read_csv(input_directory + "/states.csv")

entities_ids = entities_imported["id"].to_list()
falls = raw_data_imported[raw_data_imported["TemporalPropertyID"].isin(falls_properties_ids)]

new_states = states_imported

# Removing old states
new_states = new_states[~new_states["TemporalPropertyID"].isin(falls_properties_ids)]
new_states = new_states[~new_states["TemporalPropertyID"].isin(unused_falls_properties_ids)]

# Adding new states
max_state_id = new_states["StateID"].max()
new_state_id = max_state_id + 1

for fall_id in falls_properties_ids:
    property_name = vmap_imported[vmap_imported["Variable ID"] == fall_id]["Variable Name"].iloc[0]
    new_states = new_states.append(
        {
            "StateID": new_state_id,
            "TemporalPropertyID": fall_id,
            "Method": "???",
            "BinID": 0,
            "BinLow": -1,
            "BinHigh": 1,
            "TemporalPropertyName": property_name,
            "BinLabel": "Event",
        },
        ignore_index=True,
    )
    new_state_id += 1

# Adding bin lables
def bins(row):
    if row["TemporalPropertyID"] in falls_properties_ids:
        return "Event"
    elif row["BinID"] == 0:
        return "Decresing"
    elif row["BinID"] == 1:
        return "Stable"
    elif row["BinID"] == 2:
        return "Increasing"
    else:
        return "???"


new_states["BinLabel"] = new_states.apply(bins, axis=1)
new_states.to_csv(index=False, path_or_buf=output_directory + "/states.csv")


# Creating the falls intervals
intervals = {id: [] for id in entities_ids}
for i in range(len(falls)):
    row = falls.iloc[i]
    entity_id = int(row["EntityID"])
    start_time = int(row["TimeStamp"])
    property_id = int(row["TemporalPropertyID"])
    symbol_id = new_states[new_states["TemporalPropertyID"] == property_id]["StateID"].iloc[0]
    interval = (start_time, start_time + 1, symbol_id, property_id)
    intervals[entity_id].append(interval)

KL_imported = open(input_directory + "/KL.txt", "r")
KL_new = open(output_directory + "/KL.txt", "w")

KL_strings = KL_imported.readlines()
KL_new.writelines(KL_strings[:2])
KL_strings = KL_strings[2:]

for line_number in range(0, len(KL_strings), 2):
    head_line = KL_strings[line_number]
    data_line = KL_strings[line_number + 1]

    entity_id = head_line.split(";")[0].split(",")[0]

    current_intervals = set(intervals[int(entity_id)])
    old_intervals = data_line.split(";")
    old_intervals = filter(lambda line: line != "\n" and line != "", old_intervals)
    old_intervals = filter(
        lambda line: int(line.split(",")[3]) not in falls_properties_ids, old_intervals
    )
    old_intervals = filter(
        lambda line: int(line.split(",")[3]) not in unused_falls_properties_ids, old_intervals
    )
    old_intervals = list(old_intervals)

    for interval in current_intervals:
        old_intervals.append(f"{interval[0]},{interval[1]},{interval[2]},{interval[3]}")

    def cmp(key):
        splitted = key.split(",")
        return int(splitted[0]), int(splitted[1])

    new_intervals = sorted(old_intervals, key=cmp)

    new_data_line = ";".join(new_intervals) + ";\n"

    KL_new.write(head_line)
    KL_new.write(new_data_line)

KL_imported.close()
KL_new.close()
