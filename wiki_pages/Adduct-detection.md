### Overview


In mass spectrometry analysis, many different signals can be detected that originate from a single compound. These signals can be various ion adducts (e.g. \[M+H]<sup>+</sup>, \[M+Na]<sup>+</sup>), or stem from variable isotope composition of the compound (e.g. the +1 peak of a \[M+H]<sup>+</sup> adduct, resulting from a ¹³C isotope). These signals are often registered as individual features and obfuscate analysis (see Peak collision detection for details).

FERMO attempts to annotate related adducts and isotopic peaks during peak collision analysis. If two peaks overlap with each other (i.e. have overlaps of their retention time range), FERMO will compare their *m/z* ratios. [Blumer et al.](https://doi.org/10.1021/acs.jcim.1c00579) reported that the \[M+H]<sup>+</sup> ion is the most commonly observed adduct in ESI-LC-MS instruments. Therefore, FERMO considers one of the two adducts (peak A) to be the \[M+H]<sup>+</sup> adduct, and the other one (peak B) an other adduct, such as \[M+Na]<sup>+</sup>. For a list of commonly observed adduct types, FERMO performs the adequate mathematical operation to calculate the mass of peak A if it was that other adduct ( \[M+Na]<sup>+</sup>). If the mass deviation between the theoretical mass of peak A and the observed mass of peak B are within a user-set threshold (by default, 20 ppm mass deviation), the two peaks are considered related adducts, stemming from the same compound. 

For example, consider two overlapping peaks A (*m/z* 415.2098) and B (*m/z* 437.1912). Peak A is considered to be the \[M+H]<sup>+</sup> adduct. We hypothesize that peak B is the \[M+Na]<sup>+</sup>) adduct. Therefore, we perform (415.2098 - 1.0072 + 22.9897) and calculate the mass deviation between the result and peak B. The mass error between 437.1923 (peak A) and 437.1912 amounts to 2.5 ppm and is well within the tolerance of 20 ppm. Therefore, we can assume that peak B is indeed the \[M+Na]<sup>+</sup> adduct and peak A the \[M+H]<sup>+</sup> adduct.

Still, it is possible that two features show correlating *m/z* ratios by chance only, and are falsely attributed to be related adducts, especially when the mass deviation threshold is set high. Therefore, the user needs to scrutinize the adduct annotations critically. For example, if multiple related adducts are overlapping, it is very unlikely to be only by chance. 


#### List of adducts

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

