### Overview

FERMO provides annotation of molecular features by using the tool [**MS2Query**](https://github.com/iomega/ms2query), which matches against a large library of public mass spectrometry data. However, users may desire to search against their in-house libraries, which are often more targeted and better suited for the research question in mind. Data is matched against the spectral library using the **'modified cosine'** algorithm implemented in the Python package [**MatchMS**](https://github.com/matchms/matchms). The settings used for spectral library matching are explained in detail on the page [Processing](https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page) in this Wiki.

### Spectral library preparation

FERMO accepts a user-provided library in the .mgf-format. For a minimal example, see below. 

Keep in mind that library matching (based on modified cosine similarity) is computationally expensive, and might significantly increase computation time if a very large spectral library is used. We encourage users to provide targeted libraries which are as large as necessary, but as small as possible. For example, a targeted library with up to a few hundred entries is tolerable, while a generalized library with (tens of) thousands of entries can add take a very long time to tun. 

We remind users that FERMO's default annotation algorithm [**MS2Query**](https://github.com/iomega/ms2query) searches against a large generalized library of hundreds of thousands of spectra in a computationally much more efficient way. It is also possible to provide **MS2Query**-compatible libraries, which can be used in place of the standard libraries. However, this exceeds the scope of this tutorial.

#### Example file

```
BEGIN IONS
PEPMASS=1649.45
CHARGE=1
MSLEVEL=2
IONMODE=Positive
NAME=Siomycin_A/Sporangiomycin M+H
SCANS=1
172.073334	80.0
190.080322	201.0
... 
END IONS
```
Note: The `...` indicate further lines of fragment-intensity pairs and are not to be taken literally. 


Furthermore, following conditions that have to be met:
- Providing less than the minimally required data may lead to errors and failure of the library search.
- If the field `PEPMASS` is set to `0.0` or `1.0`, the search may fail (the case for some entries in the GNPS library).


