### Overview

This Wiki page gives an overview of the different scores that are calculated and used in FERMO to support feature inspection and prioritization. In total, there are five scores, of which two (Diversity and Specificity scores) are used in the **sample table** element, and three (Convolutedness, Novelty, and Bioactivity scores) are used as filters in the **filter and download panel** and **sample chromatogram view** elements.

For the **sample table** element:

- Diversity score: 
Measure of the overall chemical diversity of a sample, compared to the other samples
- Specificity score: 
Measure of how much of the chemical diversity of a sample is actually specific to the sample and the group it belongs to.

For the **sample chromatogram view**

- Convolutedness score: 
Measure for the overlap of the peak with other peaks, adjusted for ion adducts resulting from the same compound
- Novelty score:
Measure for the putative novelty of a feature, compared to external databases
- Bioactivity score: 
Measure for putative bioactivity-associatedness of feature


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

#### Convolutedness score

Used in the **filter and download panel** and **sample chromatogram view** elements. Feature-specific score.

Measure for the overlap of the feature peak with other peaks, adjusted for ion adducts resulting from the same compound.

Represents the proportion of the peak range not overlapping with other peaks, based on retention time. Peak overlaps represent co-elution of peaks in the chromatogram, which are considered unfavorable since they complicate consecutive isolation. In the convolutedness score, a value of 1 would indicate no overlap with other peaks, while a value of 0 would indicate complete overlap.

This calculation is corrected for different ion species that originate from the same compound, such as isotopic peaks (e.g. the +1 peak of a \[M+H]<sup>+</sup> adduct) and adducts (e.g., \[M+H]<sup>+</sup> and \[M+Na]<sup>+</sup> ), which are excluded from the convolutedness calculation.

Knowing which features/peaks result from which compounds is important to consider during any prioritization procedure.

#### Novelty score

Used in the **filter and download panel** and **sample chromatogram view** elements. Feature-specific score.

Measure for putative novelty of the feature, compared against external databases. 

The annotation of compounds is an essential step in metabolomics analysis, since it provides the means for the (biological) interpretation of results. 

In the search for novel natural products, it is essential to ensure that metabolites have not already been isolated before. This process, called dereplication, takes place during prioritization, and is usually performed by comparing the attributes of features against databases. A common automated way of doing dereplication is library matching: comparison of the MS/MS spectrum of the metabolite against a library of MS/MS spectra of standards. Even though library matching is a fast and convenient way of dereplication, if comes with  some limitations: For one, the number of MS/MS spectra in spectral libraries is orders of magnitude lower than the number of known metabolites, thus creating a "blind spot" of "known unknowns". Furthermore, in commonly used library matching algorithms, spectrum matches must match across the whole spectrum, limiting the identification of analogues that may have a good partial match due to a common substructure.

Recently, the issue of inadequate library size has been partially addressed by the MASST algorithm by Wang et al, which swaps the spectral library of identified standards with community-provided experimental data. In theory, this should hugely increase coverage of the reference library, allowing to form hypotheses about commonly occurring compounds even though the exact identity of the compounds is unknown. Also, the problem of analogue search has been recently addressed by introduction of the MS2Query tool (De Jonge et al), which uses vectorization (more specifically, spectral embeddings) for MS/MS spectra representation, allowing for partial matches between compounds. Furthermore, comparison of spectral embeddings is computationally efficient, which allows for faster search times in larger spectral libraries. 

For the novelty score in FERMO, we combine both concepts. In addition to standard library matching against a user-provided spectral library (employing a modified cosine score), we use MS2Query to compare against a library of spectra (currently, over 600,000 diversified spectra, with growing tendency). The large size of the library allows for the hypothesis that compounds that are not found in it are reasonably rare, and therefore, unlikely to have been isolated before. Using MS2Query also allows to search for analogues, increasing the coverage even further. 

The novelty score is a value between or equal to 0 and 1: a value of 0 indicates that the compound is most likely known and/or commonly occurring, while 1 indicates that the compound is most likely unknown and/or rarely occurring. This value is calculated from the results of library and/or embedding matching. If library matching yields a reliable match (highest modified cosine hit higher or equal to 0.95, highest ms2query hit higher or equal to 0.95), it is assumed to be dereplicated, and its novelty score is set to 0. If the library matching yields a less reliable match (0.95-0.8 for modified cosine, 0.95-0.4 for ms2query), the compound is assumed to be in the "twilight zone" which requires further evaluation, and it gets a score between 0 and 1, with a score closer to 1 indicating higher chances of novelty. If a compound is below the threshold (0.8 for modified cosine, 0.4 for ms2query), it is assumed to be novel, and its novelty score is set to 1. Using the threshold filters allows to search for the score.    

#### Bioactivity score: 

Used in the **filter and download panel** and **sample chromatogram view** elements. Feature-specific score.

Represents putative association to bioactivity, if a bioactivity table was provided. A feature is considered bioactivity-associated if it was only detected in samples designated as active, or if the minimal intensity across all bioactive samples is n times (by default 10 times, can be user-specified) higher than the maximal intensity across all inactive samples. This takes into account sub-inhibitory concentrations, which cause a sample to be considered inactive, even though the feature can be detected. 

For example, a bioactivity score of 0 would indicate that the feature is not bioactivity-associated, while a value greater than 0 or equal to 1 would indicate bioactivity-associatedness.

Keep in mind that a positive bioactivity score does not guarantee bioactivity of a compound. The bioactivity score is not resulting from any statistical calculation or prediction. Instead, it tells which features are possibly bioactivity-associated, and leaves it to the user to decide if this is plausible or not. Eventually, any bioactivity prediction must be confirmed by consecutive fractionation and retesting, until it is confirmed by isolation and testing of the pure compound. However, the bioactivity score can help to save time and resources by narrowing down possibilities. 
