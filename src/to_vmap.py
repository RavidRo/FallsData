import pandas as pd


def create_vmap(properties, falls, group_falls, selected_falls):
    properties = properties[["tpid", "meaning"]]
    properties = properties.drop_duplicates()
    properties = properties.rename(columns={"tpid": "Variable ID", "meaning": "Variable Name"})

    properties1 = properties[properties["Variable ID"] == 1]
    properties2 = properties[properties["Variable ID"] >= 47]
    properties = properties1.append(properties2)
    properties.append(
        pd.DataFrame.from_dict(
            falls,
        )
    )

    if group_falls:
        properties = properties.append(
            pd.DataFrame.from_dict({"Variable ID": [min(falls["ids"])], "Variable Name": "Fall"})
        )
    else:
        properties = properties.append(
            pd.DataFrame.from_dict({"Variable ID": falls["ids"], "Variable Name": falls.names})
        )

        # Removing unselected falls
        unselected_falls_properties_ids = [
            fall for fall in falls["ids"] if fall not in selected_falls
        ]
        properties = properties[~properties["Variable ID"].isin(unselected_falls_properties_ids)]

    properties = properties.fillna("missing")
    properties["Description"] = properties["Variable Name"]

    return properties


# 78,fall_no_injury,fall_no_injury
# 79,fall_monitored_injury,fall_monitored_injury
# 80,fall_minor_injury,fall_minor_injury
# 81,fall_major_injury,fall_major_injury
# 82,fall,No data on injury
