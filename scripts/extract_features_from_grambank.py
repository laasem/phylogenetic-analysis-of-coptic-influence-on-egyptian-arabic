# Script was run on metadata file for Grambank v1.0.3.
# Assumes python3, pandas, and pycldf are installed in environment.
# Requires metadata file name to be passed as arg, e.g.:
# python3 extract_features_from_grambank.py ../../datasets/grambank-grambank-7ae000c/cldf/StructureDataset-metadata.json

import csv
import pandas as pd
from numpy import array_equal
from pycldf.dataset import Dataset

# Some rows have missing values that get read by Pandas as NaN, hence this categorization
BINARY_VALUES = ["0", "1"]
NON_BINARY_VALUES = ["2", "3"]

EGYPTIAN_ARABIC_ID = "egyp1253"
COPTIC_ID = "copt1239"


# Filter for parameters that have only have "0", "1" or missing values,
# ensuring they do not have missing values for Egyptian Arabic and Coptic,
# and return their IDs
def get_selected_parameter_ids(values):
    print("Filtering parameters...")
    binary_parameter_values = get_binary_parameter_values(values)
    selected_parameter_values = get_parameter_values_where_lang_data_not_missing(
        binary_parameter_values
    )
    return list(selected_parameter_values["Parameter_ID"].unique())


def get_binary_parameter_values(values):
    parameter_id_groups = values.groupby("Parameter_ID")
    return parameter_id_groups.filter(
        lambda group: not group["Value"].isin(NON_BINARY_VALUES).any()
    )


def get_parameter_values_where_lang_data_not_missing(values):
    eg_arabic_existing_parameter_ids = list(
        values[
            values["Language_ID"].isin([EGYPTIAN_ARABIC_ID])
            & values["Value"].isin(BINARY_VALUES)
        ]["Parameter_ID"]
    )
    return values[
        values["Parameter_ID"].isin(eg_arabic_existing_parameter_ids)
        & values["Language_ID"].isin([COPTIC_ID])
        & values["Value"].isin(BINARY_VALUES)
    ]


def format_into_csv(parameters, selected_parameter_ids):
    print("Formatting into CSV...")
    data = [["id", "name"]]
    for parameter_id in selected_parameter_ids:
        parameter_name = parameters[parameters["ID"] == parameter_id]["Name"].values[0]
        data.append([parameter_id, parameter_name])
    return data


if __name__ == "__main__":
    import sys

    metadata_path = sys.argv[1]
    grambank = Dataset.from_metadata(metadata_path)

    all_values = pd.DataFrame(grambank["ValueTable"])
    selected_parameter_ids = get_selected_parameter_ids(all_values)

    all_parameters = pd.DataFrame(grambank["ParameterTable"])
    csv_data = format_into_csv(all_parameters, selected_parameter_ids)

    with open("../data/features.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print("All done!")
