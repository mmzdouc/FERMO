### Overview

Data interpretation in general and more specificly in **FERMO** strongly depends on the research question in mind. For the sake of this guide, we imagine a bioactive natural product discovery research question, where some samples showed bioactivity, while others did not. In this mock analysis, investigate the samples to see if there is any large difference between samples (a feature or a group of features) that could be responsible for the observed bioactivity. 

### Example analysis

1. Assuming bioactivity data and metadata were provided, the bioactivity filter can be used to identify features associated with biological activity. Combining with the novelty filter (set to a low setting, such as 0.2) can help to exclude features that were well annotated and therefore have a low probability of being novel.

2. After having applied the filters, the remaining features can be inspected for their likelihood to be associated to bioactivity. It is advisable to export the selected features as table, using the dedicated button, to keep track which features were already inspected. 

3. A possible way of assessing the bioactivity-likelihood is to look at the field *'Groups in molecular network'* in the element **feature information table**. If groups not associated to bioactivity also contribute to the network, chances are slim that the features in this network are really responsible for the bioactivity. However, if the network is specific to the bioactivity-associated group, chances are good that this group of features might be responsible for bioactivity.

4. Another clue can be taken by looking at the field *'Bioactivity per sample'* and *'Intensity per sample'* in the **feature information table**. Bioactivity and feature intensity should correlate, since a higher concentration of a compound should also lead to a higher biological activity signal. If they do not (e.g.  low intensity of a feature in a highly active sample, and high intensity of a feature in a sample with low activity), chances are slim that the feature is responsible for bioactivity. Since the same feature (belonging to the same compound) is compared across samples, the feature intensity can be taken as semiquantitative measure). 

5. By exclusion of features/networks unlikely to be associated for bioactivity, the search can be narrowed down to a couple of features, which can then be further investigated by chromatographic fractionation and re-testing, in case they had not been de-replicated as already known features. In the best case, this would decrease the number of fractions needed to analyze further, saving time and resources. 
