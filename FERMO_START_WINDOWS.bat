@ECHO OFF
SET FERMO_VER=FERMO
SET MINICONDAPATH=C:\Users\%USERNAME%\miniconda3\condabin\activate.bat
SET MINIENVPATH=C:\Users\%USERNAME%\miniconda3\envs\%FERMO_VER%\
SET ANACONDAPATH=C:\Users\%USERNAME%\anaconda3\condabin\activate.bat
SET ANAENVPATH=C:\Users\%USERNAME%\anaconda3\envs\%FERMO_VER%\


rem Tests if miniconda or anaconda were installed by testing if file activate.bat exists
IF NOT EXIST %MINICONDAPATH% (
	IF NOT EXIST %ANACONDAPATH% (
		ECHO WARNING: Looking for miniconda3 in C:\Users\%USERNAME%\miniconda3\ and anaconda3 in C:\Users\%USERNAME%\miniconda3\ failed. Do you have miniconda or anaconda installed? & PAUSE & GOTO :exit
	)
) 

rem Found miniconda/anaconda
ECHO Looking for miniconda3 in C:\Users\%USERNAME%\ or anaconda3 in C:\Users\%USERNAME%\ was successful. Proceeding ...

rem If env fermo_ver does not exist, create new environment, activate it, install packages using pip and run the python script
IF EXIST %MINICONDAPATH% (
	IF NOT EXIST %MINIENVPATH% (
		 ECHO WARNING: Did not find conda environment %FERMO_VER% in %MINIENVPATH%. Attempting to create environment. & CALL %MINICONDAPATH% & conda create --name %FERMO_VER% python=3.8 -y & ECHO %FERMO_VER% successfully created. Attempting to activate conda environment & conda activate %FERMO_VER% & ECHO %FERMO_VER% successfully activated. Attempting to install modules & pip install . & ECHO Packages successfully installed & python -c "import webbrowser;webbrowser.open('http://127.0.0.1:8050/')" & python src\fermo\app.py & PAUSE & GOTO :exit
	)
)

rem If env exists, activate environment, and run the script
IF EXIST %MINICONDAPATH% (
	IF EXIST %MINIENVPATH% (
		ECHO Attempting to activate conda environment %FERMO_VER% & CALL %MINICONDAPATH% & conda activate %FERMO_VER% & ECHO %FERMO_VER% successfully activated. & python -c "import webbrowser;webbrowser.open('http://127.0.0.1:8050/')" & python src\fermo\app.py & PAUSE & GOTO :exit
	)
)

rem The same as before for anaconda3
IF EXIST %ANACONDAPATH% (
	IF NOT EXIST %ANAENVPATH% (
		 ECHO WARNING: Did not find conda environment %FERMO_VER% in %ANAENVPATH%. Attempting to create environment. & CALL %ANACONDAPATH% & conda create --name %FERMO_VER% python=3.8 -y & ECHO %FERMO_VER% successfully created. Attempting to activate conda environment & conda activate %FERMO_VER% & ECHO %FERMO_VER% successfully activated. Attempting to install modules & pip install . & ECHO Packages successfully installed & python -c "import webbrowser;webbrowser.open('http://127.0.0.1:8050/')" & python src\fermo\app.py & PAUSE & GOTO :exit
	)
)

IF EXIST %ANACONDAPATH% (
	IF EXIST %ANAENVPATH% (
		ECHO Attempting to activate conda environment %FERMO_VER% & CALL %ANACONDAPATH% & conda activate %FERMO_VER% & ECHO %FERMO_VER% successfully activated. & python -c "import webbrowser;webbrowser.open('http://127.0.0.1:8050/')" & python src\fermo\app.py & PAUSE & GOTO :exit
	)
)


 

