# Script was run on metadata file for Grambank v1.0.2.
# Assumes pycldf is installed in environment.
# Requires metadata file name to be passed as arg, e.g.:
# python3 scripts/extract_features_from_grambank.py ../datasets/grambank-grambank-7ae000c/cldf/StructureDataset-metadata.json

import csv
from pycldf.dataset import Dataset


def filter_for_present_parameters(parameter_values):
    values_to_include = ["1"]
    return [value for value in parameter_values if value["Value"] in values_to_include]


def group_languages_by_parameter(parameter_values):
    grouping = {}
    for parameter_value in parameter_values:
        parameter_id = parameter_value["Parameter_ID"]
        if not grouping.get(parameter_id):
            grouping[parameter_id] = []
        grouping[parameter_id].append(parameter_value["Language_ID"])
    return grouping


def map_language_ids_to_names(languages):
    language_ids_to_names = {}
    for language in languages:
        if "Arabic" not in language["Name"] and "Coptic" not in language["Name"]:
            continue

        language_ids_to_names[language["ID"]] = language["Name"]
    return language_ids_to_names


def get_ea_and_coptic_parameters_to_language_ids_not_in_sa(
    parameter_ids_to_language_ids, language_ids_to_names
):
    egyptian_arabic = "egyp1253"
    coptic = "copt1239"
    standard_arabic = "stan1318"
    required_parameters = {}
    for parameter_id, language_ids in parameter_ids_to_language_ids.items():
        parameter_is_required = (
            egyptian_arabic in language_ids and coptic in language_ids
        ) and not (standard_arabic in language_ids)
        if not parameter_is_required:
            continue

        required_parameters[parameter_id] = language_ids
    return required_parameters


def format_into_csv(
    required_parameters_to_language_ids, language_ids_to_names, grambank
):
    data = []
    for parameter_id, language_ids in required_parameters_to_language_ids.items():
        parameter_name = grambank.get_row("ParameterTable", parameter_id)["Name"]
        source = f"Grambank {parameter_id}"
        languages = [
            language_ids_to_names[language_id]
            for language_id in language_ids
            if language_id in language_ids_to_names.keys()
        ]
        data.append([parameter_name, source, languages])
    return data


if __name__ == "__main__":
    import sys

    metadata_path = sys.argv[1]
    grambank = Dataset.from_metadata(metadata_path)

    present_parameter_values = filter_for_present_parameters(grambank["ValueTable"])
    parameter_ids_to_language_ids = group_languages_by_parameter(
        present_parameter_values
    )
    language_ids_to_names = map_language_ids_to_names(grambank["LanguageTable"])
    required_parameters_to_language_ids = (
        get_ea_and_coptic_parameters_to_language_ids_not_in_sa(
            parameter_ids_to_language_ids, language_ids_to_names
        )
    )
    csv_data = format_into_csv(
        required_parameters_to_language_ids, language_ids_to_names, grambank
    )

    with open("features.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
