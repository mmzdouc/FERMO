### Overview

This Wiki page describes the ratio behind the (pseudo)chromatogram drawing in FERMO.

### Chromatogram drawing

In mass spectrometry, an extracted ion chromatogram (EIC) peak represents a specific *m/z* that has been detected across a number of consecutive scans. Therefore, it is an continuous trace, with each data point having a specific retention time and intensity. Peak picking algorithms transform these continuous traces into discrete parameters such as retention time at the start/stop of the peak ( *rt_start*, *rt_stop*), feature width at half maximum intensity ( *fwhm*), or retention time at maximum intensity ( *rt*). Such discrete parameters allow for easier comparison of EICs than using the whole trace, and generally justify the loss in information content. Also, this form of representation is more memory-efficient then the continuous one, since a variable number of datapoints is summarized in a discrete number of parameters. 

This logic is followed in FERMO, where the EIC peaks of molecular features are constructed from the aforementioned discrete parameters. Therefore, FERMO actually draws pseudo-chromatograms, instead of real EICs. However, manual inspection showed that pseudo-chromatograms are good representations of the original chromatograms. Still, they remain abstractions of the original data, and users are advised to inspect the original chromatograms before important decision-making (e.g. before prioritization). 

Pseudo-chromatograms are drawn using following data points (x/y, where x is the retention time ( *RT*), and y is the relative intensity ( *int*):
- `rt_start (x) / 0 * int (y)`
- `rt at start of fwhm (x) / 0.5 * int (y)`
- `rt at maximum int (x) / int (y)`
- `rt at stop of fwhm (x) / 0.5 * int (y)`
- `rt_stop (x / 0 * int (y)`
    
This form of representation comes with certain limitations: 

- Shoulder peaks arising from co-eluting isomers are not considered
- Asymmetry and tailing factors are not yet utilized

Despite these limitations, we consider the use of pseudo-chromatograms a computationally efficient way of peak representation, with sufficient accuracy. 
