### Overview

This Wiki page gives an overview of the different scores that are calculated and used in FERMO to support molecular feature inspection and prioritization. Diversity, Specificity, and Mean Novelty scores are used in the **sample table** element. Novelty and the QuantData scores are used as filters in the **filter and download panel** and **sample chromatogram view** elements.

For the **sample table** element:

- Diversity score: 
Measure of the overall chemical diversity of a sample, compared to the other samples
- Specificity score: 
Measure of how much of the chemical diversity of a sample is actually specific to the sample and the group it belongs to.
- Mean Novelty score: 
The mean novelty scores of all molecular features in a sample (excluding blank-associated molecular features, if group information was provided).

For the **sample chromatogram view**

- Novelty score:
Measure for the putative novelty of a molecular feature, compared to external databases
- QuantData score: 
Indicator if molecular feature is putatively associated with the quantitative biological data.

The different scores are described in greater detail below:

#### Diversity score 

Used in the **sample table** element. Sample-specific score.

Measure for the chemical diversity of a sample, compared against the total chemical diversity in the dataset.

The chemical diversity detected in a biological sample can vary substantially, depending on variables such as the source organism, culturing conditions, extraction methods or analysis instrument. High chemical diversity of a sample is beneficial during isolation procedures, since it diversifies the risk of investing resources into the redundant characterization of structurally similar compounds. Therefore, a comprehensive metric to represent the chemical diversity of a sample is highly desirable.

The chemical diversity metric used in FERMO is based on spectral similarity cliques/networks. Such networks are created by calculating pairwise similarity between all MS2 spectra in a dataset, and connecting the most similar ones based on user-defined parameters. Since similar chemical structures tend to lead to similar mass fragmentation spectra, it has been hypothesized that spectral similarity can act as a proxy for chemical similarity. Following this logic, individual spectral similarity cliques/networks can be considered proxies of chemical classes, since they are a collection of similar MS/MS fragmentation spectra, stemming from putatively similar chemical structures. More precisely, they can be considered spectral similarity classes. 

FERMO calculates its diversity score as follows: Excluding cliques containing media components, for each sample, the number of detected spectral similarity cliques is divided by the total number of similarity cliques across all samples. A sample with a large number of similarity cliques will have a higher diversity score than a sample with a low number of similarity cliques.

However, there are some limitations to consider: First, the networks/cliques are based on MS2 spectral similarity, and not necessarily every clique represents a discrete chemical class, since it has been observed that different adducts of the same compound (e.g. \[M+H\]<sup>+</sup>, \[M+2H\]<sup>2+</sup>) can have very different MS2 spectra and will end up in different cliques. Second, also singleton nodes (i.e. not connected to any other node due to lack of spectral similarity) are considered distinct chemical classes in the diversity score calculation. If MS2 spectra have not been filtered for quality control (e.g. to assure a minimal number of fragmentation peaks) before spectral similarity calculation, it can lead to a high number of singleton peaks, simply because their MS2 spectra lack information content. This can falsely bloat the diversity score of a sample. 

#### Specificity score

Used in the **sample table** element. Sample-specific score.

Measure for the proportion of the chemical diversity of a sample that is actually specific to the sample and its corresponding group.

Derivative of the Diversity score described in the previous paragraph. Calculated as follows: Excluding cliques containing media components, for each sample, the number of detected spectral similarity cliques that are specific to the sample and the group it belongs to, divided by the total number of similarity cliques detected in this sample.

A sample with a large number of specific similarity cliqies will have a higher specificity score than a sample with a low number of specific cliques. However, this score should always be considered in tandem with the diversity score, since it relates to the sample, and not to the overall chemistry. 

For example, a sample can have a specificity score of 0.5 (half of the detected cliques are specific to the sample), but if the total number of cliques in this sample is low (e.g. a diversity score of 0.05), it is still overall poor. A much more interesting sample would be one with a high diversity score (e.g. 0.4, meaning 40% of the chemical diversity across all samples) and a high specificity score (e.g. 0.5, meaning that 50% of the cliques in this sample are specific for it, which amounts to 20% of the total cliques across all samples).

#### Novelty score

Used in the **filter and download panel** and **sample chromatogram view** elements. Feature-specific score.

Measure for putative novelty of the molecular feature, compared against external databases. 

The annotation of compounds is an essential step in metabolomics analysis, since it provides the means for the (biological) interpretation of results. 

In the search for novel natural products, it is essential to ensure that metabolites have not already been isolated before. This process, called dereplication, takes place during prioritization, and is usually performed by comparing the attributes of molecular features against databases. A common automated way of doing dereplication is library matching: comparison of the MS/MS spectrum of the metabolite against a library of MS/MS spectra of standards. Even though library matching is a fast and convenient way of dereplication, if comes with  some limitations: For one, the number of MS/MS spectra in spectral libraries is orders of magnitude lower than the number of known metabolites, thus creating a "blind spot" of "known unknowns". Furthermore, in commonly used library matching algorithms, spectrum matches must match across the whole spectrum, limiting the identification of analogues that may have a good partial match due to a common substructure.

Recently, the issue of inadequate library size has been partially addressed by the MASST algorithm by Wang et al, which swaps the spectral library of identified standards with community-provided experimental data. In theory, this should hugely increase coverage of the reference library, allowing to form hypotheses about commonly occurring compounds even though the exact identity of the compounds is unknown. Also, the problem of analogue search has been recently addressed by introduction of the MS2Query tool (De Jonge et al), which uses vectorization (more specifically, spectral embeddings) for MS/MS spectra representation, allowing for partial matches between compounds. Furthermore, comparison of spectral embeddings is computationally efficient, which allows for faster search times in larger spectral libraries. 

For the novelty score in FERMO, we combine both concepts. In addition to standard library matching against a user-provided spectral library (employing a modified cosine score), we use MS2Query to compare against a library of spectra (currently, over 300,000 diversified spectra, with growing tendency). The large size of the library allows for the hypothesis that compounds that are not found in it are reasonably rare, and therefore, unlikely to have been isolated before. Using MS2Query also allows to search for analogues, increasing the coverage even further. 

The novelty score is a value between or equal to 0 and 1: a value of 0 indicates that the compound is most likely known and/or commonly occurring, while 1 indicates that the compound is most likely unknown and/or rarely occurring. This value is calculated from the results of library and/or embedding matching. If library matching yields a reliable match (highest modified cosine hit higher or equal to 0.95, highest ms2query hit higher or equal to 0.95), it is assumed to be dereplicated, and its novelty score is set to 0. 
If the molecular feature is annotated less reliably, another factor is taken into account: in the spectral similarity network, the nearest neighbors of the molecular feature are inspected for the NPClassifier and the ClassyFire superclass annotation of the MS2Query annotation. Nearest neighbors should in the spectral similarity network are hypothesized to be chemically related and therefore, their chemical class should be similar. This is checked separately for the NPClassifier and the ClassyFire superclass annotations, since the two algorithms use different vocabularies. If these molecular features share the same chemical class annotation, this is taken as additional clue to confirm the quality of the annotation. If there are multiple chemical classes, this is taken as evidence that the annotation was less certain. 

#### QuantData score: 

Used in the **filter and download panel** and **sample chromatogram view** elements. Feature-specific score.

Represents putative association to the quantitative biological data, if such data was provided. A molecular feature is considered quantitative data-associated if it was only detected in samples designated as active, or if the minimal intensity across all the 'active' samples is n times (by default 10 times, can be user-specified) higher than the maximal intensity across all 'inactive' samples.
