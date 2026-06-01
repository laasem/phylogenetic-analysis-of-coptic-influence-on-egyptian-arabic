# Script was run on metadata file for Grambank v1.0.3.
# Assumes python3, pandas, and pycldf are installed in environment.
# Requires metadata file name to be passed as arg, e.g.:
# python3 extract_features_from_grambank.py ../../datasets/grambank-grambank-7ae000c/cldf/StructureDataset-metadata.json

import csv
import pandas as pd
from pycldf.dataset import Dataset


# Filter for parameters that have binary values for Egyptian Arabic and Coptic
# and return their IDs
def get_selected_parameter_ids(all_languages, all_values):
    print("Filtering parameters...")
    language_ids = get_language_ids(all_languages)
    selected_parameter_values = all_values[
        all_values["Value"].isin(["0", "1"])
        & all_values["Language_ID"].isin(language_ids)
    ]
    return list(selected_parameter_values["Parameter_ID"].unique())


def get_language_ids(all_languages):
    return list(
        all_languages[all_languages["Name"].isin(["Egyptian Arabic", "Coptic"])]["ID"]
    )


def format_into_csv(all_parameters, selected_parameter_ids):
    print("Formatting into CSV...")
    data = [["id", "name"]]
    for parameter_id in selected_parameter_ids:
        parameter_name = all_parameters[all_parameters["ID"] == parameter_id][
            "Name"
        ].values[0]
        data.append([parameter_id, parameter_name])
    return data


if __name__ == "__main__":
    import sys

    metadata_path = sys.argv[1]
    grambank = Dataset.from_metadata(metadata_path)
    all_languages = pd.DataFrame(grambank["LanguageTable"])
    all_parameters = pd.DataFrame(grambank["ParameterTable"])
    all_values = pd.DataFrame(grambank["ValueTable"])
    selected_parameter_ids = get_selected_parameter_ids(all_languages, all_values)
    csv_data = format_into_csv(all_parameters, selected_parameter_ids)

    with open("../data/features.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print("All done!")
