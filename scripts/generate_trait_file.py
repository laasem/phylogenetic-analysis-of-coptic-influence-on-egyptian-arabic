# Given a Grambank feature ID and a Grambank metadata file,
# the script generates a BayesTraits trait file
# with the following format:

# Language             Feature value

# e.g.
# Baharna Arabic       0
# Egyptian Arabic      0
# Sudanese Arabic      1

# e.g. python3 scripts/generate_trait_file.py ../datasets/grambank-grambank-7ae000c/cldf/StructureDataset-metadata.json GB138

from pycldf.dataset import Dataset

LANGUAGES = [
    "Hadrami Arabic",
    "Hijazi Arabic",
    "Judeo-Yemeni Arabic",
    "Sanaani Arabic",
    "Baharna Arabic",
    "Dhofari Arabic",
    "Ru'us al-Jibal",
    "Gulf Arabic",
    "Najdi Arabic",
    "Omani Arabic",
    "Ta'izzi-Adeni Arabic",
    "Tajiki Arabic",
    "Khorasan Arabic",
    "Qashqa-Darya Arabic",
    "Gilit Mesopotamian Arabic",
    "Judeo-Iraqi Arabic",
    "North Mesopotamian Arabic",
    "Eastern Egyptian Bedawi Arabic",
    "Egyptian Arabic",
    "Saidi Arabic",
    "Chadian Arabic",
    "Nubi",
    "South Sudanese Creole Arabic", 
    "Sudanese Arabic",
    "Cypriot Arabic",
    "Levantine Arabic",
    "Judeo-Tripolitanian Arabic", 
    "Libyan Arabic",
    "Hassaniyya",
    "Algerian Arabic",
    "Algerian Saharan Arabic",
    "Andalusian Arabic",
    "Judeo-Moroccan Arabic",
    "Maltese",
    "Tunisian Arabic",
    "Moroccan Arabic",
    "Standard Arabic"
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

    formatted_data = ""

    for language in LANGUAGES:
        value = get_value(filtered_values_by_language_id, language_id_by_name, language)
        formatted_data += f"{language}\t{value}\n"

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

    with open("data/trait.txt", "w", encoding="utf-8") as textfile:
        textfile.write(data)


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
