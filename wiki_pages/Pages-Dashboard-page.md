### Overview

The dashboard page represents the core element of FERMO: it provides an overview of the analyzed data and allows users to explore the detected molecular features, inspect the calculated scores, form hypotheses and prioritize molecular features for further investigation.

### Dashboard page

The dashboard is separated in six interconnected elements: the **overview tables (1)**; the **chromatogram view (2)**; the **molecular feature information table (3)**; the **sample overview** **(4)**; the **spectral similarity networking view (5)**; and the **filter and download panel (6)**.  

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard-overview.png|alt=dashboard-overview.png]]

#### Overview tables

The **overview tables (1)*** gives an overview of the samples that were included in the analysis. There are two tables: the first one shows general information across all samples, while the second one gives detailed information about single samples. The general table shows the number of samples, the total number of molecular features, the currently selected molecular features (depending on the set filters), the number of non-blank molecular features, and the number of molecular features associated to sample blanks and/ or without MS/MS information (MS1 only). The sample table shows the filename of the sample, the associated group (if group metadata was provided, else all samples are in the group 'GENERAL'), the Diversity Score, the Specificity Score (abbreviated Spec Score), the Mean Novelty Score, the number of currently selected molecular features, the total of molecular features in the sample, the number of non-blank-associated molecular features, and the number of molecular features that are associated to sample blanks and/ or without MS/MS information (MS1 only). The two tables complement each other and should be viewed in tandem. For more information on the custom scores (Diversity, Specificity, and Mean Novelty), see the ['Scores' page](https://github.com/mmzdouc/FERMO/wiki/Scores-page). Each of the rows in the sample table can be clicked, which triggers the display of the sample in the **chromatogram view (2)**.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_sample_table.png|alt=dashboard_sample_table.png]]

#### Sample chromatogram view

The **chromatogram view (2)** shows a pseudo-chromatogram of the selected sample ( *pseudo* because the chromatogram traces are constructed from a subset of the original data points, and therefore an abstraction only - see the [Chromatogram drawing](https://github.com/mmzdouc/FERMO/wiki/Chromatogram-drawing) page for details).  It is separated in two chromatograms: the upper chromatogram shows a static view of the molecular features in the sample, color-coded after their properties. Molecular features can be *Selected*, meaning that they match the user-defined filters, or *Not selected*, if they do not. Molecular features that are sample-specific have a **violet** outline. Molecular features that are not sample-specific but were only detected in the group the sample belongs to have a **black** outline. Molecular features that are blank-associated and/or had no accompanying MS² information are marked separately. All molecular features have a tooltip that appears upon cursor-hovering and gives information key attributes such as *m/z*, *RT*, and annotation. To get more information, molecular features can be clicked, which triggers various elements in the dashboard, such as the **molecular feature information table (3)**, the **sample overview (4)** and the **spectral similarity networking view (5)**.
The lower chromatogram is triggered once a molecular feature is clicked and highlights the other molecular features that are related to the selected molecular feature, based on spectral similarity networking/molecular networking.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_sample_chrom_view.png|alt=dashboard_sample_chrom_view.png]]

#### Molecular feature information table

The **molecular feature information table (3)** summarizes all available information about a molecular feature. It is separated into five parts: (i) general information about the molecular feature; (ii) calculated scores for the molecular feature; (iii) molecular feature annotation; (iv) information about grouping, intensities across samples, and annotations on co-eluting ion adducts; (v) information about the spectral similarity clique/molecular network the molecular feature is in. 

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/feature_information_table.png|alt=feature_information_table.png]]

#### Chromatogram overview

The **sample overview (4)** shows the selected molecular feature highlighted across all samples in which it was detected, sorted for highest to lowest intensity. This view can give an overview of the neighborhood of the molecular feature in the chromatograms, and to select the best sample for isolation. The view is restricted to 20% of the retention time of the sample, centered on the molecular feature under investigation. 

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_chrom_overview.png|alt=dashboard_chrom_overview.png]]

#### Spectral similarity/molecular networking view

The **spectral similarity networking view (5)** shows the spectral similarity network (also known as molecular network, similarity cluster, or similarity clique), in which the selected molecular feature was placed. Since chemically similar compounds usually show similar tandem mass fragmentation spectra, spectral similarity between two tandem mass fragmentation spectra can be used as proxy for chemical similarity of the compounds the spectra originate from.

The spectral similarity network is calculated by performing a pairwise comparison of MS² spectra of all molecular features, and clustering the most similar ones in a graph network. The nodes of the network represent individual molecular features, while the edges represent significant similarities of the associated MS² spectra. Since the molecular features contained in a similarity clique are structurally related, a similarity clique can be considered as a proxy for a chemical class. 

In the spectral similarity view, nodes are color-coded after their attributes. A molecular feature can marked as *Focused feature* (currently selected in the **chromatogram view (2)**). It can be marked as *Present in Sample*, which means that it is also present in the currently selected sample (indicated in the bottom chromatogram of the **chromatogram view (2)**, with whom the spectral similarity network view share the color-coding). A molecular feature can also be marked as *Other Samples*, which means that it is not detected in the currently selected sample. Further, the node outline indicates if the molecular feature is *Unique to sample* or *Unique to group* (the group the currently active sample belongs to). 

Nodes and edges can be clicked to get more information on them, without having to change the overall view. This triggers the tables below the network view: the left table shows general information about the clicked node, while the right shows information about the clicked edge.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_networking_view.png|alt=dashboard_networking_view.png]]

#### Filter and download panel

The **filter and download panel (6)** serves two functions. First, filters can be set to restrict the currently selected molecular features (the number of 'selected'). Second, the FERMO session file can be saved and/or peak tables/feature tables can be exported.

Molecular features can be filtered for several aspects. All filters can be combined with each other. The filters are:
- **Visualization of features**: Allows to toggle between ALL (all molecular features are shown in full) and SELECTED (not selected molecular features are grayed out). This helps in focusing on relevant features.
- **Novelty score**: Allows to select molecular features based on their Novelty score. A range between 0 (near perfect annotation, unlikely to be novel) and 1 (low certainty annotation, putatively novel) can be set. 
- **Relative intensity**: Allows to select molecular features based on the relative intensity. A range between 0 (lowest relative intensity) and 1 (highest relative intensity in the chromatogram) can be set. This makes it possible to selectively investigate a selected target range. 
- **QuantData-associated**: Allows to toggle between ON (selects only molecular features that are putatively associated to the provided quantitative biological variable) and OFF (no filtering is taking place). This makes it possible to focus on the subset of molecular features that possibly explain the observed biological variable. 
- **Adduct/isotope search**: Allows to filter for molecular features that have been annotated as adducts or isotopes of other molecular features. This field enables to use regular expression queries (POSIX ERE syntax). For example, to select all molecular features with any adduct/isotope annotation, the expression ".+" can be used. Sodium adducts can be queries with a simple "Na". For more information about the adduct/isotope annotation, see the respective Wiki page.
- **Annotation search**: Allows to filter for molecular features that have been annotated as specific compound. This field enables to use regular expression queries (POSIX ERE syntax) to search simultaneously against the spectra library annotation as well as the MS2Query annotation. Keep in mind that certain characters are interpreted as special characters by the regular expression search (e.g. the dot "." character means any character) and need to be "escaped" with a backward slash character "\". See [this guide](https://en.wikibooks.org/wiki/Regular_Expressions/POSIX-Extended_Regular_Expressions) for further information on regular expressions.
- **Feature ID search**: Allows to search for a specific molecular feature ID number. Accepts a single integer digit.
- **Spectral network ID search**: Allows to search for a specific spectral network ID. All molecular features associated with this network will be selected. Accepts a sing
- **Fold-changes filter**: Allows to search for molecular features that show a specific fold change between groups. Fold-changes are calculated by pairwise comparison of mean intensity of a molecular feature between groups (provided that group metadata was provided). The fields accepts a single integer digit. Features with associated fold changes equal to or higher than the chosen filter will be selected. This allows to identify features that show a high difference in intensity between two groups (e.g. healthy versus diseased)
- **Group filter**: Allows to filter for molecular features that are associated to a specific group (user-provided). This field enables to use regular expression queries (POSIX ERE syntax), which are described in more detail in [this guide](https://en.wikibooks.org/wiki/Regular_Expressions/POSIX-Extended_Regular_Expressions).
- **Precursor m/z search**: Allows to search for a range of precuror *m/z* values.

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
