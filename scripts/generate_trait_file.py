# Given a Grambank feature ID and a Grambank metadata file,
# the script generates a BayesTraits trait file
# with the following format:

# Language             Feature value

# e.g.
# Baharna Arabic       0
# Egyptian Arabic      0
# Sudanese Arabic      1

# e.g. python3 scripts/generate_trait_file.py ../datasets/grambank-grambank-7ae000c/cldf/StructureDataset-metadata.json GB138

import re
import csv
from pycldf.dataset import Dataset

LANGUAGES = [
    "Sanaani Arabic",
    "Baharna Arabic",
    "Gulf Arabic",
    "Eastern Egyptian Bedawi Arabic",
    "Egyptian Arabic",
    "Chadian Arabic",
    "Nubi",
    "South Sudanese Creole Arabic",
    "Cypriot Arabic",
    "North Levantine Arabic",
    "Libyan Arabic",
    "Hassaniyya",
    "Maltese",
    "Standard Arabic",
]


def map_language_name_to_id(grambank_languages):
    print("Mapping language names to IDs...")

    language_id_by_name = {}

    for language in LANGUAGES:
        language_id_results = [
            grambank_language["ID"]
            for grambank_language in grambank_languages
            if grambank_language["Name"] == language
        ]
        if not language_id_results:
            continue

        language_id = language_id_results[0]
        language_id_by_name[language] = language_id

    return language_id_by_name


def filter_values(grambank_values, feature_id, language_ids):
    print("Filtering values...")

    values_by_language_id = {}

    for value in grambank_values:
        if value["Parameter_ID"] != feature_id:
            continue

        if value["Language_ID"] not in language_ids:
            continue

        values_by_language_id[value["Language_ID"]] = value["Value"]

    return values_by_language_id


def format_data(filtered_values_by_language_id, language_id_by_name):
    print("Formatting data...")

    formatted_data = []

    for language in LANGUAGES:
        value = get_value(filtered_values_by_language_id, language_id_by_name, language)
        formatted_language_name = re.sub(r"\s+", "_", language)
        formatted_data.append([formatted_language_name, value])

    return formatted_data


def get_value(filtered_values_by_language_id, language_id_by_name, language):
    language_id = language_id_by_name.get(language)
    if not language_id:
        return 0

    grambank_value = filtered_values_by_language_id.get(language_id)
    if not grambank_value:
        return 0

    return grambank_value


def write_to_file(data):
    print("Writing to file...")

    with open("data/trait.txt", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=" ")
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    import sys

    metadata_path = sys.argv[1]
    feature_id = sys.argv[2]

    grambank = Dataset.from_metadata(metadata_path)
    language_id_by_name = map_language_name_to_id(grambank["LanguageTable"])
    language_ids = list(language_id_by_name.values())
    filtered_values_by_language_id = filter_values(
        grambank["ValueTable"], feature_id, language_ids
    )
    data = format_data(filtered_values_by_language_id, language_id_by_name)
    write_to_file(data)

    print("All done!")
