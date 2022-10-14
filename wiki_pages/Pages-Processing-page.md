### Overview

This Wiki article describes the **'Processing page'** of LC-MS/MS data processing dashboard FERMO. 

### Processing page (processing mode)

On the **Peaktable processing page**, data can be loaded into the app, and processing parameters can be set. Load the files by clicking on the respective buttons. 

The minimum requirement to run the Peaktable processing mode are:
- a [**peaktable**](https://github.com/mmzdouc/FERMO/wiki/Peaktable-generation-tutorial) 
- its accompanying **.mgf-file**. 

Optionally, users can provide:
- a table containing [**metadata**](https://github.com/mmzdouc/FERMO/wiki/Metadata-file-preparation-tutorial)
- a table containing [**bioactivity data**](https://github.com/mmzdouc/FERMO/wiki/Bioactivity-data-file-preparation-tutorial)
- a targeted [**spectral library**](https://github.com/mmzdouc/FERMO/wiki/Spectral-library-preparation-tutorial)

The file formats of the input files are described in their respective Wiki pages (see the hyperlinks above). Input files are tested for correct formatting, and a message indicates pass or fail of the assessment.

With respect to parameter settings, the default settings should match most data types but can be adjusted as needed:

#### Parameter settings

- **MS2Query**:
Allows to switch the annotation by [**MS2Query**](https://github.com/iomega/ms2query) **ON** or **OFF**. Annotation by **MS2Query** is highly efficient and also allows to search for analogues of known compounds. However, it is computationally expensive and should be ideally only run after parameter finding. 

- **Mass deviation** - *"Select the estimated mass deviation of your data (in ppm)"*:
States the expected mass deviation of the data. Used as precision threshold during different calculation steps, such as ion adduct calculation. This parameter should be set respective to the input data. As a rule of thumb, using the same mass deviation that was used for the peaktable generation is suggested.

- **Min MS2 frags** - *"Minimal required number of fragments per MS² spectrum"*:
Quality control parameter. Sets the minimal number of fragments that have to be detected in a MS² spectrum. If a MS² spectrum has fragments and does not meet the requirement, it is dropped, and the associated feature is considered MS1 only. This is done because MS² spectra with a low number of peaks have (i) low information content and (ii) may lead to false matches in (modified) cosine-based similarity searches, since their low number of fragments automatically lead to a high 'coverage' of the spectrum. In case this filter is not desired, it can be effectively switched off by setting the value to 0. 

- **Intensity cutoff** - *'Enter the feature relative intensity filter'*:
Value used to filter out low-intensity features ('cut the grass'). Indicates the minimal relative intensity (relative to the feature with the highest intensity in the sample) a feature must have to be considered for further analysis. A value of 0.05 would exclude all features with a relative intensity below 0.05, i.e. the bottom 5% of features; a value of 0 would include all features, and a value of 0.99 would exclude all features except for the most intense peak. By default, this value is 0, and should be chosen with respect to the underlying data. This parameter can be also used to reduce the number of low-intensity features in case of very large peaktables.

- **Bioactivity factor** - *'Enter the bioactivity factor'*:
Factor used in the identification of bioactivity-associated features (if bioactivity data was provided). If a feature was only detected in bioactive samples, it is possible that it is associated to bioactivity. If a feature is detected only in inactive samples, it is very unlikely that it is associated to bioactivity. However, if a feature was detected in both bioactive and inactive samples, it is more complicated, since a compound could be present in sub-inhibitory concentration and therefore lead to a missing bioactivity signal, but it could be still detected by the instrument. A pragmatic solution is to use a fold-difference between active and inactive samples: The intensity of the feature in the sample with the lowest bioactivity must be n times higher than the highest feature intensity across all inactive samples, while n is the user-specifiable Bioactivity factor. For example, a value of 10 would mean that the intensity of a feature must be 10 times higher in a bioactive sample than across the inactive samples to be still considered bioactivity-associated. 

- **Blank factor** - *'Enter the blank factor'*:
Factor used in the identification of medium-blank/sample-blank associated features (if metadata  on blank samples was provided). If a feature was only detected in blank samples, it is clearly blank-associated. If a feature is detected only in normal samples, it is unlikely to be blank-associated. However, if a feature was detected in both blank and normal samples, it is more complicated, since a high-concentration compound could be retained by the column and bleed into the blank, where it is detected by the instrument. Therefore, a simple blank subtraction is not ideal. Instead, we compare the average intensity of the feature across blanks with the average intensity across samples. Blank-associated features should be present in similar intensities across blanks and samples, while cross-contaminated features should be much lower in the blank than in the samples. Therefore, if the average intensity in samples is n times higher than the average intensity across blanks, the feature is not considered blank-associated, while n is the Blank factor. For example, a Blank factor of 10 would mean that the average intensity of the features across samples must be 10 times higher than the average intensity across blanks.


- **Spectrum similarity tolerance** - *'Enter the spectrum similarity tolerance'*:
Tolerance in m/z used in the calculation of modified cosine-based spectra similarity scores between MS² spectra. Two peaks will be considered a match if their difference is less then or equal to the m/z tolerance. Dependent on the precision and mass deviation of the instrument.

- **Spectrum similarity score cutoff** - *'Enter the spectrum similarity score cutoff'*:
Score cutoff used in the evaluation of modified cosine scores between MS2 spectra. Two spectra will be considered related only if their score exceeds the cutoff threshold. Therefore, this parameter controls how strict the similarity between two spectra must be. Keep in mind that the Diversity and Specificity scores are built upon spectral similarity, and a low score might lead to the clustering of hardly related spectra.

- **Max spectral links** - *'Enter the maximal number of spectrum similarity links'*:
Maximal number of links to other nodes, per node. Makes spectral similarity network less convoluted since it restricts the number of links between nodes to the highest n ones. 

- **Min matched peaks** - *'Enter the minimum number of matched peaks used in spectrum similarity calculation'*:
In spectrum similarity matching, the minimum number of peaks that have to be matched between two spectra to be considered a match.

### Start FERMO

Once the minimal required files are loaded into FERMO, the button **Start FERMO** can be clicked, which will start the analysis. 
Dependent on the size of the input files, the set parameters, and the computational power of the computer, the analysis can take anywhere between a few seconds and a few minutes. If in doubt, the terminal window can be checked for hints on progress.
