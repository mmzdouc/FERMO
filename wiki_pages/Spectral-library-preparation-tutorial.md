### Overview

Annotation of molecular features is an essential part in LC-MS/MS data processing. FERMO offers different ways to annotate molecular features. This article is about **Modified Cosine Score** based **spectral library matching** using the package [**matchms**](https://github.com/matchms/matchms). The settings used for spectral library matching are explained in detail on the page [Processing](https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page) in this Wiki.

**Spectral library matching** is intended for search against a targeted, user-provided in-house library. We remind users that FERMO's default annotation algorithm [**MS2Query**](https://github.com/iomega/ms2query) searches against a large generalized library of hundreds of thousands of spectra taken from the GNPS annotated spectra library. We encourage users to provide targeted libraries which are as large as necessary, but as small as possible.


### Spectral library preparation

FERMO accepts a user-provided library in the .mgf-format. Further formats may be added in future releases.

A minimum spectral library entry must:
    - Start with `BEGIN IONS`
    - Have a `PEPMASS` entry denoting the precursor ion *m/z* which must not be 0.0 or 1.0
    - Have fragment - intensity paris
    - End with `END IONS`

#### Example spectral library entry

```
BEGIN IONS
PEPMASS=1649.45
CHARGE=1
MSLEVEL=2
IONMODE=Positive
NAME=Example
SCANS=1
172.073334	80.0
190.080322	201.0
271.136536	73.0
287.135376	325.0
305.145782	284.0
333.128418	64.0
335.041229	73.0
340.161713	218.0
356.154663	101.0
358.177368	58.0
360.074463	66.0
END IONS
```
