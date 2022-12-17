### Overview

This Wiki page gives an overview of the different scores that are calculated and used in FERMO to support molecular feature inspection and prioritization. 

Scores utilized in the **sample information tables**:
    - Diversity score 
    - Specificity score 
    - Mean Novelty score 

Scores utilized in the **sample chromatogram overview**:
    - Novelty score
    - QuantData score

### Sample Information Tables Scores

#### Diversity score 

The Diversity score is a measure for the chemical diversity of a sample, compared against the total chemical diversity in the dataset. It comes in a range of 0-1, where 0 is 'worst', and 1 is 'best'. For each sample, the number of detected spectral similarity networks is divided by the total number of similarity networks across all samples. Similarity networks containing blank-associated molecular features are excluded from the calculation. 

The Diversity score is based on the assumption that molecules with similar chemical structures have similar associated fragmentation spectra, and will cluster into the same spectral similarity network. Therefore, we can consider spectral similarity networks as proxies for chemical classes, and all networks combined represent the total chemical diversity across samples. Thus, a sample with a large number of similarity networks will have a higher diversity score than a sample with a low number of networks.

There are some limitations to consider. Since the networks are based on calculated MS/MS spectral similarity, the choice of algorithm and parameter settings strongly influence the composition of similarity networks. Loose settings may lead to clustering of hardly similar MS/MS, while strict settings may lead to the separation of related spectra into disconnected networks. Furthermore, certain classes of molecules can undergo intramolecular rearrangements during MS/MS fragmentation (e.g. McLafferty-type rearrangement, Retro-Diels–Alder reactions), which may lead to substantially different spectra from similar molecules. Besides, also singleton "networks" (i.e. networks with a single spectrum due to lack of similarity to other spectra) are considered distinct chemical classes in the Diversity score calculation. Lack of spectral similarity can also be caused by a low number of fragments (and therefore, information) in a MS/MS spectrum, if no quality control on the minimum number of fragments of spectra was performed. This bloats the total number of networks, and overestimates the chemical diversity of a sample. These limitations should be taken into account and the Diversity score considered as estimate and not a precise prediction. 

#### Specificity Score

Similar to the Diversity score, the Specificity score is a measure for the proportion of the chemical diversity of a sample that is actually specific to the sample and its corresponding group. It comes in a range of 0-1, where 0 is 'worst', and 1 is 'best'. For each sample, the number of spectral similarity networks specific to the sample and its group (i.e. not found in samples of other groups) is divided by the total number of similarity networks for this sample. Similarity networks containing blank-associated molecular features are excluded from the calculation. 

The Specificity score is therefore a fraction of the Diversity score, and should be considered in tandem with it. A sample with a low Diversity score can have a high Specificity score, and vice versa. For example, a sample can have a Specificity score of 0.5 (half of the detected cliques are specific to the sample), but if the total number of cliques in this sample is low (e.g. a diversity score of 0.05), it is still overall poor. A much more interesting sample would be one with a high diversity score (e.g. 0.4, meaning 40% of the chemical diversity across all samples) and a high Specificity score (e.g. 0.5, meaning that 50% of the cliques in this sample are specific for it, which amounts to 20% of the total cliques across all samples).

Besides the limitations of the Diversity score, the Specificity score relies on user-provided sample grouping. If no such grouping was provided in form of sample grouping metadata, all samples will be put in the group 'GENERAL'. Therefore, all samples will have a Specificity score of 1, since all similarity networks are in the same group (and therefore group-specific).

#### Mean Novelty Score

The Mean Novelty score derives from the Novelty score described in the next paragraph. Here, it is the mean of the Novelty scores of all molecular features, excluding blank-associated ones. It comes in a range of 0-1, where 0 is 'worst', and 1 is best. If no annotation via MS2Query or spectral library search via matchms was performed, this score will be automatically 1.


### Sample Chromatogram Overview Scores

#### Novelty score

The Novelty score is a measure for the putative novelty of a molecular feature, compared against external data. It comes in a range of 0-1, where 0 is 'worst' (most likely known), and 1 is 'best' (most likely unknown). Blank-associated molecular features are not considered in the calculation and will automatically have a Novelty score of 1. 

The Novelty score combines results from spectral library matching via matchms and MS2Query annotation. The Novelty score is flexible in the sense that it still leads to an output even if one of the annotation methods was not performed (e.g., when no mass spectral library was provided). For the calculation, if any of these two methods yields an almost perfect annotation match (score greater or equal to 0.95), the reciprocal of the higher one of the two scores is returned as Novelty score. Else, the mean of the two scores plus the reciprocal of the number of different NPClassifier/Classyfire superclass annotations  of nearest neighbors of the molecular features in its spectral similarity network (provided by MS2Query annotation) is calculated and its reciprocal is returned as Novelty score. 

Therefore, well-annotated molecular features will have a low Novelty score, while molecular features without a good annotation will have a high Novelty score. Limitations arise from the external data against which comparisons are made. While MS2Query provides a library of over 300,000 diversified spectra and allows analog matches, the chemical space is far larger, which raises the problem of "known unknowns". Users may provide a more targeted library of compounds expected to be present.

#### QuantData score: 

The QuantData score is a measure for the putative associatedness of a molecular feature to user-provided quantitative biological data. It comes as a binary qualifier and can be applied using the respective filter on the FERMO dashboard. If no quantitative biological data was provided, the QuantData score is not applicable. 

For each molecular feature, its presence/absence across samples is considered. Molecular features that are only detected across samples not associated with the measurement is also not considered associated to the quantitative biological data. If a molecular feature is detected across both associated and non-associated samples, the lowest intensity across associated is confronted with the highest intensity across non-associated samples. If this fold-difference is higher than a so-called user-specified QuantData factor (by default, 10), the molecular feature is still associated to the quantitative bioogical data. This takes into account molecular features, which are detected in a non-associated sample, but the concentration is too low to be taken up in the quantitative biological data (e.g. sub-inhibitory concentrations in antibiotic activity assays). The quantitative data-associated molecular features can be further restricted by verifying correlation of the quantitative measure across samples with the intensity of molecular features (the trend). Therefore, molecular features unlikely to be associated to the quantitative biological measure are excluded from consideration, while the remainder can be scrutinized for plausibility. 

There are several limitations to consider: for one, it is based on the assumptions that the quantitative biological value is concentration-dependent, and that all samples were analyzed in an identical way (identical injection volumes of identical dilutions of samples). Next, the approach relies on a comparison between associated and non-associated samples. If the samples are chemically very different from each other (i.e. little overlap between features), only a low number of molecular features could be excluded from consideration.
