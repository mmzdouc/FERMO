# FERMO: Formulation of mEtrics from Reproducible Metabolomics Objects

## Overview

### Attention: **FERMO** is currently in early development and many of the modules are not finished yet.

This is the Github repository for **FERMO**, an open-source pipeline for the processing and visualization of mass-spectrometry data. **FERMO** is specifically aimed towards samples coming from natural product discovery experiments. **FERMO** allows to score samples for complexity, diversity, and novelty by wrapping tools for parameter finding, peak picking, annotation. The samples with the highest chemical diversity and novelty, but lowest convolutendess in terms of peak overlap, are highlighted. **FERMO** can also integrate bioactivity data into its metrics. In the future, an interactive web interface will allow to explore results. Aimed to guarantee reproducibility by design, **FERMO** allows to quickly prioritize interesting samples and peaks for targeted isolation and characterization. 

The goal of the project is to provide users with a pragmatic way to score samples for their appeal regarding consecutive isolation (e.g. which samples are most interesting to follow up in terms of peak separation, bioactivty, novelty, and chemical diversity).

For information on how to install and run **FERMO**, check this tutorial. Please, take into account that this tool has been currently only tested on Ubuntu.

## License
MIT License

## Documentation for users

**FERMO**  is currently in early development and many of the modules are not finished yet. At the moment, it can only be run from command line.

### Installation

First, clone the **FERMO** Github repository:

```
~$ git clone https://github.com/mmzdouc/FERMO.git
```

**FERMO** has a number of dependencies, which need to be installed first.
It is recommended to use a Python package manager, such as conda.

```
# Create conda environment and install dependencies
~$ conda create --name FERMO numpy pandas matchms pyteomics
# Activate conda environment
~$ conda activate FERMO
```


### Overview and example run
The typical workflow for FERMO consists of following steps:
1) Process LCMS/MS data with MzMine 3 and export the peaktable in *ALL/FULL* format using the *GNPS - Feature Based Molecular Networking* function. 
2) (Optional) Prepare a metadata file (indicating which samples are proper samples and which are blanks) and/or a bioactivity file (indicating active/inactive samples)
3) Run **FERMO's** ```main.py``` function as indicated below

```
# Run FERMO with example data:
~$ python ./main.py -p example_data/peaktable_full.csv -m example_data/msms.mgf -b example_data/bioactivity.csv -M example_data/metadata.csv
```

### Comments:
- Currently, **FERMO**  accepts a MzMine3 formatted peaktable. In future updates, other peakpicking program output formats will be included as well.
- **FERMO** accepts additional parameter that influence its behaviour (e.g. precursor m/z tolerance, peak collision detection strictness). To see the parameter options as well as the defaults, use **FERMO's** help function ```main.py --help```

