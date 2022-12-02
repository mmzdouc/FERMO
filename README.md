# FERMO Dashboard

**FERMO** is a dashboard app for the processing and visualization of liquid chromatography - (tandem) mass spectrometry (LC-MS/MS) data, and its pairing to quantitative biological data and other metadata. In particular, **FERMO** is aimed toward the prioritization of compounds and/or samples for consecutive investigation, based on comprehensible criteria like chemical novelty and diversity. Developed with natural products research in mind, **FERMO** can be also used in different areas of the life sciences, such as metabolomics or environmental sciences, to investigate metabolites, drugs, pollutants, or agrochemicals.

A key component of **FERMO** is the dashboard interface, aimed towards visualization and data integration. Users can provide group metadata to organize their samples, to get insight about sample- or group-specific compounds, or to annotate control/blank-associated features. Users can also provide quantitative biological data about their samples, such as from biological activity screening, to identify compounds associated to quantitative biological data. **FERMO** calculates scores on the putative chemical novelty and diversity of compounds, which can be used for prioritization of compounds based on  reproducible and comprehensible criteria.

More information on the software can be found in the publication **Zdouc et al, FERMO: a dashboard for streamlined rationalized prioritization of metabolite features from mass spectrometry data** (TBA).

## License

FERMO is licensed under the [MIT License](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for details.

## Getting Started

### Prerequisites

While FERMO is a browser-based application, it runs fully locally, with no data shared across the internet. No registration is required. To run FERMO, simply clone this repository or download the zipped folder, which can be found here (TBA). Installation instructions and a quickstart tutorial can be found below. A more thorough guide and references to specific functions of FERMO can be found in the [FERMO Wiki](https://github.com/mmzdouc/FERMO/wiki/).

FERMO requires following files for analysis:

- a peaktable in the MZmine 3 'quant_full.csv' format (tested with MZmine versions 3.0.0 to 3.2.8)
- the accompanying MZmine 3 .mgf-file, automatically created during peaktable generation. 
- (optional) a .csv file containing metadata information.
- (optional) a .csv file containing quantitative biological data information.
- (optional) a spectral library in the .mgf format.

Example files can be found in the `example_data` folder in this repository, which can be used for a test-run of the software.

Instructions for the generation of the files, as well as the required format, can be found in the [user guides on input data formats](https://github.com/mmzdouc/FERMO/wiki/Input-data-formats) in the FERMO Wiki.


### Installation

#### WINDOWS:

1. Download the FERMO zipped package to an easily accessible location to which you have write access, such as the Downloads folder or the Desktop. Unpack the package. This can be done using (free) software such as 7-Zip (https://www.7-zip.org/). Alternatively, you can also clone this repository.

2. Download and install the latest Miniconda3 version from the [Conda website](https://docs.conda.io/en/latest/miniconda.html), following the instructions of the install program. Accept the default settings and the license conditions. Alternatively, Anaconda can also be used, but its installation requires substantially more disk space. More details on the installation procedure can be found in [this Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html).

3. Once Miniconda3 (or Anaconda) is installed, there are two options to run FERMO. The easiest option is by double-clicking the startup batch script `FERMO_START_WINDOWS.bat`, which can be found in the FERMO directory. This script will start FERMO, install all dependencies, and open a browser window where FERMO can be used (refresh after a few seconds if there is nothing to see). However, the script will only work if Miniconda3 (or Anaconda) was installed with default parameters (the startup script will check for a Conda installation in `C:\Users\your_username\miniconda3\` (or `C:\Users\your_username\anaconda3\`). 

4. If the script does not start correctly, it might be because Miniconda3/Anaconda3 were installed on another drive than `C:`. In this case, FERMO has to be started manually as indicated in step **5**. Users may also edit the `FERMO_START_WINDOWS.bat` file and adapt the path variables to their system setup (`MINICONDAPATH` and `MINIENVPATH` for Miniconda3 or `ANACONDAPATH` and `ANAENVPATH` for Anaconda3).

5. **Manual install and start of FERMO**: From the Windows start menu, open the **Anaconda Prompt**. A command line interface will appear, in which the following steps are performed.

6. In the command line interface, navigate to the previously downloaded and unpacked FERMO directory, using the `cd` command (i.e. "change directory").  To show the contents of the current directory, the `dir` command can be used. This has to be done every time FERMO is started.

7. Once in the FERMO directory, create a Conda virtual environment by entering the command `conda create --name FERMO python=3.8`. This has to be done only the first time you run FERMO.

8. Activate the newly created virtual environment by entering the command `conda activate FERMO`. The prefix of the command prompt should switch to `(FERMO)`, to indicate the change in environment. This has to be done every time FERMO is started.

9. Install the packages required by FERMO in the newly created virtual environment by entering the command `pip install numpy pandas matchms pyteomics plotly dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.4.3" dash[diskcache]`. This has to be done only the first time you run FERMO.

10. To start FERMO, enter the command `python app.py` and enter the local IP address `127.0.0.1:8050` in any browser window. The dashboard should appear after a couple of seconds. If not, simply reload the browser window. Example data for testing can be found in the folder `example_data`. 

11. After use, do not forget to close the command line window in which FERMO runs, or terminate execution of the program by hitting ctrl+c.


#### macOS:


1. Download the FERMO zipped package to an easily accessible location to which you have write access, such as the Downloads folder or the Desktop. Unpack the package. This can be done using (free) software such as 7-Zip (https://www.7-zip.org/). Alternatively, you can also clone this repository.

2. Download and install the latest Miniconda3 version from the [Conda website](https://docs.conda.io/en/latest/miniconda.html). Install Miniconda3 by opening a terminal window, navigating to the Miniconda3 binary, and executing the command `bash Miniconda3-latest-MacOSX-x86_64.sh`. Accept the default settings and the license conditions. Alternatively, Anaconda can also be used, but its installation requires substantially more disk space. More details on the installation procedure can be found in [this Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html).

3. Once Miniconda3 is installed, close and re-open the terminal window to make changes take effect. Now, your terminal prompt should have the prefix `(base)`.

4. In the terminal window, navigate to the previously downloaded and unpacked FERMO directory, using the `cd` ("change directory") command. To show the contents of the current directory, the `ls` command can be used. This has to be done every time FERMO is started.

5. Once in the FERMO directory, create a Conda virtual environment by entering the command `conda create --name FERMO python=3.8`. This has to be done only the first time you run FERMO.

6. Activate the newly created virtual environment by entering the command `conda activate FERMO`. The prefix of the command prompt should switch to `(FERMO)`, to indicate the change in environment .This has to be done whenever FERMO is started.

7. Install the packages required by FERMO in the newly created virtual environment by entering the command `pip install numpy pandas matchms pyteomics plotly dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.4.3" "dash[diskcache]"`. This has to be done only at the first start of FERMO.

8. To start FERMO, enter the command `python app.py` and enter the local IP address `127.0.0.1:8050` in any browser window. The dashboard should appear after a couple of seconds. If not, simply reload the browser window. Example data for testing can be found in the folder `example_data`. 

9. After use, do not forget to close the command line window in which FERMO runs, or terminate execution of the program by hitting ctrl+c.

For Apple Mac laptops with the new M1 chip, the error `zsh: illegal hardware instruction ...` has been observed. If such an error occurs, the following commands can help to fix the problem:
```
$_ pip install virtualenv
$_ virtualenv ENV
$_ source ENV/bin/activate
$_ wget "https://github.com/tensorflow/tensorflow/archive/refs/tags/v2.4.1.zip"
$_ unzip v2.4.1.zip
$_ mv v2.4.1 tensorflow_v2.4.1.whl
$_ pip install ./tensorflow_v2.4.1.whl
```
Afterwards, repeat the command in point 7.


#### (Ubuntu) Linux

1. Download the FERMO zipped package to an easily accessible location to which you have write access, such as the Downloads folder or the Desktop. Unpack the package. Alternatively, you can also clone this repository.

2. Download and install the latest Miniconda3 version from the [Conda website](https://docs.conda.io/en/latest/miniconda.html). Install Miniconda3 by opening a terminal window, navigating to the Miniconda3 binary, and executing the command `bash Miniconda3-latest-Linux-x86_64.sh`. Accept the default settings and the license conditions. Alternatively, Anaconda can also be used, but its installation requires substantially more disk space. More details on the installation procedure can be found in [this Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html).

3. Once Miniconda3 is installed, there are two options to run FERMO. The easiest option is by double-clicking the startup script `FERMO_START_LINUX.sh`, which can be found in the FERMO directory. This script will start FERMO, create a conda environment, activate it, install the all dependencies, and open a browser window where FERMO can be used (refresh after a few seconds if there is nothing to see). However, on some Linux distributions, shell-scripts cannot be opened in the file explorer for security reasons. In this case, open a new terminal window, and execute the commands `chmod +x ./FERMO_START_LINUX.sh` and `./FERMO_START_LINUX.sh`. If that does not work, FERMO can also be started manually, as indicated below:

4. **Manual install and start of FERMO:** Open a new terminal window, navigate to the previously downloaded and unpacked FERMO directory, using the `cd` ("change directory") command. To show the contents of the current directory, the `ls` command can be used. This has to be done whenever FERMO is started.

5. Once in the FERMO directory, create a Conda virtual environment by entering the command `conda create --name FERMO python=3.8`. This has to be done only at the first start of FERMO.

6. Activate the newly created virtual environment by entering the command `conda activate FERMO`. The prefix of the command prompt should switch to `(FERMO)`, to indicate the change in environment. This has to be done whenever FERMO is started.

7. Install the packages required by FERMO in the newly created virtual environment by entering the command `pip install numpy pandas matchms pyteomics plotly dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.4.3" dash[diskcache]`. This has to be done only at the first start of FERMO.

8. To start FERMO, enter the command `python app.py` and enter the local IP address `127.0.0.1:8050` in any browser window. The dashboard should appear after a couple of seconds. If not, simply reload the browser window. Example data for testing can be found in the folder `example_data`. 

9. After use, do not forget to close the command line window in which FERMO runs, or terminate execution of the program by hitting ctrl+c.


### Quickstart Guide

#### Overview and terminology:

FERMO is designed to work with **untargeted, data-dependend acquisition (DDA) LC-MS/MS data**. FERMO works best with **high resolution data** (mass deviation 30 ppm and less). To describe data, FERMO uses the terminology commonly used in metabolomics experiments:

- **Sample**: a contiguous instrument run, containing a number of scans, that are either **MS1** (surveying) scans, or **MS2** (collision cell) scans. 
- **Molecular feature**: a LC-MS extracted ion chromatogram (EIC) peak with specific attributes like mass-to-charge-ratio *m/z*, retention time *RT*, and a tandem mass fragmentation spectrum *MS/MS*. 
- **Peak table**: a table of features detected over all samples. Identical features detected over multiple samples are collapsed to decrease redundancy. 

#### Step-by-step guide

This guide covers the essential steps to process and analyze data with FERMO. For first-time users, an example dataset is available in the folder `example_data`, which is a subset of 11 samples of the dataset [MSV000085376](https://doi.org/doi:10.25345/C5412V), described in the article [Planomonospora: A Metabolomics Perspective on an Underexplored Actinobacteria Genus](https://doi.org/10.1021/acs.jnatprod.0c00807). For more information on the input data format, see the [Input data formats overview](https://github.com/mmzdouc/FERMO/wiki/Input-data-formats) in the FERMO Wiki.

1. Start FERMO by following the instructions in the installation guide above. On the landing page, two different pages can be accessed: the **Processing mode** and the **Loading mode**, the latter allowing to load a previously saved session file. This step-by-step guide focuses on the **Processing mode**. 

3. On the **Processing mode** page, load the files by clicking on the respective buttons. The minimum requirement are a **peak table** and the corresponding **.mgf-file**. A message reports on the outcome of the data loading. Parameters can be adjusted as required, and information about them is found in the tooltips next to the fields. Once the files are loaded, the calculation can be started by clicking the **'Start FERMO'** button at the bottom of the page.

4. FERMO will automatically reload and redirect to the dashboard view, once calculations are finished. Keep in mind that processing depends on the performance of the computer. 

5. The dashboard is organized into 6 fields. Starting from the top left and continuing in a clockwise fashion, there are the **overview tables (1)**, the **chromatogram view (2)**, the **molecular feature information table (3)**, the **sample overview (4)**, the **spectral similarity networking view (5)**, and the **filter and download panel (6)** 

6. To view a specific sample, click on one of the rows in the **sample table (1)**. This triggers the sample **chromatogram view (2)**, which displays the molecular features detected in the sample. Hovering over a molecular feature presents general information, and clicking triggers a update of the **molecular feature information table (3)**, the **sample overview (4)**, and the **spectral similarity networking view (5)**. 

7. In the **feature information table (3)**, all information about a molecular feature is displayed. This includes its general attributes, its calculated scores, its annotations, and its spectrum similarity network information.

8. In the **sample overview (4)**, the distribution of the molecular feature across samples is displayed, which can be used to determine the sample most suitable for further exploration. 

9. The **spectral similarity networking view (5)** shows the relatedness of the molecular feature with other molecular features, based on similarity of their MS/MS spectra. Clicking nodes or edges triggers the **node information table** or **edge information table**, respectively, which are below the network view. 

10. In the **filter and download panel (6)**, different filters can be set that change the current selection of molecular features in the **sample chromatogram view (2)**. Further, the current session can be exported, for later loading in the FERMO loading mode. Also, peak and feature tables can be exported.   

A more thorough guide, including information on scores and data processing, can be found in the Wiki.


## For Developers

### Contributing

For details on our code of conduct, and the process for submitting pull requests to us, please read [CONTRIBUTING.md](CONTRIBUTING.md).

### Versioning

We use [Semantic Versioning](http://semver.org/) for versioning.

## Authors

- **Mitja M. Zdouc** - *Lead developer* -
- **Hannah E. Augustijn** - *Design* -

See also the list of [contributors](https://github.com/mmzdouc/FERMO/contributors) who participated in this project.

## Acknowledgments (in alphabetical order)

- Justin J. J. van der Hooft - *project supervision*
- Lina M. Bayona Maldonado - *beta testing*
- Marnix H. Medema - *project supervision*
- Marianna Iorio - *beta testing*
- Matteo Simone - *beta testing*
- Niek de Jonge - *code review*
- Soliman Khatib - *beta testing*
- Sonia Maffioli - *beta testing*
- Sylvia Soldatou - *beta testing*

