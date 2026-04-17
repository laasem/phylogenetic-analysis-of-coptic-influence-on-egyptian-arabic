# Package assumes python3 and pip3 installed in environment.
# TODO: Add comment about csv file path and grambank version.

# Install and import needed package to read CLDF datasets
# pip install pycldf
# from pycldf.dataset import Dataset

# Initialize constant of Egyptian Arabic lang ID

# Initialize constant of Coptic lang ID

# Initialize constant array of other Arabic dialect lang IDs

# Read values.csv file

# Group by Parameter_ID to generate a dict where Parameter_ID: [Array of Language_IDs]

# Loop over dict and get Parameter_IDs whose arrays have Coptic and EG Arabic IDs, but not standard Arabic

# Get parameter names from parameters.csv

# Generate CSV with Feature (parameter name), Source ("Grambank #{ID}"), Other Arabic dialects (map using languages.csv) 
