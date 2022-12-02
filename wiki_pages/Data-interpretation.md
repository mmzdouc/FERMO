### Overview

Data interpretation in general and more specificly in **FERMO** strongly depends on the research question in mind. For the sake of this guide, we imagine a bioactive natural product discovery research question, where some samples showed bioactivity, while others did not. In this mock analysis, the samples are investigated for differences (a single molecular feature or a group of molecular features) to which the observed bioactivity could be attributed. 

### Example analysis

1. The QuantData filter can be used to exclude molecular features that are unlikely to be associated to the observed biological activity from the selection. For example, this would be molecular features only observed in inactive samples, or molecular features with an measured intensity much lower across inactive samples than active samples. 

2. The Novelty score filter can be used to exclude molecular features with low Novelty score. Such molecular features were annotated with high certainty, and have therefore a low probability of being novel.

3. After having applied the filters, the remaining molecular features can be inspected for their likelihood to be associated to bioactivity. It is advisable to export the selected molecular features as table, using the dropdown-menu in the **filter and export panel**, to keep track which molecular features were already inspected. 

3. A possible way of assessing the bioactivity-likelihood is to look at the field *'Groups in molecular network'* in the element **molecular feature information table**. If groups not associated to bioactivity also contribute to the network, chances are slim that the molecular features in this network are really responsible for the bioactivity. However, if the network is specific to the bioactivity-associated group, chances are good that this group of molecular features might be responsible for bioactivity.

4. Another clue can be taken by looking at the field *'Bioactivity per sample'* and *'Intensity per sample'* in the **feature information table**. Bioactivity and molecular feature intensity should correlate, since a higher concentration of a compound should also lead to a higher biological activity signal. If they do not (e.g. low intensity of a molecular feature in a highly active sample, and high intensity of a molecular feature in a sample with low activity), chances are slim that the molecular feature is responsible for bioactivity. Since the same molecular feature (belonging to the same compound) is compared across samples, the intensity can be taken as semiquantitative measure. 

5. By exclusion of molecular features and similarity networks unlikely to be associated for bioactivity, the search can be narrowed down to a couple of molecular features, which can then be further investigated by chromatographic fractionation and re-testing, in case they had not been de-replicated as already known molecular features. In the best case, this would decrease the number of fractions needed to analyze further, saving time and resources. 
