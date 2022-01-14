import copy
import random

def balance_entities(entities_imported, target, balance):
    ids_list = entities_imported["id"].to_list()
    columns = entities_imported.columns.drop(["id"]).to_list()

    bins = {}
    bins_target = {}
    bins_count = {}
    bins_count_total = {}  # Used for evaluating results

    # initiating data structures
    for column in columns:
        unique_list = entities_imported[column].unique().tolist()
        bins[column] = unique_list
        bins_count[column] = [0] * len(unique_list)
        bins_count_total[column] = [0] * len(unique_list)
        bins_target[column] = [target / len(unique_list)] * len(unique_list)

    # Getting the data in the right format
    entities = entities_imported.drop("id", axis=1)
    entities = entities.to_dict(orient="records")
    # Female,85, 1, High -> {'Gender': 0, 'Age_Range': 0, 'Score': 1, 'Frequency': 2}
    entities_indexes = list(
        map(
            lambda entity: {column: bins[column].index(entity[column]) for column in columns},
            entities,
        )
    )

    # entity for example: {'Gender': 0, 'Age_Range': 0, 'Score': 1, 'Frequency': 2}
    # Score function for choosing the best entity each iteration
    def entity_score(entity, bins_count):
        if entity is None:
            return -100 * len(columns)

        if balance:
            score = 0
            for column in columns:
                index = entity[column]
                target = bins_target[column][index]
                current_count = bins_count[column][index]
                # The precentage needed to get to our goal
                # The score is in precentage because we want to treat equally all columns
                score += (target - current_count) / target
            
            return score
        else:
            return random.uniform(-1, 1)

    # returns the best candidate and its index, by the score function
    def get_best_candidate(candidates, bins_count):
        best_candidate = None
        best_index = -1
        best_score = -100 * len(columns)

        index = 0
        while index < len(candidates):
            candidate = candidates[index]
            score = entity_score(candidate, bins_count)
            if score >= best_score:
                best_score = score
                best_candidate = candidate
                best_index = index

            index += 1

        return best_candidate, best_index

    # Choosing the best TARGET sized group

    solution_ids = set()
    # After chosen put None in candidates instead of the chosen one
    candidates = copy.deepcopy(entities_indexes)
    while len(solution_ids) < target:
        candidate, index = get_best_candidate(candidates, bins_count)
        for column in candidate:
            bin_index = candidate[column]
            bins_count[column][bin_index] += 1
        solution_ids.add(ids_list[index])
        candidates[index] = None

    filtered_entities = entities_imported[entities_imported["id"].isin(solution_ids)]

    # For debugging :
    for entity in entities_indexes:
        for column in entity:
            bin_index = entity[column]
            bins_count_total[column][bin_index] += 1

    print("Entities balanced:")
    print(bins_count)
    print(bins_count_total)

    return filtered_entities
