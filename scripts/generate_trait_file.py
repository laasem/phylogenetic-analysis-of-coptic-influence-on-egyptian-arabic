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


def filter_values(grambank, feature_id):
    values = grambank["ValueTable"]
    filtered_values = []
    for value in values:
        if value["Parameter_ID"] != feature_id:
            continue

        if value["Language_ID"]

if __name__ == "__main__":
    import sys

    metadata_path = sys.argv[1]
    grambank = Dataset.from_metadata(metadata_path)
    feature_id = sys.argv[2]
