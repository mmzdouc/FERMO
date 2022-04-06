# FERMO: Formulation of mEtrics from Reproducible Metabolomics Objects

## Overview

Attention: **FERMO**  is currently in early development and many of the modules are not finished yet.

**FERMO** is an open-source pipeline for the processing and visualization of mass-spectrometry data. **FERMO** wraps tools for parameter finding, peak picking, annotation, and allows to score samples for complexity, diversity, and novelty. The samples with the highest chemical diversity and novelty, but lowest complexity in terms of peak overlap, are highlighted. **FERMO** can also integrate various bioactivity data into its metrics, which can be explored by an interactive web interface. Aimed to guarantee reproducibility by design, **FERMO** allows to quickly prioritize interesting samples and peaks for targeted isolation and characterization. 

The goal of the project is to provide a user-friendly, modular, and easily extendable pipeline that allows users to quickly process their samples and visualize them, without having to learn to use each of the tools separately or invest extensive amounts of time into parameter optimization. 


## License
MIT License


## Documentation for users

**FERMO**  is currently in early development and many of the modules are not finished yet. At the moment, it can only be run from command line and has no graphical user iterface. 

**FERMO**  accepts a MzMine3 formatted peaktable and the corresponding .mgf-file

### Running FERMO

Prerequesites:
- Python 3.9
- MzMine3-style peaktable

Running FERMO from command line:

```
$_ python main.py mzmine3style_peaktable.csv mzmine3style_peaktable.mgf
```
