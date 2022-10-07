# GITHUB WIKI

Hello and welcome to the FERMO Dashboard wiki pages. 
This wiki can be separated into three parts:
- User-guides
    - Peaktable generation tutorial (LINK)
    - Metadata file preparation tutorial (LINK)
    - Bioactivity data file preparation tutorial (LINK)
    - Spectral library preparation (LINK)
    - Data interpretation (LINK)
- Pages
    - Landing page (LINK)
    - Processing page (processing mode) (LINK)
    - MZmine page (raw data mode) (LINK)
    - Loading page (loading mode) (LINK)
    - Dashboard page (LINK)
- References
    - Scores (LINK)
    - Adduct detection (LINK)
    - Peak collision detection (LINK)
    - Chromatogram drawing (LINK)
    - FAQ (LINK)


## Peaktable generation tutorial

Prepare the peaktable by processing the LC-MS/MS data with MZmine3. Export the peaktable via **'Feature list methods'** → **'Export feature list'** → **'GNPS - feature based molecular networking'**. Settings can be left default except for: **'Filter rows: ALL'**, **'Feature intensity: Peak height'**, **'CSV export: ALL'**. Save the files to a folder of your choice, start FERMO as indicated in the **Installation instructions** of the README, and load the peaktable and .mgf-file in the **Peaktable processing page (standard mode)**.

![peaktable_export.png](/assets/peaktable_export.png)


If you do not know how to process your data with MZmine3, you can either use FERMO's **raw data mode** (not implemented yet); or continue reading to get instructions on how to run MZmine on your computer.

### MZmine3 step-by-step guide

**Disclaimer: described below is a 'basic' workflow for inexperienced users, and processing steps have been chosen for simplicity over performance.**

1. Download the newest version of [MZmine3](http://mzmine.github.io/) and install it on your computer. 

2. To process "raw" LC-MS/MS data with MZmine3, the data has to be in a format readable by MZmine3. Mass spectrometry instruments usually generate data in a vendor-specific binary format. Mzmine3 can read some of these formats, in particular the formats **RAW (Thermo Scientific)**, **RAW (Waters)**, **TDF** and **TSF (Bruker)**. Other vendor-specific formats have to be converted first to a text-based format, such as .mzXML or its successor, the .mzML format. This can be done using the **msConvert** program of the **ProteoWizard** suite, which can be downloaded from (the ProteoWizard website)[https://proteowizard.sourceforge.io/]. An excellent tutorial on using **ProteoWizard** and LC-MS/MS data conversion in general can be found in the [GNPS documentation](https://ccms-ucsd.github.io/GNPSDocumentation/fileconversion/). 

3. Once LC-MS/MS data is in a format readable by MZmine3, it can be imported and processed in two ways: 1) by loading an MZmine3-specific batch file, which contains instructions on the steps to perform on the raw LC-MS/MS data; or 2) by performing the steps manually in the graphical user interface. The former is intended for data for which parameters are already known, while the latter allows user to explore the data and fine-tune the parameters. A description on the steps of a 'standard' workflow can be found below.

4. Import LC-MS/MS data into MZmine3 by going to **'Raw data methods'** → **'Raw data import'** and clicking on the import button respective to the data format at hand.

5. Once imported, the masses contained in the data have to be detected. In a nutshell, a LC-MS/MS analysis run is made up by numerous consecutive scans. Each scan is like a *snapshot* of what the instrument can *see* at that particular moment. Usually, MS (MS1) survey scans are intertwined with tandem MS (MS2) fragmentation scans. MS1 and MS2 spectra need to be processed separately. For MS1, perform the following step: **'Raw data methods'** → **'Mass detection'** → **'Mass detection'**, with default settings except: **'Raw data files: All raw data files'**, **'Scans: MS level 1'**; **'Mass detector: Centroid'**; **'Noise Level: see below'**. The noise level is data-specific and the easiest way to set this parameter sensibly is to check the data in the live preview and set the value so that the instrument noise is cut off (also called "cutting the grass"). 

![mzmine3_ms1_detection.png](/assets/mzmine3_ms1_detection.png)

6. After MS1 mass detection, the MS2 spectra have to be processed too: **'Raw data methods'** → **'Mass detection'** → **'Mass detection'**, with default settings except for: **'Raw data files: All raw data files'**, **'Scans: MS level 2'**; **'Mass detector: Centroid'**; **'Noise Level: see below'**. Again, the noise level is best determined by looking at the raw data and 'cutting the grass'.

![mzmine3_ms2_detection.png](/assets/mzmine3_ms2_detection.png)

7. Once MS1 and MS2 spectra have been processed, the massed detected in the MS1 spectra are used to create time/signal intensity curves, so-called extracted ion chromatograms. For this, execute the following step: **'Feature detection'** → **'LC-MS'** → **'ADAP chromatogram builder'**, with default settings except **'Raw data files: All raw data files'**; **'Scans: MS level 1'**; **'Min group size in # of scans: see below'**; **'Group intensity threshold: see below'**; **'Min highest intensity : see below'**; **'Scan to scan accuracy: see below'**. The user-dependent parameters are intended to reduce the probability to pick up noise signals. For the parameter **'Min group size in # of scans'**, give the minimum number of consecutive scans a mass must appear in to be considered a trace, and should be reasonably high (e.g. 8). The parameter **'Group intensity threshold'** sets the minimum intensity of a signal to be considered member of a group. This parameter needs to be set by looking at any known compound in the chromatogram, and determining the minimum intensity at which the first scan related to this compound rises from the 'grass' (i.e. the noise). The parameter **'Min highest intensity'** sets the minimum intensity a mass needs to reach so that a new chromatogram is started. To determine this parameter, check which maximum intensity the instrument noise reaches, and set a value below that, taking into account a safety margin (e.g. if the instrument noise is around 1E1, you can set the parameter to 3E1). The parameter **'Scan to scan accuracy'** indicates the mass deviation that can be expected between scans. The mass deviation can be estimated by looking at consecutive scans of a known compound, and calculating the average mass deviation. 

![mzmine3_chrom_building.png](/assets/mzmine3_chrom_building.png)

8. After chromatograms have been created, individual peaks have to be resolved (split up). The easiest method is the baseline cutoff, where the baseline is increased until non-resolved peaks with local minima are split by the new baseline. Execute: **'Feature detection'** → **'chromatogram resolving'** → **'Baseline resolver'**, with default settings except **'Feature lists: all feature lists'**, **'MS/MS scan pairing: ticked'**, **'Min peak height: see below'**; **'Peak duration range: see below'**; **'Baseline level: see below'**; **'Min # of data points: see below'**. The parameter **'Min peak height'** sets the minimal height/intensity a peak must reach to be considered signal and not noise, and has to be determined by looking at the data. A pragmatic way to do this is to take the average height of a number of low-intensity peaks with nice (gaussian) peak shapes. The parameter **'Peak duration range'** depends on the LC method and the column used, and can be estimated by looking at a peak corresponding to a known compound. The parameter **'Baseline level'** is the absolute cutoff below which all data points are deleted and on which a 'new' x-axis is drawn. The **'Min # of data points'** sets the minimum number of consecutive mass signals a peak is allowed to have. This needs to be a minimum of 3 (start, maximum, stop), but should ideally be higher, and needs to be assessed by looking at the number of scans in the peak of a known compound.

![mzmine3_baseline_cutoff.png](/assets/mzmine3_baseline_cutoff.png)

9. After individual peaks have been resolved, isotopic peaks coming from the same compound need to be collapsed, to reduce data redundancy. To do so, go to **'Feature list methods'** → **'Isotopes'** → **'13C isotope filter'**, with default parameter settings except **'Feature lists: all feature lists'**, **'m/z tolerance: see below'**, **'Retention time tolerance:  see below'**. The **m/z tolerance** and the **retention time tolerance** can be set relatively strictly, since the values are coming from a single LC-MS/MS run and should be fairly uniform.

![mzmine3_13Cdeiso.png](/assets/mzmine3_13Cdeiso.png)

10. After 13C isotopic peaks have been removed, LC-MS runs/samples can be aligned and identical peaks collapsed, to reduce data redundancy. This can be done by going to **'Feature list methods'** → **'Alignment'** → **'Join aligner'**, with default parameter settings except **'m/z tolerance: see below'**; **'Weight for m/z: see below'**; **'Retention time tolerance: see below'**; **'Weight for RT: see below'**. For the parameters **'m/z tolerance'** and **'Retention time tolerance'**, the settings are dependent on how different the mass precision and the retention time variation of the individual samples are from each other. If they have been analyzed as part of the same batch, retention time drift and mass drift should be relatively similar. If samples were part of different batches, retention time drift and mass drift can lead to bigger differences, and therefore require larger tolerances. Similarly, for **'Weight for m/z'** and **'Weight for RT'** values should be adjusted dependent on aforementioned sample similarity. If no weight preference should be given, both values can be set to 50. 

![mzmine3_join_aligner.png](/assets/mzmine3_join_aligner.png)

11. After samples have been aligned and peaks collapsed, the peak list can be filtered by applying **'Feature list methods'** → **'Feature list filtering'**. The filters can be applied upon individual preferences, but we suggest to use **'Feature List Row Filter'** and set a filter on the retention time window, so that the solvent peak at the beginning of the instrument run is filtered out. Also, we suggest to remove the wash step at the end of the LC gradient. In this case, the field **'Never remove feature with MS2 scan'** must not be ticked.

12. After the optional filtering step, the peak list can be exported to be analyzed with FERMO. For this, go to **'Feature list methods'** → **'Export feature list'** → **'GNPS - feature based molecular networking'** and default settings except for **'Filter rows: ALL'**, **'Feature intensity: Peak height'**, **'CSV export: ALL'**. Save the files to a folder of your choice.

13. The peaktable export leads to three files. Only two of them are used for the further analysis: the peaktable, which is a file ending with **'_quant_full.csv'**, and the file containing the MS/MS data, ending with **'.mgf'**. The third file, which ends in '_quant.csv', only contains limited information and is not used further. If the file ending in **'_quant_full.csv'** is missing, verify if the file export in MZmine3 was performed with the setting **'CSV export: ALL'**.




## Metadata file preparation tutorial

Metadata is an essential part of LC-MS/MS data, since it provides context about the analyzed sample. FERMO accepts two kinds of metadata: bioactivity data, which is discussed in a separate article, and metadata regarding **sample grouping**. Sample grouping helps with data differentiation, to distinguish samples based on external information, and allows for rational interpretation of results. 

FERMO accepts grouping metadata (from here: metadata for short) in form of a .csv (comma-separated values)-file, which can be prepared using a spreadsheet program (e.g. Microsoft Excel, OpenOffice Calc). It requires the following format :

- A column with the title `sample_name` and the full names of the samples (including their endings)
- A column with the title `attribute`, containing the group lable the sample belongs to

```
sample_name,attribute
MEDIUM-BLANK.mzXML,BLANK
P-algeriensis-107089.mzXML,algeriensis
P-corallina-96662.mzXML,corallina
P-sphaerica-91781.mzXML,sphaerica
P-algeriensis-114239.mzXML,algeriensis
P-sphaerica-135062.mzXML,sphaerica
P-max-91428.mzXML,max
P-corallina-135044.mzXML,corallina
P-corallina-97500.mzXML,corallina
P-sphaerica-107188.mzXML,sphaerica
P-sphaerica-91431.mzXML,sphaerica
```

![metadata_table.png](/assets/metadata_table.png)


The group names can be chosen arbitrarily, with two exceptions: first, the label `BLANK` (in capital letters) must only be used to denominate sample/instrument/medium/solvent blanks, since features detected in blanks will be treated differently from other features. Second, the label `GENERAL` (in capital letters) is reserved to group samples without any grouping information, and must not be used by the user. 

Additionally, the following conditions must be met; else, there will be an error during loading, indicating the wrong formatting:

- There must be only two columns, with the titles `sample_name` and `attribute`
- Each sample must be associated to a single group

Furthermore, there are some suggestions:

-We advise the following naming convention for group names: single words made up by lowercase letters (a-z) and digits (0-9), without any whitespace, punctuation, or special characters (except for the underscore symbol '_'. Good group names would be for example `group_1`, `group_2`, or `marine`, `terrestrial`, or `treatment`, `control`. Bad group names would be for example `45%-78%`, `+#.-.`, `XxXxxXx`, or `*`.
- Group names are case-sensitive, meaning that `group1`, `Group1` and `GROUP1` would be interpreted as three different groups by the program. 
- While there is no limit on the number of different groups used, it is suggested to keep this number low, to make it easier to detect differences between groups. 
- The nesting of groups is not supported. 

Common mistakes during metadata file preparation are:

- The metadata file format was mistaken with the one used in GNPS molecular networking
- Instead of a comma `,`, some other delimiter (e.g. `tab`, `;`, `|`) was used in the .csv-file (can be checked by opening the file in a text editor (e.g. Notepad)


## Bioactivity data file preparation tutorial

FERMO accepts two kinds of metadata: group metadata, which is discussed in a separate article, and metadata regarding **biological activity**. Attributing biological activity to samples (and compounds) provides an additional data dimension for prioritization purposes and is important regarding commercialization of research.

FERMO accepts biological activity data (from here: bioactivity data for short) in form of a .csv (comma-separated values)-file, which can be prepared using a spreadsheet program (e.g. Microsoft Excel, OpenOffice Calc). It requires the following format :

- A column with the title `sample_name` and the full names of the samples (including their endings)
- A column with the title `bioactivity`, containing the measured activity of the sample (in numeric form).


```
sample_name,bioactivity
P-sphaerica-107188.mzXML,100
P-sphaerica-135062.mzXML,100
P-sphaerica-91431.mzXML,100
P-sphaerica-91781.mzXML,80
```

![bioactivity_table.png](/assets/bioactivity_table.png)



There is a large variety of bioactivity tests and accompanying data formats. However, many of them measure either a concentration (e.g. EIC, MIC, IC50), or a percentage of inhibition. Usually, for concentration, a lower value signifies higher activity, while for percentage, a higher value signifies a higher activity. In FERMO, the kind of bioactivity data (concentration or percentage) can be indicated on the processing page. Keep in mind that only samples for which bioactivity was detected should be contained in the bioactivity table. Samples with no (negative) bioactivity must be excluded, since all samples contained in the table will be considered bioactive, even if their value is 0.

Additionally, the following conditions must be met:

- There must be only two columns, with the titles `sample_name` and `bioactivity`
- Each sample must have a single measurement associated to it (no duplicate entries in column `sample_name`)
- The bioactivity values must be positive numeric values 
- Only bioactive samples must be contained in table. If a sample showed no bioactivity (negative), exclude from table. 

Common mistakes during bioactivity file preparation are:

- Instead of a comma `,`, some other delimiter (e.g. `tab`, `;`, `|`) was used in the .csv-file (can be checked by opening the file in a text editor (e.g. Notepad)

## Spectral library preparation

FERMO provides annotation of features by using the tool [MS2Query](https://github.com/iomega/ms2query), which matches against a large library of public mass spectrometry data. However, users may provide their in-house library too, which is often more targeted and better suited for the research question in mind. 

FERMO accepts a user-provided library in the .mgf-format. For a minimal working example, see below.

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

Providing less than the minimally required data may lead to errors and failure of the library search. Also, if the field `PEPMASS` is set to `0.0` or `1.0`, the search may fail (the case for some entries in the GNPS library).

Keep in mind that library matching is computationally expensive, and might add significantly to computation time. We encourage users to provide targeted libraries which are as large as necessary, but as small as possible. For example, a targeted library with up to a few hundred entries is tolerable, while a generalized library with thousands of entries can add take a very long time to tun. Keep in mind that the default search algorithm MS2Query searches against a large generalized library of hundreds of thousands of spectra in a computationally much more efficient way.

## Data interpretation

Data interpretation strongly depends on the research question in mind. For a bioactive natural product discovery research question, following analysis workflow can be imagined: 

1. Assuming bioactivity data and metadata were provided, the bioactivity filter can be used to identify features associated with biological activity. Combining with the novelty filter (set to a low setting, such as 0.2) can help to exclude features that are well annotated and therefore have a low probability of being novel.

2. After having applied the filters, the remaining features can be inspected for their likelihood to be associated to bioactivity. It is advisable to export the selected features as table, using the dedicated button, to keep track which features were already inspected. 

3. A possible way of assessing the bioactivity-likelihood is to look at the field *'Groups in molecular network'* in the element **feature information table**. If also groups contribute to the network that are not associated to bioactivity, chances are slim that the features in this network are really responsible for the bioactivity. However, if the network is specific to the bioactivity-associated group, chances are good that this group of features might be responsible for bioactivity.

4. Another clue can be taken by looking at the field *'Bioactivity per sample'* and *'Intensity per sample'* in the **feature information table**. Bioactivity and feature intensity should correlate, since a higher concentration of a compound should also lead to a higher biological activity signal. If they do not (e.g.  low intensity of a feature in a highly active sample, and high intensity of a feature in a sample with low activity), chances are slim that the feature is responsible for bioactivity. Since the same feature (belonging to the same compound) is compared across samples, the feature intensity can be taken as semiquantitative measure). 

5. By exclusion of features/networks unlikely to be associated for bioactivity, the search can be narrowed down to a couple of features, which can then be further investigated by chromatographic fractionation and re-testing. In the best case, this would decrease the number of fractions needed to analyze. 

## Landing page 

The landing page allows to select the mode in which FERMO should be run. The user can choose between three options:

- **Peaktable processing page (standard mode)** (LINK)
- **Data pre-processing page (raw data mode)** (not implemented yet) (LINK)
- **Restart session page (loading mode)** (LINK)

## Processing page (processing mode)

On the **Peaktable processing page**, data can be loaded into the app, and processing parameters can be set. Load the files by clicking on the respective buttons. The minimum requirement to run the Peaktable processing mode are a **peaktable** and its accompanying **.mgf-file**. Optionally, users can provide **metadata**, **bioactivity data**, and a targeted **spectral library**, which are described in their respective wiki pages. Input files are tested for correct formatting, and a message indicates pass or fail of the assessment. With respect to parameter settings, the default settings should match most data types but can be adjusted as needed:

- **Mass deviation** - *"Select the estimated mass deviation of your data (in ppm)"*:
States the expected mass deviation of the data. Used as precision threshold during different calculation steps, such as ion adduct calculation. This parameter should be set respective to the input data. As a rule of thumb, using the same mass deviation that was used for MZmine3 processing is suggested.

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

## MZmine page (raw data mode)

TBA - not implemented yet

## Loading page (loading mode)

session-file: a FERMO-specific file in the .pickle-format (a Python-specific data storage format). It is created during FERMO processing (as 'FERMO_cache.session') and used to cache data, to prevent redundant re-calculations. User can also load the session file only, by starting FERMO in the loading mode (see References -> Modes). This also allows users to share their analysis with collaborators by sending a single file. However, keep in mind to load FERMO session files from TRUSTED SOURCES ONLY! This has to do with the file format of the session file. In theory, a wrongdoer might insert malicious code into the file, which is executed upon loading and may cause harm. If in doubt, do not load the session file. Instead, ask for the original files (i.e. peaktable).
When working with session files, it is recommended to rename any file that needs to be stored as soon as possible, since FERMO may overwrite file that are named 'FERMO_cache.session'. While no naming conventions need to be followed, it is recommended to include FERMO as prefix and .session as suffix, to make the purpose of the file clear.



## Dashboard page


The dashboard page represents the core of FERMO: it provides an overview of the analyzed data and allows users to explore the calculated scores. The dashboard is separated in six interconnected elements: the **sample table** **(1)**; the **sample chromatogram view** **(2)**; the **feature information table** **(3)**; the **chromatogram overview** **(4)**; the **spectral similarity/molecular networking view** **(5)**; and the **filter and download panel** **(6)**.  

![dashboard-overview.png](/assets/dashboard-overview.png)

The **sample table** **(1)** gives an overview of the samples that were included in the analysis and consists of six columns: The column **Filename** shows the filename of the sample. The column **Group** shows the name of the group the sample belongs to (if no metadata table was provided on the processing page, all samples will be in the group GENERAL). The column **Diversity score** shows the calculated diversity score of the sample, which indicates the chemical diversity a sample contains, in comparison to the total chemical diversity of the dataset (see the page "Scores" for a more detailed explanation (LINK)).The column **Spec score** stands for specificity score and indicates proportion of chemical diversity in a sample that is specific to the sample and the group it is in (see the page "Scores" for a more detailed explanation (LINK)). The column **Total** gives the number of features per sample. The column **Non-blank** gives the number of features per sample that are not associated with the blank samples. The column **Over cutoff** gives the number of features per sample that remain after the user-defined filters have been applied.
Each of the rows can be clicked, which triggers the display of the sample in the **sample chromatogram view (2)**.

![dashboard_sample_table.png](/assets/dashboard_sample_table.png)

The **sample chromatogram view (2)** shows a pseudo-chromatogram of the selected sample ( *pseudo* because the chromatogram traces are constructed from a subset of the original datapoints, and therefore an abstraction only - see the references for details on the plotting).  It is separated in two chromatograms: the upper chromatogram shows a static view of the features in the sample, color-coded after their properties. Features can be *Over cutoff*, meaning that they match the user-defined filters, or *Below cutoff*, if they do not. Features that are sample-specific have a violet outline. Features that are not sample-specific but were only detected in the group the sample belongs to have a black outline. Features that are blank-associated and/or had no accompanying MS2 information are marked separately. All features have a tooltip that appears upon cursor-hovering and gives information on attributes such as *m/z*, *RT*, and annotation. To get more information, features can be clicked, which triggers various elements in the dashboard, such as the **feature information table** **(3)**, the **chromatogram overview** **(4)** and the **spectral similarity/molecular networking view** **(5)**.
The lower chromatogram is activated once a feature is clicked and highlights the features that are related to the selected feature, based on spectral similarity networking/molecular networking.

![dashboard_sample_chrom_view.png](/assets/dashboard_sample_chrom_view.png)

The **feature information table** **(3)** summarizes all available information about a feature. It is separated into five parts: (i) general information about the feature; (ii) calculated scores for the feature; (iii) feature annotation; (iv) information about grouping, intensities across samples, and annotations on co-eluting ion adducts; (v) information about the spectral similarity clique/molecular network the feature is in. 

![dashboard-feature_information_table.png](/assets/dashboard-feature_information_table.png)

The **chromatogram overview** **(4)** shows the selected feature highlighted across all samples in which it was detected, sorted for highest to lowest intensity. This view can give an overview of the neighborhood of the feature in the chromatograms, and to select the best sample for isolation. 

![dashboard_chrom_overview.png](/assets/dashboard_chrom_overview.png)

The **spectral similarity/molecular networking view** **(5)** shows the spectral similarity network (also known as molecular network, cluster, or similarity clique), in which the selected feature was placed. Since chemically similar compounds usually show similar tandem mass fragmentation spectra, spectral similarity between two tandem mass fragmentation spectra can be used as proxy for chemical similarity of the compounds the spectra originate from. The spectral similarity network is calculated by performing a pairwise comparison of MS2 spectra of all features, and clustering the most similar ones in a graph network. The nodes of the network represent individual features, while the edges represent significant similarities of the associated MS2 spectra. Since the features contained in a similarity clique are structurally related, a similarity clique can be considered as a proxy for a chemical class. Details on calculation and reasoning can be found in the Wiki (LINK).
In the spectral similarity view, nodes are color-coded after their attributes. A feature can marked as *Selected Feature* (currently selected in the sample chromatogram view). It can be marked as *Present in Sample*, which means that it is also present in the currently active sample (indicated in the bottom chromatogram of the **sample chromatogram view (2)**, with whom the spectral similarity network view share the color-coding). A feature can also be marked as *Other Samples*, which means that it is not detected in the currently selected sample. Futher, the node outline indicates if the feature is *Unique to sample* or *Unique to group* (the group the currently active sample belongs to). 
Nodes and edges can be clicked to get more information on them, without having to change the overall view. This triggers the tables below the network view: the left table shows general information about the clicked node, while the right shows information about the clicked node.

![dashboard_networking_view.png](/assets/dashboard_networking_view.png)

The **filter and download panel** **(6)** allows to set thresholds, which are then used to color-code features in the **sample chromatogram view (2)**. It also provides export/save buttons where either the feature/sample information or the FERMO session file can be saved. The filters are: 

- Intensity score: relative intensity of the feature in sample, relative to the most intense feature in the sample. Here, a threshold value of 0 would select all peaks, and a threshold value of 1 would select only the most intense feature. 

- Convolutedness score: represents the proportion of the feature not overlapping with other features, based on retention time. Feature overlaps represent co-elution of peaks in the chromatogram, which are considered unfavorable since they complicate consecutive isolation. In the convolutedness score, a value of 1 would indicate no overlap with other peaks, while a value of 0 would indicate complete overlap. Isotopic peaks (e.g. the +1 peak of a \[M+H]<sup>+</sup> adduct) and different adducts originating from the same compound (e.g., \[M+H]<sup>+</sup> and \[M+Na]<sup>+</sup> ) are detected and not considered in the calculation, since they do not represent different molecules. More details can be found in the references.

- Bioactivity score: represents putative association to bioactivity, if a bioactivity table was provided. A feature is considered bioactivity-associated if it was only detected in samples designated as active, or if the minimal intensity across all bioactive samples is n times (by default 10 times, can be user-specified) higher than the maximal intensity across all inactive samples. This takes into account sub-inhibitory concentrations, which cause a sample to be considered inactive, even though the feature can be detected. A bioactivity score of 0 would indicate that the feature is not bioactivity-associated, while a value greater than 0 or equal to 1 would indicate bioactivity-associatedness. Keep in mind that a positive bioactivity score does not guarantee bioactivity of a compound. Instead, it tells which features are possibly bioactivity-associated. For more details and limitations, see the references. 

- Novelty score: represents putative novelty of feature, compared to external data. Indicates likeliness that the compound represented by the feature has not been described yet. This score is calculated from the results of the matching against the user-specified spectral library, and the MS2Query matching. If no reliable match was found, the feature is considered to be likely novel. Therefore, a score of 1 would indicate high probability of novelty, a score between 1-0.1 would indicate a less reliable match and therefore, putative novelty, and a score of 0 would indicate no novelty. 

![dashboard_filters_export.png](/assets/dashboard_filters_export.png)

## References

### Scores

- Diversity score (utils.py)
    Measure for the chemical diversity of a sample, compared against the total chemical diversity in the dataset. Sample-specific measure.
    The chemical diversity detected in a biological sample can vary substantially, depending on variables such as the source organism, culturing conditions, extraction methods or analysis instrument. High chemical diversity of a sample is beneficial during isolation procedures, since it diversifies the risk of investing resources into the redundant characterization of structurally similar compounds. Therefore, a comprehensive metric to represent the chemical diversity of a sample is highly desirable.
    The chemical diversity metric used in FERMO is based on spectral similarity cliques/networks. Such networks are created by calculating pairwise similarity between all MS2 spectra in a dataset, and connecting the most similar ones based on user-defined parameters. Since similar chemical structures tend to lead to similar mass fragmentation spectra, it has been hypothesized that spectral similarity can act as a proxy for chemical similarity. Following this logic, individual spectral similarity cliques/networks can be considered proxies of chemical classes, since they are a collection of similar MS/MS fragmentation spectra, stemming from putatively similar chemical structures. More precisely, they can be considered spectral similarity classes. 
    FERMO calculates its diversity score as follows: Excluding cliques containing media components, for each sample, the number of detected spectral similarity cliques is divided by the total number of similarity cliques across all samples. A sample with a large number of similarity cliques will have a higher diversity score than a sample with a low number of similarity cliques.
    However, there are some limitations to consider: First, the networks/cliques are based on MS2 spectral similarity, and not necessarily every clique represents a discrete chemical class, since it has been observed that different adducts of the same compound (e.g. \[M+H\]<sup>+</sup>, \[M+2H\]<sup>2+</sup>) can have very different MS2 spectra and will end up in different cliques. Second, also singleton nodes (i.e. not connected to any other node due to lack of spectral similarity) are considered distinct chemical classes in the diversity score calculation. If MS2 spectra have not been filtered for quality control (e.g. to assure a minimal number of fragmentation peaks) before spectral similarity calculation, it can lead to a high number of singleton peaks, simply because their MS2 spectra lack information content. This can falsely bloat the diversity score of a sample. 
    
- Specificity score (utils.py)
    Measure for the proportion of specific chemistry of a sample. Derivative of the Diversity score described in the previous paragraph. Calculated as follows: Excluding cliques containing media components, for each sample, the number of detected spectral similarity cliques that are specific to the sample and the group it belongs to, divided by the total number of similarity cliques detected in this sample. A sample with a large number of specific similarity cliqies will have a higher specificity score than a sample with a low number of specific cliques. However, this score should always be considered in tandem with the diversity score, since it relates to the sample, and not to the overall chemistry. For example, a sample can have a specificity score of 0.5 (half of the detected cliques are specific to the sample), but if the total number of cliques in this sample is low (e.g. a diversity score of 0.05), it is still overall poor. A much more interesting sample would be one with a high diversity score (e.g. 0.4, meaning 40% of the chemical diversity across all samples) and a high specificity score (e.g. 0.5, meaning that 50% of the cliques in this sample are specific for it, which amounts to 20% of the total cliques across all samples).
    
- Convolutedness score (calculate_feature_overlap.py)
    Represents the proportion of the feature not overlapping with other features, based on retention time. Feature overlaps represent co-elution of peaks in the chromatogram, which are considered unfavorable since they complicate consecutive isolation. In the convolutedness score, a value of 1 would indicate no overlap with other peaks, while a value of 0 would indicate complete overlap. Isotopic peaks (e.g. the +1 peak of a \[M+H]<sup>+</sup> adduct) and different adducts originating from the same compound (e.g., \[M+H]<sup>+</sup> and \[M+Na]<sup>+</sup> ) are detected and excluded from the colvolutedness, since they stem from the same compounds and are only adducts caused by the instrument.

- Novelty score (dashboard.py):
    Measure for putative novelty of the feature, compared against an external database. Feature-specific measure.
    In the search for novel natural products, it is essential to ensure that metabolites have not already been isolated before. This process, called dereplication, takes place during prioritization, and is usually performed by comparing the attributes of features against databases. A common automated way of doing dereplication is library matching: comparison of the MS/MS spectrum of the metabolite against a library of MS/MS spectra of standards. Even though library matching is a fast and convenient way of dereplication, if comes with  some limitations: For one, the number of MS/MS spectra in spectral libraries is orders of magnitude lower than the number of known metabolites, thus creating a "blind spot" of "known unknowns". Furthermore, in commonly used library matching algorithms, spectrum matches must match across the whole spectrum, limiting the identification of analogues that may have a good partial match due to a common substructure. Recently, the issue of inadequate library size has been partially addressed by the MASST algorithm by Wang et al, which swaps the spectral library of identified standards with community-provided experimental data. In theory, this should hugely increase coverage of the reference library, allowing to form hypotheses about commonly occurring compounds even though the exact identity of the compounds is unknown. Also, the problem of analogue search has been recently addressed by introduction of the MS2Query tool (De Jonge et al), which uses vectorization (more specifically, spectral embeddings) for MS/MS spectra representation, allowing for partial matches between compounds. Furthermore, comparison of spectral embeddings is computationally efficient, which allows for faster search times in larger spectral libraries. 
    For the novelty score in FERMO, we combine both concepts. In addition to standard library matching against a user-provided spectral library (employing a modified cosine score), we use MS2Query to compare against a library of spectra of both standards and non-annotated community-provided spectra. The large size of the library (currently, over 600,000 diversified spectra, with growing tendency) allows for the hypothesis that compounds that are not found in it are reasonably rare, and therefore, unlikely to have been isolated before. Using MS2Query also allows to search for analogues, increasing the coverage even further. 
    The novelty score is a value between or equal to 0 and 1: a value of 0 indicates that the compound is most likely known and/or commonly occurring, while 1 indicates that the compound is most likely unknown and/or rarely occurring. This value is calculated from the results of library and/or embedding matching. If library matching yields a reliable match (highest modified cosine hit higher or equal to 0.95, highest ms2query hit higher or equal to 0.95), it is assumed to be dereplicated, and its novelty score is set to 0. If the library matching yields a less reliable match (0.95-0.8 for modified cosine, 0.95-0.4 for ms2query), the compound is assumed to be in the "twilight zone" which requires further evaluation, and it gets a score between 0 and 1, with a score closer to 1 indicating higher chances of novelty. If a compound is below the threshold (0.8 for modified cosine, 0.4 for ms2query), it is assumed to be novel, and its novelty score is set to 1. Using the threshold filters allows to search for the score.    

- Bioactivity score: 
    Represents putative association to bioactivity, if a bioactivity table was provided. A feature is considered bioactivity-associated if it was only detected in samples designated as active, or if the minimal intensity across all bioactive samples is n times (by default 10 times, can be user-specified) higher than the maximal intensity across all inactive samples. This takes into account sub-inhibitory concentrations, which cause a sample to be considered inactive, even though the feature can be detected. A bioactivity score of 0 would indicate that the feature is not bioactivity-associated, while a value greater than 0 or equal to 1 would indicate bioactivity-associatedness. Keep in mind that a positive bioactivity score does not guarantee bioactivity of a compound. The bioactivity score is not resulting from any statistical calculation or prediction. Instead, it tells which features are possibly bioactivity-associated, and leaves it to the user to decide if this is plausible or not. Eventually, any bioactivity prediction must be confirmed by consecutive fractionation and retesting, until it is confirmed by isolation and testing of the pure compound. However, the bioactivity score can help to save time and resources by narrowing down possibilities. 


### Adduct detection (calculate_feature_overlap.py):

In mass spectrometry analaysis, many different signals can be detected from a single compound. These signals can be various adducts (e.g. \[M+H]<sup>+</sup>, \[M+Na]<sup>+</sup>), or stem from variable isotope composition of the compound (e.g. the +1 peak of a \[M+H]<sup>+</sup> adduct, from the 13C isotope). These signals are often registered as individual features and obfuscate analysis (see Peak collision detection for details).

FERMO attempts to annotate related adducts and isotopic peaks during peak collision analysis. If two peaks overlap with each other (i.e. have a similar retention time window), FERMO will compare their *m/z* ratios. [Blumer et al.](https://doi.org/10.1021/acs.jcim.1c00579) reported that the \[M+H]<sup>+</sup> ion is the most commonly observed adduct in ESI-LC-MS instruments. Therefore, FERMO considers one of the two adducts (peak A) to be the \[M+H]<sup>+</sup> adduct, and the other one (peak B) an other adduct, such as \[M+Na]<sup>+</sup>. For a list of commonly observed adduct types, FERMO performs the adequate mathematical operation to calculate the mass of peak A if it was that other adduct ( \[M+Na]<sup>+</sup>). If the mass deviation between the theoretical mass of peak A and the observed mass of peak B are within a user-set threshold (by default, 20 ppm), the two peaks are considered related adducts, stemming from the same compound. 

Consider two overlapping peaks A (*m/z* 415.2098) and B (*m/z* 437.1912). Peak A is considered to be the \[M+H]<sup>+</sup> adduct. We hypothesize that peak B is the \[M+Na]<sup>+</sup>) adduct. Therefore, we perform (415.2098 - 1.0072 + 22.9897) and calculate the mass deviation between the result and peak B. The mass error between 437.1923 (peak A) and 437.1912 amounts to 2.5 ppm and is well within the tolerance of 20 ppm. Therefore, we can assume that peak B is indeed the \[M+Na]<sup>+</sup> adduct and peak A the \[M+H]<sup>+</sup> adduct.

Currently, 16 different adducts and isotopes are considered and the calculation described below. A_mz denotes peak A and is considered the \[M+H]<sup>+</sup>. Masses are defined as: Na = 21.981942 )(proton already subtracted), H = 1.007276 (mass of proton), C13_12 = 1.0033548 (mass difference between 13C and 12C isotopes).

- **\[M+Na\]<sup>+</sup>:** `(A_mz + Na)`
    
- **\[2M+Na\]<sup>+</sup>:** `((2 * (A_mz - H)) + Na + H)`

- **\[M+2H\]<sup>2+</sup>, \[2M+H\]<sup>+</sup>**: `((A_mz + H)/2)` **\[1\]**

- **\[M+3H\]<sup>3+</sup>**: `((A_mz + (2 * H))/3)`

- **\[M+1+H\]<sup>+</sup>**: `(A_mz + C13_12)`

- **\[M+2+H\]<sup>+</sup>**: `(A_mz + (2 * C13_12))`

- **\[M+3+H\]<sup>+</sup>**: `(A_mz + (3 * C13_12))`

- **\[M+4+H\]<sup>+</sup>**: `(A_mz + (4 * C13_12))`

- **\[M+5+H\]<sup>+</sup>**: `(A_mz + (5 * C13_12))`

- **\[M+1+2H\]<sup>2+</sup>**: `((A_mz + (C13_12 + H)) / 2)`

- **\[M+2+2H\]<sup>2+</sup>**: `((A_mz + ((2 * C13_12) + H)) / 2)`

- **\[M+3+2H\]<sup>2+</sup>**: `((A_mz + ((3 * C13_12) + H)) / 2)`

- **\[M+4+2H\]<sup>2+</sup>**: `((A_mz + ((4 * C13_12) + H)) / 2)`

- **\[M+5+2H\]<sup>2+</sup>**: `((A_mz + ((5 * C13_12) + H)) / 2)`

- **+1 isotopic peak of \[M+2H\]<sup>2+</sup>**: `(A_mz + (C13_12/2))` **\[2\]**

**\[1\]**: Here, one of the ions is the \[2M+H\]<sup>+</sup> ion, the other one is the \[M+2H\]<sup>2+</sup> ion. Lack of isotopic pattern makes it not possible to say which is which, so both are annotated. Consider two overlapping peaks A and B: peak A with *m/z* 1648.47; peak B with *m/z* 824.74. If A is assumed \[M+H\]<sup>+</sup>, B would be \[M+2H\]<sup>2+</sup>. If B is assumed \[M+H\]<sup>+</sup>, A would be \[2M+H\]<sup>+</sup>. Thus, assignment is performed for \[M+2H\]<sup>2+</sup> and \[2M+H\]<sup>+</sup> in parallel.

**\[2\]**: For certain compounds classes, such as thiopeptides, the \[M+H]<sup>+</sup> adduct is only poorly or not at all detected, while the \[M+2H\]<sup>2+</sup> adduct is detected well. In this case, the \[M+1+2H\]<sup>2+</sup> isotope of \[M+2H\]<sup>2+</sup> is not annotated, since it misses its corresponding protonated adduct. Consider two overlapping peaks A and B: peak A with *m/z* 790.2263; peak B with *m/z* 790.7269. If A is assumed to be \[M+2H\]<sup>2+</sup>, B would be the \[M+1+2H\]<sup>2+</sup>. In theory, two unrelated peaks with a mass difference of 0.5017 could appear at the same retention time, but chances for that are very slim.

### Peak collision detection (calculate_feature_overlap.py)

In LC-MS(MS) analysis, it is a common occurrence that two compounds leave the chromatography column at the same time. This is also known as co-elution or peak collision, and both compounds will be in the same acquisition scan of the mass spectrometer. If the compounds have different molecular masses, the instrument can distinguish and register them as individual, overlapping peaks. 

Co-elution of compounds is unfavorable since it complicates consecutive isolation of each of the compounds. Therefore, it is an important factor to consider during the metabolite prioritization procedure. FERMO detects co-elution of two peaks by calculation of retention time window overlap. Each peak is simplified to a one-dimensional vector, denoted with two points x1 (retention time of the beginning of the peak) and x2 (retention time of the end of the peak). Consider two peaks A and B with A(x1,x2) and B(x1,x2). If any of (Ax2 < Bx1) or (Bx2 < Ax1) is False, peaks do overlap. FERMO checks for collisions by performing a pairwise comparison between all peaks (all-against-all).

However, not all peak collisions stem from co-elution of discrete compounds. A single compound can lead to many different peaks, due to detection of different adducts (e.g. \[M+H]<sup>+</sup>, \[M+Na]<sup>+</sup>), isotopes (e.g. the +1 peak of a \[M+H]<sup>+</sup> adduct, from the 13C isotope), and combinations thereof (e.g. \[M+1+2H]<sup>2+</sup>). Such 'artifacts' usually have a similar retention time window, and can be related to each other by discrete mathematical operations. They are often filtered out by pre-processing programs (e.g. MZmine), but can also persist until in the final peaktable. Overlaps between such 'artificial' peaks do not affect consecutive isolation, since they stem from the same compound (even though they can give valuable information about the chemical structure of an unknown analyte). 

Therefore, FERMO examines each peak collision, and if one of the two peaks results to be a plausible adduct of the other, the overlap is not considered a collision. The relationship between the two peaks is registered and presented to the user in the dashboard in the Feature information table in the field 'Putative adducts'.

For more information on how which adducts or isotopes are detected, see the point 'Adduct detection' of this references. 



### Chromatogram drawing (calculate_pseudochrom_traces.py)

In mass spectrometry, a *m/z* chromatogram peak represents a specific *m/z* that has been detected across a number of consecutive scans. Therefore, it is an continuous trace, with each datapoint having a specific retention time and intensity. Peak picking algorithms transform these continuous traces into discrete parameters such as retention time at the start/stop of the peak, feature width at half maximum intensity, or retention time at maximum intensity. This form of representation is more memory-efficient then the continuous one and generally justifies the loss in information about the original chromatogram trace. 

In FERMO, the chromatograms peaks are drawn only from the discrete parameters mentioned above, since the peaktable used as input does not contain continuous chromatogram traces. Therefore, FERMO actually draws pseudo-chromatograms. Manual inspection showed that pseudo-chromatograms are good representations of the original chromatograms. Still, they remain abstractions of the original data, and users are advised to inspect the original chromatograms before important decision-making (e.g. before prioritization). 

Pseudo-chromatograms are drawn using following data points (x/y, where x is the retention time (rt), and y is the relative intensity (int):
- `rt at start of peak/0*int`
- `rt at start of feature width at half maximum/0.5*int`
- `rt at maximum int/int`
- `rt at stop of feature width at half maximum/0.5*int`
- `rt at stop of peak/0*int`
    
This form of representation comes with certain limitations: for example, shoulder peaks arising from co-eluting isomers are not considered. Also, the MZmine3 peaktable does not report asymmetry and tailing factors for all features, limiting their use in chromatogram drawing. Despite these limitations, we consider the use of pseudo-chromatograms a computationally efficient way of peak representation, with sufficient accuracy. 

### FAQ

TBA




