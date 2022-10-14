### Overview

In LC-MS(MS) analysis, it is a common occurrence that two compounds leave the chromatography column at the same time. This is also known as co-elution or peak collision, and both compounds will be in the same acquisition scan of the mass spectrometer. If the compounds have different molecular masses, the instrument can distinguish and register them as individual, overlapping peaks. 

#### Peak collision detection

Co-elution of compounds is unfavorable since it complicates consecutive isolation of each of the compounds. Therefore, it is an important factor to consider during the metabolite prioritization procedure. FERMO detects co-elution of two peaks by calculation of retention time window overlap. Each peak is simplified to a one-dimensional vector, denoted with two points x1 (retention time of the beginning of the peak) and x2 (retention time of the end of the peak).

Consider two peaks A and B with A(x1,x2) and B(x1,x2). If any of (Ax2 < Bx1) or (Bx2 < Ax1) is False, peaks do overlap. FERMO checks for collisions by performing a pairwise comparison between all peaks (all-against-all).

However, not all peak collisions stem from co-elution of discrete compounds. A single compound can lead to many different peaks, due to detection of different adducts (e.g. \[M+H]<sup>+</sup>, \[M+Na]<sup>+</sup>), isotopes (e.g. the +1 peak of a \[M+H]<sup>+</sup> adduct, from the ¹³C isotope), and combinations thereof (e.g. \[M+1+2H]<sup>2+</sup>). Such 'artifacts' usually have a similar retention time window, and can be related to each other by discrete mathematical operations. They are often filtered out by pre-processing programs (e.g. MZmine), but can also persist until in the final peaktable. Overlaps between such 'artificial' peaks do not affect consecutive isolation, since they stem from the same compound (even though they can give valuable information about the chemical structure of an unknown analyte). 

Therefore, FERMO examines each peak collision, and if one of the two peaks results to be a plausible adduct of the other, the overlap is not considered a collision. The relationship between the two peaks is registered and presented to the user in the dashboard in the Feature information table in the field 'Putative adducts'.

For more information on how which adducts or isotopes are detected, see the point 'Adduct detection' of the references. 
