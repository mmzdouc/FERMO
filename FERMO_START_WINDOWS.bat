@ECHO OFF
SET FERMO_VER=FERMO_v_0.5
SET CONDAPATH=C:\Users\%USERNAME%\miniconda3\condabin\activate.bat
SET ENVPATH=C:\Users\%USERNAME%\miniconda3\envs\%FERMO_VER%\

rem Tests if mniconda was installed by testing if file activate.bat exists
IF NOT EXIST %CONDAPATH% ECHO WARNING: Looking for miniconda3 in C:\Users\%USERNAME%\ failed. Do you have miniconda installed? & PAUSE & GOTO :exit 

rem found miniconda 
ECHO Looking for miniconda3 in C:\Users\%USERNAME%\ was successful. Proceeding ...

rem activate 

rem If env fermo_ver does not exist, create new environment, activate it, install packages using pip and run the python script
IF NOT EXIST %ENVPATH% ECHO WARNING: Did not find conda environment %FERMO_VER% in %ENVPATH%. Attempting to create environment. & CALL %CONDAPATH% & conda create --name %FERMO_VER% python=3.8 -y & ECHO %FERMO_VER% successfully created. Attempting to activate conda environment & conda activate %FERMO_VER% & ECHO %FERMO_VER% successfully activated. Attempting to install modules & pip install numpy pandas matchms pyteomics plotly argparse dash dash-cytoscape dash_bootstrap_components networkx "ms2query==0.3.3" dash[diskcache] dash[celery] & ECHO Packages successfully installed & python -c "import webbrowser;webbrowser.open('http://127.0.0.1:8050/')" & python app.py & PAUSE & GOTO :exit

rem If env exists, activate environment, and run the script
IF EXIST %ENVPATH% ECHO Attempting to activate conda environment %FERMO_VER% & CALL %CONDAPATH% & conda activate %FERMO_VER% & ECHO %FERMO_VER% successfully activated. & python -c "import webbrowser;webbrowser.open('http://127.0.0.1:8050/')" & python app.py & PAUSE & GOTO :exit

