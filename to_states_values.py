import pandas as pd


output_directory = "Falls_two_class_10000_unbalanced"
input_directory = "data"

states_imported = pd.read_csv(input_directory + "/states.csv")

# Adding bin lables
def bins(row):
    if row["BinID"] == 0:
        return "Low"
    elif row["BinID"] == 1:
        return "Medium"
    elif row["BinID"] == 2:
        return "High"
    else:
        return "???"


states_imported["BinLabel"] = states_imported.apply(bins, axis=1)
states_imported.to_csv(index=False, path_or_buf=output_directory + "/states.csv")
