#!/bin/bash

eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"

FERMO_VER="test_env_src"

if ! command -v conda >/dev/null 2>&1
then
    echo "conda could not be found. Have you installed miniconda or anaconda?"
    exit
else
    echo "conda installation was found - continue"
fi


if ! { conda info --envs | cut -d " " -f 1 | grep ^"$FERMO_VER"; } >/dev/null 2>&1;
then 
    echo "conda environment $FERMO_VER was not found and will be created"
    conda create --name $FERMO_VER python=3.8 -y >/dev/null 2>&1
    echo "conda environment $FERMO_VER was successfully created"
    conda activate $FERMO_VER
    echo "conda environment $FERMO_VER was successfully activated"
    echo "Starting with package installation - this might take some time"
    pip install . --quiet
    echo "Packages were successfully installed in conda environment $FERMO_VER"
    python -c "import webbrowser;webbrowser.open('http://127.0.0.1:8050/')"
    python ./src/fermo/app.py
else 
    echo "conda environment $FERMO_VER was found and will be activated"
    conda activate $FERMO_VER
    echo "conda environment $FERMO_VER was successfully activated"
    python -c "import webbrowser;webbrowser.open('http://127.0.0.1:8050/')"
    python ./src/fermo/app.py
fi
