def create_vmap(properties):
    properties = properties[["tpid", "meaning"]]
    properties = properties.drop_duplicates().dropna()
    properties = properties.rename(columns={"tpid": "Variable ID", "meaning": "Variable Name"})
    properties = properties.append({"Variable ID": -1, "Variable Name": "fell"}, ignore_index=True)

    properties["Description"] = properties["Variable Name"]

    return properties
