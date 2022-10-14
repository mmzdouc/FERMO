## Overview

This Wiki article describes the 'Loading page' of LC-MS/MS data processing dashboard FERMO.

## Loading page (loading mode)

The loading page allows to load a previously generated FERMO session file. Such a file can be created during an analysis in the FERMO dashboard analysis. Loading a session file is much faster and than re-calculating the whole analysis, since no additional processing has to be performed. Furthermore, it allows to share saved FERMO session files with collaborators, or load session files created by collaborators. 

The Loading page is separated in two parts: on the left-hand side, the session file can be loaded. This will trigger the table on the right-hand side of the page, which shows information on which files were used in the preceding analysis, which parameters were set, and data on when and with which FERMO version the session file was created. 

The minimum requirement to run the Loading mode is:
- a FERMO session file in the `.json` format

When a session file is loaded, FERMO checks for the version that was used to create the session file. If the versions of the session file and the current FERMO version differ, a warning will pop up, alterting the user that different versions were detected, and that there might be problems in loading. Generally it is safe to try loading nonetheless, but there might be inconsistencies resulting from different versions. Therefore, it is recommended to work with session files that result from the same FERMO version. 

Once the session file is loaded, processing can be started by pressing the button **'Start FERMO Dashboard'**. This will reload the file and redirect to the Dashboard. 