#!/bin/bash

eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"

FERMO_VER="FERMO_v_0.5"

if ! command -v conda >/dev/null 2>&1
then
    echo "conda could not be found. Have you installed miniconda?"
    exit
else
    echo "conda installation was found - continue"
fi


if ! conda env list | grep $FERMO_VER >/dev/null 2>&1
then 
    echo "conda environment $FERMO_VER was not found and will be created"
    conda create --name $FERMO_VER python=3.8 -y >/dev/null 2>&1
    echo "conda environment $FERMO_VER was successfully created"
    conda activate $FERMO_VER
    echo "conda environment $FERMO_VER was successfully activated"
    echo "Starting with package installation - this might take some time"
    pip install numpy pandas matchms pyteomics plotly argparse dash \
        dash-cytoscape dash_bootstrap_components networkx \
        'ms2query==0.3.3' dash[diskcache] dash[celery] --quiet
    echo "Packages were successfully installed in conda environment $FERMO_VER"
    python ./app.py
else 
    echo "conda environment $FERMO_VER was found and will be activated"
    conda activate $FERMO_VER
    echo "conda environment $FERMO_VER was successfully activated"
    python ./app.py
fi
