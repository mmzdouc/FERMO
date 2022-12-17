## Overview

This Wiki article describes the **Loading mode** of LC-MS/MS data processing dashboard FERMO.

## Loading mode

The **Loading mode** allows to load a previously generated **FERMO session file**.
**FERMO session files** can be created after data processing in the FERMO dashboard. Loading a session file is much faster and than re-calculating the whole analysis, since no additional processing has to be performed. Furthermore, it allows to share saved FERMO session files with collaborators, or load session files created by collaborators. 

The **Loading mode** page is separated in two parts: on the left-hand side, the session file can be loaded. This will trigger the table on the right-hand side of the page, which shows information on which files were used in the preceding analysis, which parameters were set, and data on when and with which FERMO version the session file was created. 

The minimum requirement to run the **Loading mode** is:
- a FERMO session file in the `.json` format

When a session file is loaded, FERMO checks for the version that was used to create the session file. FERMO employs semantic versioning, which designates versions in a Major-Minor-Patch pattern (i.e. x.y.z). Due to the dynamic development situation, Major and Minor versions are currently not backward compatible, which will be indicated by an error message. Patch versions are backward compatible inside the Minor version. In other words, a session file created by version 0.6.0 is not compatible with FERMO 0.7.0, but a session file created by version 0.7.1 is compatible with FERMO 0.7.4.

Once the session file is loaded, processing can be started by pressing the button **'Start FERMO Dashboard'**. This will reload the file and redirect to the Dashboard. 
