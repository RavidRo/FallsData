def create_raw_data(entities, data, selected_falls, all_falls, group_falls):
    ids = entities["id"].drop_duplicates().to_list()
    data = data[["EntityID", "TemporalPropertyID", "TimeStamp", "TemporalPropertyValue"]]
    data = data[data["EntityID"].isin(ids)]

    unselected_falls_properties_ids = [fall for fall in all_falls if fall not in selected_falls]

    # Removing minor falls
    filtered_data = data[~data["TemporalPropertyID"].isin(unselected_falls_properties_ids)]

    # Grouping major falls
    def group_falls(row):
        if row["TemporalPropertyID"] in selected_falls:
            # print("Found row with property: " + str(row["TemporalPropertyID"]))
            row["TemporalPropertyID"] = min(all_falls)
            # print("Changed to " + str(row["TemporalPropertyID"]))
        return row

    if group_falls:
        filtered_data = filtered_data.apply(group_falls, axis=1)

    int_columns = ["EntityID", "TemporalPropertyID", "TimeStamp"]
    filtered_data[int_columns] = filtered_data[int_columns].astype(int)

    print(
        f"Created raw data: there are {len(filtered_data[filtered_data['TemporalPropertyID'].isin(all_falls)])} events of falls"
    )

    return filtered_data
