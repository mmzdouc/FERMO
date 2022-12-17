### Overview

The dashboard page represents the core element of FERMO: it provides an overview of the analyzed data and allows users to explore the detected molecular features, inspect the calculated scores, form hypotheses and prioritize molecular features for further investigation.

### Dashboard Page

The dashboard is organized into six fields:
- **sample information tables (1)**
- **sample chromatogram overview (2)**
- **molecular feature information table (3)**
- **sample chromatograms (4)**
- **Cytoscape view - spectral similarity networking (5)**
- **filter and export panel (6)**

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard-overview.png|alt=dashboard-overview.png]]

#### Sample Information Tables

The **sample information tables (1)** gives an overview of the samples that were included in the analysis. There are two tables: the first one shows general information across all samples, while the second one gives detailed information about single samples. Each of the rows in the sample table can be clicked, which triggers the display of the sample in the **sample chromatogram overview (2)**.

The general table shows:
- the number of samples
- the total number of molecular features
- the number of currently selected molecular features
- the number of currently selected spectral similarity networks
- the number of non-blank molecular features
- the number of blank-associated and/or molecular features without MS/MS information

In the sample table, each row represents one sample, with information on:
- the filename of the sample
- the associated group ('GENERAL', if no sample grouping metadata was provided
- the number of currently selected molecular features
- the number of currently selected spectral similarity networks
- the Diversity Score
- the the Spec(ificity) Score 
- the Mean Novelty Score
- the total number of moleculat features
- the number of non-blank molecular features
- the number of blank-associated and/or molecular features without MS/MS information

For more information on the custom scores (Diversity, Specificity, and Mean Novelty), see the ['Scores' page](https://github.com/mmzdouc/FERMO/wiki/Scores-page).
 
[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_sample_table.png|alt=dashboard_sample_table.png]]

#### Sample Chromatogram Overview

The **sample chromatogram overview (2)** shows a pseudo-chromatogram of the selected sample (see the [chromatogram drawing](https://github.com/mmzdouc/FERMO/wiki/Chromatogram-drawing) page for details).  

The upper chromatogram shows all molecular features in the sample, color-coded after their properties:
    - Selected ( **green** fill - match the user-defined filters)
    - Not selected ( **cyan** fill - do not match the user-defined filters)
    - Unique to sample ( **violet** outline)
    - Unique to sample group ( **black** outline)
    - Blank-associated/MS1 only ( **yellow** fill)

The lower chromatogram shows spectral similarity between molecular features:
    - Focused feature ( **blue** fill - currently focused on)
    - Related ( **red** fill - same spectral similarity network as focused feature)


All molecular features have a tooltip that appears upon cursor-hovering and gives information key attributes such as *m/z*, *RT*, and annotation. To get more information, molecular features can be clicked, which triggers various elements in the dashboard, such as the **molecular feature information table (3)**, the ***sample chromatograms (4)** and the **Cytoscape view - spectral similarity networking (5)**.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_sample_chrom_view.png|alt=dashboard_sample_chrom_view.png]]

#### Molecular Feature Information Table

The **molecular feature information table (3)** summarizes all available information about the focused molecular feature. It is separated into five parts: 
    - general information about the molecular feature
    - calculated scores for the molecular feature
    - molecular feature annotation
    - information about grouping, intensities across samples, and annotations on co-eluting ion adducts
    - information about the associated spectral similarity network

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/feature_information_table.png|alt=feature_information_table.png]]

#### Sample Chromatograms

The **sample chromatograms (4)** shows the focused molecular feature highlighted across all samples in which it was detected, sorted for highest to lowest intensity. This view can give an overview of the neighborhood of the molecular feature in the chromatograms, and to select the best sample for isolation. The view is restricted to +- 10% of the retention time of the sample, centered on the molecular feature under investigation. 

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_chrom_overview.png|alt=dashboard_chrom_overview.png]]

#### Cytoscape View - Spectral Similarity Networking

The **Cytoscape view - spectral similarity networking (5)** shows the spectral similarity network (also known as molecular network, similarity cluster, or similarity clique), in which the selected molecular feature was placed. Since chemically similar compounds usually show similar tandem mass fragmentation spectra, spectral similarity between two tandem mass fragmentation spectra can be used as proxy for chemical similarity of the compounds the spectra originate from.

The spectral similarity network is calculated by performing a pairwise comparison of MS² spectra of all molecular features, and clustering the most similar ones in a graph network. The nodes of the network represent individual molecular features, while the edges represent significant similarities of the associated MS² spectra. Since the molecular features contained in a similarity clique are structurally related, a similarity clique can be considered as a proxy for a chemical class. 

In the spectral similarity view, nodes are color-coded after their attribute:
    - Focused feature ( **blue** fill)
    - Present in sample ( **red** fill - present alongside focused molecular feature in current sample)
    - Other samples ( **grey** fill - not present in current sample)
    - Unique to sample ( **violet** outline - specific to current sample)
    - Unique to group ( **black** outline - specific to group of current sample)

Nodes and edges can be clicked to get more information on them, without having to change the overall view. This triggers the tables below the network view: the left table shows general information about the clicked node, while the right shows information about the clicked edge.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_networking_view.png|alt=dashboard_networking_view.png]]

#### Filter and download panel

The **filter and download panel (6)** serves two functions. First, filters can be set to restrict the currently selected molecular features (the number of 'selected'). Second, the FERMO session file can be saved and/or peak tables/feature tables can be exported.

Molecular features can be filtered for several aspects. All filters can be combined with each other. The filters are:
- **Visualization of features**: Toggle: allows to toggle between 'ALL' (all molecular features are shown in full), 'SELECTED' (not selected molecular features are grayed out), and 'HIDDEN' (not selected molecular features are completely hidden from view). This allows to focus on low-intensity signals.
- **BLANK-associated features**: Toggle: allows to toggle the specific designation of blank-associated features. If set to 'DESIGNATE', blank-associated molecular features are color-coded and automatically excluded from selection. 'DO NOT DESIGNATE' disables this behavior, and blank-associated molecular features are not automatically excluded from selection.
- **Novelty score**: Range: allows to select molecular features based on their Novelty score. A range between 0 (near perfect annotation, unlikely to be novel) and 1 (low certainty annotation, putatively novel) can be set. 
- **Relative intensity**: Range: allows to select molecular features based on the relative intensity. A range between 0 (lowest relative intensity) and 1 (highest relative intensity in the chromatogram) can be set.
- **QuantData-associated**: Toggle: allows to toggle between 'OFF', 'SPECIFICITY' (selects only molecular features that are putatively associated to the provided quantitative biological variable), and 'SPEC.+TREND' (also test for correlation between quantitative value and intensity).
- **Adduct/isotope search**: Text search: allows to filter for molecular features that have been annotated as adducts or isotopes of other molecular features. This field enables to use regular expression queries (POSIX ERE syntax). The exact kinds of annotation can be found [on this page](https://github.com/mmzdouc/FERMO/wiki/Adduct-detection). Examples:
    - '.+' (any annotation)
    - 'Fe' (iron)
    - 'Na' (sodium)
    - '\+' (a literal plus)
- **Annotation search**: Text search: allows to filter for molecular features that have been annotated as specific compound. This field enables to use regular expression queries to search simultaneously against the spectra library annotation as well as the MS2Query annotation. Examples:
    - '.' (any character)
    - '.+' (any annotation)
    - 'siomycin' (the annotation 'siomycin')
    - '^((?!siomycin).)*$' (everything except siomycin)
- **Feature ID search**: Integer search: allows to search for a specific molecular feature ID number. Example:
    - 83 (select the molecular feature with the ID number 83)
- **Spectral network ID search**: Integer search: allows to search for a specific spectral network ID. All molecular features associated with this network will be selected. Example:
    - 0 (select all molecular features in the spectral network with number 0)
- **Fold-changes filter**: Integer search: allows to search for molecular features that show a specific fold change between groups. Fold-changes are calculated by pairwise comparison of mean intensity of a molecular feature between groups (provided that group metadata was provided). The fields accepts a single integer digit. Features with associated fold changes equal to or higher than the chosen filter will be selected. This allows to identify features that show a high difference in intensity between two groups (e.g. healthy versus diseased). Example:
    - 4 (select all molecular feature showing a fold change of 4 or higher between groups)
- **Group filter (features)**: Text search: allows to filter for molecular features that are associated to a specific group. This field enables to use regular expressions. Examples:
    - '^group_1$' (select molecular features only found in group_1)
    - 'group_1|group_2' (select all molecular features either in group_1 or in group_2)
    - ^((?!group_1).)*$ (select all molecular features NOT observed in group_1)
- **Group filter (networks)**: Text search: allows to filter for molecular features based on all the groups detected for features in a spectral network. In other words, selects molecular features that are not sharing spectral similarity with features from an undesired group (for example, the BLANK group).
- **Sample name filter**: text search: allows to filter for molecular features associated to a specific sample. Uses regular expressions.
- **Number samples filter**: range: allows to filter for molecular features that have been found in a certain number of samples (e.g. at least two samples and/or at most in 3 samples)
- **Precursor m/z search**: range: allows to search for a range of precursor *m/z* values.

Furthermore, buttons are provided that allow to save the FERMO session file or to export molecular feature tables/peak tables:
- **Save FERMO session file (JSON)**: Allows to save the current FERMO session for later use, or to share it with collaborators.
- **Export - Peak table | selected sample, selected features**: 
- **Export - Peak table | selected sample, all features**:
- **Export - Peak table | all samples, selected features**:
- **Export - Peak table | all samples, all features**:
- **Export - Feature table | selected features**:
- **Export - Feature table | all features**:

Peak table and feature table exports will automatically provide the processing log (as JSON formatted file, containing the used processing parameters) with every download.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_filters_export.png|alt=dashboard_filters_export.png]]
