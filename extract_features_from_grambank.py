# Script was run on metadata file for Grambank v1.0.2 and assumes pycldf is installed in environment.

from itertools import groupby
from pycldf.dataset import Dataset

def map_language_names_to_ids(languages):
    language_names_to_ids = {}
    for language in languages:
        if "Arabic" not in language["Name"] and "Coptic" not in language["Name"]: continue

        language_names_to_ids[language["Name"]] = language["ID"]
    return language_names_to_ids

def get_positive_features(values):
    values_to_exclude = ["0", None]
    return [value for value in values if value["Value"] not in values_to_exclude]

if __name__ == '__main__':
    import sys

    metadata_path = sys.argv[1]
    grambank = Dataset.from_metadata(metadata_path)

    language_names_to_ids = map_language_names_to_ids(grambank["LanguageTable"])
    positive_features = get_positive_features(grambank["ValueTable"])
    # groupby(positive_features, "Parameter_ID")

# Group by Parameter_ID to generate a dict where Parameter_ID: [Array of Language_IDs]

# Loop over dict and get Parameter_IDs whose arrays have Coptic and EG Arabic IDs, but not standard Arabic

# Get parameter names from parameters.csv

# Generate CSV with Feature (parameter name), Source ("Grambank #{ID}"), Other Arabic dialects (map using languages.csv)

# Include value (whether 1 or 2 or 3) in output
