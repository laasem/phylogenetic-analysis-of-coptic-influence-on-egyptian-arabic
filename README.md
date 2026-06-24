# "Mā Tiktib": A Phylogenetic Analysis of Egyptian Arabic Grammatical Deviation Towards Coptic

An R pipeline to phylogenetically assess Egyptian Arabic grammatical deviation towards Coptic.

Part of a master's thesis by Lara Ahmed under the supervision of Dr. Thomas Brochhagen. Submitted to Universitat Pompeu Fabra's Department of Translation and Language Studies for the Master's Degree in Theoretical and Applied Linguistics.

## Setup

1. Install R version 4.5.1, Python version 3.14.3, and the uv Python package manager if not installed.
2. Download [BayesTraits](https://www.evolution.reading.ac.uk/BayesTraitsV5.0.3/BayesTraitsV5.0.3.html) and set the `BAYESTRAITS_PATH` constant in the `BayesTraits.Rmd` file to the relative path for the BayesTraits binary.
3. Download the [Grambank dataset](https://zenodo.org/records/7844558) and and set the `GRAMBANK_PATH` constant in the `BayesTraits.Rmd` file to the relative path for `StructureDataset-metadata.json` file.
4. Clone https://github.com/ddediu/lgfam-newick and set the `LGFAMNEWICK_PATH` to the relative path to that repository.

## Run

```shell
cd scripts
uv sync
source .venv/bin/activate
Rscript BayesTraits.Rmd
```

The Python scripts can also be run on their own to extract features and generate trait files. See each individual script for requirements.
