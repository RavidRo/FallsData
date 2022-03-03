import pandas as pd

def create_vmap(properties, risk_mapping):
    properties = properties.fillna("")
    not_missings = properties[properties['meaning'] != ""]
    not_missings = not_missings[["tpid", "meaning"]].drop_duplicates()
    missings = properties[properties['meaning'] == ""]
    for index, row in missings.iterrows():
        meaning = risk_mapping[risk_mapping['tpid'] == row['id']]['meaning'].to_list()[0]
        agg = row['agg']
        new_meaning = meaning + " " + agg
        missings.at[index, 'meaning'] = new_meaning

    merged = pd.concat([missings, not_missings])

    merged = merged.rename(columns={"tpid": "Variable ID", "meaning": "Variable Name"})
    merged = merged.append({"Variable ID": -1, "Variable Name": "fell"}, ignore_index=True)
    merged["Description"] = merged["Variable Name"]
    merged = merged[["Variable ID", "Variable Name", "Description"]]
    return merged


def filter_vmap(properties, raw_data):
    properties_ids = raw_data["TemporalPropertyID"].drop_duplicates().to_list()
    properties = properties[properties["Variable ID"].isin(properties_ids)]

    return properties
