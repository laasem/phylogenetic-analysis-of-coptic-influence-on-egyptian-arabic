# Given a list of Grambank feature IDs and a Grambank metadata file,
# the script generates and saves the corresponding BayesTraits trait files,
# each with the following format:

# Language             Feature value

# e.g.
# Baharna Arabic       0
# Egyptian Arabic      0
# Sudanese Arabic      1

# Script was run on metadata file for Grambank v1.0.3.
# Assumes python3, pandas, and pycldf are installed in environment.
# Requires metadata file name to be passed as arg, e.g.:
# python3 generate_trait_file.py ../../datasets/grambank-grambank-7ae000c/cldf/StructureDataset-metadata.json GB111,GB107,GB326

import re
import csv
import pandas as pd
from pycldf.dataset import Dataset

LANGUAGES = [
    "Sanaani Arabic",
    "Baharna Arabic",
    "Gulf Arabic",
    "Eastern Egyptian Bedawi Arabic",
    "Egyptian Arabic",
    "Chadian Arabic",
    "Nubi",
    "Cypriot Arabic",
    "North Levantine Arabic",
    "Libyan Arabic",
    "Hassaniyya",
    "Maltese",
]


def get_languages(grambank):
    languages = pd.DataFrame(grambank["LanguageTable"])
    id_name_data = languages[languages["Name"].isin(LANGUAGES)][["ID", "Name"]]
    return dict(zip(id_name_data["Name"], id_name_data["ID"]))


def get_values(grambank, feature_ids, language_ids):
    values = pd.DataFrame(grambank["ValueTable"])
    return values[
        values["Language_ID"].isin(language_ids)
        & values["Parameter_ID"].isin(feature_ids)
    ]


def get_data(feature_values, languages):
    formatted_data = []
    for language in LANGUAGES:
        language_id = languages[language]
        value = get_value(feature_values, language_id)
        formatted_language_name = re.sub(r"\s+", "_", language)
        formatted_data.append([formatted_language_name, value])
    return formatted_data


def get_value(feature_values, language_id):
    results = feature_values[feature_values["Language_ID"] == language_id]
    value = results["Value"].values[0]
    if value not in ["0", "1"]:
        return "-"

    return value


def write_to_file(data, feature_id):
    print("Writing to file...")

    with open(
        f"../data/trait_files/trait_{feature_id}.txt", "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file, delimiter=" ")
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    import sys

    metadata_path = sys.argv[1]
    feature_ids = sys.argv[2].split(",")

    grambank = Dataset.from_metadata(metadata_path)
    languages = get_languages(grambank)
    language_ids = list(languages.values())
    values = get_values(grambank, feature_ids, language_ids)

    for feature_id in feature_ids:
        print(f"Generating trait file for Grambank parameter with ID {feature_id}...")
        feature_values = values[values["Parameter_ID"] == feature_id]
        data = get_data(feature_values, languages)
        write_to_file(data, feature_id)
        print(f"All done for feature {feature_id}!")

    print("All done for all features!")
