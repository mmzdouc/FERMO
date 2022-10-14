### Overview

The dashboard page represents the core of FERMO: it provides an overview of the analyzed data and allows users to explore the detected features, inspect the calculated scores, form hypotheses and reach conclusions.

### Dashboard page

The dashboard is separated in six interconnected elements: the **sample table** **(1)**; the **sample chromatogram view** **(2)**; the **feature information table** **(3)**; the **chromatogram overview** **(4)**; the **spectral similarity/molecular networking view** **(5)**; and the **filter and download panel** **(6)**.  

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard-overview.png|alt=dashboard-overview.png]]

#### Sample table 

The **sample table** **(1)** gives an overview of the samples that were included in the analysis and consists of six columns: The column **Filename** shows the filename of the sample. The column **Group** shows the name of the group the sample belongs to (if no metadata table was provided on the processing page, all samples will be in the group GENERAL). The column **Diversity score** shows the calculated diversity score of the sample, which indicates the chemical diversity a sample contains, in comparison to the total chemical diversity of the dataset (see the page ['Scores'](https://github.com/mmzdouc/FERMO/wiki/Scores-page) for a more detailed explanation. The column **Spec score** stands for specificity score and indicates proportion of chemical diversity in a sample that is specific to the sample and the group it is in (see the page ['Scores'](https://github.com/mmzdouc/FERMO/wiki/Scores-page) for a more detailed explanation). The column **Total** gives the number of features per sample. The column **Non-blank** gives the number of features per sample that are not associated with the blank samples. The column **Over cutoff** gives the number of features per sample that remain after the user-defined filters have been applied.
Each of the rows can be clicked, which triggers the display of the sample in the **sample chromatogram view (2)**.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_sample_table.png|alt=dashboard_sample_table.png]]

#### Sample chromatogram view

The **sample chromatogram view (2)** shows a pseudo-chromatogram of the selected sample ( *pseudo* because the chromatogram traces are constructed from a subset of the original data points, and therefore an abstraction only - see the [Chromatogram drawing](https://github.com/mmzdouc/FERMO/wiki/Chromatogram-drawing) page for details).  It is separated in two chromatograms: the upper chromatogram shows a static view of the features in the sample, color-coded after their properties. Features can be *Over cutoff*, meaning that they match the user-defined filters, or *Below cutoff*, if they do not. Features that are sample-specific have a **violet** outline. Features that are not sample-specific but were only detected in the group the sample belongs to have a **black** outline. Features that are blank-associated and/or had no accompanying MS² information are marked separately. All features have a tooltip that appears upon cursor-hovering and gives information on attributes such as *m/z*, *RT*, and annotation. To get more information, features can be clicked, which triggers various elements in the dashboard, such as the **feature information table** **(3)**, the **chromatogram overview** **(4)** and the **spectral similarity/molecular networking view** **(5)**.
The lower chromatogram is activated once a feature is clicked and highlights the other features that are related to the selected feature, based on spectral similarity networking/molecular networking.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_sample_chrom_view.png|alt=dashboard_sample_chrom_view.png]]

#### Feature information table

The **feature information table** **(3)** summarizes all available information about a feature. It is separated into five parts: (i) general information about the feature; (ii) calculated scores for the feature; (iii) feature annotation; (iv) information about grouping, intensities across samples, and annotations on co-eluting ion adducts; (v) information about the spectral similarity clique/molecular network the feature is in. 

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/feature_information_table.png|alt=feature_information_table.png]]

#### Chromatogram overview


The **chromatogram overview** **(4)** shows the selected feature highlighted across all samples in which it was detected, sorted for highest to lowest intensity. This view can give an overview of the neighborhood of the feature in the chromatograms, and to select the best sample for isolation. 

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_chrom_overview.png|alt=dashboard_chrom_overview.png]]

#### Spectral similarity/molecular networking view

The **spectral similarity/molecular networking view** **(5)** shows the spectral similarity network (also known as molecular network, cluster, or similarity clique), in which the selected feature was placed. Since chemically similar compounds usually show similar tandem mass fragmentation spectra, spectral similarity between two tandem mass fragmentation spectra can be used as proxy for chemical similarity of the compounds the spectra originate from.

The spectral similarity network is calculated by performing a pairwise comparison of MS² spectra of all features, and clustering the most similar ones in a graph network. The nodes of the network represent individual features, while the edges represent significant similarities of the associated MS² spectra. Since the features contained in a similarity clique are structurally related, a similarity clique can be considered as a proxy for a chemical class. 

In the spectral similarity view, nodes are color-coded after their attributes. A feature can marked as *Selected Feature* (currently selected in the sample chromatogram view). It can be marked as *Present in Sample*, which means that it is also present in the currently active sample (indicated in the bottom chromatogram of the **sample chromatogram view (2)**, with whom the spectral similarity network view share the color-coding). A feature can also be marked as *Other Samples*, which means that it is not detected in the currently selected sample. Further, the node outline indicates if the feature is *Unique to sample* or *Unique to group* (the group the currently active sample belongs to). 

Nodes and edges can be clicked to get more information on them, without having to change the overall view. This triggers the tables below the network view: the left table shows general information about the clicked node, while the right shows information about the clicked node.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_networking_view.png|alt=dashboard_networking_view.png]]

#### Filter and download panel

The **filter and download panel** **(6)** allows to set thresholds, which are then used to color-code features in the **sample chromatogram view (2)**. It also provides export/save buttons where either the feature/sample information or the FERMO session file can be saved. The filters are: 

- **Intensity score**: relative intensity of the feature in sample, relative to the most intense feature in the sample. Here, a threshold value of 0 would select all peaks, and a threshold value of 1 would select only the most intense feature. 
- **Convolutedness score**: represents the proportion of the feature not overlapping with other features, based on retention time. Feature overlaps represent co-elution of peaks in the chromatogram, which are considered unfavorable since they complicate consecutive isolation. In the convolutedness score, a value of 1 would indicate no overlap with other peaks, while a value of 0 would indicate complete overlap. Isotopic peaks (e.g. the +1 peak of a \[M+H]<sup>+</sup> adduct) and different adducts originating from the same compound (e.g., \[M+H]<sup>+</sup> and \[M+Na]<sup>+</sup> ) are detected and not considered in the calculation, since they do not represent different molecules. More details can be found in the references.
- **Bioactivity score**: represents putative association to bioactivity, if a bioactivity table was provided. A feature is considered bioactivity-associated if it was only detected in samples designated as active, or if the minimal intensity across all bioactive samples is n times (by default 10 times, can be user-specified) higher than the maximal intensity across all inactive samples. This takes into account sub-inhibitory concentrations, which cause a sample to be considered inactive, even though the feature can be detected. A bioactivity score of 0 would indicate that the feature is not bioactivity-associated, while a value greater than 0 or equal to 1 would indicate bioactivity-associatedness. Keep in mind that a positive bioactivity score does not guarantee bioactivity of a compound. Instead, it tells which features are possibly bioactivity-associated. For more details and limitations, see the references. 
- **Novelty score**: represents putative novelty of feature, compared to external data. Indicates likeliness that the compound represented by the feature has not been described yet. This score is calculated from the results of the matching against the user-specified spectral library, and the MS2Query matching. If no reliable match was found, the feature is considered to be likely novel. Therefore, a score of 1 would indicate high probability of novelty, a score between 1-0.1 would indicate a less reliable match and therefore, putative novelty, and a score of 0 would indicate no novelty. Keep in mind that blank-associated features and features with no MS² information are never considered in the novelty score calculation and always have a score of 0. 

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/dashboard_filters_export.png|alt=dashboard_filters_export.png]]
