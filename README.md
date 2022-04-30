### FERMO: Formulation of mEtrics from Reproducible Metabolomics Objects

## Overview

###Attention: **FERMO** is currently in early development and many of the modules are not finished yet.

This is the Github repository for **FERMO**, an open-source pipeline for the processing and visualization of mass-spectrometry data. **FERMO** wraps tools for parameter finding, peak picking, annotation, and allows to score samples for complexity, diversity, and novelty. The samples with the highest chemical diversity and novelty, but lowest convolutendess in terms of peak overlap, are highlighted. **FERMO** can also integrate bioactivity data into its metrics. In the future, an interctive web interface will allow to explore results. Aimed to guarantee reproducibility by design, **FERMO** allows to quickly prioritize interesting samples and peaks for targeted isolation and characterization. 

The goal of the project is to provide a user-friendly, modular, and easily extendable pipeline that allows users to quickly process their samples and visualize them, without having to learn to use each of the tools separately or invest extensive amounts of time into parameter optimization. 

For information on how to install and run **FERMO**, check this tutorial. Please, take into account that this tool has been currently only tested on Ubuntu.

## License
MIT License

## Documentation for users

**FERMO**  is currently in early development and many of the modules are not finished yet. At the moment, it can only be run from command line.

### Installation

First, clone the **FERMO** Github repository:

#+BEGIN_EXAMPLE
~$ git clone https://github.com/mmzdouc/FERMO.git
#+END_EXAMPLE

**FERMO** has a number of dependencies, which need to be installed first.
It is recommended to use a Python package manager, such as conda.

#+BEGIN_EXAMPLE
# Create conda environment
~$ conda env create FERMO
~$ conda activate FERMO
# Install dependecies
~$ conda install numpy pandas matchms pyteomics
#+END_EXAMPLE


### Overview and example run
The typical workflow for FERMO consists of following steps:
1) Process LCMS/MS data with MzMine 3 and export the peaktable in *ALL/FULL* format using the *GNPS - Feature Based Molecular Networking* function. 
2) (Optional) Prepare a metadata file (indicating which samples are proper samples and which are blanks) and/or a bioactivity file (indicating active/inactive samples)
3) Run **FERMO's** ```main.py``` function as indicated below

#+BEGIN_EXAMPLE
# Run FERMO with exmple data:
~$ python 3.10 ./main.py -p example_data/peaktable_full.csv -m example_data/msms.mgf -b example_data/bioactivity.csv -M example_data/metadata.csv
#+END_EXAMPLE

### Comments:
- Currently, **FERMO**  accepts a MzMine3 formatted peaktable. In future updates, other peakpicking program output formats will be included as well.
- **FERMO** accepts additional parameter that influence its behaviour (e.g. precursor m/z tolerance, peak collision detection strictness). To see the parameter options as well as the defaults, use **FERMO's** help function ```main.py --help```

