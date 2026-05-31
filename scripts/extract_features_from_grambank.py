# Script was run on metadata file for Grambank v1.0.3.
# Assumes pandas and pycldf are installed in environment.
# Requires metadata file name to be passed as arg, e.g.:
# python3 extract_features_from_grambank.py ../../datasets/grambank-grambank-7ae000c/cldf/StructureDataset-metadata.json

import csv
import pandas as pd
from pycldf.dataset import Dataset


# Get only parameters that have binary values for Egyptian Arabic and Coptic
def filter_parameters(languages, values):
    print("Filtering parameters...")
    language_ids = get_language_ids(languages)
    return values[
        values["Value"].isin(["0", "1"]) & values["Language_ID"].isin(language_ids)
    ]


def get_language_ids(languages):
    return list(languages[languages["Name"].isin(["Egyptian Arabic", "Coptic"])]["ID"])


def format_into_csv(parameters, parameter_values):
    print("Formatting into CSV...")
    data = [["id", "name"]]
    for _, parameter_value in parameter_values.iterrows():
        parameter_id = parameter_value["Parameter_ID"]
        parameter_name = parameters[parameters["ID"] == parameter_id]["Name"].values[0]
        data.append([parameter_id, parameter_name])
    return data


if __name__ == "__main__":
    import sys

    metadata_path = sys.argv[1]
    grambank = Dataset.from_metadata(metadata_path)
    languages = pd.DataFrame(grambank["LanguageTable"])
    parameters = pd.DataFrame(grambank["ParameterTable"])
    values = pd.DataFrame(grambank["ValueTable"])
    parameter_values = filter_parameters(languages, values)
    csv_data = format_into_csv(parameters, parameter_values)

    with open("../data/features.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print("All done!")
