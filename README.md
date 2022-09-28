## Installation
This installation tutorial will focus on the installation via the zipped package. Please follow the instructions written for your respective operating system.

### WINDOWS:

1. Download the FERMO zipped package to an easily accessible location, such as the Downloads folder or the Desktop. Unpack the package. This can be done using free software such as 7-Zip (https://www.7-zip.org/).

2. Download and install the latest Miniconda3 version from the Conda website (https://docs.conda.io/en/latest/miniconda.html), following the instructions of the install program. Accept the default settings and the license conditions. For more details on the installation procedure, see (https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)

3. Once Miniconda3 is installed, there are two options to run FERMO. The easiest option is by double-clicking the startup batch script `FERMO_START_WINDOWS.bat`, which can be found in the FERMO directory. This script will start FERMO and open a browser window where FERMO can be used (refresh after a few seconds if there is nothing to see). However, the script will only work if Miniconda3 was installed with default parameters, meaning that it lives in `C:\Users\your_username\miniconda3\`. If this does not apply (e.g. because Anaconda is installed, or because there are multiple drives) FERMO must be started via command line as described below. This also applies if the startup script does not work for some reason.

4. Manual start of FERMO: From the Windows start menu, open the Anaconda Prompt. A command line interface will appear, in which the steps following below are performed.

5. In the command line interface, navigate to the previously downloaded and unpacked FERMO directory, using the `cd` command. This command stands for "change directory".  To show the contents of the current directory, the `dir` command can be used.

6. Once in the FERMO directory, create a Conda virtual environment by entering the command `conda create --name FERMO_v_0.5 python=3.8`. This has to be done only at the first start of FERMO.

7. Activate the newly created virtual environment by entering the command `conda activate FERMO_v_0.5`. The prefix of the command prompt should switch to `(FERMO_v_0.5)`, to indicate the change in environment. This has to be done whenever FERMO is started.

8. Install the packages required by FERMO in the newly created virtual environment by entering the command `pip install numpy pandas matchms pyteomics plotly argparse dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.3.3" dash[diskcache] dash[celery]`. This has to be done only at the first start of FERMO.

9. To start FERMO, enter the command `python app.py` and enter the local IP address `127.0.0.1:8050` in any browser window. The dashboard should appear after a couple of seconds. If not, simply reload the browser window. Example data for testing can be found in the folder `example_data`. 

10. After use, do not forget to close the command line window in which FERMO runs, or terminate execution of the program by hitting ctrl+c.


### macOS:


1. Download the FERMO zipped package to an easily accessible location, such as the Downloads folder or the Desktop. Unpack the package. This can be done using free software such as 7-Zip (https://www.7-zip.org/).

2. Download and install the latest Miniconda version from the Conda website (https://docs.conda.io/en/latest/miniconda.html). Install Miniconda by opening a terminal window, navigating to the Miniconda binary, and executing the command `bash Miniconda3-latest-MacOSX-x86_64.sh`. Accept the default settings and the license conditions. For more details on the installation procedure, see https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html.

3. Once Miniconda is installed, close and re-open the terminal window to make changes take effect. Now, your terminal prompt should have the prefix `(base)`.

4. In the terminal window, navigate to the previously downloaded and unpacked FERMO directory, using the `cd` ("change directory") command. To show the contents of the current directory, the `ls` command can be used.

5. Once in the FERMO directory, create a Conda virtual environment by entering the command `conda create --name FERMO_v_0.5 python=3.8`. This has to be done only at the first start of FERMO.

6. Activate the newly created virtual environment by entering the command `conda activate FERMO_v_0.5`. The prefix of the command prompt should switch to `(FERMO_v_0.5)`, to indicate the change in environment .This has to be done whenever FERMO is started.

7. Install the packages required by FERMO in the newly created virtual environment by entering the command `pip install numpy pandas matchms pyteomics plotly argparse dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.3.3" dash[diskcache] dash[celery]`. This has to be done only at the first start of FERMO.

9. To start FERMO, enter the command `python app.py` and enter the local IP address `127.0.0.1:8050` in any browser window. The dashboard should appear after a couple of seconds. If not, simply reload the browser window. Example data for testing can be found in the folder `example_data`. 

10. After use, do not forget to close the command line window in which FERMO runs, or terminate execution of the program by hitting ctrl+c.

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
Afterwards, repeat the command in point 8.









### (Ubuntu) Linux

1. Download the FERMO zipped package to an easily accessible location, such as the Downloads folder or the Desktop. Unpack the package.

2. Download and install the latest Miniconda version from the Conda website (https://docs.conda.io/en/latest/miniconda.html). Install Miniconda by opening a terminal window, navigating to the Miniconda binary, and executing the command `bash Miniconda3-latest-Linux-x86_64.sh`. Accept the default settings and the license conditions. For more details on the installation procedure, see https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html.

3. Once Miniconda is installed, there are two options to run FERMO. The easiest option is by double-clicking the startup script `FERMO_START_LINUX.sh`, which can be found in the FERMO directory. This script will start FERMO and open a browser window where FERMO can be used (refresh after a few seconds if there is nothing to see). However, on some Linux distributions, shell-scripts cannot be opened via the file explorer. In this case, open a new terminal window, and execute the commands `chmod +x ./FERMO_START_LINUX.sh` and `./FERMO_START_LINUX.sh`. If that does not work, FERMO can also be started manually, as indicated below:

4. Open a new terminal window, navigate to the previously downloaded and unpacked FERMO directory, using the `cd` ("change directory") command. To show the contents of the current directory, the `ls` command can be used.

5. Once in the FERMO directory, create a Conda virtual environment by entering the command `conda create --name FERMO_v_0.5 python=3.8`. This has to be done only at the first start of FERMO.

6. Activate the newly created virtual environment by entering the command `conda activate FERMO_v_0.5`. The prefix of the command prompt should switch to `(FERMO_v_0.5)`, to indicate the change in environment. This has to be done whenever FERMO is started.

7. Install the packages required by FERMO in the newly created virtual environment by entering the command `pip install numpy pandas matchms pyteomics plotly argparse dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.3.3" dash[diskcache] dash[celery]`. This has to be done only at the first start of FERMO.

8. To start FERMO, enter the command `python app.py` and enter the local IP address `127.0.0.1:8050` in any browser window. The dashboard should appear after a couple of seconds. If not, simply reload the browser window. Example data for testing can be found in the folder `example_data`. 

9. After use, do not forget to close the command line window in which FERMO runs, or terminate execution of the program by hitting ctrl+c.
